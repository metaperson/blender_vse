bl_info = {
    "name": "Add a keymap for sequencer",
    "author": "meta person",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "category": "Sequencer",
}

import bpy

addon_keymaps = list()

def register():
    wm = bpy.context.window_manager
    kcfg = wm.keyconfigs.addon

    if kcfg:
        km = kcfg.keymaps.new(name= 'Sequencer', space_type= 'SEQUENCE_EDITOR', region_type= 'WINDOW')
        
        kmi = km.keymap_items.new("screen.frame_offset", type= 'RIGHT_ARROW', value= 'PRESS', ctrl= True, repeat= True)
        kmi.properties.delta = 10
        addon_keymaps.append((km,kmi))

        kmi = km.keymap_items.new("screen.frame_offset", type= 'LEFT_ARROW', value= 'PRESS', ctrl= True, repeat= True)
        kmi.properties.delta = -10
        addon_keymaps.append((km,kmi))

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == '__main__':
    register()
    