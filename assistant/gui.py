import threading
import tkinter as tk
from tkinter import messagebox

from assistant.assistant import DesktopAssistant


class AssistantGUI:
    """Simple interactive GUI for the local desktop assistant."""

    def __init__(self, model_path: str = None):
        self.assistant = DesktopAssistant(model_path=model_path)
        self.root = tk.Tk()
        self.root.title("Jarvis Local Assistant")
        self.root.geometry("420x260")
        self._build_ui()

    def _build_ui(self) -> None:
        title = tk.Label(self.root, text="Local Voice App Launcher", font=("Arial", 14, "bold"))
        title.pack(pady=(12, 6))

        self.status_label = tk.Label(self.root, text="Ready. Click Listen and speak a command.", wraplength=380)
        self.status_label.pack(pady=(0, 12))

        listen_button = tk.Button(self.root, text="Listen", command=self._start_listen, width=20)
        listen_button.pack(pady=6)

        commands_frame = tk.Frame(self.root)
        commands_frame.pack(pady=(12, 0), fill="both", expand=True)

        tk.Label(commands_frame, text="Supported commands:", anchor="w").pack(fill="x")
        commands_text = tk.Text(commands_frame, height=6, width=50, padx=6, pady=6)
        commands_text.insert("1.0", self.assistant.available_commands())
        commands_text.configure(state="disabled")
        commands_text.pack(fill="both", expand=True)

    def _start_listen(self) -> None:
        self.status_label.config(text="Listening... speak now.")
        thread = threading.Thread(target=self._listen_command, daemon=True)
        thread.start()

    def _listen_command(self) -> None:
        try:
            response = self.assistant.run_once()
        except Exception as exc:
            response = f"Error: {exc}"
        self.root.after(0, lambda: self.status_label.config(text=response))

    def run(self) -> None:
        self.root.mainloop()
