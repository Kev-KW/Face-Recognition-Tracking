"""Visual effects applied to the live camera frame."""

from __future__ import annotations

import cv2
from settings import COUNTDOWN_TINT_MAX_OPACITY


def apply_countdown_tint(
	frame,
	progress: float,
	maximum_opacity: float = COUNTDOWN_TINT_MAX_OPACITY,
) -> None:
	"""Increase a red screen tint from clear to maximum as progress reaches one."""

	progress = max(0.0, min(1.0, progress))
	opacity = progress * maximum_opacity
	if opacity == 0.0:
		return
	red_frame = frame.copy()
	red_frame[:] = (0, 0, 255)
	cv2.addWeighted(frame, 1.0 - opacity, red_frame, opacity, 0.0, dst=frame)
