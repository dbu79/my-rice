#!/usr/bin/env bash

wall_dir="$HOME/Pictures/wallpapers/cropped"

rofi_theme="$HOME/.config/rofi/wallpaper-config.rasi"

selected=$(
find "$wall_dir" -type f \( -iname "*.jpg" -o -iname "*.png" -o -iname "*.jpeg" \) \
| while read -r img; do
    name=$(basename "$img")
    printf '%s\0icon\x1f%s\n' "$name" "$img"
  done \
| rofi \
    -dmenu \
    -show-icons \
    -theme "$rofi_theme"
)

[ -z "$selected" ] && exit 0

wallpaper="$wall_dir/$selected"

# Set wallpaper
swww img "$wallpaper" \
--transition-type grow \
--transition-pos "$(hyprctl cursorpos)" \
--transition-duration 1

# Generate Matugen colors
matugen image "$wallpaper" --source-color-index 0

# Reload Waybar
pkill -SIGUSR2 waybar

hyprctl reload