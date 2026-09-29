"""Check file sizes and SHA-256 hashes against manifest.tsv."""

import argparse
import csv
import hashlib
from pathlib import Path


def verify(root: Path, sample_only: bool) -> int:
    checked = 0
    with (root / "manifest.tsv").open(newline="") as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            relative = Path(row["path"])
            if relative.is_absolute() or ".." in relative.parts:
                raise ValueError(f"unsafe manifest path: {relative}")
            if sample_only and relative.name[:9] != "clip00000":
                continue
            path = root / "sample" / relative if sample_only else root / relative
            expected_size = int(row["bytes"])
            if path.stat().st_size != expected_size:
                raise ValueError(f"size mismatch: {path}")
            digest = hashlib.sha256()
            with path.open("rb") as payload:
                for chunk in iter(lambda: payload.read(8 * 1024 * 1024), b""):
                    digest.update(chunk)
            if digest.hexdigest() != row["sha256"]:
                raise ValueError(f"SHA-256 mismatch: {path}")
            checked += 1
    if checked == 0:
        raise ValueError("no files checked")
    return checked


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--sample", action="store_true")
    args = parser.parse_args()
    print(f"verified {verify(args.root, args.sample)} files")
