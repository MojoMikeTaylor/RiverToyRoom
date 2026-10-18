# POST-REBOOT / RELOCATION WORKFLOW PIPELINE CHECK
## RiverToyRoom - MACROHARD Status Report

**Date of check:** 2026-06-02 (post-reboot / post-relocation to C:\Dev)
**Machine:** Windows NT 10.0.26200.0 (user: mojom)
**CWD:** C:\Dev\RiverToyRoom
**Python:** 3.14.3 (Windows store/app local: C:\Users\mojom\AppData\Local\Python\pythoncore-3.14-64)
**runwayml SDK:** 4.15.0
**Git:** 2.54.0.windows.1 (remote functional despite display concat in some outputs)

## Verdict: OFFICIALLY MACROHARD
**Microsoft friction has NOT been eliminated.**

We are still fully locked into Windows / Microsoft tooling ecosystem for the "pipeline".

### 1. Deployment Pipeline (push-to-github.ps1)
- Still the only mechanism documented in README and used.
- 100% PowerShell 5.1 (Microsoft).
- Interactive (Read-Host Y/N, credential prompts for git push).
- Hard-codes Git for Windows install advice, winget for gh.
- No cross-platform equivalent (.sh / python git wrapper).
- No CI automation.
- Current state: git remote appears functional (ahead by 1), but script always force-resets remote on run.

**Status:** Still requires Windows + PS to deploy. Not eliminated.

### 2. GitHub Actions / Official Workflow Pipeline
- **No .github/ directory at all.**
- No workflow/*.yml ever committed (confirmed via git ls-tree + history).
- GitHub Pages is configured (or intended) for manual branch deploy or "GitHub Actions" but no custom workflows present.
- gh CLI not installed on this machine.
- Result: Zero automated pipeline. Pure local manual push.

**Status:** No official automated workflow. Friction remains (manual Windows steps).

### 3. Content/Video Production "Workflow Pipeline" (the real "Sovereign + Runway" one)
This is what the scripts/ refer to as "workflow" and "full pipeline".

#### a) scripts/generate_dance_party_reel.py (SovereignRunwayPipeline)
- **BROKEN after reboot/relocation.**
- Fails at SovereignRunwayPipeline(...) with: "runwayml SDK not installed..."
- Root cause (revealed by repro): 
  - runway_client.py:44 does `from runwayml import exceptions as runway_exceptions`
  - In v4.15.0 of runwayml, NO `exceptions` submodule. Exceptions are top-level (RunwayMLError, TaskFailedError, etc.).
  - The except ImportError turns it into misleading "not installed" message.
- Also triggers import side-effects from tAyI_Sovereign_AI/core/editor_in_chief.py due to sys.path hack + relative imports (". import runway_client").
- Prints:
  [Editor] Runway client not available (install runwayml + set RUNWAYML_API_SECRET for Gen-3 support)
  [Editor] Local pipeline import note: attempted relative import with no known parent package...
- Depends on (via CFG and sovereign):
  - C:\Program Files\CyberLink\PowerDirector23\PowerDirector23.exe
  - C:\Program Files\Voicemod V3\Voicemod.exe
  - AutoHotkey automation (find_ahk_exe hardcodes many Program Files paths)
  - C:\Dev\Runway-Integration , C:\Dev\tAyI_Sovereign_AI , C:\Dev\Runway_Clips , C:\Dev\River_Uploads
- The "Sovereign" is deeply tied to Windows GUI app control via AHK.

**Status:** Non-functional. Classic Microsoft + brittle integration friction.

#### b) scripts/runway_generate_dance_party.py (the "bypass")
- **Partially works (dry-run succeeds, health_check passes).**
- Only imports `from runwayml import RunwayML` (no exceptions) --> succeeds.
- Still 100% hardcoded Windows paths:
  PHOTO_DIR = Path(r"C:\Dev\RiverToyRoom\...")
  OUTPUT_DIR = Path(r"C:\Dev\Runway_Clips\...")
- Has good bits: base64 data URI to bypass uploads, direct URL support, proper polling.
- No Voicemod/PowerDirector coupling (good).
- But still "C:\" everywhere, not portable.

**Status:** Usable for generation in dry + (presumably) real, but path friction remains.

#### c) debug_runway_import.py
- **Also broken.** Uses the same failing "from runwayml import exceptions" pattern.
- Confirms the "improved lazy loading" (Gemini rec) doesn't match current SDK.

### 4. Other Microsoft Friction Indicators
- All large media checked into git (videos, high-res photos) -- Windows dev common anti-pattern but present.
- Hardcoded user paths in multiple places (C:\Users\mojom\..., C:\Dev\... after "relocation" update in c4cfd2f).
- CFG in reel.py points to specific versioned Windows software installs.
- Push script + README exclusively document `powershell .\push-to-github.ps1`
- No use of WSL, containers, or cross-platform abstractions for the prod pipeline.
- Python is the Windows "pythoncore" app execution alias style install.

### 5. What "after reboot" / relocation exposed
- The c4cfd2f commit updated paths inside RiverToyRoom/ scripts and added media.
- But the *dependent* projects (Runway-Integration, tAyI_Sovereign_AI) were not updated in lockstep, and still have their own hard-coded paths + the import fragility was latent.
- SDK version or python env state post-reboot made the exceptions import fail (previously may have worked with older runwayml wheel).
- Result: the "full workflow" that the reel script is built around is dead.

## Summary Table

| Component                 | MS/Win Friction                                      | Functional Post-Reboot? | Notes |
|---------------------------|------------------------------------------------------|-------------------------|-------|
| push-to-github.ps1        | Extreme (PS1, interactive)                           | Yes (but manual)        | Only deploy path |
| .github/workflows         | N/A (absent)                                         | N/A                     | No automation |
| Sovereign full pipeline   | Extreme (AHK, PowerDir, Voicemod, paths, relative import hacks) | **NO**             | SDK mismatch + Win GUI |
| Direct Runway script      | High (hardcoded C:\ paths)                           | Yes (dry)               | Better isolation |
| debug + client code       | High                                                 | Broken                  | Outdated import pattern for runwayml v4+ |

## Recommendation (for if/when eliminating friction)
To become "not MACROHARD":
1. Replace/duplicate push-to-github.ps1 with a python or bash script (or just `git push` instructions + gh).
2. Add .github/workflows for Pages if desired (ubuntu runner, no MS needed).
3. Make all paths in scripts/ use relative or os.environ / config.json (no r"C:\Dev").
4. Update/fork the runway_client.py + debug to handle current runwayml (v4+) exceptions (they are top level now; no need separate import or catch specifically).
5. Decouple the "full reel workflow" from PowerDirector + Voicemod + AHK. Use ffmpeg + open voice models or cross platform.
6. Consider making Runway-Integration a proper pip installable package instead of sys.path hacks + relative import assumptions.
7. Document Linux/Mac friendly dev (even if primary is Win).

**Current official status: We are MACROHARD. Friction not eliminated. The reboot exposed more of it.**
