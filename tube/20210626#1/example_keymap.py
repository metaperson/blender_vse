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
    kcfg = bpy.context.window_manager.keyconfigs.addon
    km = kcfg.keymaps.new(name= 'Sequencer', space_type= 'SEQUENCE_EDITOR', region_type= 'WINDOW')
    
    kmi = km.keymap_items.new("screen.frame_offset", type= 'RIGHT_ARROW', value= 'PRESS', ctrl= True, repeat= True)
    kmi.properties.delta = 10
    addon_keymaps.append((km,kmi))

    kmi = km.keymap_items.new("screen.frame_offset", type= 'LEFT_ARROW', value= 'PRESS', ctrl= True, repeat= True)
    kmi.properties.delta = -10
    addon_keymaps.append((km,kmi))

    kmi = km.keymap_items.new("screen.frame_offset", type= 'RIGHT_ARROW', value= 'PRESS', ctrl= True, shift= True, repeat= True)
    kmi.properties.delta = 20
    addon_keymaps.append((km,kmi))

    kmi = km.keymap_items.new("screen.frame_offset", type= 'LEFT_ARROW', value= 'PRESS', ctrl= True, shift= True, repeat= True)
    kmi.properties.delta = -20
    addon_keymaps.append((km,kmi))

    kmi = km.keymap_items.new("anim.change_frame", type= 'PERIOD', value= 'PRESS', shift= False)
    addon_keymaps.append((km,kmi))
    
def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

