#!/bin/bash

options="Lock\nLogout\nSleep\nReboot\nShutdown"

choice=$(printf "Lock\nLogout\nSleep\nReboot\nShutdown" | rofi \
  -dmenu \
  -p "Power" \
  -theme ~/.config/rofi/power-config.rasi)

case "$choice" in
"Lock")
  hyprlock
  ;;
"Logout")
  hyprctl dispatch exit
  ;;
"Sleep")
  systemctl suspend
  ;;
"Reboot")
  systemctl reboot
  ;;
"Shutdown")
  systemctl poweroff
  ;;
esac
