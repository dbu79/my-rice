#!/usr/bin/env bash

wall_dir="$HOME/Pictures/wallpapers"

selected=$(
    find "$wall_dir" -type f \( -iname "*.jpg" -o -iname "*.png" -o -iname "*.jpeg" \) \
    | xargs -n1 basename \
    | rofi -dmenu -p "Select Wallpaper"
)

[ -z "$selected" ] && exit 0

wallpaper="$wall_dir/$selected"

# Set wallpaper
awww img "$wallpaper" \
    --transition-type grow \
    --transition-pos "$(hyprctl cursorpos)" \
    --transition-duration 1

# Generate Matugen colors
matugen image "$wallpaper" --source-color-index 0

# Reload Waybar
pkill -SIGUSR2 waybar