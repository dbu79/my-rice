#!/usr/bin/env python3
"""
Waybar clock -> calendar popup.
Click the clock module in waybar to toggle this open/closed.

Requires:
  - python-gobject
  - gtk3-layer-shell  (AUR: gtk-layer-shell / gtk3-layer-shell)
  - GTK3

On EndeavourOS / Arch:
  sudo pacman -S python-gobject gtk3
  yay -S gtk-layer-shell
"""

import os
import sys
import signal
import datetime

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("GtkLayerShell", "0.1")
from gi.repository import Gtk, GLib, GtkLayerShell, Gdk

LOCK_FILE = "/tmp/waybar_calendar_popup.pid"

CSS = b"""
window {
    background-color: rgba(30, 32, 34, 0.92);
    border: 2px solid rgba(148, 226, 213, 0.55); /* teal/cyan accent */
    border-radius: 14px;
}

#header-box {
    padding: 14px 18px 8px 18px;
}

#clock-label {
    font-family: "JetBrainsMono Nerd Font", monospace;
    font-size: 28px;
    font-weight: 700;
    color: #94e2d5; /* catppuccin teal */
}

#date-label {
    font-family: "JetBrainsMono Nerd Font", monospace;
    font-size: 13px;
    color: #a6adc8;
}

calendar {
    background-color: transparent;
    color: #cdd6f4;
    font-family: "JetBrainsMono Nerd Font", monospace;
    font-size: 12px;
    border: none;
    margin: 8px 14px 16px 14px;
}

calendar.header {
    background-color: transparent;
    color: #94e2d5;
    font-weight: bold;
}

calendar:selected {
    background-color: #94e2d5;
    color: #1e1e2e;
    border-radius: 8px;
}

calendar.button {
    color: #89dceb;
}
"""


def load_css():
    provider = Gtk.CssProvider()
    provider.load_from_data(CSS)
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
    )


def build_window():
    win = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
    win.set_decorated(False)
    win.set_resizable(False)
    win.set_skip_taskbar_hint(True)
    win.set_skip_pager_hint(True)

    GtkLayerShell.init_for_window(win)
    GtkLayerShell.set_layer(win, GtkLayerShell.Layer.OVERLAY)
    GtkLayerShell.set_keyboard_mode(win, GtkLayerShell.KeyboardMode.ON_DEMAND)

    # Anchor to top-right, offset down/left from the bar so it sits under the clock.
    # Tweak TOP_MARGIN / RIGHT_MARGIN to line it up under your clock widget.
    GtkLayerShell.set_anchor(win, GtkLayerShell.Edge.TOP, True)
    GtkLayerShell.set_anchor(win, GtkLayerShell.Edge.RIGHT, True)
    GtkLayerShell.set_margin(win, GtkLayerShell.Edge.TOP, 44)
    GtkLayerShell.set_margin(win, GtkLayerShell.Edge.RIGHT, 44)
    outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    win.add(outer)

    header = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, name="header-box")
    outer.pack_start(header, False, False, 0)

    now = datetime.datetime.now()
    clock_label = Gtk.Label(label=now.strftime("%H:%M"), name="clock-label")
    clock_label.set_halign(Gtk.Align.START)
    date_label = Gtk.Label(label=now.strftime("%A, %d %B %Y"), name="date-label")
    date_label.set_halign(Gtk.Align.START)
    header.pack_start(clock_label, False, False, 0)
    header.pack_start(date_label, False, False, 0)

    cal = Gtk.Calendar()
    cal.set_hexpand(True)
    outer.pack_start(cal, False, False, 0)

    def tick():
        n = datetime.datetime.now()
        clock_label.set_text(n.strftime("%H:%M"))
        date_label.set_text(n.strftime("%A, %d %B %Y"))
        return True

    GLib.timeout_add_seconds(1, tick)

    # Close when it loses focus, so clicking elsewhere dismisses it.
    def on_focus_out(widget, event):
        Gtk.main_quit()
        return False

    win.connect("focus-out-event", on_focus_out)
    win.connect("destroy", lambda w: Gtk.main_quit())

    # Esc to close
    def on_key(widget, event):
        if event.keyval == Gdk.KEY_Escape:
            Gtk.main_quit()

    win.connect("key-press-event", on_key)

    return win


def toggle():
    """If a popup instance is already running, kill it (this acts as the toggle)
    and exit. Otherwise write our pid and show the window."""
    if os.path.exists(LOCK_FILE):
        try:
            with open(LOCK_FILE) as f:
                pid = int(f.read().strip())
            os.kill(pid, signal.SIGTERM)
        except (ValueError, ProcessLookupError, FileNotFoundError):
            pass
        finally:
            try:
                os.remove(LOCK_FILE)
            except FileNotFoundError:
                pass
        sys.exit(0)

    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))

    def cleanup(*_):
        try:
            os.remove(LOCK_FILE)
        except FileNotFoundError:
            pass
        Gtk.main_quit()

    signal.signal(signal.SIGTERM, cleanup)

    load_css()
    win = build_window()
    win.show_all()
    win.connect("destroy", cleanup)

    try:
        Gtk.main()
    finally:
        try:
            os.remove(LOCK_FILE)
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    toggle()
