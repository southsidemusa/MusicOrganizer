#!/usr/bin/env python3
"""
Re-sort music files based on embedded genre tags
"""

import os
import shutil
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
from mutagen.aiff import AIFF

def get_genre_tag(filepath):
    """Read genre tag from audio file"""
    ext = os.path.splitext(filepath)[1].lower()

    try:
        if ext == '.mp3':
            audio = MP3(filepath)
            if audio.tags and audio.tags.get('TCON'):
                return str(audio.tags.get('TCON')[0])
        elif ext == '.flac':
            audio = FLAC(filepath)
            if audio.get('genre'):
                return audio.get('genre')[0]
        elif ext == '.m4a':
            audio = MP4(filepath)
            if audio.get('\xa9gen'):
                return audio.get('\xa9gen')[0]
        elif ext in ['.aiff', '.aif']:
            audio = AIFF(filepath)
            if audio.tags and audio.tags.get('TCON'):
                return str(audio.tags.get('TCON')[0])
    except Exception as e:
        pass

    return None

def get_artist_tag(filepath):
    """Read artist tag from audio file"""
    ext = os.path.splitext(filepath)[1].lower()

    try:
        if ext == '.mp3':
            audio = MP3(filepath)
            if audio.tags and audio.tags.get('TPE1'):
                return str(audio.tags.get('TPE1')[0])
        elif ext == '.flac':
            audio = FLAC(filepath)
            if audio.get('artist'):
                return audio.get('artist')[0]
        elif ext == '.m4a':
            audio = MP4(filepath)
            if audio.get('\xa9ART'):
                return audio.get('\xa9ART')[0]
        elif ext in ['.aiff', '.aif']:
            audio = AIFF(filepath)
            if audio.tags and audio.tags.get('TPE1'):
                return str(audio.tags.get('TPE1')[0])
    except Exception as e:
        pass

    return None

def classify_genre(genre_tag):
    """Map genre tag to folder structure"""
    if not genre_tag:
        return 'Unknown'

    genre_lower = genre_tag.lower()

    # Hip-Hop
    if any(x in genre_lower for x in ['hip hop', 'hip-hop', 'rap', 'trap']):
        return 'Hip-Hop'

    # R&B
    if any(x in genre_lower for x in ['r&b', 'rnb', 'soul', 'neo-soul', 'funk', 'rhythm and blues']):
        return 'R&B'

    # Deep House
    if any(x in genre_lower for x in ['deep house', 'soulful house', 'afro house', 'amapiano',
                                       'jazzy house', 'broken beat', 'nu jazz', 'acid jazz']):
        return 'House/Deep House'

    # House
    if any(x in genre_lower for x in ['house', 'techno', 'electronic', 'dance', 'garage',
                                       'uk bass', 'drum and bass', 'jungle', 'breakbeat']):
        return 'House'

    return 'Unknown'

def main():
    source_base = "/Volumes/BIG DRIVE/Rekordbox_ByGenre"
    dest_base = "/Volumes/BIG DRIVE/Rekordbox_Tagged"

    # Create destination folders
    os.makedirs(f"{dest_base}/Hip-Hop", exist_ok=True)
    os.makedirs(f"{dest_base}/R&B", exist_ok=True)
    os.makedirs(f"{dest_base}/House/Deep House", exist_ok=True)
    os.makedirs(f"{dest_base}/House", exist_ok=True)
    os.makedirs(f"{dest_base}/_Unsorted", exist_ok=True)

    # Track stats
    stats = {'Hip-Hop': 0, 'R&B': 0, 'House/Deep House': 0, 'House': 0, 'Unknown': 0}

    # Find all audio files
    for root, dirs, files in os.walk(source_base):
        for f in files:
            if f.lower().endswith(('.mp3', '.flac', '.m4a', '.aiff', '.aif')):
                if f.startswith('._'):
                    continue

                filepath = os.path.join(root, f)

                # Get tags
                genre = get_genre_tag(filepath)
                artist = get_artist_tag(filepath)

                # Classify
                category = classify_genre(genre)

                # Clean artist name for folder
                if artist:
                    artist_clean = artist.replace('/', '-').replace(':', '-')[:50]
                else:
                    artist_clean = "Unknown Artist"

                # Determine destination
                if category == 'Hip-Hop':
                    dest_dir = f"{dest_base}/Hip-Hop/{artist_clean}"
                elif category == 'R&B':
                    dest_dir = f"{dest_base}/R&B/{artist_clean}"
                elif category == 'House/Deep House':
                    dest_dir = f"{dest_base}/House/Deep House/{artist_clean}"
                elif category == 'House':
                    dest_dir = f"{dest_base}/House/{artist_clean}"
                else:
                    dest_dir = f"{dest_base}/_Unsorted/{artist_clean}"

                os.makedirs(dest_dir, exist_ok=True)

                # Copy file
                dest_path = os.path.join(dest_dir, f)
                if os.path.exists(dest_path):
                    # Handle duplicates
                    base, ext = os.path.splitext(f)
                    counter = 1
                    while os.path.exists(os.path.join(dest_dir, f"{base}_{counter}{ext}")):
                        counter += 1
                    dest_path = os.path.join(dest_dir, f"{base}_{counter}{ext}")

                shutil.copy2(filepath, dest_path)
                stats[category if category != 'Unknown' else 'Unknown'] += 1

                print(f"[{category}] {artist_clean} - {f}")

    print("\n" + "="*60)
    print("SORT COMPLETE")
    print("="*60)
    for cat, count in stats.items():
        print(f"{cat}: {count} files")
    print(f"\nOutput: {dest_base}")

if __name__ == '__main__':
    main()
