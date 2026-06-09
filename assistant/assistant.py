from typing import Optional

from assistant.commands import AppCommand, find_command, list_commands
from assistant.voice_engine import RecognitionResult, VoiceEngine


class DesktopAssistant:
    """Core assistant logic for handling voice commands."""

    def __init__(self, model_path: Optional[str] = None):
        self.engine = VoiceEngine(model_path=model_path)

    def run_once(self) -> str:
        result = self.engine.listen()
        if not result.text:
            return "I did not hear a command. Please try again."

        command = self.match_command(result.text)
        if not command:
            return f"Command not recognized: {result.text}. Supported commands: {', '.join([cmd.name for cmd in list_commands()])}"

        return self.execute_command(command)

    def match_command(self, text: str) -> Optional[AppCommand]:
        return find_command(text)

    def execute_command(self, command: AppCommand) -> str:
        if not command.safe:
            if not self.confirm_execution(command):
                return f"Canceled action: {command.name}."
        try:
            command.action()
            return f"Opening {command.description}."
        except Exception as exc:
            return f"Failed to launch {command.name}: {exc}"

    def confirm_execution(self, command: AppCommand) -> bool:
        answer = input(f"This action may be unsafe. Confirm execution of {command.name}? (yes/no): ").strip().lower()
        return answer in {"yes", "y"}

    def available_commands(self) -> str:
        return "\n".join(list_commands())
