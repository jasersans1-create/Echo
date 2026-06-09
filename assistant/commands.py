import os
import shutil
import subprocess
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional


@dataclass
class AppCommand:
    name: str
    description: str
    keywords: List[str]
    action: Callable[[], None]
    safe: bool = True


def _find_executable(names: List[str]) -> Optional[str]:
    for name in names:
        path = shutil.which(name)
        if path:
            return path
    return None


def _run_process(command: List[str]) -> None:
    try:
        subprocess.Popen(command)
        print(f"[launcher] Launched: {' '.join(command)}")
    except Exception as exc:
        raise RuntimeError(f"Unable to launch {' '.join(command)}: {exc}")

def open_chrome() -> None:
    browser = _find_executable([
        "google-chrome-stable",
        "google-chrome",
        "chrome",
        "chromium",
        "chromium-browser",
        "brave-browser",
        "firefox",
    ])
    if browser:
        _run_process([browser])
        return
    raise RuntimeError("Chrome or a compatible browser was not found on this system.")



def open_vscode() -> None:
    code = _find_executable(["code", "code-insiders"])
    if code:
        _run_process([code])
        return
    raise RuntimeError("VS Code was not found. Install it or add 'code' to your PATH.")


def open_file_manager() -> None:
    if _find_executable(["xdg-open"]):
        _run_process(["xdg-open", os.path.expanduser("~")])
        return

    file_manager = _find_executable(["nautilus", "thunar", "dolphin", "pcmanfm", "caja"])
    if file_manager:
        _run_process([file_manager, os.path.expanduser("~")])
        return

    raise RuntimeError("No file manager command was found on this system.")


def open_terminal() -> None:
    terminal = _find_executable([
        "gnome-terminal",
        "konsole",
        "xfce4-terminal",
        "tilix",
        "xterm",
        "kitty",
        "alacritty",
    ])
    if terminal:
        _run_process([terminal])
        return
    raise RuntimeError("No terminal application was found on this system.")

def open_minecraft() -> None:
    _run_process(["bash", "-lc", "prime-run sklauncher"])

COMMANDS: Dict[str, AppCommand] = {
    "chrome": AppCommand(
        name="chrome",
        description="Open the Chrome browser",
        keywords=["chrome", "google chrome", "browser"],
        action=open_chrome,
    ),
    "vscode": AppCommand(
        name="vscode",
        description="Open Visual Studio Code",
        keywords=["vscode", "visual studio code", "code"],
        action=open_vscode,
    ),
    "file_manager": AppCommand(
        name="file_manager",
        description="Open the file manager",
        keywords=["file manager", "files", "folders", "explorer"],
        action=open_file_manager,
    ),
    "terminal": AppCommand(
        name="terminal",
        description="Open the terminal",
        keywords=["terminal", "console", "shell"],
        action=open_terminal,
    ),
    
    "minecraft": AppCommand(
        name="minecraft",
        description="Launch Minecraft",
        keywords=[
    "minecraft",
    "mine craft",
    "mc",
    "minecroft",
    "mind craft",
    "minecart",
    "play minecraft",
    "open minecraft",
    "launch minecraft",
],
        action=open_minecraft,
    )
}


def find_command(text: str) -> Optional[AppCommand]:
    normalized = text.strip().lower()

    aliases = {
        "rome": "chrome",
        "google": "chrome",
        "google chrome": "chrome",

        "vs code": "vscode",
        "visual studio code": "vscode",

        "files": "file manager",
        "folders": "file manager",

        "console": "terminal",
        "shell": "terminal",
  "mine craft": "minecraft",
    "mincraft": "minecraft",
    "minecraft": "minecraft",
    "minecart": "minecraft",
    "mine shaft": "minecraft",
    "mind craft": "minecraft",
    "my craft": "minecraft",
    "main craft": "minecraft",
    "minecroft": "minecraft",
    "mine croft": "minecraft",
    "minecraft game": "minecraft",
    "mc": "minecraft",
    "m c": "minecraft",
    "launch minecraft": "minecraft",
    "open minecraft": "minecraft",
    "play minecraft": "minecraft",
    "start minecraft": "minecraft",
    "start mc": "minecraft",
    "open mc": "minecraft",
    "go minecraft": "minecraft",
    "minecraft launcher": "minecraft",
    "launch mc": "minecraft",
    "play mc": "minecraft",
    }

    normalized = aliases.get(normalized, normalized)

    for command in COMMANDS.values():
        if any(keyword in normalized for keyword in command.keywords):
            return command

    return None

def list_commands() -> List[str]:
    return [f"{cmd.name}: {cmd.description}" for cmd in COMMANDS.values()]
