import sys
if sys.version_info.major == 3:
    import tkinter as Tk, tkinter.font as tkFont
else:
    import Tkinter as Tk, tkFont
root = Tk.Tk()

print(tkFont.families())
print(tkFont.names())
if "Bell MT" in tkFont.families():print("In Familie")
if "Bell MT" in tkFont.names(): print("In Names")
#Bell MT