import bpy

owner = object()
scene_workspace = dict()
prevent_workspace_callback = False

def cleanup_scene_workspace():
    global scene_workspace
    removes = list()
    for scene in scene_workspace:
        if str(scene) == '<bpy_struct, Scene invalid>':
            removes.append(scene)
        elif str(scene_workspace[scene]) == '<bpy_struct, WorkSpace invalid>':
            removes.append(scene)
    for remove in removes:
        del(scene_workspace[remove])
            
def workspace_change_callback():
    global scene_workspace
    global prevent_workspace_callback
    cleanup_scene_workspace()
    if not prevent_workspace_callback:
        scene_workspace[bpy.context.scene] = bpy.context.workspace
    prevent_workspace_callback = False

def scene_change_callback():
    global scene_workspace
    global prevent_workspace_callback
    cleanup_scene_workspace()
    if bpy.context.scene in scene_workspace:
        if bpy.context.window.workspace != scene_workspace[bpy.context.scene]:
            prevent_workspace_callback = True
            bpy.context.window.workspace = scene_workspace[bpy.context.scene]
    else:
        scene_workspace[bpy.context.scene] = bpy.context.workspace

def register():
    bpy.msgbus.subscribe_rna(key=(bpy.types.Window, "scene"),
                             owner=owner,
                             args=(),
                             notify=scene_change_callback,
                             options={"PERSISTENT"})

    bpy.msgbus.subscribe_rna(key=(bpy.types.Window, "workspace"),
                             owner=owner,
                             args=(),
                             notify=workspace_change_callback,
                             options={"PERSISTENT"})
                             
def unregister():
    bpy.msgbus.clear_by_owner(owner)
    
if __name__ == '__main__':
    scene_workspace.clear()
    scene_workspace[bpy.context.scene] = bpy.context.workspace
    register()
