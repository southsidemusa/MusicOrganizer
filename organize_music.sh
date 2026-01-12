#!/bin/bash

BASE="/Volumes/BIG DRIVE/Rekordbox"
ORGANIZED="/Volumes/BIG DRIVE/Rekordbox_Organized"
UNSORTED="$ORGANIZED/_Unsorted"

# Create organized folder
mkdir -p "$ORGANIZED"
mkdir -p "$UNSORTED"

# Read metadata file and organize
while IFS='|' read -r filepath artist album title; do
    # Get filename and extension
    filename=$(basename "$filepath")
    ext="${filename##*.}"
    
    # Clean up artist/album - remove special chars that break paths
    artist=$(echo "$artist" | sed 's/[<>:"\\|?*]/-/g' | sed 's/\.$//' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    album=$(echo "$album" | sed 's/[<>:"\\|?*]/-/g' | sed 's/\.$//' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    title=$(echo "$title" | sed 's/[<>:"\\|?*]/-/g' | sed 's/\.$//' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    
    # If no artist, try to parse from filename
    if [ -z "$artist" ]; then
        # Try to extract "Artist - Title" from filename
        if [[ "$filename" =~ ^[0-9]*[[:space:]]*[-.]?[[:space:]]*(.*)[[:space:]]-[[:space:]](.*)\..*$ ]]; then
            artist="${BASH_REMATCH[1]}"
            title="${BASH_REMATCH[2]}"
        fi
    fi
    
    # If still no artist, put in Unsorted
    if [ -z "$artist" ]; then
        dest="$UNSORTED/$filename"
    else
        # Use "Singles" if no album
        if [ -z "$album" ]; then
            album="Singles"
        fi
        
        # Create title-based filename, or use original if no title
        if [ -n "$title" ]; then
            newname="$title.$ext"
        else
            newname="$filename"
        fi
        
        dest="$ORGANIZED/$artist/$album/$newname"
        mkdir -p "$ORGANIZED/$artist/$album"
    fi
    
    # Copy file (safer than move)
    if [ -f "$filepath" ]; then
        # Handle duplicates by adding number
        if [ -f "$dest" ]; then
            counter=1
            base="${dest%.*}"
            while [ -f "${base}_${counter}.$ext" ]; do
                ((counter++))
            done
            dest="${base}_${counter}.$ext"
        fi
        cp "$filepath" "$dest" 2>/dev/null && echo "OK: $artist / $album / $(basename "$dest")"
    fi
done < /tmp/music_metadata.txt

echo ""
echo "=== Organization complete ==="
