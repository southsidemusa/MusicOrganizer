# organize_music.sh

## Overview
Bash script that organizes music files into an Artist/Album folder structure by reading metadata using ffprobe. This is the initial organization step before genre-based sorting.

## Dependencies
```bash
brew install ffmpeg
```

## What It Does
1. Scans source directory for audio files
2. Uses ffprobe to extract artist, album, and title metadata
3. Creates `Artist/Album/` folder structure
4. Copies files with clean filenames (title.ext)
5. Handles files with missing metadata

## Folder Structure Created
```
Rekordbox_Organized/
├── Artist Name/
│   ├── Album Name/
│   │   ├── Track Title.mp3
│   │   └── ...
│   └── Singles/
│       └── (tracks without album)
└── _Unsorted/
    └── (files without metadata)
```

## Configuration
Edit these variables at the top of the script:
- `BASE`: Source directory containing music files
- `ORGANIZED`: Destination directory for organized files
- `UNSORTED`: Subfolder for files without metadata

## Usage
```bash
chmod +x organize_music.sh
./organize_music.sh
```

## Metadata Extraction
Uses ffprobe to read:
- `artist` tag → folder name
- `album` tag → subfolder name
- `title` tag → filename

## Special Character Handling
- `/` and `:` in metadata are replaced with `-`
- Leading/trailing whitespace is trimmed
- Files without artist default to `_Unsorted`
- Files without album go to `Singles` subfolder

## Notes
- Creates a metadata scan file at `/tmp/music_metadata.txt`
- Files are copied, not moved
- Duplicate filenames get `_1`, `_2` suffix
