from __future__ import annotations

from .transport import FACE_COUNT, FACE_SIZE, FLAG_COUNT


class HyperXiState:
    """
    Minimal lab state describing the core HyperXi system.
    """

    def __init__(self) -> None:
        self.cell_name = "dodecahedron"
        self.face_count = FACE_COUNT
        self.face_size = FACE_SIZE
        self.flags = FLAG_COUNT
        self.thalions = 60
        self.chamber_degree = 4
        self.default_word = "FSF"
        self.petrie_word = "SV"

    def summary(self) -> list[str]:
        return [
            f"cell: {self.cell_name}",
            f"faces: {self.face_count}",
            f"face size: {self.face_size}",
            f"flags: {self.flags}",
            f"thalions: {self.thalions}",
            f"chamber graph degree: {self.chamber_degree}",
            f"default word: {self.default_word}",
            f"petrie word: {self.petrie_word}",
        ]
