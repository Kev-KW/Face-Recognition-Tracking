"""Timestamped face-entry event logging."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


def record_face_entry(log_path: Path, point: tuple[int, int]) -> None:
	"""Append one timestamped line when a face enters the camera view."""

	log_path.parent.mkdir(parents=True, exist_ok=True)
	timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
	with log_path.open("a", encoding="utf-8") as log_file:
		log_file.write(f"{timestamp} - Face detected at ({point[0]}, {point[1]})\n")
