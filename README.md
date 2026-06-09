# Jarvis Local Assistant

A simple local desktop assistant that listens for voice commands and launches applications on your computer.

## What this project does

- Listens for voice commands locally
- Maps recognized commands to installed applications
- Opens Chrome, VS Code, file manager, or terminal
- Includes a small interactive GUI and a CLI mode
- Keeps the code modular and easy to extend

## Files

- `main.py` - entrypoint for CLI or GUI mode
- `assistant/voice_engine.py` - local speech recognition support
- `assistant/commands.py` - app launch mappings and helpers
- `assistant/assistant.py` - core logic for matching and executing commands
- `assistant/gui.py` - minimal Tkinter-based interactive interface
- `requirements.txt` - Python dependency list
- `mem.md` - notes and mistakes to avoid repeating

## Requirements

- Python 3.9+
- Linux desktop with a microphone
- `python3-tk` installed for GUI mode

## Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

If you want the GUI, also install Tkinter:

```bash
sudo apt update
sudo apt install python3-tk
```

## Download a VOSK model

For the best local speech recognition experience, use VOSK.

1. Download a small English model, for example:

```bash
mkdir -p models
cd models
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
```

2. Run the assistant with the model path:

```bash
python3 main.py --model models/vosk-model-small-en-us-0.15
```

If you do not have a VOSK model installed, the project can fall back to PocketSphinx if `speech_recognition` and `pocketsphinx` are available.

## Run the assistant

### CLI mode

```bash
python3 main.py --model models/vosk-model-small-en-us-0.15
```

### Interactive GUI mode

```bash
python3 main.py --gui --model models/vosk-model-small-en-us-0.15
```

### List commands

```bash
python3 main.py --list --model models/vosk-model-small-en-us-0.15
```

## Supported commands

- `open chrome`
- `open vscode`
- `open file manager`
- `open terminal`

## Extending commands

Add a new function to `assistant/commands.py`, then add an entry to `COMMANDS` with keywords and a description.

## Notes

- The assistant runs locally and does not require paid services.
- It asks for confirmation only for actions marked unsafe.
- The GUI is intentionally small and focused on voice command launching.
