#!/bin/bash

options="Lock\nLogout\nReboot\nShutdown"

choice=$(printf "Lock\nLogout\nReboot\nShutdown" | rofi \
    -dmenu \
    -p "Power" \
    -theme ~/.config/rofi/config-power.rasi)

case "$choice" in
    "Lock")
        hyprlock
        ;;
    "Logout")
        hyprctl dispatch exit
        ;;
    "Reboot")
        systemctl reboot
        ;;
    "Shutdown")
        systemctl poweroff
        ;;
esac