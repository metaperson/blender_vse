bl_info = {
    'name': 'Slide Show Tools',
    'author': 'Meta Person',
    'version': (0, 5),
    'blender': (2, 80, 0),
    'description': 'Slide Show Tools for Blender VSE',
    'category': 'Sequencer',
}

import bpy

class StripRelocation:
    def __init__(self, strip):
        self.strip = strip
        self.channel = strip.channel
        self.frame_final_start = strip.frame_final_start
        self.frame_final_duration = strip.frame_final_duration
        
    def check_collision(self, strip):
        if self.channel != strip.channel:
            return False
        if self.frame_final_start > strip.frame_final_start:
            if self.frame_final_start >= (strip.frame_final_start + strip.frame_final_duration):
                return False
        elif self.frame_final_start < strip.frame_final_start:
            if (self.frame_final_start + self.frame_final_duration) <= strip.frame_final_start:
                return False
        return True

    def check_need_to_relocate(self):
        if self.frame_final_start != self.strip.frame_final_start:
            return True
        if self.channel != self.strip.channel:
            return True
        return False

    def relocate(self):
        frame_movement = self.frame_final_start - self.strip.frame_final_start
        channel_movement = self.channel - self.strip.channel
        # bpy.ops.transform.seq_slide(value=(frame_movement, channel_movement))
        (self.strip.frame_start, self.strip.channel) = (self.strip.frame_start + frame_movement,
                                                        self.strip.channel + channel_movement)
        

class SLIDE_TOOLS_OT_align_strips(bpy.types.Operator):
    bl_description = 'align selected strips with given gap'
    bl_idname = 'slide_tools.align_strips'
    bl_label = 'Align Strips'
    
    frame_overlap: bpy.props.IntProperty(
        name='Frame Overlap',
        description='amount of the overlap between strips',
        default=0,
        )
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        # get selected strips.
        relocations = list()
        unselected_strips = list()
        for strip in context.sequences:
            if strip.select:
                strip_relocation = StripRelocation(strip)
                relocations.append(strip_relocation)
            else:
                unselected_strips.append(strip)

        # check the list empty.
        if not relocations:
            self.report({'WARNING'}, 'There is no selection')
            return {'CANCELLED'}

        # sort the strips by the order of the frame number.
        relocations = sorted(relocations, key=lambda x: (x.strip.frame_final_start + x.strip.frame_final_end), reverse=False)

        # calc the start frame and channel of the strip for relocating it.
        previous_relocation = None
        first_relocation = None
        for idx, relocation in enumerate(relocations):
            if previous_relocation:
                relocation.frame_final_start = previous_relocation.frame_final_start \
                                             + previous_relocation.frame_final_duration \
                                             - self.frame_overlap
                if self.frame_overlap > 0:
                    if idx % 2:
                        relocation.channel = first_relocation.channel + 1
                    else:
                        relocation.channel = first_relocation.channel
                else:
                    relocation.channel = first_relocation.channel
            else:
                first_relocation = relocation
            previous_relocation = relocation

        # check the collision
        for relocation in relocations:
            # check the collision among the selected strips
            for relocation2 in relocations:
                if relocation2 is not relocation:
                    if relocation.check_collision(relocation2):
                        self.report({'WARNING'}, 'unable to align : collision among the selected strips')
                        return {'CANCELLED'}
            # check the collision with the unselected strips
            for unselected_strip in unselected_strips:
                if relocation.check_collision(unselected_strip):
                    self.report({'WARNING'}, 'unable to align : collision with the unselected strips')
                    return {'CANCELLED'}
        
        # relocating the strips
        relocation_total = len(relocations)
        relocation_count = 0
        while relocations:
            count_before = len(relocations)
            for relocation in relocations:
                if not relocation.check_need_to_relocate():
                    relocations.remove(relocation)
                    continue
                # check the place(frame area and channel) of this relocation is available.
                collision = False
                for relocation2 in relocations:
                    if relocation2 is not relocation:
                        if relocation.check_collision(relocation2.strip):
                            collision = True
                            break
                if not collision:
                    relocation.relocate()
                    relocations.remove(relocation)
                    relocation_count += 1
            # CAUTION : loop infinitely
            #   when you find out len(relocations) unchanged, it may fall infinite repeats of this loop.
            if len(relocations) == count_before:
                self.report({'WARNING'}, 'can not be done successfully : unknown')
                # there are somethings maybe to undo, when you get relocation_count != 0
                if relocation_count != 0:
                    return {'FINISHED'}
                return {'CANCELLED'}
                

        self.report({'INFO'}, 'relocate strips : {}/{}'.format(relocation_count, relocation_total))
        return {'FINISHED'}

class SLIDE_TOOLS_OT_cross_strips(bpy.types.Operator):
    bl_description = 'add the cross effects between the selected strips'
    bl_idname = 'slide_tools.cross_strips'
    bl_label = 'Cross Strips'

    @staticmethod
    def check_overlaped(strip1, strip2):
        if strip1.frame_final_start > strip2.frame_final_start:
            if strip1.frame_final_start >= strip2.frame_final_end:
                return False
        elif strip1.frame_final_start < strip2.frame_final_start:
            if strip1.frame_final_end <= strip2.frame_final_start:
                return False
        return True

    def execute(self, context):
        # get selected strips.
        strips = list()
        for strip in context.sequences:
            if strip.select:
                strips.append(strip)

        # check the list empty.
        if not strips:
            self.report({'WARNING'}, 'There is no selection')
            return {'CANCELLED'}

        # sort the strips by the order of the frame number.
        strips = sorted(strips, key=lambda x: (x.frame_final_start + x.frame_final_end), reverse=False)

        # adds the effect between the two consecutive and overlapped strips.
        previous_strip = None
        effect_count = 0
        for strip in strips:
            if previous_strip:
                if __class__.check_overlaped(previous_strip, strip):
                    context.scene.sequence_editor.sequences.new_effect(
                        name='Cross', type='CROSS',
                        channel = max(previous_strip.channel, strip.channel) + 1,
                        frame_start = 0,
                        seq1=previous_strip, seq2=strip)
                    effect_count += 1
            previous_strip = strip

        self.report({'INFO'}, 'add effects : {}'.format(effect_count))
        return {'FINISHED'}


class SLIDE_TOOLS_MT_main(bpy.types.Menu):
    bl_description = 'Slide show tools from meta person'
    bl_label = 'Slide tools'

    def draw(self, context):
        layout = self.layout
        layout.operator(SLIDE_TOOLS_OT_align_strips.bl_idname, text="Align Strips", icon='ALIGN_FLUSH')
        layout.operator(SLIDE_TOOLS_OT_cross_strips.bl_idname, text="Cross Strips", icon='NONE')


def menu_draw(self, context):
    layout = self.layout
    layout.menu('SLIDE_TOOLS_MT_main')
    

def register():
    bpy.utils.register_class(SLIDE_TOOLS_OT_align_strips)
    bpy.utils.register_class(SLIDE_TOOLS_OT_cross_strips)
    bpy.utils.register_class(SLIDE_TOOLS_MT_main)
    bpy.types.SEQUENCER_HT_header.append(menu_draw)

def unregister():
    bpy.utils.unregister_class(SLIDE_TOOLS_OT_align_strips)
    bpy.utils.unregister_class(SLIDE_TOOLS_OT_cross_strips)
    bpy.utils.unregister_class(SLIDE_TOOLS_MT_main)
    bpy.types.SEQUENCER_HT_header.remove(menu_draw)
