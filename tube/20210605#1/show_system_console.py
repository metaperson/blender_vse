def toggle_system_console():
    import bpy
    bpy.ops.wm.console_toggle()


def show_system_console(show):
    import ctypes

    # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-showwindow
    SW_HIDE = 0
    SW_SHOW = 5
    
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), SW_SHOW if show else SW_HIDE)
    

if __name__ == '__main__':
    #toggle_system_console()
    #show_system_console(True)
    show_system_console(False)
    