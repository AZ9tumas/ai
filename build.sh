#!/usr/bin/env bash

set -euo pipefail

PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3.12}"
MANIMGL_BIN="${MANIMGL_BIN:-manimgl}"
SCENE_FILE="$PROJECT_DIR/find_peak_corrected_visualization.py"
SCENE_NAME="FindPeakElementCorrectedTrace"
RENDER_CONFIG="$PROJECT_DIR/find_peak_render.yml"
ENCODER_WRAPPER="$PROJECT_DIR/render_tools/ffmpeg_hq.sh"
OUTPUT_DIR="$PROJECT_DIR/renders/final"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    echo "Error: $PYTHON_BIN was not found." >&2
    exit 1
fi

if ! command -v "$MANIMGL_BIN" >/dev/null 2>&1; then
    echo "Error: $MANIMGL_BIN was not found." >&2
    exit 1
fi

if [[ ! -x "$ENCODER_WRAPPER" ]]; then
    echo "Error: the high-quality ffmpeg wrapper is missing or not executable:" >&2
    echo "       $ENCODER_WRAPPER" >&2
    exit 1
fi

OUTPUT_NAME="$(
    "$PYTHON_BIN" -c '
import sys
sys.path.insert(0, sys.argv[1])
from visualization_settings import validate_settings
print(validate_settings())
' "$PROJECT_DIR"
)"

mkdir -p "$OUTPUT_DIR"
cd "$PROJECT_DIR"

echo "Rendering array and trace from visualization_settings.py"
echo "Output: $OUTPUT_DIR/$OUTPUT_NAME.mp4"

"$MANIMGL_BIN" \
    "$SCENE_FILE" \
    "$SCENE_NAME" \
    -w \
    --config_file "$RENDER_CONFIG" \
    --video_dir "$OUTPUT_DIR" \
    --file_name "$OUTPUT_NAME"

echo "Finished: $OUTPUT_DIR/$OUTPUT_NAME.mp4"
