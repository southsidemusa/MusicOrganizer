#!/bin/bash

BASE="/Volumes/BIG DRIVE/Rekordbox_Organized"
GENRE_BASE="/Volumes/BIG DRIVE/Rekordbox_ByGenre"
GENRE_MAP="/tmp/genre_map.txt"

# Create genre folders
mkdir -p "$GENRE_BASE/Hip-Hop"
mkdir -p "$GENRE_BASE/R&B"
mkdir -p "$GENRE_BASE/House/Deep House"
mkdir -p "$GENRE_BASE/_Unsorted"

# Function to find genre for an artist
get_genre() {
    local artist="$1"
    # Check each line in genre map
    while IFS='|' read -r genre pattern; do
        # Skip comments and empty lines
        [[ "$genre" =~ ^#.*$ ]] && continue
        [[ -z "$genre" ]] && continue
        
        # Case-insensitive partial match
        if echo "$artist" | grep -qi "$pattern"; then
            echo "$genre"
            return
        fi
    done < "$GENRE_MAP"
    echo "UNKNOWN"
}

# Process each file from organized folder
find "$BASE" -type f \( -name "*.mp3" -o -name "*.flac" -o -name "*.wav" -o -name "*.aiff" -o -name "*.aif" -o -name "*.m4a" \) 2>/dev/null | while read -r filepath; do
    # Extract artist from path (Artist/Album/Track.ext)
    relative="${filepath#$BASE/}"
    artist=$(echo "$relative" | cut -d'/' -f1)
    
    # Get filename
    filename=$(basename "$filepath")
    
    # Get genre
    genre=$(get_genre "$artist")
    
    # Determine destination
    case "$genre" in
        "HIP-HOP")
            dest="$GENRE_BASE/Hip-Hop/$artist"
            ;;
        "R&B")
            dest="$GENRE_BASE/R&B/$artist"
            ;;
        "DEEP-HOUSE")
            dest="$GENRE_BASE/House/Deep House/$artist"
            ;;
        "HOUSE")
            dest="$GENRE_BASE/House/$artist"
            ;;
        *)
            dest="$GENRE_BASE/_Unsorted/$artist"
            ;;
    esac
    
    mkdir -p "$dest"
    
    # Copy file
    if cp "$filepath" "$dest/$filename" 2>/dev/null; then
        echo "[$genre] $artist - $filename"
    fi
done

echo ""
echo "=== Genre organization complete ==="
