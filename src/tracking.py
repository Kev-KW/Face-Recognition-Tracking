"""Face detection, smoothing, and camera-frame drawing."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence

import cv2


@dataclass(frozen=True)
class FaceTarget:
	"""A detected face rectangle and its center point in image coordinates."""

	x: int
	y: int
	width: int
	height: int

	@property
	def center(self) -> tuple[int, int]:
		return (self.x + self.width // 2, self.y + self.height // 2)


class ExponentialSmoother:
	"""Smooth a moving point while still following it responsively."""

	def __init__(self, response: float = 0.35) -> None:
		if not 0.0 < response <= 1.0:
			raise ValueError("response must be greater than 0 and at most 1")
		self.response = response
		self._point: Optional[tuple[float, float]] = None

	def update(self, point: tuple[int, int]) -> tuple[int, int]:
		if self._point is None:
			self._point = (float(point[0]), float(point[1]))
		else:
			self._point = tuple(
				current + self.response * (target - current)
				for current, target in zip(self._point, point)
			)
		return round(self._point[0]), round(self._point[1])

	def reset(self) -> None:
		self._point = None


def choose_largest_face(detections: Sequence[Sequence[int]]) -> Optional[FaceTarget]:
	"""Return the largest detected face, or None when no face was found."""

	if len(detections) == 0:
		return None
	x, y, width, height = max(detections, key=lambda box: box[2] * box[3])
	return FaceTarget(int(x), int(y), int(width), int(height))


def draw_target(frame, target: FaceTarget, point: tuple[int, int]) -> None:
	"""Draw the face bounds, crosshair, and high-contrast pinpoint."""

	x, y, width, height = target.x, target.y, target.width, target.height
	frame_height, frame_width = frame.shape[:2]
	crosshair_color = (255, 180, 0)
	cv2.line(frame, (point[0], 0), (point[0], frame_height - 1), crosshair_color, 1)
	cv2.line(frame, (0, point[1]), (frame_width - 1, point[1]), crosshair_color, 1)
	cv2.rectangle(frame, (x, y), (x + width, y + height), (80, 220, 120), 2)
	cv2.circle(frame, point, 13, (0, 0, 0), -1)
	cv2.circle(frame, point, 9, (0, 70, 255), -1)
	cv2.circle(frame, point, 3, (255, 255, 255), -1)
