#!/usr/bin/env python3
import gi
import argparse
import os
from threading import Thread
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

try:
    from playsound import playsound
    SOUND_SUPPORT = True
except ImportError:
    SOUND_SUPPORT = False
    # print("Note: For sound support, install playsound module: pip install playsound")

class StandaloneDialog:
    def __init__(self, show_yes, show_no, show_ok, icon_path, title, text, sound_path):
        # Play sound if specified (in a separate thread to avoid blocking)
        """
        Create a standalone dialog with a specified icon, title, and text.

        If an icon path is provided, it will be loaded and displayed next to the text.
        If not, the text will be displayed alone.

        The dialog will have buttons based on the command-line arguments provided.

        :param show_yes: If True, include a Yes button
        :param show_no: If True, include a No button
        :param show_ok: If True, include an Ok button
        :param icon_path: The path to the icon image file
        :param title: The title of the dialog window
        :param text: The text to display in the dialog
        :param sound_path: The path to the sound file to play when the dialog opens
        """
        if sound_path and SOUND_SUPPORT:
            Thread(target=self.play_sound, args=(sound_path,), daemon=True).start()
        
        # Create the dialog without a parent window
        self.dialog = Gtk.Dialog(title=title)
        self.dialog.set_default_size(300, 100)
        
        # Make it modal and keep above other windows
        self.dialog.set_modal(True)
        self.dialog.set_keep_above(True)

        # Create a horizontal box for the icon and text
        content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        content_box.set_margin_top(10)
        content_box.set_margin_bottom(10)
        content_box.set_margin_start(10)
        content_box.set_margin_end(10)

        # Add icon if path is provided
        if icon_path:
            try:
                # Create an image widget
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    filename=icon_path,
                    width=48,
                    height=48,
                    preserve_aspect_ratio=True
                )
                image = Gtk.Image.new_from_pixbuf(pixbuf)
                content_box.pack_start(image, False, False, 0)
            except gi.repository.GLib.Error as e:
                print(f"Error loading icon: {e}")
            except Exception as e:
                print(f"Unexpected error loading icon: {e}")

        # Add the text label to the dialog
        label = Gtk.Label(label=text)
        label.set_line_wrap(True)
        label.set_justify(Gtk.Justification.LEFT)
        label.set_halign(Gtk.Align.START)
        content_box.pack_start(label, True, True, 0)

        # Add the content box to the dialog
        self.dialog.get_content_area().add(content_box)

        # Add buttons based on command-line arguments
        if show_yes:
            self.dialog.add_button("Yes", Gtk.ResponseType.YES)
        if show_no:
            self.dialog.add_button("No", Gtk.ResponseType.NO)
        if show_ok:
            self.dialog.add_button("Ok", Gtk.ResponseType.OK)

        # Connect dialog response signal
        self.dialog.connect("response", self.on_dialog_response)
        
        # Show the dialog and all its contents
        self.dialog.show_all()

    def play_sound(self, sound_path):
        """
        Play a sound from the specified file path.

        This function attempts to play a sound file located at the given path
        using the playsound module. If an error occurs during playback, it logs
        an error message.

        :param sound_path: The path to the sound file to be played.
        """
        try:
            playsound(sound_path)
        except Exception as e:
            print(f"Error playing sound: {e}")

    def on_dialog_response(self, dialog, response):
        """
        Handles the response from the dialog.

        This function is called when a button in the dialog is clicked. It prints
        the response type of the button clicked (Yes, No, or Ok) and then destroys
        the dialog. Finally, it quits the Gtk main loop.

        :param dialog: The Gtk dialog instance
        :param response: The response ID of the button clicked
        """
        if response in [Gtk.ResponseType.YES, Gtk.ResponseType.NO, Gtk.ResponseType.OK]:
            print(f"Button clicked: {response}")
        self.dialog.destroy()
        Gtk.main_quit()

if __name__ == "__main__":
    # Set up argparse with cli args
    parser = argparse.ArgumentParser(description="Create a standalone dialog with specified buttons and icon.")
    parser.add_argument('--yes', action='store_true', help='Add a Yes button')
    parser.add_argument('--no', action='store_true', help='Add a No button')
    parser.add_argument('--ok', action='store_true', help='Add an Ok button')
    parser.add_argument('--icon', type=str, help='Path to the icon image file')
    parser.add_argument('--title', type=str, default="Dialog", help='Title of the dialog window')
    parser.add_argument('--text', type=str, default="", help='Text to display in the dialog')
    parser.add_argument('--sound', type=str, help='Path to sound file to play when dialog opens')

    args = parser.parse_args()

    # Verify icon path if it was specified, if not there exit
    if args.icon and not os.path.isfile(args.icon):
        print(f"Error: Icon file '{args.icon}' does not exist")
        exit(1)

    # Verify sound path if specified, if not exit
    if args.sound:
        if not SOUND_SUPPORT:
            print("Error: Sound support requires the playsound module")
            exit(1)
        if not os.path.isfile(args.sound):
            print(f"Error: Sound file '{args.sound}' does not exist")
            exit(1)

    # Create/display the dialog 
    app = StandaloneDialog(args.yes, args.no, args.ok, args.icon, args.title, args.text, args.sound)
    Gtk.main()