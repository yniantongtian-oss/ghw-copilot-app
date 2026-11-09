# Copilot log

This game was built with **GitHub Copilot CLI** (`@github/copilot` v1.0.107, run as `copilot -p "<prompt>"` on 2026-11-09, Asia/Singapore time) under the GitHub account `yniantongtian-oss`. Copilot wrote all the code, tests, README, and devcontainer. I checked each step by running the tests and playing the game myself.

Copilot was allowed to write files and run `python3`, `ls`, and `cat` only. Git was denied.

## Prompt 1: build the app

> Build a small command-line "choose your own adventure" game in Python 3 (standard library only). Theme: a student lost in a campus optics lab the night before a hackathon deadline. Requirements: story stored as a data structure (dict of scenes with text and numbered choices), at least 8 scenes and 3 different endings (good, bad, secret), an inventory that changes some choices, input validation, a "q" to quit, and a --seed option is not needed. Put the game in adventure.py with a main() function, add tests in test_adventure.py using unittest that check every choice points to an existing scene and every ending is reachable, and a README.md with how to run it. Do not use git and do not access the network. After writing, run: python3 -m unittest -v

### Copilot output (trimmed transcript)

```text
 / Search "**/*" No matches found

 $ Shell Inspect project files 4 lines…
   pwd && find . -maxdepth 2 -type f -print

 ● Edit  Create adventure.py (+182)  Create test_adventure.py (+75)  Create README.md (+20)

 $ Shell Run the requested unittest suite 10 lines…
   python3 -m unittest -v

 ● Edit  Edit test_adventure.py (+2 -2)

 $ Shell Rerun the unittest suite after final edits 10 lines…
   python3 -m unittest -v

Implemented the campus optics lab adventure in `adventure.py`, with inventory-gated choices, input validation, and `q` to quit. Added `test_adventure.py` and run instructions in `README.md`.

`python3 -m unittest -v` passes all 5 tests.



Changes    +279 -2
AI Credits 0.39 (51s)
Tokens     ↑ 101.6k (92.8k cached, 8.8k written) • ↓ 3.7k (913 reasoning)
```

## Prompt 2: renumber choices and add a Codespaces devcontainer

> Two improvements: (1) When an inventory-gated choice is hidden, the menu currently shows gaps like "1." then "3." — renumber the visible choices consecutively (1, 2, 3...) while still mapping to the right scene, and add a unittest for this. (2) For the GitHub Codespaces challenge, add a .devcontainer/devcontainer.json using the image mcr.microsoft.com/devcontainers/python:3.12 with the ms-python.python extension and a postCreateCommand that runs the tests. Also add a .gitignore for Python. Do not use git or the network. Then run: python3 -m unittest -v

### Copilot output (trimmed transcript)

```text
 PY Read adventure.py 182 lines read

 PY Read test_adventure.py 75 lines read

 MD Read README.md 20 lines read

 $ Shell List project files 5 lines…
   find . -maxdepth 3 -type f -not -path './.git/*' -print

 ● Edit  Edit adventure.py (+5 -3)  Edit test_adventure.py (+15)  Create .devcontainer/devcontainer…

 $ Shell Run the complete unittest suite 11 lines…
   python3 -m unittest -v

Visible choices are now numbered consecutively, with each number still selecting its corresponding scene. Added a unittest for the hidden-choice case, Python Codespaces configuration, and a Python `.gitignore`.

`python3 -m unittest -v` passed all 6 tests. No Git or network commands were used.



Changes    +61 -3
AI Credits 0.25 (22s)
Tokens     ↑ 82.1k (73.5k cached, 8.5k written) • ↓ 1.4k (472 reasoning)
```

## Human verification

- `python3 -m unittest -v`: 6 tests pass.
- I played the game by hand. Hidden choices are now renumbered 1, 2, … with no gaps.
- `.devcontainer/devcontainer.json` uses `mcr.microsoft.com/devcontainers/python:3.12` and runs the tests on create.
