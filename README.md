# Music Organizer for Rekordbox

A collection of scripts to organize music files for DJ software like Rekordbox. Includes MusicBrainz API integration for accurate genre tagging.

## Quick Start

### Prerequisites
```bash
# Install Homebrew dependencies
brew install ffmpeg

# Install Python dependencies
pip3 install mutagen musicbrainzngs
```

### Recommended Workflow

1. **Clean junk files** (macOS metadata)
   ```bash
   find /path/to/music -name "._*" -type f -delete
   ```

2. **Scan and tag with MusicBrainz** (recommended)
   ```bash
   python3 enrich_tags.py
   ```
   Edit `base_dir` in script to point to your music folder.

3. **Re-sort by embedded genre tags**
   ```bash
   python3 resort_by_tags.py
   ```
   Edit `source_base` and `dest_base` in script.

4. **Import to Rekordbox**
   - File → Import → Folder
   - Select the organized folder
   - Genre tags will populate automatically

## Scripts

| Script | Purpose | Language |
|--------|---------|----------|
| `enrich_tags.py` | Query MusicBrainz API and write genre/year tags | Python |
| `resort_by_tags.py` | Organize files by embedded genre tags | Python |
| `organize_music.sh` | Organize by Artist/Album structure | Bash |
| `organize_by_genre.sh` | Organize by manual genre mapping | Bash |

## Folder Structure

After running `resort_by_tags.py`:
```
Music_Tagged/
├── Hip-Hop/
│   ├── Kendrick Lamar/
│   ├── Slum Village/
│   └── ...
├── R&B/
│   ├── SZA/
│   ├── Baby Rose/
│   └── ...
├── House/
│   ├── Deep House/
│   │   ├── Theo Parrish/
│   │   ├── Moodymann/
│   │   └── ...
│   ├── Joy Orbison/
│   └── ...
└── _Unsorted/
    └── (files without genre tags)
```

## Genre Categories

### Hip-Hop
hip hop, rap, trap, grime, boom bap, conscious hip hop, gangsta rap, southern hip hop, underground hip hop, alternative hip hop, jazz rap

### R&B
r&b, rhythm and blues, soul, neo-soul, funk, quiet storm, new jack swing, motown

### Deep House
deep house, soulful house, afro house, amapiano, jazzy house, garage house, broken beat, nu jazz, acid jazz, detroit techno

### House
house, techno, electronic, dance, tech house, progressive house, uk funky, uk bass, drum and bass, jungle, breakbeat

## MusicBrainz Notes

- Rate limited to 1 request/second
- ~180 files takes ~4-5 minutes
- South African house artists have limited coverage
- Files without matches go to `_Unsorted`

## Supported Formats

- MP3 (.mp3)
- FLAC (.flac)
- M4A (.m4a)
- AIFF (.aiff, .aif)
- WAV (.wav) - limited tag support

## Tips for Rekordbox

1. Import the `_Tagged` folder after organization
2. Use Rekordbox's intelligent playlists to filter by genre
3. Run analysis after import for BPM/key detection
4. Genre tags sync to USB exports for CDJs
