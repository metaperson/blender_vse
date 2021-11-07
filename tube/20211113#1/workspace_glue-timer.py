bl_info = {
    'name': 'Workspace Glue - timer version',
    'author': 'Meta Person',
    'version': (1, 0),
    'blender': (2, 80, 0),
    'description': 'Changing the workspace as when the scene changed.\n'
                   'It uses a timer to detect changing the workspace and the scene.',
    'category': 'Sequencer',
}

import re
import bpy
from bpy.app.handlers import persistent 

DEBUG = False
scene_workspace = dict()
last_scene = None
last_workspace = None

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

def change_event_polling_loop():
    global scene_workspace
    global last_scene
    global last_workspace

    # CAUTION : Do processing about the workspace first.
    #           If not, a workspace changing is rise twice when the scene is changed.
    if last_workspace is not bpy.context.workspace:
        if DEBUG: print(f'workspace is changed {last_workspace.name:16} -> {bpy.context.workspace.name:16}')
        cleanup_scene_workspace()
        scene_workspace[bpy.context.scene] = bpy.context.workspace
        last_workspace = bpy.context.workspace

    # CAUTION : Do processing about the scene after processing the workspace.
    #           If not, a workspace changing is rise twice when the scene is changed.
    if last_scene is not bpy.context.scene:
        if DEBUG: print(f'scene is changed {last_scene.name:16} -> {bpy.context.scene.name:16}')
        cleanup_scene_workspace()
        if bpy.context.scene in scene_workspace:
            if bpy.context.scene is not scene_workspace[bpy.context.scene]:
                # NOTE : change 'bpy.context.window.workspace' instead of 'bpy.context.workspace'.
                #        because 'bpy.context.workspace' is read only.
                # NOTE : 'bpy.context.window.workspace' is not applied immediately after assignment.
                #        Do not do processing about the workspace after this.
                bpy.context.window.workspace = scene_workspace[bpy.context.scene]
                # prevent the workspace event from rising.
                last_workspace = scene_workspace[bpy.context.scene]
        else:
            scene_workspace[bpy.context.scene] = bpy.context.workspace
        last_scene = bpy.context.scene
    return 0.1

def mapping_workspace():
    global scene_workspace
    
    workspaces = dict()
    workspaces = {'Layout': None,
                  'Animation': None,
                  'Modeling': None,
                  'Sculpting': None,
                  'Shading': None,
                  '2D Animation': None,
                  '2D Full Canvas': None,
                  'Video Editing': None}
    
    if DEBUG: print(f'workspace group')
    for workspace in bpy.data.workspaces:
        key = re.sub('[.][0-9]+$','',workspace.name)
        workspaces[key] = workspace
        if DEBUG: print(f'  {workspace.name:16} -> {key:10}')

    workspace_vse = workspaces['Video Editing']
    workspace_2d = workspaces['2D Animation'] or workspaces['2D Full Canvas']
    workspace_3d = workspaces['Layout'] or workspaces['Animation'] or workspaces['Modeling'] or workspaces['Sculpting'] or workspaces['Sculpting']

    if DEBUG: print(f'workspace default: vse={workspace_vse.name}, 2D={workspace_2d.name}, 3D={workspace_3d.name}')

    for scene in bpy.data.scenes:
        sequence_count = len(scene.sequence_editor.sequences_all) if scene.sequence_editor else 0
        collection_2d_count = len(list(filter(lambda x: x.type in ['GPENCIL', 'EMPTY'], scene.collection.all_objects)))
        collection_3d_count = len(list(filter(lambda x: x.type not in ['GPENCIL', 'EMPTY'], scene.collection.all_objects)))
        
        if DEBUG:
            print(f'scene[{scene.name:16}] objects: seq={sequence_count} 2D={collection_2d_count} 3D={collection_3d_count}')
            for obj in scene.collection.all_objects:
                print(f'  name={obj.name:16} type={obj.type:10} empty={obj.empty_display_type:16}')

        if sequence_count > 0:
            if workspace_vse:
                scene_workspace[scene] = workspace_vse
        elif collection_3d_count > 0:
            if workspace_3d or workspace_2d:
                scene_workspace[scene] = workspace_3d or workspace_2d
        elif collection_2d_count > 0:
            if workspace_2d or workspace_3d:
                scene_workspace[scene] = workspace_2d or workspace_3d

@persistent
def load_post_handler(dummy):
    scene_workspace.clear()
    cleanup_scene_workspace()
    mapping_workspace()

    last_scene = bpy.context.scene
    last_workspace = bpy.context.workspace

    print(f'Workspace Glue: scene[{len(bpy.data.scenes)}], workspace[{len(bpy.data.workspaces)}]')
    for scene in bpy.data.scenes:
        if scene in scene_workspace:
            print(f'  {scene.name:<30} -> {scene_workspace[scene].name:<20}') 

def register():
    # CAUTION : 'bpy.context.scene' can not be available in the registering time.
    global last_scene
    global last_workspace
    
    print('Workspace Glue: the event polling loop is enabled. (for detecting the change of the workspace and scene)')
    bpy.app.timers.register(change_event_polling_loop, persistent=True)
    
    bpy.app.handlers.load_post.append(load_post_handler)

def unregister():
    bpy.app.handlers.load_post.remove(load_post_handler)

    if bpy.app.timers.is_registered(change_event_polling_loop):
        bpy.app.timers.unregister(change_event_polling_loop)
        print('Workspace Glue: the event polling loop is disabled. (for detecting the change of the workspace and scene)')
    
    scene_workspace.clear()

if __name__ == '__main__':
    # This for debugging
    import ctypes
    # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-showwindow
    SW_HIDE = 0
    SW_SHOW = 5
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), SW_SHOW)

    DEBUG = True

    scene_workspace.clear()
    cleanup_scene_workspace()
    mapping_workspace()

    last_scene = bpy.context.scene
    last_workspace = bpy.context.workspace
    scene_workspace[bpy.context.scene] = bpy.context.workspace

    print(f'Workspace Glue: scene[{len(bpy.data.scenes)}], workspace[{len(bpy.data.workspaces)}]')
    for scene in bpy.data.scenes:
        if scene in scene_workspace:
            print(f'  {scene.name:<30} -> {scene_workspace[scene].name:<20}') 

    print('Workspace Glue: the event polling loop is enabled. (for detecting the change of the workspace and scene)')
    bpy.app.timers.register(change_event_polling_loop)
    #register()

