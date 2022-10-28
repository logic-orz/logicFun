import pywintypes
import win32clipboard as wcb
import win32con as wc


def setClipboard(text: str):
    wcb.OpenClipboard()
    wcb.EmptyClipboard()

    wcb.SetClipboardData(wc.CF_TEXT, text.encode("gbk"))
    wcb.CloseClipboard()
