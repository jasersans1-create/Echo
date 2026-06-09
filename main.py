import argparse
import sys

from assistant.gui import AssistantGUI
from assistant.assistant import DesktopAssistant


def main() -> int:
    parser = argparse.ArgumentParser(description="Jarvis Local Assistant: launch apps with voice commands.")
    parser.add_argument("--gui", action="store_true", help="Run the interactive GUI.")
    parser.add_argument("--model", type=str, default=None, help="Path to the VOSK model directory.")
    parser.add_argument("--list", action="store_true", help="List supported commands and exit.")
    args = parser.parse_args()

    if args.list:
        assistant = DesktopAssistant(model_path=args.model)
        print("Supported commands:\n" + assistant.available_commands())
        return 0

    if args.gui:
        try:
            gui = AssistantGUI(model_path=args.model)
            gui.run()
            return 0
        except Exception as exc:
            print(f"Failed to start GUI: {exc}")
            return 1

    try:
        assistant = DesktopAssistant(model_path=args.model)
        print("Jarvis Local Assistant is ready. Speak a command when prompted.")
        response = assistant.run_once()
        print(response)
    except Exception as exc:
        print(f"Error: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
