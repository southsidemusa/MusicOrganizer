#!/usr/bin/env python3
"""
MusicBrainz Tag Enrichment Script
Queries MusicBrainz API for metadata and writes tags using mutagen
"""

import os
import sys
import time
import json
import musicbrainzngs
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
from mutagen.aiff import AIFF
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TCON, TDRC, ID3NoHeaderError

# Set up MusicBrainz API
musicbrainzngs.set_useragent("MusicTagger", "1.0", "musabey@example.com")

# Rate limiting - MusicBrainz allows 1 request per second
RATE_LIMIT = 1.1  # seconds between requests

def get_current_tags(filepath):
    """Extract current tags from audio file"""
    ext = os.path.splitext(filepath)[1].lower()

    try:
        if ext == '.mp3':
            audio = MP3(filepath)
            tags = audio.tags
            if tags:
                artist = str(tags.get('TPE1', [''])[0]) if tags.get('TPE1') else ''
                title = str(tags.get('TIT2', [''])[0]) if tags.get('TIT2') else ''
                album = str(tags.get('TALB', [''])[0]) if tags.get('TALB') else ''
                genre = str(tags.get('TCON', [''])[0]) if tags.get('TCON') else ''
                return {'artist': artist, 'title': title, 'album': album, 'genre': genre}
        elif ext == '.flac':
            audio = FLAC(filepath)
            return {
                'artist': audio.get('artist', [''])[0] if audio.get('artist') else '',
                'title': audio.get('title', [''])[0] if audio.get('title') else '',
                'album': audio.get('album', [''])[0] if audio.get('album') else '',
                'genre': audio.get('genre', [''])[0] if audio.get('genre') else ''
            }
        elif ext == '.m4a':
            audio = MP4(filepath)
            return {
                'artist': audio.get('\xa9ART', [''])[0] if audio.get('\xa9ART') else '',
                'title': audio.get('\xa9nam', [''])[0] if audio.get('\xa9nam') else '',
                'album': audio.get('\xa9alb', [''])[0] if audio.get('\xa9alb') else '',
                'genre': audio.get('\xa9gen', [''])[0] if audio.get('\xa9gen') else ''
            }
        elif ext in ['.aiff', '.aif']:
            audio = AIFF(filepath)
            tags = audio.tags
            if tags:
                artist = str(tags.get('TPE1', [''])[0]) if tags.get('TPE1') else ''
                title = str(tags.get('TIT2', [''])[0]) if tags.get('TIT2') else ''
                album = str(tags.get('TALB', [''])[0]) if tags.get('TALB') else ''
                genre = str(tags.get('TCON', [''])[0]) if tags.get('TCON') else ''
                return {'artist': artist, 'title': title, 'album': album, 'genre': genre}
    except Exception as e:
        print(f"  Error reading tags: {e}")

    return {'artist': '', 'title': '', 'album': '', 'genre': ''}

def search_musicbrainz(artist, title):
    """Search MusicBrainz for a recording and get genre/tags"""
    try:
        # Clean up artist name (remove feat. etc for better matching)
        clean_artist = artist.split(' feat')[0].split(' ft.')[0].split(' ft ')[0].split(',')[0].strip()
        clean_title = title.split('(')[0].split('[')[0].strip()  # Remove remix info for initial search

        # Search for recording
        result = musicbrainzngs.search_recordings(
            artist=clean_artist,
            recording=clean_title,
            limit=5
        )

        if not result.get('recording-list'):
            return None

        recording = result['recording-list'][0]
        recording_id = recording['id']

        # Get detailed info with tags
        detailed = musicbrainzngs.get_recording_by_id(
            recording_id,
            includes=['artists', 'releases', 'tags', 'artist-credits']
        )

        rec = detailed['recording']

        # Extract genres from tags
        genres = []
        if 'tag-list' in rec:
            # Sort by count, get top tags
            sorted_tags = sorted(rec['tag-list'], key=lambda x: int(x.get('count', 0)), reverse=True)
            genres = [tag['name'] for tag in sorted_tags[:3]]

        # Get artist info for more tags
        if 'artist-credit' in rec:
            for credit in rec['artist-credit']:
                if isinstance(credit, dict) and 'artist' in credit:
                    artist_id = credit['artist']['id']
                    try:
                        artist_detail = musicbrainzngs.get_artist_by_id(artist_id, includes=['tags'])
                        if 'tag-list' in artist_detail.get('artist', {}):
                            artist_tags = sorted(artist_detail['artist']['tag-list'],
                                                key=lambda x: int(x.get('count', 0)), reverse=True)
                            for tag in artist_tags[:3]:
                                if tag['name'] not in genres:
                                    genres.append(tag['name'])
                    except:
                        pass
                    break  # Only check first artist

        # Get release year
        year = ''
        if 'release-list' in rec and rec['release-list']:
            for release in rec['release-list']:
                if 'date' in release:
                    year = release['date'][:4]
                    break

        return {
            'genres': genres,
            'year': year,
            'mb_artist': rec.get('artist-credit-phrase', ''),
            'mb_title': rec.get('title', '')
        }

    except Exception as e:
        print(f"  MusicBrainz error: {e}")
        return None

