import requests
import zipfile
import io
import csv
import json

# Official FIDE rating list ZIPs
FIDE_LIST_URLS = {
    "classical": "https://ratings.fide.com/download/standard_rating_list.zip",
    "rapid":     "https://ratings.fide.com/download/rapid_rating_list.zip",
    "blitz":     "https://ratings.fide.com/download/blitz_rating_list.zip"
}


def download_fide_csv(url):
    """Download FIDE ZIP → extract the TXT → return as CSV reader."""
    print(f"Downloading: {url}")
    response = requests.get(url)
    response.raise_for_status()

    zf = zipfile.ZipFile(io.BytesIO(response.content))
    txt_file = [f for f in zf.namelist() if f.endswith(".txt")][0]

    print(f"Extracting: {txt_file}")
    data = zf.read(txt_file).decode("utf-8", errors="ignore")
    return io.StringIO(data)


def parse_fide_list(stream):
    """Parse a FIDE .txt list into raw rows."""
    stream.seek(0)
    return list(csv.reader(stream, delimiter=';'))


print("Step 1: Downloading all lists...")

# Download all three lists
streams = {cat: download_fide_csv(url) for cat, url in FIDE_LIST_URLS.items()}
rows = {cat: parse_fide_list(stream) for cat, stream in streams.items()}

print("Step 2: Building database...")

# Final dictionary: fide_id → data
players = {}

# First load classical list (for base info)
for r in rows["classical"]:
    if len(r) < 8:
        continue

    fide_id = r[0].strip()
    name = r[1].strip()
    title = r[2].strip()
    classical = r[3].strip()
    fed = r[7].strip()

    if not fide_id.isdigit():
        continue

    players[fide_id] = {
        "id": fide_id,
        "name": name,
        "title": title,
        "federation": fed,
        "classical": int(classical) if classical.isdigit() else None,
        "rapid": None,
        "blitz": None
    }

# Merge RAPID + BLITZ
for category in ["rapid", "blitz"]:
    for r in rows[category]:
        if len(r) < 4:
            continue

        fide_id = r[0].strip()
        if fide_id not in players:
            continue

        rating = r[3].strip()
        if rating.isdigit():
            players[fide_id][category] = int(rating)

print("Step 3: Saving to all_fide_players.json ...")

with open("all_fide_players.json", "w", encoding="utf-8") as f:
    json.dump(list(players.values()), f, indent=2, ensure_ascii=False)

print("DONE!")
print("File saved as all_fide_players.json (WARNING: very large file)")
