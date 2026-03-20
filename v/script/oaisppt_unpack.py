#!/usr/bin/env python3
"""Unpack and format XML contents of Office files (.docx, .pptx, .xlsx)"""

import random
import sys
import defusedxml.minidom
import zipfile
from pathlib import Path
import argparse

def unpack_office_file(input_file: Path, output_dir: Path):
    """
    Unpacks an Office file (.docx, .pptx, .xlsx) and pretty-prints its XML contents.

    Raises:
        zipfile.BadZipFile: If the file is not a valid ZIP archive
        PermissionError: If there's no permission to read the file or write to output
        ValueError: If the file format is not supported
    """
    # Validate file extension
    valid_extensions = {".docx", ".pptx", ".xlsx"}
    if input_file.suffix.lower() not in valid_extensions:
        raise ValueError(f"Unsupported file format: {input_file.suffix}. Expected: {valid_extensions}")

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Extract all contents with proper error handling
    with zipfile.ZipFile(input_file) as zf:
        zf.extractall(output_dir)

    # Pretty print all XML files
    xml_files = list(output_dir.rglob("*.xml")) + list(output_dir.rglob("*.rels"))
    for xml_file in xml_files:
        content = xml_file.read_text(encoding="utf-8")
        dom = defusedxml.minidom.parseString(content)
        # Fix: write with utf-8 encoding to prevent data corruption for non-ASCII content
        xml_file.write_bytes(dom.toprettyxml(indent="  ", encoding="utf-8"))

    # For .docx files, suggest an RSID for tracked changes
    if input_file.suffix == ".docx":
        suggested_rsid = "".join(random.choices("0123456789ABCDEF", k=8))
        print(f"Suggested RSID for edit session: {suggested_rsid}")

def main():
    parser = argparse.ArgumentParser(
        description="Unpack and format XML contents of Office files (.docx, .pptx, .xlsx)"
    )
    parser.add_argument(
        "input_file",
        type=Path,
        help="Path to the Office file (.docx, .pptx, .xlsx) to unpack",
    )
    parser.add_argument(
        "output_dir",
        type=Path,
        help="Directory where the unpacked and formatted contents will be saved",
    )
    args = parser.parse_args()

    if not args.input_file.exists():
        print(f"Error: Input file '{args.input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    if not args.input_file.is_file():
        print(f"Error: Input file '{args.input_file}' is not a file.", file=sys.stderr)
        sys.exit(1)

    try:
        unpack_office_file(args.input_file, args.output_dir)
        print(f"Successfully unpacked '{args.input_file}' to '{args.output_dir}'")
    except zipfile.BadZipFile:
        print(f"Error: '{args.input_file}' is not a valid ZIP/Office file or is corrupted.", file=sys.stderr)
        sys.exit(1)
    except PermissionError as e:
        print(f"Error: Permission denied - {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
