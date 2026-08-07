"""Download the latest GLEIF Golden Copy (LEI Level 1, CSV format).

The download link contains the publication date and changes every day.
So this script asks the GLEIF API where the newest file is and then
downloads it (around 500 MB). After that, prepare_dataset.py can be
run on the downloaded zip.
"""

import json
import urllib.request

API_URL = "https://goldencopy.gleif.org/api/v2/golden-copies/publishes/lei2/latest"


def get_latest_csv_info():
    """Ask the GLEIF API for the URL and size of the newest CSV file."""
    with urllib.request.urlopen(API_URL) as response:
        data = json.load(response)
    info = data["data"]["full_file"]["csv"]
    return info["url"], info["size_human_readable"]


def download(url):
    """Download the file into the current directory with a simple progress display."""
    filename = url.split("/")[-1]

    def show_progress(blocks, block_size, total_size):
        """Print the progress in percent, urlretrieve calls this after every block."""
        percent = blocks * block_size * 100 // total_size
        if percent > 100:  # the last block can push it over 100
            percent = 100
        print(f"\rDownloading {filename}: {percent}%", end="", flush=True)

    urllib.request.urlretrieve(url, filename, reporthook=show_progress)
    print()
    return filename


def main():
    """Get the latest download link and fetch the file."""
    url, size = get_latest_csv_info()
    print(f"Latest Golden Copy: {url} ({size})")
    filename = download(url)
    print(f"Done. Next step: python prepare_dataset.py --source {filename}")


if __name__ == "__main__":
    main()
