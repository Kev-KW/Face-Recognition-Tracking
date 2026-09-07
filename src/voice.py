"""Local playback for the single generated Mike countdown WAV."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Optional

import pygame
from settings import VOICE_AUDIO_FILE, VOICE_VOLUME


class CountdownSpeaker:
	"""Play one complete pre-generated WAV script while the face stays in-zone."""

	def __init__(
		self,
		voice_name: str = "Mike (for Telephone)",
		text_path: Optional[Path] = None,
		pitch: int = 110,
		speed: int = 150,
		volume: float = VOICE_VOLUME,
		audio_path: Path = VOICE_AUDIO_FILE,
	) -> None:
		if not audio_path.is_file():
			raise FileNotFoundError(
				f"Generated audio not found: {audio_path}. "
				"Run 'py src/create_audio.py' first."
			)
		self.sound = pygame.mixer.Sound(str(audio_path))
		self.sound.set_volume(volume)
		self.channel: Optional[pygame.mixer.Channel] = None
		self.started_at: Optional[float] = None
		self.duration = self.sound.get_length()

	def update(self, in_zone: bool) -> None:
		if not in_zone:
			self.stop()
			return
		if self.channel is None:
			self.channel = self.sound.play()
			self.started_at = time.monotonic()

	def stop(self) -> None:
		if self.channel is not None:
			self.channel.stop()
		self.channel = None
		self.started_at = None

	@property
	def finished(self) -> bool:
		return self.channel is not None and not self.channel.get_busy()

	@property
	def progress(self) -> float:
		if self.started_at is None or self.duration <= 0:
			return 0.0
		return min(1.0, (time.monotonic() - self.started_at) / self.duration)
