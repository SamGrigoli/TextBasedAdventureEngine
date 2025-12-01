#!/bin/bash

echo "Text Adventure Game Launcher"
echo "============================"
echo ""

# Check if data directory exists
if [ ! -d "../data" ]; then
    echo "Error: data folder not found!"
    echo "Please run the editor first to create a game."
    exit 1
fi

# List available games
echo "Available games:"
echo ""
count=0
games=()
for dir in ../data/*/; do
    if [ -d "$dir" ]; then
        game_name=$(basename "$dir")
        # Skip if it's just the data folder itself
        if [ "$game_name" != "data" ] && [ -f "$dir/world.json" ]; then
            games+=("$game_name")
            count=$((count + 1))
            echo "[$count] $game_name"
        fi
    fi
done

if [ $count -eq 0 ]; then
    echo "No games found!"
    echo "Please create a game using the editor first."
    exit 1
fi

echo ""
read -p "Enter the name of the game you want to play: " gamename

if [ ! -d "../data/$gamename" ]; then
    echo "Error: Game '$gamename' not found!"
    exit 1
fi

# Update loadgame.json
echo "\"$gamename\"" > ../data/loadgame.json

# Run the game
./textgame

read -p "Press Enter to exit..."