"""Load and check one aligned Gaussian video pair and its optional 3D scene."""

import argparse
from pathlib import Path

import torch


def load_clip(root: Path, clip: str) -> dict:
    if not clip.startswith("clip") or not clip[4:].isdigit() or len(clip) != 9:
        raise ValueError("clip must have the form clip00000")
    gauss = torch.load(root / "gauss" / f"{clip}_gauss.pt", map_location="cpu", weights_only=True)
    target = torch.load(root / "dv" / f"{clip}_dv.pt", map_location="cpu", weights_only=True)
    t, n, channels = gauss["tok9"].shape
    if channels != 9 or target["xyz_world"].shape != (t, n, 3):
        raise ValueError("token and world-coordinate shapes disagree")
    if target["xyz_canon"].shape != (n, 3) or target["visible"].shape != (t, n):
        raise ValueError("canonical coordinates or visibility disagree")
    if not torch.equal(gauss["obj_id"], target["obj_id"]):
        raise ValueError("token and target object identities disagree")
    scene_path = root / "scene" / f"{clip}_scene.pt"
    scene = torch.load(scene_path, map_location="cpu", weights_only=True) if scene_path.exists() else None
    if scene is not None and (scene["obj_pos"].shape[1] != t or scene["cam_pos"].shape != (t, 3)):
        raise ValueError("scene and pair time axes disagree")
    return {"gauss": gauss, "target": target, "scene": scene}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("clip")
    args = parser.parse_args()
    data = load_clip(args.root, args.clip)
    t, n, _ = data["gauss"]["tok9"].shape
    print(f"{args.clip}: {t} frames, {n} projected Gaussians, scene={'yes' if data['scene'] is not None else 'no'}")
