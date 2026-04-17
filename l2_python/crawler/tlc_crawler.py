"""
Simple wget-like crawler for TLC Trip Record Data.
This script downloads the January 2026 trip data for yellow, green, and FHV (for-hire vehicle) taxis from the NYC TLC CDN.
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
"""

import urllib.request
import os

# List of data URLs to download (from NYC TLC CDN)
URLS = [
    "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2026-01.parquet",
    "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2026-01.parquet",
    "https://d37ci6vzurychx.cloudfront.net/trip-data/fhv_tripdata_2026-01.parquet",
]

DEST_DIR = "downloads"


def wget(url, dest_dir):
    """Download a single file — simulates: wget <url> -P <dest_dir>"""
    os.makedirs(dest_dir, exist_ok=True)
    filename = url.split("/")[-1]
    dest_path = os.path.join(dest_dir, filename)

    print(f"Downloading: {url}")
    urllib.request.urlretrieve(url, dest_path)
    print(f"Saved to:    {dest_path}\n")


if __name__ == "__main__":
    for url in URLS:
        wget(url, DEST_DIR)
