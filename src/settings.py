"""All user-adjustable application settings and asset paths."""

from pathlib import Path

WINDOW_NAME = "Face Center Tracking"
WINDOW_FULLSCREEN = False
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Camera and tracking
CAMERA_INDEX = 0
CAMERA_WIDTH = WINDOW_WIDTH
CAMERA_HEIGHT = WINDOW_HEIGHT
SMOOTHING_RESPONSE = 0.35
TOP_ZONE_FRACTION = 1 # Area of the screen that is considered "in-zone" for the face center
FACE_SCALE_FACTOR = 1.1
FACE_MIN_NEIGHBORS = 5
FACE_MIN_SIZE = (80, 80)

# Assets
ASSETS_DIR = Path(__file__).resolve().parent / "assets"
TEXT_DIR = Path(__file__).resolve().parent / "text"
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
FACE_EVENT_LOG = LOG_DIR / "face_events.log"
ALARM_SOUND = ASSETS_DIR / "deathALARM.mp3"
VIDEO_OVERLAY = ASSETS_DIR / "after_voice.mp4"

# Mike SAPI4 web voice
VOICE_NAME = "Mike (for Telephone)"
VOICE_VOLUME = 1.0
VOICE_PITCH = 110
VOICE_SPEED = 150
VOICE_API_URL = "https://tetyys.com/SAPI4/SAPI4"
VOICE_AUDIO_DIR = ASSETS_DIR / "mike_audio"
VOICE_AUDIO_FILE = VOICE_AUDIO_DIR / "mike_countdown.wav" # VOICE FILE RAN, CHANGE IF YOU WANT NEW FILE
VOICE_SCRIPT = """REMOVE YOURSELF FROM FRAME
THIS IS A WARNING
Three
REMOVE YOURSELF FROM FRAME
THIS IS A WARNING
Two
REMOVE YOURSELF IMMEDIAELY FROM FRAME
THIS IS YOUR FINAL WARNING
One""" # CHANGE THIS SCRIPT  IF YOU WANT TO CUSTOMIZE THE COUNTDOWN

# Alarm and visual effect
ALARM_VOLUME = 0.70
COUNTDOWN_TINT_MAX_OPACITY = 0.75
