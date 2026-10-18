#!/usr/bin/env python3
"""
Improved isolated test based on Gemini's recommended pattern.
Run this and paste the full output.
"""

print("=== Testing IMPROVED lazy loading pattern (per Gemini recommendation) ===\n")

# This is the new recommended pattern (no top-level poisoning)
# runwayml v4+ dropped the 'exceptions' submodule (exceptions are top-level classes now);
# we keep the loader but drop the dead import that was causing "not installed" false positives.
_runway_sdk = None

def get_runway_sdk():
    global _runway_sdk
    if _runway_sdk is None:
        try:
            from runwayml import RunwayML
            _runway_sdk = RunwayML
            print("  [get_runway_sdk] Import succeeded on first call")
        except ImportError as e:
            raise ImportError("runwayml SDK not installed. Run: pip install runwayml") from e
    return _runway_sdk, None


print("Calling get_runway_sdk() for the first time...")
try:
    sdk, exc = get_runway_sdk()
    print("SUCCESS")
    print(f"  SDK class: {sdk}")
    print(f"  Exceptions (compat): {exc}")
except Exception as e:
    print(f"FAILED: {e}")

print("\nCalling get_runway_sdk() a second time (should be cached)...")
try:
    sdk2, _ = get_runway_sdk()
    print(f"  Same object? {sdk is sdk2}")
except Exception as e:
    print(f"FAILED on second call: {e}")

print("\n=== Final State ===")
print(f"_runway_sdk is not None? {_runway_sdk is not None}")