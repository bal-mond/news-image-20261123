#!/usr/bin/env python3
"""Copy-only entrypoint for make.fun bounty news-image-20261123.

The poster for Monday 23 November 2026 (entry.png, 1024x1024, rendered
and checked at build time) is copied byte-for-byte to
$MAKEFUN_OUTPUT_DIR/entry.png. Rendering at grade time was tried on the
22 November entry and failed in the grader, so this program does no
rendering at all: standard library only, no fonts, no network, no
third-party imports. After the copy it verifies the output (file exists,
at most 1 MiB, PNG magic bytes, 1024x1024 read from the IHDR chunk,
sha256 identical to the source). The source is also size-checked before
copying, so an oversized poster fails fast instead of producing a bad
output. Any failure exits non-zero with a clear message on stderr.
"""

import hashlib
import os
import shutil
import struct
import sys

SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"
MAX_BYTES = 1048576
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print("error: %s" % message, file=sys.stderr)
    return 1


def resolve_output_dir():
    """Return a writable output dir: $MAKEFUN_OUTPUT_DIR, else /output, else ./out."""
    requested = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    for candidate in (requested, "/output", "./out"):
        try:
            os.makedirs(candidate, exist_ok=True)
            probe = os.path.join(candidate, ".write-test")
            with open(probe, "wb") as handle:
                handle.write(b"")
            os.remove(probe)
            return candidate
        except OSError:
            continue
    return None


def read_png_size(path):
    """Return (width, height) parsed from the PNG IHDR chunk, stdlib only."""
    with open(path, "rb") as handle:
        header = handle.read(33)
    if len(header) < 33 or header[:8] != PNG_MAGIC:
        raise ValueError("not a PNG file (bad magic bytes)")
    length, chunk_type = struct.unpack(">I4s", header[8:16])
    if chunk_type != b"IHDR" or length != 13:
        raise ValueError("first chunk is not a 13-byte IHDR")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)
    if not os.path.isfile(source):
        return fail("source image not found: %s" % source)

    # Fail early if the shipped poster itself is over the limit, rather
    # than copying it and only then discovering the output is too big.
    try:
        source_size = os.path.getsize(source)
    except OSError as exc:
        return fail("cannot stat source image: %s" % exc)
    if source_size > MAX_BYTES:
        return fail("source image %d bytes exceeds 1 MiB limit" % source_size)

    output_dir = resolve_output_dir()
    if output_dir is None:
        return fail("no writable output directory found")
    destination = os.path.join(output_dir, OUTPUT_NAME)

    try:
        shutil.copyfile(source, destination)
    except OSError as exc:
        return fail("copy failed: %s" % exc)

    # The whole point is a byte-identical copy, so compare digests and
    # catch a truncated or partial copy here instead of downstream.
    source_digest = sha256_file(source)
    destination_digest = sha256_file(destination)
    if source_digest != destination_digest:
        return fail(
            "copy mismatch: source sha256 %s != output sha256 %s"
            % (source_digest, destination_digest)
        )

    try:
        size = os.path.getsize(destination)
    except OSError as exc:
        return fail("cannot stat output: %s" % exc)
    if size > MAX_BYTES:
        return fail("output %d bytes exceeds 1 MiB limit" % size)

    try:
        width, height = read_png_size(destination)
    except (OSError, ValueError, struct.error) as exc:
        return fail("output verification failed: %s" % exc)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        return fail(
            "output is %dx%d, expected %dx%d"
            % (width, height, EXPECTED_WIDTH, EXPECTED_HEIGHT)
        )

    print(
        "wrote %s (%d bytes, %dx%d, sha256 %s)"
        % (destination, size, width, height, destination_digest)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
