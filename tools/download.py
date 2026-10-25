
"""
Polite downloader
-----------------
Usage:
    python tools/download.py urls.txt

Input:
    urls.txt — one URL per line.
    Lines starting with # are skipped.

Output:
    Downloaded files are saved to data/raw/.
    Every successful download is logged to data/manifest.csv.
"""

import csv
import hashlib
import os
import sys
import time
from datetime import date
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests


# --------------------------------------------------
# Configuration
# --------------------------------------------------

RAW = "data/raw"
MANIFEST = "data/manifest.csv"

HEADERS = {
    "User-Agent": (
        "ExamateStudentProject/1.0 "
        "(learning project; contact: your-email@example.com)"
    )
}

DELAY = 2  # Seconds between requests

robots = {}


# --------------------------------------------------
# Robots.txt Permission Check
# --------------------------------------------------

def allowed(url):
    """Check robots.txt to determine whether crawling is allowed."""
    parsed_url = urlparse(url)
    root = f"{parsed_url.scheme}://{parsed_url.netloc}"

    if root not in robots:
        robot_parser = RobotFileParser(f"{root}/robots.txt")

        try:
            robot_parser.read()
        except Exception:
            # If robots.txt cannot be reached, deny by default.
            robot_parser = None

        robots[root] = robot_parser

    robot_parser = robots[root]

    if robot_parser is None:
        return False

    return robot_parser.can_fetch(HEADERS["User-Agent"], url)


# --------------------------------------------------
# Filename Generation
# --------------------------------------------------

def name_for(url):
    """Generate a filename from the URL path."""
    filename = os.path.basename(urlparse(url).path) or "index.html"
    return filename.replace(" ", "_")


# --------------------------------------------------
# Environment Setup
# --------------------------------------------------

def setup_environment():
    """Create the download directory and manifest CSV if needed."""
    os.makedirs(RAW, exist_ok=True)
    os.makedirs(os.path.dirname(MANIFEST), exist_ok=True)

    if not os.path.exists(MANIFEST):
        with open(
            MANIFEST,
            "w",
            newline="",
            encoding="utf-8",
        ) as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(
                ["filename", "url", "sha256", "date_downloaded"]
            )


# --------------------------------------------------
# Download Processing
# --------------------------------------------------

def download_urls(url_file):
    """Download permitted URLs and record successful downloads."""
    setup_environment()

    if not os.path.isfile(url_file):
        print(f"Error: File '{url_file}' not found.")
        sys.exit(1)

    with open(url_file, "r", encoding="utf-8") as file:
        urls = [
            line.strip()
            for line in file
            if line.strip() and not line.strip().startswith("#")
        ]

    if not urls:
        print("No URLs found in the input file.")
        return

    for url in urls:
        parsed_url = urlparse(url)

        if parsed_url.scheme not in ("http", "https") or not parsed_url.netloc:
            print(f"Skipping invalid URL: {url}")
            continue

        if not allowed(url):
            print(f"Skipping (disallowed or robots.txt unavailable): {url}")
            continue

        filename = name_for(url)
        filepath = os.path.join(RAW, filename)

        try:
            print(f"Downloading: {url}")

            response = requests.get(
                url,
                headers=HEADERS,
                timeout=15,
            )
            response.raise_for_status()

            # Save the downloaded content.
            with open(filepath, "wb") as output_file:
                output_file.write(response.content)

            # Calculate SHA-256 hash for integrity verification.
            sha256_hash = hashlib.sha256(
                response.content
            ).hexdigest()

            today = date.today().isoformat()

            # Record the successful download.
            with open(
                MANIFEST,
                "a",
                newline="",
                encoding="utf-8",
            ) as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(
                    [filename, url, sha256_hash, today]
                )

            print(f"Saved to: {filepath}")
            print(f"SHA-256: {sha256_hash}")

        except requests.RequestException as error:
            print(f"Download failed for {url}: {error}")

        except OSError as error:
            print(f"File operation failed for {url}: {error}")

        finally:
            # Wait between requests to avoid overloading servers.
            time.sleep(DELAY)


# --------------------------------------------------
# Main Entry Point
# --------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tools/download.py <path_to_urls_txt>")
        sys.exit(1)

    download_urls(sys.argv[1])
