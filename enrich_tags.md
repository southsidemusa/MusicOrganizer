# enrich_tags.py

## Overview
Python script that queries the MusicBrainz API to enrich audio file metadata with accurate genre, year, and artist information, then writes the tags directly to the files using mutagen.

## Dependencies
```bash
pip3 install mutagen musicbrainzngs
```

## Supported Formats
- MP3 (.mp3)
- FLAC (.flac)
- M4A (.m4a)
- AIFF (.aiff, .aif)

## What It Does
1. Scans a directory for audio files
2. Reads existing artist/title tags from each file
3. Queries MusicBrainz API for matching recordings
4. Extracts genre tags from MusicBrainz (both recording and artist tags)
5. Classifies genres into categories: Hip-Hop, R&B, Deep House, House, Unknown
6. Writes the genre and year tags back to the audio files

## Configuration
Edit these variables in the script:
- `RATE_LIMIT`: Seconds between API requests (default: 1.1 - MusicBrainz allows 1 req/sec)
- `base_dir`: Source directory to scan

## Usage
```bash
python3 enrich_tags.py
```

## Output
- Tags are written directly to audio files
- Results saved to `/tmp/tagging_results.json`
- Console output shows progress and summary

## MusicBrainz Rate Limiting
The script includes a 1.1-second delay between API calls to comply with MusicBrainz rate limits. For 180 files, expect ~4-5 minutes runtime.

## Genre Classification
The script maps MusicBrainz tags to these categories:
- **Hip-Hop**: hip hop, rap, trap, grime, boom bap, etc.
- **R&B**: r&b, soul, neo-soul, funk, etc.
- **Deep House**: deep house, soulful house, afro house, amapiano, etc.
- **House**: house, techno, electronic, dance, etc.

## Notes
- Files without artist/title tags are skipped
- Artists not in MusicBrainz will show "No match found"
- South African house artists often have limited MusicBrainz coverage
