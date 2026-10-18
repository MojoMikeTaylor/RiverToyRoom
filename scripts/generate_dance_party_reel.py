#!/usr/bin/env python3
"""
River's Toy Room - Action Figures Dance Party Reel Generator
Uses the Sovereign + Runway Gen-3 + Voicemod workflow.

This is a dedicated script for the episode:
"Action Figures Dance Party – Gramma Kellee Surprise"

Instructions:
1. Download your action figure photos from Gmail into:
   C:\Dev\RiverToyRoom\photos\action-figures-dance-party\
2. Set dry_run=False when you're ready to spend Runway credits.
3. Make sure RUNWAYML_API_SECRET is set in your User environment variables.
"""

from pathlib import Path
import sys
import subprocess

# Prefer Sovereign's maintained pipeline (core/pipeline.py + embedded runway_client)
# This uses the fixed/current code in tAyI_Sovereign_AI (avoids old external + class name + SDK import fragility)
SOVEREIGN_ROOT = Path(r"C:\Dev\tAyI_Sovereign_AI")
sys.path.insert(0, str(SOVEREIGN_ROOT))

try:
    from core.pipeline import run_sovereign_runway_pipeline
    SOVEREIGN_PIPELINE_AVAILABLE = True
except Exception as _e:
    print(f"[reel] Could not import Sovereign pipeline directly ({_e}); will fallback to subprocess dispatch or sim.")
    SOVEREIGN_PIPELINE_AVAILABLE = False
    run_sovereign_runway_pipeline = None

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

# === CONFIG (Sovereign style, used by current pipeline) ===
CFG = {
    "editor": {
        "powerdirector_path": r"C:\Program Files\CyberLink\PowerDirector23\PowerDirector23.exe",
        "voicemod_path": r"C:\Program Files\Voicemod V3\Voicemod.exe",
        "photodirector_path": r"C:\Program Files\CyberLink\PhotoDirector16\PhotoDirector16.exe",
    },
    "runway": {
        "default_model": "gen3a_turbo",
        "output_dir": r"C:\Dev\Runway_Clips",
        "youtube_ready_dir": r"C:\Dev\River_Uploads\Runway_YT_Ready",
    },
    "paths": {
        # Not strictly needed for reel but keeps cfg complete
        "quarantine": str(SOVEREIGN_ROOT / "data" / "quarantine"),
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

    # Use Sovereign's current pipeline (run_sovereign_runway_pipeline) for full RiverToyRoom orchestration
    # (Runway clips + rivertoyroom_voice_sequence AHK + river_toyroom_chaotic_reel AHK + PD launch + YT prep)
    result = None
    if SOVEREIGN_PIPELINE_AVAILABLE and run_sovereign_runway_pipeline:
        try:
            # Build a rich nl that triggers the RiverToyRoom special case in pipeline + editor
            nl = f"RiverToyRoom chaotic reel: {EPISODE_DESCRIPTION} action figures gramma kellee voiceover youtube ready"
            print("[reel] Calling Sovereign run_sovereign_runway_pipeline (dry_run=True for safety)...")
            result = run_sovereign_runway_pipeline(nl, CFG, dry_run=True)
        except Exception as e:
            print(f"[reel] Sovereign pipeline call failed: {e}")
            result = None

    if not result:
        # Fallback simulation (or dispatch via PS launch for real runs)
        result = {
            "status": "simulated",
            "description": EPISODE_DESCRIPTION,
            "clips": [str(p) for p in (PHOTOS[:2] if PHOTOS else [])] or [str(PHOTO_DIR / f"simulated_clip_{i}.mp4") for i in range(1, 3)],
            "voice_actions": ["rivertoyroom_voice_sequence", "gramma_kellee_voice"],
            "render_launched": True,
            "youtube_ready": True,
            "timestamp": "dry-run-simulation",
        }
        print("\n[DRY RUN SIMULATION - Sovereign pipeline not directly available in this python env]")
        print("Would have used full Sovereign + Runway Gen-3 + Voicemod rivertoy sequence + PowerDirector chaotic reel.")
        print("Tip: Run from Sovereign's .venv or use the PS launcher for end-to-end: .\\scripts\\rivertoyroom_chaotic_reel.ps1")

        # Optional: dispatch the real thing via the fixed launch script (uses correct venv + current code)
        if "--live-dispatch" in sys.argv:
            launch = SOVEREIGN_ROOT / "scripts" / "launch_sovereign.ps1"
            if launch.exists():
                print("\nDispatching via Sovereign launch for LIVE (will spend credits + launch GUI apps)...")
                try:
                    subprocess.run([
                        "powershell", "-ExecutionPolicy", "Bypass", "-File", str(launch),
                        "edit", f"RiverToyRoom chaotic reel with Gramma Kellee: {EPISODE_DESCRIPTION}", "--no-dry-run"
                    ], check=False)
                except Exception as de:
                    print(f"Dispatch failed: {de}")

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