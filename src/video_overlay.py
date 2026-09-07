"""Video playback for the post-countdown camera overlay."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path
from typing import Optional

import cv2
import imageio_ffmpeg
import pygame


class VideoOverlay:
	"""Play a video file over the camera frame once from start to finish."""

	def __init__(self, video_path: Path) -> None:
		self.video_path = video_path
		self.capture: Optional[cv2.VideoCapture] = None
		self.audio: Optional[pygame.mixer.Sound] = None
		self.audio_channel: Optional[pygame.mixer.Channel] = None
		self.audio_path: Optional[Path] = None

	def start(self) -> bool:
		if not self.video_path.is_file():
			return False
		self.stop()
		self.capture = cv2.VideoCapture(str(self.video_path))
		if not self.capture.isOpened():
			self.stop()
			return False
		self._start_audio()
		return True

	def _start_audio(self) -> None:
		try:
			temporary_audio = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
			temporary_audio.close()
			self.audio_path = Path(temporary_audio.name)
			subprocess.run(
				[
					imageio_ffmpeg.get_ffmpeg_exe(),
					"-y",
					"-i",
					str(self.video_path),
					"-vn",
					"-acodec",
					"pcm_s16le",
					"-ar",
					"44100",
					"-ac",
					"2",
					str(self.audio_path),
				],
				check=True,
				stdout=subprocess.DEVNULL,
				stderr=subprocess.DEVNULL,
			)
			self.audio = pygame.mixer.Sound(str(self.audio_path))
			self.audio_channel = self.audio.play()
		except (OSError, RuntimeError, subprocess.SubprocessError):
			self._cleanup_audio()

	def next_frame(self, width: int, height: int):
		if self.capture is None:
			return None
		success, frame = self.capture.read()
		if not success:
			self.stop()
			return None
		return cv2.resize(frame, (width, height), interpolation=cv2.INTER_LINEAR)

	def stop(self) -> None:
		if self.capture is not None:
			self.capture.release()
			self.capture = None
		if self.audio_channel is not None:
			self.audio_channel.stop()
		self.audio_channel = None
		self.audio = None
		self._cleanup_audio()

	def _cleanup_audio(self) -> None:
		if self.audio_path is not None:
			self.audio_path.unlink(missing_ok=True)
			self.audio_path = None
