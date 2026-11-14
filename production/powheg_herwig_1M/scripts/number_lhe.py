#!/usr/bin/env python3
import argparse
import importlib.util
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
parser.add_argument("--output", required=True)
parser.add_argument("--index", type=int, required=True)
parser.add_argument("--script", required=True)
args = parser.parse_args()

if not 0 <= args.index < 1000:
    raise ValueError("Invalid file index")

input_file = Path(args.input).resolve()
output_file = Path(args.output).resolve()

if not input_file.is_file():
    raise FileNotFoundError(input_file)
if output_file.exists():
    raise FileExistsError(output_file)

spec = importlib.util.spec_from_file_location(
    "addLHEnumbers", args.script
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

offset = args.index * 1000

last_event = module.number_events(
    str(input_file),
    str(output_file),
    offset=offset
)

if last_event != offset + 1000:
    raise RuntimeError(
        f"Expected 1000 events, got {last_event - offset}"
    )

with output_file.open() as f:
    count = sum("<event_num num=" in line for line in f)

if count != 1000:
    raise RuntimeError(f"Found {count} numbered events")

print(f"Numbered events {offset + 1} to {last_event}")
