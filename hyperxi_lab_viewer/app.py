from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from .state import HyperXiState
from .transport import Flag, orbit_length, summary
from .transport import Flag, orbit_length, summary


class HyperXILabViewerApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("hyperxi_lab_viewer")
        self.root.geometry("1200x720")
        self.root.minsize(900, 560)

        self.state = HyperXiState()

        self.tree: ttk.Treeview | None = None
        self.main_title_var = tk.StringVar(value="Main View")
        self.main_body_var = tk.StringVar(value="Select an object from the explorer.")
        self.report_console: ScrolledText | None = None
        self.main_content_frame: ttk.Frame | None = None
        self.word_var = tk.StringVar(value=self.state.default_word)
        self.word_result_var = tk.StringVar(value="Select Word Explorer to run a transport word.")

        self._configure_style()
        self._build_ui()
        self._render_text_view(self.main_body_var.get())
        self._populate_tree()
        self._boot_log()

    def _configure_style(self) -> None:
        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")

    def _build_ui(self) -> None:
        outer = ttk.Frame(self.root, padding=10)
        outer.pack(fill="both", expand=True)

        header = ttk.Frame(outer)
        header.pack(fill="x", pady=(0, 10))

        title = ttk.Label(
            header,
            text="hyperxi_lab_viewer",
            font=("TkDefaultFont", 18, "bold"),
        )
        title.pack(anchor="w")

        subtitle = ttk.Label(
            header,
            text="HyperXi transport, Petrie structure, and chamber-graph exploration",
        )
        subtitle.pack(anchor="w", pady=(2, 0))

        panes = ttk.Panedwindow(outer, orient=tk.HORIZONTAL)
        panes.pack(fill="both", expand=True)

        left = ttk.Frame(panes, padding=8)
        center = ttk.Frame(panes, padding=8)
        right = ttk.Frame(panes, padding=8)

        panes.add(left, weight=1)
        panes.add(center, weight=3)
        panes.add(right, weight=2)

        self._build_left_pane(left)
        self._build_center_pane(center)
        self._build_right_pane(right)

        status = ttk.Frame(outer)
        status.pack(fill="x", pady=(10, 0))

        self.status_var = tk.StringVar(value="Ready.")
        status_label = ttk.Label(status, textvariable=self.status_var)
        status_label.pack(anchor="w")

    def _build_left_pane(self, parent: ttk.Frame) -> None:
        label = ttk.Label(parent, text="Object Explorer", font=("TkDefaultFont", 11, "bold"))
        label.pack(anchor="w", pady=(0, 8))

        tree = ttk.Treeview(parent, show="tree", selectmode="browse")
        tree.pack(fill="both", expand=True)
        tree.bind("<<TreeviewSelect>>", self._on_tree_select)
        self.tree = tree

    def _build_center_pane(self, parent: ttk.Frame) -> None:
        label = ttk.Label(parent, text="Main View", font=("TkDefaultFont", 11, "bold"))
        label.pack(anchor="w", pady=(0, 8))

        card = ttk.Frame(parent, padding=16, relief="ridge")
        card.pack(fill="both", expand=True)

        main_title = ttk.Label(
            card,
            textvariable=self.main_title_var,
            font=("TkDefaultFont", 16, "bold"),
        )
        main_title.pack(anchor="w", pady=(0, 12))

        content = ttk.Frame(card)
        content.pack(fill="both", expand=True)

        self.main_content_frame = content

        main_body = ttk.Label(
            content,
            textvariable=self.main_body_var,
            justify="left",
            wraplength=520,
        )
        main_body.pack(anchor="w")

    def _build_right_pane(self, parent: ttk.Frame) -> None:
        label = ttk.Label(parent, text="Report Console", font=("TkDefaultFont", 11, "bold"))
        label.pack(anchor="w", pady=(0, 8))

        console = ScrolledText(parent, wrap="word", height=20)
        console.pack(fill="both", expand=True)
        console.configure(state="disabled")
        self.report_console = console

    def _populate_tree(self) -> None:
        assert self.tree is not None

        root = self.tree.insert("", "end", text="HyperXi", open=True)

        model = self.tree.insert(root, "end", text="Model", open=True)
        self.tree.insert(model, "end", text="Cell")
        self.tree.insert(model, "end", text="Flags")
        self.tree.insert(model, "end", text="Generators")

        transport = self.tree.insert(root, "end", text="Transport", open=True)
        self.tree.insert(transport, "end", text="Petrie Cycles")
        self.tree.insert(transport, "end", text="Orbit Scan")
        self.tree.insert(transport, "end", text="Word Explorer")

        quotient = self.tree.insert(root, "end", text="Quotient", open=True)
        self.tree.insert(quotient, "end", text="Thalions")
        self.tree.insert(quotient, "end", text="Chamber Graph")

        analysis = self.tree.insert(root, "end", text="Analysis", open=True)
        self.tree.insert(analysis, "end", text="Invariants")
        self.tree.insert(analysis, "end", text="Spectrum")
        self.tree.insert(analysis, "end", text="Antipodes")

    def _boot_log(self) -> None:
        self.log("HyperXi Lab Viewer v0.1")
        self.log("--------------------------------")

        for line in self.state.summary():
            self.log(line)

        self.log("")
        self.log("Lab shell initialized.")
        self.log("")
        self.log("Next:")
        self.log("- transport kernel")
        self.log("- Petrie cycle explorer")
        self.log("- chamber graph inspector")
        self.status_var.set("Lab initialized.")

    def _on_tree_select(self, event: tk.Event) -> None:
        if self.tree is None:
            return

        selection = self.tree.selection()
        if not selection:
            return

        item_id = selection[0]
        label = self.tree.item(item_id, "text")

        handled = self._handle_special_view(label)
        if not handled:
            self.main_title_var.set(label)
            self._render_text_view(self._describe_node(label))

        self.log(f"Selected: {label}")
        self.status_var.set(f"Viewing: {label}")

    def _describe_node(self, label: str) -> str:
        descriptions = {
            "HyperXi": "Top-level lab namespace for transport, quotient, and graph analysis.",
            "Model": "Core mathematical objects and incidence structures.",
            "Cell": "Canonical dodecahedral cell model and incidence relations.",
            "Flags": "Lifted flag states, typically represented as (v, e, f).",
            "Generators": "Local moves such as S, F, and V acting on lifted flags.",
            "Transport": "Word dynamics and local motion through the lifted state space.",
            "Petrie Cycles": "Petrie transport classes and decagon traversals.",
            "Orbit Scan": "Cycle decomposition and orbit summaries for chosen words.",
            "Word Explorer": "Interactive application of words in the transport generators.",
            "Quotient": "Chamber reduction and Petrie-based quotient structures.",
            "Thalions": "Quotient chamber objects induced by the transport system.",
            "Chamber Graph": "The 60-vertex graph induced by chamber adjacencies.",
            "Analysis": "Invariant and structural diagnostics.",
            "Invariants": "Counts, shells, triangles, degree, diameter, and related data.",
            "Spectrum": "Adjacency eigenvalues and multiplicities.",
            "Antipodes": "Distance-6 structure and unique antipodal behavior.",
        }
        return descriptions.get(label, "No description available yet.")

    def _clear_main_content(self) -> None:
        if self.main_content_frame is None:
            return

        for child in self.main_content_frame.winfo_children():
            child.destroy()


    def _handle_special_view(self, label: str) -> bool:
        if label == "Word Explorer":
            self.main_title_var.set("Word Explorer")
            self._render_word_explorer()
            self._run_word_explorer()
            return True

        return False

    def _render_text_view(self, body: str) -> None:
        self._clear_main_content()

        if self.main_content_frame is None:
            return

        main_body = ttk.Label(
            self.main_content_frame,
            text=body,
            justify="left",
            wraplength=520,
        )
        main_body.pack(anchor="w")

    def _render_word_explorer(self) -> None:
        self._clear_main_content()

        if self.main_content_frame is None:
            return

        controls = ttk.Frame(self.main_content_frame)
        controls.pack(anchor="w", fill="x", pady=(0, 12))

        word_label = ttk.Label(controls, text="Word:")
        word_label.pack(side="left")

        word_entry = ttk.Entry(controls, textvariable=self.word_var, width=20)
        word_entry.pack(side="left", padx=(8, 8))
        word_entry.bind("<Return>", self._on_run_word)

        run_button = ttk.Button(controls, text="Run", command=self._run_word_explorer)
        run_button.pack(side="left")

        result = ttk.Label(
            self.main_content_frame,
            textvariable=self.word_result_var,
            justify="left",
            wraplength=520,
        )
        result.pack(anchor="w")

        word_entry.focus_set()

    def _on_run_word(self, event: tk.Event) -> None:
        self._run_word_explorer()

    def _run_word_explorer(self) -> None:
        word = self.word_var.get().strip().upper()
        seed = Flag(face=0, slot=0, orient=0)

        try:
            lines = [
                f"seed: {seed}",
                "",
                *summary(word),
                f"orbit length from seed: {orbit_length(seed, word)}",
            ]
            self.word_result_var.set("\n".join(lines))

            self.log("")
            self.log("[word explorer]")
            self.log(f"word: {word}")
            self.log(f"seed: {seed}")
            self.log(f"orbit length from seed: {orbit_length(seed, word)}")

            self.status_var.set(f"Viewing: Word Explorer ({word})")
        except Exception as exc:
            self.word_result_var.set(f"Error: {exc}")
            self.log("")
            self.log("[word explorer error]")
            self.log(f"word: {word}")
            self.log(f"error: {exc}")
            self.status_var.set("Word Explorer error")


    def log(self, message: str) -> None:
        if self.report_console is None:
            return

        self.report_console.configure(state="normal")
        self.report_console.insert("end", message + "\n")
        self.report_console.see("end")
        self.report_console.configure(state="disabled")

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    app = HyperXILabViewerApp()
    app.run()
