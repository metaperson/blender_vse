import bpy
from bpy_extras.io_utils import ImportHelper

class VSE_TOOLS_OT_import_strips(bpy.types.Operator, ImportHelper):
    bl_description = 'import strips'
    bl_idname = 'vse_tools.import_strips'
    bl_label = 'Import Strips'

    files: bpy.props.CollectionProperty(name='Import Strips', type=bpy.types.OperatorFileListElement)

    order_by: bpy.props.EnumProperty(name='Order by',
                description='Strips are sorted by this order',
                items=[('PICK',         'Pick',                 'No Sort, as selected order'),
                       ('CREATE_TIME',  'File Create Time',     'Sort order by the file created time'),
                       ('FILE_NAME',    'File Name',            'Sort order by the file name'),
                       ('FILE_SIZE',    'File Size',            'Sort order by the file size')],
                default='FILE_NAME')

    reversed_order: bpy.props.BoolProperty(name='Reversed order', description='Reversed order for sorting', default=False)
    
    channel: bpy.props.IntProperty(name='Channel', description='Assign channel to put strips', default=1, min=1)
    
    fit_method: bpy.props.EnumProperty(name='Fit Method',
                description='Scale fit method',
                items=[('FIT',          'Scale to Fit',         'Scale image to fit within the canvas'),
                       ('FILL',         'Scale to Fill',        'Scale image to completely fill the canvas'),
                       ('STRETCH',      'Stretch to Fill',      'Stretch image to fill the canvas'),
                       ('ORIGINAL',     'Use Original Size',    'Keep image at its original size')],
                default='FIT')

    image_strip_length: bpy.props.IntProperty(name='Image Length', description='Image strip length', default=25, min=1)

    @classmethod
    def poll(cls, context):
        if not bpy.ops.sequencer.movie_strip_add.poll():
            return False
        if not bpy.ops.sequencer.sound_strip_add.poll():
            return False
        if not bpy.ops.sequencer.image_strip_add.poll():
            return False
        return True

    def execute(self, context):
        import os
        #print('ImportHelper.files : {}'.format(self.files))
        #print('file path : {}'.format(self.filepath))
        #print('Sort by order : {}'.format(self.order_by))
        
        strip_dirname = os.path.dirname(self.filepath)
        strip_files = self.files

        #for strip_file in strip_files:
        #    print(strip_file)

        if self.order_by == 'PICK':
            if self.reversed_order:
                strip_files = reversed(strip_files)
            else:
                strip_files = list(strip_files)
        elif self.order_by == 'CREATE_TIME':
            strip_files = sorted(strip_files, key=lambda x: os.path.getctime(os.path.join(strip_dirname, x.name)), reverse=self.reversed_order)
        elif self.order_by == 'FILE_NAME':
            strip_files = sorted(strip_files, key=lambda x: x.name, reverse=self.reversed_order)
        elif self.order_by == 'FILE_SIZE':
            strip_files = sorted(strip_files, key=lambda x: os.path.getsize(os.path.join(strip_dirname, x.name)), reverse=self.reversed_order)
        else:
            return {'CANCELLED'}

        # for strip_file in strip_files:
        #     print(strip_file)

        count_movie = 0
        count_sound = 0
        count_image = 0
        
        for strip_file in strip_files:
            strip_ext = os.path.splitext(strip_file.name)[1].lower()
            # print(strip_dirname, strip_file.name, strip_ext)
            frame_start = max([seq.frame_final_end for seq in context.sequences] or [0])
            if strip_ext in ('.avi', '.mp4', '.mpg', '.mpeg', '.mov', '.mkv', '.dv', '.flv'):
                strip_path = os.path.join(strip_dirname, strip_file.name)
                bpy.ops.sequencer.movie_strip_add(filepath=strip_path,
                                                  frame_start=frame_start,
                                                  channel=self.channel,
                                                  fit_method=self.fit_method)
                count_movie += 1
            elif strip_ext in ('.acc', '.ac3', '.flac', '.mp2', '.mp3', '.m4a','.pcm', '.ogg'):
                strip_path = os.path.join(strip_dirname, strip_file.name)
                bpy.ops.sequencer.sound_strip_add(filepath=strip_path,
                                                  frame_start=frame_start,
                                                  channel=self.channel)
                count_sound += 1
            elif strip_ext in ('.jpg', '.jpeg', '.bmp', '.png', '.gif', '.tga', '.tiff'):
                bpy.ops.sequencer.image_strip_add(directory=strip_dirname + '\\', files=[{"name":strip_file.name, "name":strip_file.name}],
                                                  show_multiview=False,
                                                  frame_start=frame_start, frame_end=frame_start+self.image_strip_length,
                                                  channel=self.channel,
                                                  fit_method=self.fit_method)
                count_image += 1
                                                  
        self.report({'INFO'}, 'Imported Movie[{}], Sound[{}], Image[{}], Total[{}]'.format(count_movie,
                                                                                           count_sound,
                                                                                           count_image,
                                                                                           count_movie + count_sound + count_image))

        return {'FINISHED'}

def register():
    bpy.utils.register_class(VSE_TOOLS_OT_import_strips)

def unregister():
    bpy.utils.unregister_class(VSE_TOOLS_OT_import_strips)
    
if __name__ == '__main__':
    register()
    #bpy.ops.vse_tools.VSE_TOOLS_OT_import_strips('INVOKE_DEFAULT')
    #bpy.ops.vse_tools.VSE_TOOLS_OT_import_strips('EXEC_DEFAULT')
    #unregister()
