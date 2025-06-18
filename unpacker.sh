#!/bin/bash

INPUT_FILE="project_pack.txt"

if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Packed data file '$INPUT_FILE' not found."
    exit 1
fi

current_file=""
echo "Starting targeted unpack/update..."

while IFS= read -r line; do
    if [[ "$line" =~ ^---FILE:(.+)---$ ]]; then
        current_file="${BASH_REMATCH[1]}"
        echo "  -> Updating file: $current_file"

        dir=$(dirname "$current_file")

        # Create directory if it doesn't exist
        mkdir -p "$dir"

        # Overwrite the file, creating it if it doesn't exist
        > "$current_file"
    elif [[ "$line" == "---END_FILE---" ]]; then
        current_file=""
    elif [ -n "$current_file" ]; then
        # Append content to the current file
        echo "$line" >> "$current_file"
    fi
done < "$INPUT_FILE"

echo "Update complete."