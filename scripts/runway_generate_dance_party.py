#!/usr/bin/env python3
"""
Clean, standalone Runway Gen-3 generator for River's Toy Room episodes.

This bypasses the old Sovereign pipeline (which has import fragility)
and talks directly to the official runwayml SDK using your existing
RUNWAYML_API_SECRET environment variable.

Usage:
    python scripts/runway_generate_dance_party.py --dry-run
    python scripts/runway_generate_dance_party.py          # real generation
"""

import os
import sys
import time
import urllib.request
import base64
from pathlib import Path
from typing import List, Optional, Tuple

# === Robust SDK Loader (following recommended pattern) ===
_runway_sdk = None

def get_runway_sdk():
    """Single source of truth for the RunwayML SDK. Lazy + cached."""
    global _runway_sdk
    if _runway_sdk is None:
        try:
            from runwayml import RunwayML
            _runway_sdk = RunwayML
        except ImportError:
            raise ImportError("runwayml SDK not installed. Run: pip install runwayml")
    return _runway_sdk


# === Project Paths & Config ===
PHOTO_DIR = Path(r"C:\Dev\RiverToyRoom\photos\action-figures-dance-party")
OUTPUT_DIR = Path(r"C:\Dev\Runway_Clips\action-figures-dance-party")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

EPISODE_TITLE = "Action Figures Dance Party – Gramma Kellee Surprise"
EPISODE_PROMPT = (
    "High-energy joyful dance party with colorful superhero action figures happily dancing, jumping and celebrating together in a bright messy children's toy room surrounded by open colorful toy boxes and scattered toys. Upbeat fun party atmosphere with floating music notes, bright vibrant colorful lighting, happy smiling expressions on the toys. Dynamic exciting camera moves, playful wholesome cartoonish toy photography style, energetic positive joyful mood, saturated bright colors. Kid-friendly and fun, no scary or negative elements, pure positive energy."
)

# === DIRECT IMAGE URLS (Recommended when uploads are restricted) ===
# Paste your two direct HTTPS image links here (must be publicly accessible .jpg/.jpeg/.png)
DIRECT_IMAGE_URLS = [
    # Example:
    # "https://i.imgur.com/xxxxxxx.jpg",
    # "https://i.imgur.com/yyyyyyy.jpg",
]

def get_photos() -> List[Path]:
    # Prefer resized versions to keep base64 manageable
    resized = sorted(PHOTO_DIR.glob("resized_*.jpg")) + sorted(PHOTO_DIR.glob("resized_*.jpeg")) + sorted(PHOTO_DIR.glob("resized_*.png"))
    if resized:
        return resized
    photos = sorted(PHOTO_DIR.glob("*.jpg")) + sorted(PHOTO_DIR.glob("*.jpeg")) + sorted(PHOTO_DIR.glob("*.png"))
    return photos


def get_image_sources() -> List[str | Path]:
    """
    Returns either direct HTTPS URLs (preferred when uploads are restricted)
    or local file paths.
    """
    if DIRECT_IMAGE_URLS:
        return DIRECT_IMAGE_URLS
    return get_photos()


def image_to_data_uri(image_path: Path) -> str:
    """Convert local (resized) image to data:image/...;base64 URI to bypass Runway upload restrictions entirely."""
    mime = "image/jpeg" if image_path.suffix.lower() in {".jpg", ".jpeg"} else "image/png"
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def health_check() -> bool:
    """Simple environment validation to catch common issues early."""
    print("Running environment health check...")
    python_path = sys.executable
    print(f"  Python: {python_path}")

    # Check API key
    api_key = os.getenv("RUNWAYML_API_SECRET")
    if not api_key:
        print("  [FAIL] RUNWAYML_API_SECRET not set in environment")
        return False
    print(f"  API Key: {api_key[:8]}... (detected)")

    # Check runwayml can be loaded via our helper
    try:
        RunwayML = get_runway_sdk()
        print("  runwayml SDK: importable")
    except Exception as e:
        print(f"  [FAIL] runwayml import error: {e}")
        return False

    print("  Health check passed.\n")
    return True

