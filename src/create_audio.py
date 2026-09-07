"""Generate one local Mike WAV file from settings.VOICE_SCRIPT."""

from __future__ import annotations

import argparse
from pathlib import Path

import requests
from settings import VOICE_API_URL, VOICE_AUDIO_FILE, VOICE_NAME, VOICE_PITCH, VOICE_SCRIPT, VOICE_SPEED


def create_audio(output_path: Path, force: bool) -> None:
	if output_path.exists() and not force:
		print(f"Already exists: {output_path}")
		print("Use --force to regenerate it.")
		return

	output_path.parent.mkdir(parents=True, exist_ok=True)
	print(f"Generating Mike audio: {output_path}")
	response = requests.get(
		VOICE_API_URL,
		params={
				"text": " ".join(VOICE_SCRIPT.splitlines()),
			"voice": VOICE_NAME,
			"pitch": VOICE_PITCH,
			"speed": VOICE_SPEED,
		},
		timeout=60,
	)
	response.raise_for_status()
	output_path.write_bytes(response.content)
	print(f"Audio ready: {output_path}")


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Generate one Mike WAV file for the full countdown script.")
	parser.add_argument("--output", type=Path, default=VOICE_AUDIO_FILE, help="Output WAV path.")
	parser.add_argument("--force", action="store_true", help="Regenerate the existing WAV file.")
	return parser.parse_args()


if __name__ == "__main__":
	args = parse_args()
	create_audio(args.output, args.force)
