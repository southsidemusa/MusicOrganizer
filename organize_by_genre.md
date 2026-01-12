# organize_by_genre.sh

## Overview
Bash script that organizes music files by genre using a predefined artist-to-genre mapping. Useful for initial genre organization before MusicBrainz enrichment.

## Dependencies
- Bash shell
- A genre mapping file (`/tmp/genre_map.txt`)

## What It Does
1. Reads a genre mapping file (artist → genre)
2. Scans source directory for audio files
3. Matches each file's artist to the genre map
4. Copies files to genre-based folder structure

## Folder Structure Created
```
Rekordbox_ByGenre/
├── Hip-Hop/
│   └── Artist Name/
├── R&B/
│   └── Artist Name/
├── House/
│   ├── Deep House/
│   │   └── Artist Name/
│   └── Artist Name/
└── _Unsorted/
    └── Artist Name/
```

## Genre Mapping File Format
Create `/tmp/genre_map.txt` with format:
```
GENRE|Artist Name
```

Example:
```
HIP-HOP|Kendrick Lamar
HIP-HOP|Slum Village
R&B|Baby Rose
R&B|SZA
DEEP-HOUSE|Theo Parrish
DEEP-HOUSE|Moodymann
HOUSE|Joy Orbison
```

Supported genres:
- `HIP-HOP` → Hip-Hop/
- `R&B` → R&B/
- `DEEP-HOUSE` → House/Deep House/
- `HOUSE` → House/

## Configuration
Edit these variables at the top of the script:
- `BASE`: Source directory (already organized by artist)
- `GENRE_BASE`: Destination directory
- `GENRE_MAP`: Path to genre mapping file

## Usage
```bash
# First create the genre map file
chmod +x organize_by_genre.sh
./organize_by_genre.sh
```

## Notes
- Artist matching is case-insensitive partial match
- Unmatched artists go to `_Unsorted`
- Files are copied, not moved
- Comments in genre map start with `#`
