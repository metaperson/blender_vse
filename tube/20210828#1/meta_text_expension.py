bl_info = {
    'name': 'Meta Text Expension',
    'author': 'Meta Person',
    'version': (1, 0),
    'blender': (2, 80, 0),
    'description': 'The text expansion for the meta-data',
    'category': 'Sequencer',
}

import bpy
from bpy.app.handlers import persistent

@persistent
def meta_text_handler(scene):
    for strip in scene.sequence_editor.sequences_all:
        if strip.type == 'TEXT':
            if strip.name == '@meta.frame':
                strip.text = str(scene.frame_current)
            elif strip.name == '@meta.time':
                strip.text = bpy.utils.smpte_from_frame(scene.frame_current)

def register():
    bpy.app.handlers.frame_change_pre.append(meta_text_handler)
    bpy.app.handlers.render_pre.append(meta_text_handler)

def unregister():
    bpy.app.handlers.frame_change_pre.remove(meta_text_handler)
    bpy.app.handlers.render_pre.remove(meta_text_handler)
