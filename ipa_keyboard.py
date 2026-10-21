"""The Pronunciation Studio's IPA keyboard and symbol key.

Most of Azure's IPA isn't on a keyboard. ``Keyboard`` is a small pop-out of
every symbol Azure's en-US voice speaks (pronunciation.AZURE_VOWELS and
AZURE_CONSONANTS) plus the stress and syllable marks; a click types the symbol
into whichever IPA box last had focus. ``Guide`` is the key: each symbol with
the English sound it stands for and a word that has it.

Only Azure's own set is offered. Other IPA (ɒ, ɜː, length marks) is still
accepted when typed or pasted -- pronunciation.azure_ipa() converts it -- but
these are the sounds the voice actually makes.
"""

import tkinter as tk
from tkinter import ttk

import pronunciation

# (symbol, sounds like, as in). American values: the house voice is American.
# The examples spell the sound in capitals where the word holds more than it.
VOWELS = (
    ("i",  "ee",            "sEE, machIne"),
    ("ɪ",  "short i",       "sIt, gIve"),
    ("ɛ",  "short e",       "bEd, sAId"),
    ("æ",  "short a",       "cAt, trAp"),
    ("ɑ",  "ah",            "fAther, hOt"),
    ("ɔ",  "aw",            "lAW, cAUght"),
    ("ʊ",  "short oo",      "bOOk, pUt"),
    ("u",  "long oo",       "fOOd, trUE"),
    ("ʌ",  "short u",       "cUp, lOve"),
    ("ə",  "uh (unstressed)", "About, sofA"),
    ("ɚ",  "er (unstressed)", "buttER, suppER"),
    ("ɝ",  "er (stressed)", "fUR, bIRd"),
)
DIPHTHONGS = (
    ("eɪ", "ay",            "sAY, gAte"),
    ("aɪ", "eye",           "mY, rIde"),
    ("ɔɪ", "oy",            "bOY, cOIn"),
    ("aʊ", "ow",            "nOW, hOUse"),
    ("oʊ", "oh",            "gO, bOAt"),
)
CONSONANTS = (
    ("p",  "p",             "Pen"),
    ("b",  "b",             "Bad"),
    ("t",  "t",             "Top"),
    ("d",  "d",             "Dog"),
    ("k",  "k",             "Cat, Kick"),
    ("g",  "hard g",        "Go, biG"),
    ("m",  "m",             "Man"),
    ("n",  "n",             "No"),
    ("ŋ",  "ng",            "siNG, thiNk"),
    ("f",  "f",             "Fan, PHone"),
    ("v",  "v",             "Van"),
    ("θ",  "th (breathed)", "THin, baTH"),
    ("ð",  "th (voiced)",   "THis, moTHer"),
    ("s",  "s",             "Sun, Cell"),
    ("z",  "z",             "Zoo, iS"),
    ("ʃ",  "sh",            "SHip, naTIon"),
    ("ʒ",  "zh",            "meaSure, viSIon"),
    ("h",  "h",             "Hat"),
    ("tʃ", "ch",            "CHurCH"),
    ("dʒ", "j",             "Judge, Gem"),
    ("l",  "l",             "Leg"),
    ("ɹ",  "r",             "Red"),
    ("w",  "w",             "Wet"),
    ("j",  "y  (never j!)", "Yes, Yet"),
)
MARKS = (
    ("ˈ",  "main stress",   "put before the stressed syllable: /ˈmoʊ.zɪz/ MO-zes"),
    ("ˌ",  "lighter stress", "a second, weaker beat: /ˌdʒɛ.ɹə.ˈmaɪ.ə/"),
    (".",  "syllable break", "between syllables: /ˈæ.dəm/"),
)
GROUPS = (("Vowels", VOWELS), ("Diphthongs", DIPHTHONGS),
          ("Consonants", CONSONANTS), ("Marks", MARKS))

KEY_FONT = ("Segoe UI", 14)
PER_ROW = 8


def symbols():
    """Every phone the keyboard offers (marks left out)."""
    return {sym for _, group in GROUPS[:3] for sym, _, _ in group}


def hint(sym, sounds, example):
    return f"{sym}   {sounds} — as in {example}"


