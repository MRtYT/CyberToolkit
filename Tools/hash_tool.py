"""File and text hashing helpers."""

from __future__ import annotations

import hashlib
from pathlib import Path

SUPPORTED_ALGORITHMS = {"md5", "sha1", "sha256", "sha512"}


def hash_text(value: str, algorithm: str = "sha256") -> str:
    algorithm = algorithm.lower()
    if algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"unsupported algorithm: {algorithm}")
    return hashlib.new(algorithm, value.encode("utf-8")).hexdigest()


def hash_file(path: str, algorithm: str = "sha256") -> str:
    algorithm = algorithm.lower()
    if algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"unsupported algorithm: {algorithm}")
    digest = hashlib.new(algorithm)
    try:
        with Path(path).open("rb") as file:
            for chunk in iter(lambda: file.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise ValueError(f"could not read file: {exc}") from exc
    return digest.hexdigest()
