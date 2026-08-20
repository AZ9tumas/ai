"""Shared settings for the Find Peak Element visualization."""

import re


# ---------------------------------------------------------------------------
# EDIT THESE TWO VALUES
# ---------------------------------------------------------------------------

# Adjacent values must be different, matching the Find Peak Element problem.
# For the clearest layout, keep the array between 1 and 18 integers.
NUMS = [2, 1]

# The .mp4 extension is optional. The video is written to renders/final/.
OUTPUT_VIDEO_NAME = "find_peak_element_corrected_code"


def validate_settings():
    """Validate the editable settings and return a safe output-file stem."""
    if not isinstance(NUMS, (list, tuple)) or not NUMS:
        raise ValueError("NUMS must be a non-empty list or tuple of integers.")
    if len(NUMS) > 18:
        raise ValueError("NUMS supports at most 18 values so the video stays readable.")
    if any(isinstance(value, bool) or not isinstance(value, int) for value in NUMS):
        raise ValueError("Every value in NUMS must be an integer.")
    if any(left == right for left, right in zip(NUMS, NUMS[1:])):
        raise ValueError("Adjacent values in NUMS must be different.")

    if not isinstance(OUTPUT_VIDEO_NAME, str):
        raise ValueError("OUTPUT_VIDEO_NAME must be a string.")
    output_stem = OUTPUT_VIDEO_NAME.strip()
    if output_stem.lower().endswith(".mp4"):
        output_stem = output_stem[:-4]
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", output_stem):
        raise ValueError(
            "OUTPUT_VIDEO_NAME may contain letters, numbers, dots, underscores, "
            "and hyphens, and cannot contain a directory path."
        )
    return output_stem
