#!/usr/bin/python
"""
This reads text from the clipboard and replaces emojis in a string with their
canonical names. It displays the result, and also stores it on the clipboard.
(This is intended to be bound to a hotkey for easy use from any application.)

Requirements:
    apt install python3-{tk,emoji,pyperclip}

And, for use on wayland also:
    apt install wl-clipboard
"""

import os
from emoji import demojize
from tkinter.messagebox import showinfo
if os.environ.get('WAYLAND_DISPLAY'):
    # pyperclip prefers the gtk clipboard api, which doesn't work for me.
    from pyperclip import init_wl_clipboard
    copy, paste = init_wl_clipboard()
else:
    from pyperclip import copy, paste
copy(result := demojize(paste()))
showinfo('demoji', result)
