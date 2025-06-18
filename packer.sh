#!/bin/bash

# packer.sh - v4 (Whitelist Method - Foolproof)
# This script only packs items from a predefined list, making it very reliable.

OUTPUT_FILE="project_pack.txt"

# --- List of all essential files and directories for your project ---
# We will only pack what is on this list.
FILES_TO_PACK=(
    ".replit"
    "main.py"
    "poetry.lock"
    "pyproject.toml"
    "quiz_content.py"
    "replit.nix"
    "static"      # This is a directory
    "templates"   # This is a directory
)

echo "Packing project into '$OUTPUT_FILE'..."
# Create or clear the output file.
> "$OUTPUT_FILE"

# Function to process a single file to avoid repeating code.
process_file() {
    local file_path="$1"
    # Make sure it's actually a file.
    if [ -f "$file_path" ]; then
        echo "  -> Packing: $file_path"
        # Append the header, the content, and the footer to our output file.
        echo "---FILE:$file_path---" >> "$OUTPUT_FILE"
        cat "$file_path" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        echo "---END_FILE---" >> "$OUTPUT_FILE"
    fi
}

# Go through each item in our whitelist.
for item in "${FILES_TO_PACK[@]}"; do
    if [ ! -e "$item" ]; then
        echo "  -> Warning: '$item' not found, skipping."
        continue
    fi

    if [ -d "$item" ]; then
        # If the item is a directory, find all files inside it and process them.
        find "$item" -type f | while read -r found_file; do
            process_file "$found_file"
        done
    elif [ -f "$item" ]; then
        # If the item is just a file, process it directly.
        process_file "$item"
    fi
done

echo "Packing complete. You can now copy the contents of '$OUTPUT_FILE'."