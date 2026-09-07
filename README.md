# Face-Recognition-Tracking
Testing Facial Recognition for future Arduino Turret Test

## Live face-center tracking

Install the dependency with the Python interpreter you want to use:

```powershell
py -m pip install --force-reinstall -r requirements.txt
```

Start the tracker:

```powershell
py src/main.py
```

Generate one local Mike countdown audio file:

```powershell
py src/create_audio.py
```

Edit `VOICE_SCRIPT` in `src/settings.py`, then run this again. Use `--force` to regenerate the existing file:

```powershell
py src/create_audio.py --force
```

The mirrored camera window opens fullscreen and draws a red pinpoint plus horizontal and vertical crosshair lines at the center of the largest detected face. The live `(x, y)` coordinate appears in both the top-left corner and the console. The `src/assets/deathALARM.mp3` sound loops while the smoothed face center remains in the top quarter of the screen, then stops immediately when it leaves. The countdown plays one local Mike WAV file, `src/assets/mike_audio/mike_countdown.wav`, so the tracker does not contact the website while running. After the complete voice file finishes, `src/assets/after_voice.mp4` plays once over the camera window with its audio track. Face detection pauses for the entire video, so moving below the zone does not interrupt it. The window close button is disabled; press `Q` or `q` in the camera window to stop. Use `--camera 1` for another camera, or adjust responsiveness with `--smoothing 0.6`.

### Custom voice text

Edit `VOICE_SCRIPT` in `src/settings.py` to change what Mike says, then run `py src/create_audio.py --force`.

```text
Warning
Five
Four
Three
Two
One
```

Change the values in `src/settings.py` to tune the camera, detection, smoothing, Mike voice, alarm, video, and red-tint behavior. Set `WINDOW_FULLSCREEN = False` for a windowed camera. In windowed mode, change `WINDOW_WIDTH` and `WINDOW_HEIGHT` to control the window size and aspect ratio; the camera capture resolution follows those same values automatically. `VOICE_SCRIPT`, `VOICE_PITCH`, `VOICE_SPEED`, and `VOICE_VOLUME` control generated audio. The audio-generation command requires an internet connection; the tracker itself does not.

While the combined voice file is being spoken, the camera slowly gains a red tint. The tint reaches its maximum at the end of the WAV file, then clears when the countdown resets.

When a face enters the camera view, one timestamped line is appended to `logs/face_events.log`. A face must leave and re-enter before another line is recorded.

### Source layout

- `src/main.py` boots the application.
- `src/app.py` coordinates the camera and application loop.
- `src/create_audio.py` generates the single local Mike WAV file.
- `src/tracking.py` contains face detection results, smoothing, and drawing.
- `src/voice.py` plays the single local Mike WAV file.
- `src/video_overlay.py` handles MP4 frames and audio.
- `src/visual_effects.py` handles the countdown screen tint.
- `src/settings.py` contains asset paths and tunable alarm settings.
