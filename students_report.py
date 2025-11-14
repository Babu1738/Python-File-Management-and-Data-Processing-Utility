#!/usr/bin/env python3
"""
students_report.py
Task 7: Read students.json, compute averages, write report.csv sorted by average desc.
Uses: json, csv, and basic error handling.
"""

import json
import csv
from statistics import mean

INPUT_JSON = "students.json"
OUTPUT_CSV = "report.csv"

def load_students(json_path):
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                print("Unexpected JSON structure: expected a list of student objects.")
                return []
            return data
    except FileNotFoundError:
        print(f"Error: '{json_path}' not found. Please ensure the file exists in the current folder.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error loading JSON: {e}")
        return None

def compute_averages(students):
    results = []
    for s in students:
        sid = s.get("id", "")
        name = s.get("name", "")
        scores = s.get("scores", [])
        if not isinstance(scores, list) or len(scores) == 0:
            avg = 0.0
        else:
            try:
                # convert to floats/ints and compute mean
                vals = [float(x) for x in scores]
                avg = round(sum(vals) / len(vals), 2)
            except Exception:
                avg = 0.0
        results.append({"id": sid, "name": name, "average": avg})
    return results

def write_csv(results, csv_path):
    try:
        # sort by average descending
        results_sorted = sorted(results, key=lambda r: r["average"], reverse=True)
        with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["id", "name", "average"])
            writer.writeheader()
            for r in results_sorted:
                writer.writerow(r)
        print(f"Report written to '{csv_path}'")
    except Exception as e:
        print(f"Error writing CSV: {e}")

def main():
    students = load_students(INPUT_JSON)
    if students is None:
        # load_students prints informative message; exit gracefully
        return
    results = compute_averages(students)
    write_csv(results, OUTPUT_CSV)

if __name__ == "__main__":
    main()
