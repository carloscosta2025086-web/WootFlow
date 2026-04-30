import os
import json
from typing import Dict, Any

def load_profiles(profile_dir: str) -> Dict[str, Any]:
    """Load all JSON profiles from the given directory. Returns dict: profile_name -> profile_data."""
    profiles = {}
    for fname in os.listdir(profile_dir):
        if fname.endswith('.json'):
            path = os.path.join(profile_dir, fname)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    name = data.get('name') or fname[:-5]
                    profiles[name.lower()] = data
            except Exception as e:
                print(f"[profile_loader] Failed to load {fname}: {e}")
    return profiles

def find_profile_by_process(profiles: Dict[str, Any], process_name: str) -> Any:
    """Finds a profile whose trigger matches the process name."""
    process_name = process_name.lower()
    for profile in profiles.values():
        triggers = profile.get('trigger', [])
        if any(process_name == t.lower() for t in triggers):
            return profile
    return None

def get_default_profile(profiles: Dict[str, Any]) -> Any:
    for profile in profiles.values():
        if not profile.get('trigger'):
            return profile
    return None