def classify_genre(genres):
    """Classify into main genre categories based on MusicBrainz tags"""
    genres_lower = [g.lower() for g in genres]

    # Hip-Hop indicators
    hip_hop_tags = ['hip hop', 'hip-hop', 'rap', 'trap', 'grime', 'boom bap', 'conscious hip hop',
                    'gangsta rap', 'southern hip hop', 'west coast hip hop', 'east coast hip hop',
                    'underground hip hop', 'alternative hip hop', 'jazz rap']

    # R&B indicators
    rnb_tags = ['r&b', 'rnb', 'rhythm and blues', 'soul', 'neo-soul', 'neo soul', 'contemporary r&b',
                'funk', 'quiet storm', 'new jack swing', 'motown']

    # Deep House indicators
    deep_house_tags = ['deep house', 'soulful house', 'afro house', 'afro-house', 'amapiano',
                       'jazzy house', 'garage house', 'uk garage', 'broken beat', 'nu jazz',
                       'acid jazz', 'future jazz', 'detroit techno']

    # House indicators (broader)
    house_tags = ['house', 'electronic', 'dance', 'techno', 'tech house', 'progressive house',
                  'electro house', 'uk funky', 'uk bass', 'drum and bass', 'jungle', 'breakbeat']

    # Check for matches
    for tag in genres_lower:
        for ht in hip_hop_tags:
            if ht in tag:
                return 'Hip-Hop'

    for tag in genres_lower:
        for rt in rnb_tags:
            if rt in tag:
                return 'R&B'

    for tag in genres_lower:
        for dht in deep_house_tags:
            if dht in tag:
                return 'Deep House'

    for tag in genres_lower:
        for hot in house_tags:
            if hot in tag:
                return 'House'

    return 'Unknown'

def write_tags(filepath, genre, year=None):
    """Write genre (and optionally year) tags to audio file"""
    ext = os.path.splitext(filepath)[1].lower()

    try:
        if ext == '.mp3':
            try:
                audio = MP3(filepath, ID3=ID3)
                if audio.tags is None:
                    audio.add_tags()
            except ID3NoHeaderError:
                audio = MP3(filepath)
                audio.add_tags()

            audio.tags.add(TCON(encoding=3, text=genre))
            if year:
                audio.tags.add(TDRC(encoding=3, text=year))
            audio.save()

        elif ext == '.flac':
            audio = FLAC(filepath)
            audio['genre'] = genre
            if year:
                audio['date'] = year
            audio.save()

        elif ext == '.m4a':
            audio = MP4(filepath)
            audio['\xa9gen'] = [genre]
            if year:
                audio['\xa9day'] = [year]
            audio.save()

        elif ext in ['.aiff', '.aif']:
            audio = AIFF(filepath)
            if audio.tags is None:
                audio.add_tags()
            audio.tags.add(TCON(encoding=3, text=genre))
            if year:
                audio.tags.add(TDRC(encoding=3, text=year))
            audio.save()

        return True
    except Exception as e:
        print(f"  Error writing tags: {e}")
        return False

def main():
    base_dir = "/Volumes/BIG DRIVE/Rekordbox_ByGenre"
    results = []

    # Find all audio files
    audio_files = []
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if f.lower().endswith(('.mp3', '.flac', '.m4a', '.aiff', '.aif')):
                if not f.startswith('._'):
                    audio_files.append(os.path.join(root, f))

    print(f"Found {len(audio_files)} audio files to process")
    print("="*60)

    for i, filepath in enumerate(audio_files):
        filename = os.path.basename(filepath)
        print(f"\n[{i+1}/{len(audio_files)}] {filename}")

        # Get current tags
        tags = get_current_tags(filepath)
        artist = tags['artist']
        title = tags['title']

        if not artist or not title:
            print(f"  Skipping - missing artist/title tags")
            results.append({'file': filepath, 'status': 'skipped', 'reason': 'missing tags'})
            continue

        print(f"  Artist: {artist}")
        print(f"  Title: {title}")

        # Query MusicBrainz
        time.sleep(RATE_LIMIT)  # Rate limiting
        mb_data = search_musicbrainz(artist, title)

        if mb_data and mb_data['genres']:
            genres = mb_data['genres']
            year = mb_data['year']
            main_genre = classify_genre(genres)

            print(f"  MusicBrainz genres: {', '.join(genres)}")
            print(f"  Classified as: {main_genre}")
            if year:
                print(f"  Year: {year}")

            # Write tags
            # Use first genre or main classification
            genre_to_write = main_genre if main_genre != 'Unknown' else (genres[0] if genres else '')
            if genre_to_write:
                if write_tags(filepath, genre_to_write, year):
                    print(f"  Tags written successfully")
                    results.append({
                        'file': filepath,
                        'status': 'success',
                        'genre': genre_to_write,
                        'mb_genres': genres,
                        'year': year
                    })
                else:
                    results.append({'file': filepath, 'status': 'write_error'})
            else:
                results.append({'file': filepath, 'status': 'no_genre'})
        else:
            print(f"  No MusicBrainz match found")
            results.append({'file': filepath, 'status': 'no_match', 'artist': artist, 'title': title})

    # Save results
    with open('/tmp/tagging_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    success = len([r for r in results if r['status'] == 'success'])
    no_match = len([r for r in results if r['status'] == 'no_match'])
    skipped = len([r for r in results if r['status'] == 'skipped'])
    errors = len([r for r in results if r['status'] in ['write_error', 'no_genre']])

    print(f"Successfully tagged: {success}")
    print(f"No MusicBrainz match: {no_match}")
    print(f"Skipped (missing tags): {skipped}")
    print(f"Errors: {errors}")
    print(f"\nResults saved to /tmp/tagging_results.json")

if __name__ == '__main__':
    main()
