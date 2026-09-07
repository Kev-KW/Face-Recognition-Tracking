"""Windows-specific window behavior helpers."""

from __future__ import annotations

import ctypes


SC_CLOSE = 0xF060
MF_BYCOMMAND = 0x00000000
MF_GRAYED = 0x00000001


def disable_close_button(window_name: str) -> None:
	"""Disable the Windows close command so only Q exits the tracker."""

	user32 = ctypes.windll.user32
	hwnd = user32.FindWindowW(None, window_name)
	if not hwnd:
		return
	system_menu = user32.GetSystemMenu(hwnd, False)
	if system_menu:
		user32.EnableMenuItem(system_menu, SC_CLOSE, MF_BYCOMMAND | MF_GRAYED)
