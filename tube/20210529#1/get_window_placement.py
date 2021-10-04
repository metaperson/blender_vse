import ctypes
import ctypes.wintypes
from typing import Tuple

# URL : https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-windowplacement
#   typedef struct tagWINDOWPLACEMENT {
#       UINT  length;
#       UINT  flags;
#       UINT  showCmd;
#       POINT ptMinPosition;
#       POINT ptMaxPosition;
#       RECT  rcNormalPosition;
#       RECT  rcDevice;
#   } WINDOWPLACEMENT;
class tagWINDOWPLACEMENT(ctypes.Structure):
    _fields_ = [
        ('length', ctypes.wintypes.UINT),
        ('flags', ctypes.wintypes.UINT),
        ('showCmd', ctypes.wintypes.UINT),
        ('ptMinPosition', ctypes.wintypes.POINT),
        ('ptMaxPosition', ctypes.wintypes.POINT),
        ('rcNormalPosition', ctypes.wintypes.RECT),
        ('rcDevice', ctypes.wintypes.RECT),
    ]
assert ctypes.sizeof(tagWINDOWPLACEMENT) == 60, ctypes.sizeof(tagWINDOWPLACEMENT)
assert ctypes.alignment(tagWINDOWPLACEMENT) == 4, ctypes.alignment(tagWINDOWPLACEMENT)

# URL : https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowplacement
#   BOOL GetWindowPlacement(
#       HWND            hWnd,
#       WINDOWPLACEMENT *lpwndpl
#   );
def GetWindowPlacement(hWnd : ctypes.wintypes.HWND) -> Tuple[ctypes.wintypes.BOOL, tagWINDOWPLACEMENT]:
    _GetWindowPlacement = ctypes.windll.user32.GetWindowPlacement
    _GetWindowPlacement.argtypes = [ctypes.wintypes.HWND, ctypes.POINTER(tagWINDOWPLACEMENT)]
    _GetWindowPlacement.restype  = ctypes.wintypes.BOOL
    wndpl = tagWINDOWPLACEMENT()
    wndpl.length = ctypes.sizeof(tagWINDOWPLACEMENT)
    return _GetWindowPlacement(hWnd, ctypes.byref(wndpl)), wndpl

if __name__ == '__main__':
    hWnd = ctypes.windll.kernel32.GetConsoleWindow()
    ret, wndpl = GetWindowPlacement(hWnd)
    print('the func returns : {}'.format(ret))
    print('length : {}'.format(wndpl.length))
    print('flags : {}'.format(wndpl.flags))
    print('showCmd : {}'.format(wndpl.showCmd))
    print('ptMinPosition : {},{}'.format(wndpl.ptMinPosition.x, wndpl.ptMinPosition.y))
    print('ptMaxPosition : {},{}'.format(wndpl.ptMaxPosition.x, wndpl.ptMaxPosition.y))
    print('rcNormalPosition : {},{},{},{}'.format(wndpl.rcNormalPosition.left, wndpl.rcNormalPosition.top,
                                                  wndpl.rcNormalPosition.right, wndpl.rcNormalPosition.bottom))
    print('rcDevice : {},{},{},{}'.format(wndpl.rcDevice.left, wndpl.rcDevice.top,
                                          wndpl.rcDevice.right, wndpl.rcDevice.bottom))
