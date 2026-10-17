import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.hash_tool import hash_file, hash_text
from tools.scanners.port_scanner import validate_port_range
from tools.scanners.subdomain_scanner import normalize_domain


class ToolkitTests(unittest.TestCase):
    def test_hash_text(self):
        self.assertEqual(
            hash_text("CyberToolkit"),
            "2a3f0a27338014f716e65c4c48df9902a5243c8447bd2a1fa2d78b2afca30b8d",
        )

    def test_hash_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.txt"
            path.write_text("hello", encoding="utf-8")
            self.assertEqual(
                hash_file(str(path), "sha256"),
                "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
            )

    def test_invalid_port_range(self):
        with self.assertRaises(ValueError):
            validate_port_range(0, 10)
        with self.assertRaises(ValueError):
            validate_port_range(10, 1)

    def test_normalize_domain(self):
        self.assertEqual(normalize_domain("https://Example.com/"), "example.com")


if __name__ == "__main__":
    unittest.main()
