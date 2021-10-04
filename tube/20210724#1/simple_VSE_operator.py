import bpy

class EXAMPLE_OT_simple_vse_operator(bpy.types.Operator):
    bl_description = 'a simple example of the VSE operator'
    bl_idname = 'example.simple_vse_operator'
    bl_label = 'Example - Simple VSE Operator'
    
    frame_offset: bpy.props.IntProperty()
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    @classmethod
    def poll(cls, context):
        if context.area.type == 'SEQUENCE_EDITOR':
            return True
        # print("False poll of '{}' in '{}'".format(cls.bl_idname, context.area.type))
        return False

    def execute(self, context):
        strip_count = 0
        for strip in context.sequences:
            if strip.select:
                strip.frame_start += self.frame_offset
                strip_count += 1

        self.report({'INFO'}, 'move strips : {}'.format(strip_count))
        return {'FINISHED'}

def register():
    bpy.utils.register_class(EXAMPLE_OT_simple_vse_operator)

def unregister():
    bpy.utils.unregister_class(EXAMPLE_OT_simple_vse_operator)
    
if __name__ == '__main__':
    register()
