from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


class HyperXILabViewerApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("hyperxi_lab_viewer")
        self.root.geometry("1200x720")
        self.root.minsize(900, 560)

        self.tree: ttk.Treeview | None = None
        self.main_title_var = tk.StringVar(value="Main View")
        self.main_body_var = tk.StringVar(value="Select an object from the explorer.")
        self.report_console: ScrolledText | None = None

        self._configure_style()
        self._build_ui()
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

        main_body = ttk.Label(
            card,
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
        self.log("Lab shell initialized.")
        self.log("Explorer loaded.")
        self.log("Main view ready.")
        self.log("Report console ready.")
        self.log("")
        self.log("Planned next:")
        self.log("- state model")
        self.log("- transport kernel")
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

        self.main_title_var.set(label)
        self.main_body_var.set(self._describe_node(label))
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
