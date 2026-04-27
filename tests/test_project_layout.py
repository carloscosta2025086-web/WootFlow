from pathlib import Path


def test_new_src_layout_exists():
    repo_root = Path(__file__).resolve().parents[1]
    assert (repo_root / "core").is_dir()
    assert (repo_root / "services").is_dir()
    assert (repo_root / "utils").is_dir()
    assert (repo_root / "tools").is_dir()
    assert (repo_root / "tests").is_dir()