def main(dry_run: bool = True):
    print("=" * 70)
    print("River's Toy Room - Direct Runway Gen-3 Generator")
    print(f"Episode: {EPISODE_TITLE}")
    print("=" * 70)

    sources = get_image_sources()
    print(f"\nFound {len(sources)} image source(s)")
    for s in sources:
        note = " (resized)" if isinstance(s, Path) and str(s).startswith(str(PHOTO_DIR / "resized_")) else ""
        print(f"  - {s}{note}")

    if not sources:
        print("\n[ERROR] No image sources found. Add direct URLs to DIRECT_IMAGE_URLS or add photos to the local folder.")
        return

    if dry_run:
        print("\n[DRY RUN MODE - No credits will be used]")
        health_check()
        print("Would send the following to Runway Gen-3 (gen3a_turbo or similar):")
        print(f"  Prompt: {EPISODE_PROMPT[:150]}...")
        print(f"  Reference images: {len(sources)}")
        print(f"  Duration: 5 seconds per clip")
        print(f"  Output folder: {OUTPUT_DIR}")
        if DIRECT_IMAGE_URLS:
            print("  Mode: Direct HTTPS URLs (no upload required)")
        else:
            print("  Mode: Local files via base64 data URI (bypasses upload restrictions)")
        print("\nTo do a real generation, run without --dry-run")
        return

    # === Real generation ===
    if not health_check():
        print("Health check failed. Fix the issues above before proceeding.")
        return

    RunwayML = get_runway_sdk()
    api_key = os.getenv("RUNWAYML_API_SECRET")

    print(f"\nAPI key detected: {api_key[:8]}...")

    client = RunwayML(api_key=api_key, base_url="https://api.dev.runwayml.com")

    print("\nStarting generation (this will use credits)...")

    for i, source in enumerate(sources, 1):
        label = source if isinstance(source, str) else source.name
        print(f"\n--- Generating clip {i}/{len(sources)} from {label} ---")
        try:
            if isinstance(source, str):
                # Direct HTTPS URL - bypasses upload entirely
                prompt_image = source
                print("  Using direct image URL (no upload needed)")
            else:
                # Local file - use base64 data URI to bypass upload restrictions
                print("  Converting to base64 data URI (bypassing uploads)...")
                prompt_image = image_to_data_uri(source)

            task = client.image_to_video.create(
                prompt_image=prompt_image,
                prompt_text=EPISODE_PROMPT,
                model="gen3a_turbo",
                duration=5,   # Valid values: 5 or 10
            )
            print(f"Task created: {task.id}")
            print("Polling for completion (this can take 30-90 seconds)...")

            # Proper polling
            final_task = client.tasks.retrieve(task.id)
            while final_task.status not in ("SUCCEEDED", "FAILED"):
                print(f"  Status: {final_task.status} ...")
                time.sleep(5)
                final_task = client.tasks.retrieve(task.id)

            if final_task.status == "SUCCEEDED":
                video_url = final_task.output[0] if final_task.output else None
                stem = Path(label).stem if isinstance(source, Path) else f"url_{i}"
                if video_url:
                    output_path = OUTPUT_DIR / f"{EPISODE_TITLE.replace(' ', '_')}_{i}_{stem}.mp4"
                    print(f"  Downloading to: {output_path}")
                    urllib.request.urlretrieve(video_url, output_path)
                    print(f"  ✓ Saved: {output_path}")
                else:
                    print("  Task succeeded but no output URL found.")
            else:
                print(f"  Task failed: {final_task.failure}")
        except Exception as e:
            print(f"Error generating from {label}: {e}")

    print("\nDone. Clips saved to:", OUTPUT_DIR)

if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    main(dry_run=dry)