class Keyboard:
    """A pop-out row of IPA keys. ``get_target`` returns the Entry to type
    into (or None); ``on_guide`` opens the key."""

    def __init__(self, parent, get_target, on_guide):
        self.get_target = get_target
        self.win = tk.Toplevel(parent)
        self.win.title("IPA keyboard")
        self.win.resizable(False, False)
        self.win.transient(parent)          # stays above the Studio
        frame = ttk.Frame(self.win, padding=8)
        frame.pack(fill="both", expand=True)

        self.hint_var = tk.StringVar(
            value="Click in an IPA box, then click a symbol to type it.")
        r = 0
        for title, group in GROUPS:
            ttk.Label(frame, text=title, font=("Segoe UI", 9, "bold")).grid(
                row=r, column=0, columnspan=PER_ROW, sticky="w", pady=(6, 2))
            r += 1
            for k, (sym, sounds, example) in enumerate(group):
                key = tk.Button(frame, text=sym, font=KEY_FONT, width=3,
                                takefocus=0, command=lambda s=sym: self.type(s))
                key.grid(row=r + k // PER_ROW, column=k % PER_ROW, padx=1, pady=1)
                text = hint(sym, sounds, example)
                key.bind("<Enter>", lambda e, t=text: self.hint_var.set(t))
            r += (len(group) + PER_ROW - 1) // PER_ROW

        bar = ttk.Frame(frame)
        bar.grid(row=r, column=0, columnspan=PER_ROW, sticky="ew", pady=(8, 0))
        ttk.Button(bar, text="⌫", width=4, takefocus=0,
                   command=self.backspace).pack(side="left")
        ttk.Button(bar, text="What do these mean?", takefocus=0,
                   command=on_guide).pack(side="right")
        ttk.Label(frame, textvariable=self.hint_var, foreground="#555",
                  wraplength=PER_ROW * 46).grid(
            row=r + 1, column=0, columnspan=PER_ROW, sticky="w", pady=(6, 0))

    def _target(self):
        ent = self.get_target()
        if ent is None or not ent.winfo_exists():
            self.hint_var.set("Click in an IPA box first.")
            return None
        return ent

    def type(self, sym):
        ent = self._target()
        if ent is None:
            return
        if ent.selection_present():         # typing replaces a selection
            ent.delete("sel.first", "sel.last")
        ent.insert("insert", sym)
        ent.focus_set()

    def backspace(self):
        ent = self._target()
        if ent is None:
            return
        if ent.selection_present():
            ent.delete("sel.first", "sel.last")
        else:
            i = ent.index("insert")
            if i:
                ent.delete(i - 1)
        ent.focus_set()


class Guide:
    """The key: what each of Azure's symbols sounds like to an English ear."""

    def __init__(self, parent):
        self.win = tk.Toplevel(parent)
        self.win.title("IPA key")
        self.win.resizable(False, False)
        frame = ttk.Frame(self.win, padding=10)
        frame.pack(fill="both", expand=True)

        left = ttk.Frame(frame)
        left.grid(row=0, column=0, sticky="n", padx=(0, 24))
        right = ttk.Frame(frame)
        right.grid(row=0, column=1, sticky="n")
        r = self._section(left, 0, "Vowels", VOWELS)
        r = self._section(left, r, "Diphthongs (two vowels glided as one)", DIPHTHONGS)
        self._section(left, r, "Marks", MARKS)
        self._section(right, 0, "Consonants", CONSONANTS)

        ttk.Label(frame, foreground="#555", wraplength=760, justify="left", text=(
            "These are the sounds Azure's American voice makes. Capitals in an "
            "example mark the letters that make the sound. Other IPA you paste in "
            "(ɒ, ɜː, length marks ː) is converted to these automatically, and "
            "syllable breaks are added for you, but writing them in yourself "
            "puts the stress exactly where you mean it.")).grid(
            row=1, column=0, columnspan=2, sticky="w", pady=(10, 0))

    @staticmethod
    def _section(parent, r, title, group):
        ttk.Label(parent, text=title, font=("Segoe UI", 10, "bold")).grid(
            row=r, column=0, columnspan=3, sticky="w", pady=(8, 2))
        r += 1
        for sym, sounds, example in group:
            ttk.Label(parent, text=sym, font=KEY_FONT, width=3).grid(
                row=r, column=0, sticky="w")
            ttk.Label(parent, text=sounds, width=16).grid(row=r, column=1, sticky="w")
            ttk.Label(parent, text=example, foreground="#555").grid(
                row=r, column=2, sticky="w", padx=(6, 0))
            r += 1
        return r


def show(attr_owner, attr, make):
    """Raise the pop-out held in ``attr_owner.attr``, or make it."""
    pop = getattr(attr_owner, attr, None)
    if pop is not None and pop.win.winfo_exists():
        pop.win.deiconify()
        pop.win.lift()
        return pop
    pop = make()
    setattr(attr_owner, attr, pop)
    return pop
