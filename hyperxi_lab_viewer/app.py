from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class HyperXILabViewerApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("hyperxi_lab_viewer")
        self.root.geometry("720x420")
        self._build_ui()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=16)
        frame.pack(fill="both", expand=True)

        title = ttk.Label(
            frame,
            text="hyperxi_lab_viewer",
            font=("TkDefaultFont", 18, "bold"),
        )
        title.pack(anchor="w", pady=(0, 8))

        subtitle = ttk.Label(
            frame,
            text="Hello world. Lab scaffold is alive.",
        )
        subtitle.pack(anchor="w", pady=(0, 16))

        status = ttk.Label(
            frame,
            text="Next: transport kernel + chamber graph explorer.",
        )
        status.pack(anchor="w")

        quit_button = ttk.Button(frame, text="Quit", command=self.root.destroy)
        quit_button.pack(anchor="w", pady=(24, 0))

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    app = HyperXILabViewerApp()
    app.run()
