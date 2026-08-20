#!/bin/bash

# ManimGL streams raw RGBA frames to ffmpeg. Add a slow, visually lossless
# H.264 encode while preserving every argument selected by ManimGL.
ffmpeg_args=("$@")
last_index=$((${#ffmpeg_args[@]} - 1))
output_path="${ffmpeg_args[$last_index]}"
unset 'ffmpeg_args[$last_index]'

exec /opt/homebrew/bin/ffmpeg "${ffmpeg_args[@]}" \
  -preset slow \
  -crf 14 \
  -tune animation \
  -movflags +faststart \
  "$output_path"
