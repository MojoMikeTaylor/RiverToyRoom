#!/usr/bin/env python3
"""
River's Toy Room - Action Figures Dance Party Reel Generator
Uses the Sovereign + Runway Gen-3 + Voicemod workflow.

This is a dedicated script for the episode:
"Action Figures Dance Party – Gramma Kellee Surprise"

Instructions:
1. Download your action figure photos from Gmail into:
   C:/Users/mojom/RiverToyRoom/photos/action-figures-dance-party/
2. Set dry_run=False when you're ready to spend Runway credits.
3. Make sure RUNWAYML_API_SECRET is set in your User environment variables.
"""

from pathlib import Path
import sys

# Add the Runway-Integration project to the path
RUNWAY_INTEGRATION = Path(r"C:\Dev\Runway-Integration")
sys.path.insert(0, str(RUNWAY_INTEGRATION))

from pipeline import SovereignRunwayPipeline

# === EPISODE DETAILS ===
EPISODE_TITLE = "Action Figures Dance Party – Gramma Kellee Surprise"
EPISODE_DESCRIPTION = (
    "Action figures (Iron Man, Loki, Thanos and friends) are wildly dancing to upbeat music "
    "like Pitbull “Fireball”. When they hear Gramma Kellee coming down the hallway they panic, "
    "freeze, and scramble back into their toy boxes. Once she leaves, one figure whispers "
    "“Ok Gramps, the coast is clear!” and the music starts again. They all jump out and resume "
    "dancing until they hear Gramma coming back — then they run to the boxes again to fast-paced "
    "rock like Godsmack. Fun, chaotic, and wholesome kid-friendly scene."
)

# === PHOTOS FOLDER (download from your Gmail inbox) ===
PHOTO_DIR = Path(r"C:\Dev\RiverToyRoom\photos\action-figures-dance-party")
PHOTOS = sorted(PHOTO_DIR.glob("*.jpg")) + sorted(PHOTO_DIR.glob("*.png")) + sorted(PHOTO_DIR.glob("*.jpeg"))

# === CONFIG (matches your previous Sovereign + Runway setup) ===
CFG = {
    "editor": {
        "powerdirector_path": r"C:\Program Files\CyberLink\PowerDirector23\PowerDirector23.exe",
        "voicemod_path": r"C:\Program Files\Voicemod V3\Voicemod.exe",
    },
    "runway": {
        "default_model": "gen3a_turbo",
        "output_dir": r"C:\Dev\Runway_Clips",
        "youtube_ready_dir": r"C:\Dev\River_Uploads\Runway_YT_Ready",
    }
}

# === RECOMMENDED VOICE STYLES FOR THIS EPISODE ===
# From the existing Voicemod AHK mappings:
#   - "gramma_kellee"       → Gramma Kellee voice (great for the surprise/panic moments)
#   - "toy_whisper"         → High-pitched whisper for the toys (perfect for “Ok Gramps, the coast is clear!”)
#   - "river_summer"        → Kid whisper voices
#   - "deep_narrator"       → Classic deep voice
#   - Special full sequence: "rivertoyroom_voice_sequence"
VOICE_STYLE = "gramma_kellee"   # Change to "toy_whisper" or "rivertoyroom_voice_sequence" as needed


if __name__ == "__main__":
    print("=" * 70)
    print("River's Toy Room — Action Figures Dance Party Reel Generator")
    print(f"Episode: {EPISODE_TITLE}")
    print("=" * 70)

    if not PHOTOS:
        print("\n[WARNING] No photos found in:")
        print(f"  {PHOTO_DIR}")
        print("\nPlease download your action figure photos from Gmail and drop them there.")
        print("The script will fall back to pure text-to-video generation.\n")
    else:
        print(f"\nFound {len(PHOTOS)} photo(s):")
        for p in PHOTOS:
            print(f"  - {p.name}")

    print(f"\nVoice Style: {VOICE_STYLE}")
    print(f"Description:\n{EPISODE_DESCRIPTION[:200]}...\n")

    # Try to use the real SovereignRunwayPipeline
    pipeline = None
    try:
        pipeline = SovereignRunwayPipeline(sovereign_config=CFG)
    except Exception as e:
        print(f"[Dry Run Fallback] Could not initialize full pipeline: {e}")
        print("[Dry Run Fallback] Running pure simulation mode instead (still useful for prompt + photo validation).\n")

    if pipeline:
        # === DRY RUN MODE (safe, no credits used) ===
        result = pipeline.run_full_workflow(
            description=EPISODE_DESCRIPTION,
            photos=PHOTOS if PHOTOS else None,
            voice_style=VOICE_STYLE,
            duration_per_clip=6,
            model="gen3a_turbo",
            do_voiceover=True,
            do_final_render=True,
            dry_run=True,
        )
    else:
        # Pure local simulation for dry run
        result = {
            "description": EPISODE_DESCRIPTION,
            "clips": [str(PHOTO_DIR / f"simulated_clip_{i}.mp4") for i in range(1, 3)],
            "voice_style": VOICE_STYLE,
            "youtube_ready": None,
            "timestamp": "dry-run-simulation",
        }
        print("\n[DRY RUN SIMULATION - Full Pipeline Not Available]")
        print("Would have generated 1-2 short clips using Runway Gen-3 from the provided photos + prompt.")
        print(f"Voice style target: {VOICE_STYLE}")
        print("Would launch Voicemod and generate a voiceover script with suggested lines for the story beats.")

    print("\n" + "=" * 70)
    print("Result:")
    for k, v in result.items():
        print(f"  {k}: {v}")
    print("=" * 70)

    print("\nNext steps:")
    print("1. Review the suggested voiceover script that was generated.")
    print("2. When ready, edit this file and set dry_run=False to actually call Runway.")
    print("3. Use Voicemod with the chosen preset (or the full rivertoyroom_voice_sequence).")
    print("4. Import clips into PowerDirector for final music sync (Suno tracks) + editing.")