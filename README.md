# Modal Dialog

This is a python dialog box that will stay on top of all other windows until closed. I put it together because I needed something to call from shell scripts that wouldn't go un-noticed if you have a ton of windows open. The dialog can include a `Yes`, `No`, and `Ok` button, along with an icon, title, and of course a message. Additionally, it will play a notification sound when the dialog opens if the python `playsound` module is installed.

A bash script is included which demos everything.

## Motivation

The `zenity` command on Linux is a useful and a well thought-out tool for creating dialog boxes, but I couldn't figure out how to get it to stay on top of other windows and things that I wanted to get notified about kept getting buried under other windows.

## Features

- Creates a standalone modal dialog with specified buttons (Yes, No, Ok).
- Displays an icon next to the text.
- Plays a sound when the dialog opens (requires the `playsound` module).
- Specifiy title and text for the dialog.
- Returns standard GTK constants for the buttons specified.

## Installation

To use this script, you need to have Python 3 and the GTK library installed. Additionally, if you want sound support, you need to install the `playsound` module.

### Prerequisites

- Python 3
- Python GTK library (`python3-gi` package)
- `playsound` module (optional, for sound support)

### Installation Steps

1. Install the GTK library:

```bash
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0
```

2. Install the `playsound` module (optional):

```bash
pip install playsound
```

## Usage

### Command-Line Arguments

- `--yes`: Add a Yes button to the dialog.
- `--no`: Add a No button to the dialog.
- `--ok`: Add an Ok button to the dialog.
- `--icon`: Path to the icon image file.
- `--title`: Title of the dialog window (default: "Dialog").
- `--text`: Text to display in the dialog (default: "").
- `--sound`: Path to the sound file to play when the dialog opens.

### Example

To create a dialog with Yes, No, and Ok buttons, an icon, a title, text, and a sound, you can run the following command:

```bash
python3 standalone_dialog.py --yes --no --ok --icon path/to/icon.png --title "Test Dialog" --text "Click a button to test." --sound path/to/sound.mp3
```

## License

This project is licensed under the GPLv3 License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Acknowledgments

- Inspired by the need for a modal dialog solution on Linux.
- Thanks to the developers of the GTK library and the `playsound` module.
