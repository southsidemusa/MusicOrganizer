# resort_by_tags.py

## Overview
Python script that reads embedded genre tags from audio files and reorganizes them into a folder structure based on those tags. Designed to run after `enrich_tags.py` has written genre metadata to files.

## Dependencies
```bash
pip3 install mutagen
```

## Supported Formats
- MP3 (.mp3)
- FLAC (.flac)
- M4A (.m4a)
- AIFF (.aiff, .aif)

## What It Does
1. Scans source directory for audio files
2. Reads the genre tag from each file
3. Classifies into categories: Hip-Hop, R&B, House, Deep House, Unknown
4. Copies files to destination organized by genre and artist

## Folder Structure Created
```
Rekordbox_Tagged/
├── Hip-Hop/
│   ├── Artist Name/
│   │   └── track.mp3
│   └── ...
├── R&B/
│   └── ...
├── House/
│   ├── Deep House/
│   │   └── ...
│   └── Artist Name/
└── _Unsorted/
    └── (files without genre tags)
```

## Configuration
Edit these variables in the script:
- `source_base`: Directory containing files to sort
- `dest_base`: Destination directory for organized files

## Usage
```bash
python3 resort_by_tags.py
```

## Genre Classification
Maps embedded genre tags to folders:
- **Hip-Hop**: Tags containing "hip hop", "rap", "trap"
- **R&B**: Tags containing "r&b", "soul", "funk"
- **House/Deep House**: Tags containing "deep house", "soulful house", "afro house"
- **House**: Tags containing "house", "techno", "electronic"
- **_Unsorted**: Files with no genre tag or unrecognized genres

## Notes
- Files are copied, not moved (preserves source)
- Duplicate filenames get `_1`, `_2` suffix
- Artist names are sanitized for filesystem compatibility
