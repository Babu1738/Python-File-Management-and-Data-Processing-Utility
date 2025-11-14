#!/usr/bin/env python3
"""
file_manager.py
Implements Tasks 1-6 of the INTE 472 project.
Uses: os, sys, shutil, datetime, json, csv
"""

import os
import sys
import shutil
from datetime import datetime, date
import json
import csv  # included because project requires it (not used heavily here)

# CONFIG
BASE_FOLDER = "StudentFiles"
LOG_FILE = "activity_log.txt"

def log_message(folder_path, message):
    """Append a timestamped message to activity_log.txt inside folder_path."""
    log_path = os.path.join(folder_path, LOG_FILE)
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    entry = f"{timestamp} {message}\n"
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(entry)
    except Exception as e:
        # If logging fails, print to console (do not crash)
        print(f"Failed to write to log: {e}")

def ensure_student_folder():
    """Task 1: ensure StudentFiles exists, show absolute path, handle errors."""
    try:
        if not os.path.exists(BASE_FOLDER):
            os.mkdir(BASE_FOLDER)
            print(f"Folder '{BASE_FOLDER}' created.")
        else:
            print(f"Folder '{BASE_FOLDER}' already exists.")
        abs_path = os.path.abspath(BASE_FOLDER)
        print(f"Absolute path: {abs_path}")
        return abs_path
    except Exception as e:
        print(f"Error creating/accessing folder '{BASE_FOLDER}': {e}")
        sys.exit(1)

def create_records_file(folder_path):
    """Task 2: create file named records_YYYY-MM-DD.txt and write 5 student names."""
    today = date.today().isoformat()  # YYYY-MM-DD
    filename = f"records_{today}.txt"
    fullpath = os.path.join(folder_path, filename)
    try:
        print("\nEnter five student names. Press Enter after each name.")
        names = []
        while len(names) < 5:
            name = input(f"Name {len(names)+1}: ").strip()
            if name:
                names.append(name)
            else:
                print("Empty name ignored — please enter a valid name.")
        with open(fullpath, "w", encoding="utf-8") as f:
            for n in names:
                f.write(n + "\n")
        creation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\nSuccess: '{filename}' created at {creation_time}.")
        log_message(folder_path, f"{filename} created successfully.")
        return filename, fullpath
    except Exception as e:
        log_message(folder_path, f"ERROR creating {filename}: {e}")
        print(f"Error creating file: {e}")
        sys.exit(1)

def read_file_info(file_path):
    """Task 3: read and display contents, size and last modified date."""
    try:
        print("\n--- File contents ---")
        with open(file_path, "r", encoding="utf-8") as f:
            contents = f.read()
            print(contents.strip() or "(file empty)")
        size = os.path.getsize(file_path)
        mtime = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M:%S")
        print(f"File size: {size} bytes")
        print(f"Last modified: {mtime}")
    except Exception as e:
        folder = os.path.dirname(file_path) or "."
        log_message(folder, f"ERROR reading {file_path}: {e}")
        print(f"Error reading file info: {e}")

def backup_and_archive(folder_path, filename):
    """Task 4: create backup copy, Archive folder, move backup there, list archive."""
    try:
        today = date.today().isoformat()
        src = os.path.join(folder_path, filename)
        backup_name = f"backup_{filename}"
        backup_path = os.path.join(folder_path, backup_name)
        # copy
        shutil.copy(src, backup_path)
        print(f"\nBackup created: {backup_name}")
        # ensure Archive exists
        archive_folder = os.path.join(folder_path, "Archive")
        if not os.path.exists(archive_folder):
            os.mkdir(archive_folder)
            print("Archive folder created.")
        # move backup into Archive
        dest_path = os.path.join(archive_folder, backup_name)
        shutil.move(backup_path, dest_path)
        print(f"Backup moved to Archive/{backup_name}")
        # list files in Archive
        archived_files = os.listdir(archive_folder)
        print("\nFiles in Archive:")
        for f in archived_files:
            print(" -", f)
        log_message(folder_path, f"{filename} created and archived successfully.")
        return archive_folder
    except Exception as e:
        log_message(folder_path, f"ERROR during backup/archive of {filename}: {e}")
        print(f"Error during backup/archive: {e}")

def advanced_file_ops(folder_path):
    """Task 6: ask user if they want to delete a file, delete if requested, log it."""
    try:
        answer = input("\nWould you like to delete a file from StudentFiles? (Yes/No): ").strip().lower()
        if answer == "yes":
            current_files = os.listdir(folder_path)
            print("\nCurrent files in StudentFiles:")
            for f in current_files:
                print(" -", f)
            to_delete = input("\nEnter the exact file name to delete (include extension): ").strip()
            target = os.path.join(folder_path, to_delete)
            if os.path.exists(target) and os.path.isfile(target):
                os.remove(target)
                print(f"'{to_delete}' deleted.")
                log_message(folder_path, f"{to_delete} deleted by user.")
            else:
                print(f"File '{to_delete}' not found.")
                log_message(folder_path, f"Attempted to delete '{to_delete}' but file not found.")
        else:
            print("Skipping deletion step.")
        # Show remaining files
        remaining = os.listdir(folder_path)
        print("\nRemaining files in StudentFiles:")
        for f in remaining:
            print(" -", f)
    except Exception as e:
        log_message(folder_path, f"ERROR during advanced file ops: {e}")
        print(f"Error during advanced file operations: {e}")

def main():
    print("=== Python File Management and Data Processing Utility ===")
    folder_path = ensure_student_folder()
    # Task 2
    filename, file_path = create_records_file(folder_path)
    # Task 3
    read_file_info(file_path)
    # Task 4
    backup_and_archive(folder_path, filename)
    # Task 6
    advanced_file_ops(folder_path)
    print("\nProgram finished. Check activity_log.txt inside StudentFiles for a run log.")
    print("Goodbye!")

if __name__ == "__main__":
    main()
