"""Face tracking application implementation."""

from __future__ import annotations

import argparse

import cv2
import pygame
from settings import (
	ALARM_SOUND,
	ALARM_VOLUME,
	CAMERA_HEIGHT,
	CAMERA_INDEX,
	CAMERA_WIDTH,
	FACE_MIN_NEIGHBORS,
	FACE_MIN_SIZE,
	FACE_SCALE_FACTOR,
	FACE_EVENT_LOG,
	SMOOTHING_RESPONSE,
	TOP_ZONE_FRACTION,
	VIDEO_OVERLAY,
	VOICE_VOLUME,
	WINDOW_FULLSCREEN,
	WINDOW_HEIGHT,
	WINDOW_NAME,
	WINDOW_WIDTH,
)
from tracking import ExponentialSmoother, choose_largest_face, draw_target
from visual_effects import apply_countdown_tint
from voice import CountdownSpeaker
from video_overlay import VideoOverlay
from event_log import record_face_entry
from window_controls import disable_close_button


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Track the center of the nearest face.")
	parser.add_argument("--camera", type=int, default=CAMERA_INDEX, help=f"Camera index (default: {CAMERA_INDEX}).")
	parser.add_argument(
		"--smoothing",
		type=float,
		default=SMOOTHING_RESPONSE,
		help=f"Tracking response from 0 to 1 (default: {SMOOTHING_RESPONSE}).",
	)
	parser.add_argument("--width", type=int, default=CAMERA_WIDTH, help="Requested camera width.")
	parser.add_argument("--height", type=int, default=CAMERA_HEIGHT, help="Requested camera height.")
	return parser.parse_args()


def main() -> None:
	args = parse_args()
	smoother = ExponentialSmoother(args.smoothing)
	if not ALARM_SOUND.is_file():
		raise FileNotFoundError(f"Alarm sound not found: {ALARM_SOUND}")
	pygame.mixer.init()
	alarm_sound = pygame.mixer.Sound(str(ALARM_SOUND))
	alarm_sound.set_volume(ALARM_VOLUME)
	countdown = CountdownSpeaker(volume=VOICE_VOLUME)
	video_overlay = VideoOverlay(VIDEO_OVERLAY)
	if not hasattr(cv2, "CascadeClassifier"):
		raise RuntimeError(
			"This tracker requires OpenCV 4.x. Run "
			"'py -m pip install --force-reinstall -r requirements.txt' and try again."
		)
	cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
	detector = cv2.CascadeClassifier(cascade_path)
	if detector.empty():
		raise RuntimeError(f"Could not load face detector: {cascade_path}")

	camera = cv2.VideoCapture(args.camera)
	camera.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
	camera.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)
	if not camera.isOpened():
		raise RuntimeError(f"Could not open camera {args.camera}")

	cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
	disable_close_button(WINDOW_NAME)
	if WINDOW_FULLSCREEN:
		cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
	else:
		cv2.resizeWindow(WINDOW_NAME, WINDOW_WIDTH, WINDOW_HEIGHT)
	print("Camera tracking started. Press Q or Esc in the video window to quit.")
	alarm_active = False
	video_started = False
	video_active = False
	face_in_frame = False
	try:
		while True:
			success, frame = camera.read()
			if not success:
				print("Could not read a frame from the camera.")
				break

			if video_active:
				overlay_frame = video_overlay.next_frame(frame.shape[1], frame.shape[0])
				if overlay_frame is None:
					video_active = False
					continue
				cv2.imshow(WINDOW_NAME, overlay_frame)
				key = cv2.waitKeyEx(1) & 0xFF
				if key in (ord("q"), ord("Q")):
					break
				continue

			frame = cv2.flip(frame, 1)
			grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			detections = detector.detectMultiScale(
				grayscale,
				scaleFactor=FACE_SCALE_FACTOR,
				minNeighbors=FACE_MIN_NEIGHBORS,
				minSize=FACE_MIN_SIZE,
			)
			target = choose_largest_face(detections)

			if target is None:
				face_in_frame = False
				smoother.reset()
				countdown.update(False)
				video_overlay.stop()
				video_started = False
				video_active = False
				if alarm_active:
					alarm_sound.stop()
				alarm_active = False
				print("\rTarget: (no face)", end="", flush=True)
				cv2.putText(
					frame,
					"No face detected",
					(24, 42),
					cv2.FONT_HERSHEY_SIMPLEX,
					0.9,
					(0, 70, 255),
					2,
					cv2.LINE_AA,
				)
			else:
				point = smoother.update(target.center)
				if not face_in_frame:
					record_face_entry(FACE_EVENT_LOG, point)
					face_in_frame = True
				draw_target(frame, target, point)
				in_top_zone = point[1] < frame.shape[0] * TOP_ZONE_FRACTION
				countdown.update(in_top_zone)
				if not in_top_zone:
					video_overlay.stop()
					video_started = False
					video_active = False
				elif countdown.finished and not video_started:
					video_started = True
					video_active = video_overlay.start()
					if not video_active:
						print(f"\nVideo overlay not found or could not open: {VIDEO_OVERLAY}")
				if in_top_zone and not alarm_active:
					alarm_sound.play(loops=-1)
					alarm_active = True
				elif not in_top_zone or countdown.finished:
					alarm_sound.stop()
					alarm_active = False
				print(f"\rTarget: ({point[0]}, {point[1]})", end="", flush=True)
				cv2.putText(
					frame,
					f"({point[0]}, {point[1]})",
					(24, 42),
					cv2.FONT_HERSHEY_SIMPLEX,
					0.75,
					(80, 220, 120),
					2,
					cv2.LINE_AA,
				)
				if alarm_active:
					cv2.putText(
						frame,
						"ALARM: FACE IN TOP QUARTER",
						(24, 82),
						cv2.FONT_HERSHEY_SIMPLEX,
						0.75,
						(0, 0, 255),
						2,
						cv2.LINE_AA,
					)

			apply_countdown_tint(frame, countdown.progress)
			cv2.imshow(WINDOW_NAME, frame)
			key = cv2.waitKeyEx(1) & 0xFF
			if key in (ord("q"), ord("Q")):
				break
	finally:
		print()
		countdown.stop()
		alarm_sound.stop()
		video_overlay.stop()
		pygame.mixer.quit()
		camera.release()
		cv2.destroyAllWindows()
