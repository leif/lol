#!/usr/bin/env python
"""
Take a screenshot, OCR it with tesseract (in German mode), display text the
text, put it on the clipboard, and ask if it should be opened in firefox's
offline translator.

This is intended to be bound to a hotkey for easy use.

based on https://github.com/edwineas/ubuntu-text-capture/blob/master/main.py

apt install python3-{tk,tesserocr}
"""
import os
import tesserocr
from PIL import Image
from tkinter.messagebox import askokcancel
from subprocess import call
from urllib.parse import quote

if os.environ.get("WAYLAND_DISPLAY"):
    # pyperclip prefers the gtk clipboard api, which doesn't work for me.
    from pyperclip import init_wl_clipboard

    copy, paste = init_wl_clipboard()
else:
    from pyperclip import copy, paste


def capture_screenshot():
    screenshot_path = "/tmp/screenshot.png"

    os.system(f"gnome-screenshot -a -f {screenshot_path}")

    screenshot = Image.open(screenshot_path)

    text = tesserocr.image_to_text(screenshot, lang="deu").strip()

    os.remove(screenshot_path)

    copy(text)

    if askokcancel("Translate?", text):
        call(
            [
                "firefox",
                "--private-window",
                f"about:translations#src=detect&trg=en&text={quote(text)}",
            ]
        )


if __name__ == "__main__":
    capture_screenshot()
