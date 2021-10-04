def show_system_console(show):
    import ctypes

    # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-showwindow
    SW_HIDE = 0
    SW_SHOW = 5
    
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(),
                                    SW_SHOW if show else SW_HIDE)
    

def set_system_console_topmost(top):
    import ctypes

    # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowpos
    HWND_NOTOPMOST = -2
    HWND_TOPMOST = -1
    HWND_TOP = 0
    SWP_NOMOVE = 0x0002
    SWP_NOSIZE = 0x0001
    SWP_NOZORDER = 0x0004
    
    ctypes.windll.user32.SetWindowPos(ctypes.windll.kernel32.GetConsoleWindow(),
                                        HWND_TOP if top else HWND_NOTOPMOST,
                                        0,0,0,0, SWP_NOMOVE | SWP_NOSIZE)
                                        
if __name__ == '__main__':
    show_system_console(True)
    #show_system_console(False)
    set_system_console_topmost(True)
    
    