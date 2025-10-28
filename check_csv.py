#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import sys


def check_csv_encoding(csv_file):
    """Check if German characters are properly encoded in CSV"""

    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")

        count = 0
        for row in reader:
            count += 1
            for cell in row:
                if isinstance(cell, str):
                    # Check for common German words/characters
                    if any(
                        word in cell.lower()
                        for word in ["straße", "für", "mühl", "schön", "köpf", "bühl"]
                    ):
                        print(f"Row {count}: Found German text: {cell}")
                        if count > 10:  # Only show first 10 examples
                            return

    print("No German characters found or encoding test complete.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        check_csv_encoding(sys.argv[1])
    else:
        print("Usage: python check_csv.py <csv_file>")
