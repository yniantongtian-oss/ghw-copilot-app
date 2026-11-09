"""A small, choice-driven campus adventure."""

STORY = {
    "entrance": {
        "text": (
            "It's the night before the hackathon deadline, and you've somehow "
            "gotten lost in the campus optics lab. The lobby is quiet except "
            "for a blinking security panel."
        ),
        "choices": [
            {"number": 1, "text": "Follow the dim hallway.", "next": "corridor"},
            {"number": 2, "text": "Check the unattended reception desk.", "next": "reception"},
            {"number": 3, "text": "Take the freight stairs down.", "next": "stairwell"},
        ],
    },
    "reception": {
        "text": (
            "Under a stack of lab forms you find a visitor badge. A hand-drawn "
            "map points toward the optics wing."
        ),
        "choices": [
            {
                "number": 1,
                "text": "Take the badge and head into the hallway.",
                "next": "corridor",
                "gives": "lab badge",
            },
            {"number": 2, "text": "Ignore the map and try the freight stairs.", "next": "stairwell"},
        ],
    },
    "corridor": {
        "text": (
            "The hallway splits. A red light glows over a badge reader; a "
            "darkroom door stands ajar across from it."
        ),
        "choices": [
            {"number": 1, "text": "Slip into the darkroom.", "next": "darkroom"},
            {
                "number": 2,
                "text": "Use your badge at the reader.",
                "next": "optics_hall",
                "requires": "lab badge",
            },
            {"number": 3, "text": "Look for a way through the freight stairs.", "next": "stairwell"},
        ],
    },
    "darkroom": {
        "text": (
            "On a workbench, a small glass prism catches the glow of an "
            "instrument display. It might be useful for the laser setup."
        ),
        "choices": [
            {"number": 1, "text": "Pocket the prism and return to the hallway.", "next": "corridor", "gives": "prism"},
            {"number": 2, "text": "Leave it and return to the hallway.", "next": "corridor"},
        ],
    },
    "stairwell": {
        "text": (
            "The stairwell door slams behind you. The emergency lights fail, "
            "and the security system locks the lab for the night."
        ),
        "ending": "bad",
    },
    "optics_hall": {
        "text": (
            "You reach the optics hall. A laser bench hums beside a service "
            "panel, and a beam makes a strange pattern on the wall."
        ),
        "choices": [
            {
                "number": 1,
                "text": "Use the prism to trace the strange reflection.",
                "next": "secret_ending",
                "requires": "prism",
            },
            {"number": 2, "text": "Follow the equipment cables.", "next": "server_bay"},
            {"number": 3, "text": "Try to calibrate the laser.", "next": "alignment"},
        ],
    },
    "server_bay": {
        "text": (
            "The cables lead to a terminal with the hackathon build still "
            "running. Its status says the final test is waiting on one optical "
            "calibration."
        ),
        "choices": [
            {"number": 1, "text": "Go to the laser bench.", "next": "alignment"},
            {"number": 2, "text": "Head back to the optics hall.", "next": "optics_hall"},
        ],
    },
    "alignment": {
        "text": (
            "The laser is out of alignment. You can carefully adjust the "
            "mount, or force the old controls and hope for the best."
        ),
        "choices": [
            {
                "number": 1,
                "text": "Use the prism to align the beam precisely.",
                "next": "hackathon_room",
                "requires": "prism",
            },
            {"number": 2, "text": "Force the controls and run the test.", "next": "bad_test_ending"},
            {"number": 3, "text": "Return to the optics hall.", "next": "optics_hall"},
        ],
    },
    "hackathon_room": {
        "text": (
            "The calibration clicks into place. The build passes, and you "
            "make it back to the hackathon room just as the deadline arrives."
        ),
        "ending": "good",
    },
    "bad_test_ending": {
        "text": (
            "The beam scorches a sensor. The lab alarms sound, and your "
            "unfinished build won't be ready by the deadline."
        ),
        "ending": "bad",
    },
    "secret_ending": {
        "text": (
            "The prism reveals a hidden alignment mark and a tiny service "
            "passage. Behind it is the lab's original optical prototype—and "
            "the missing calibration file for your project. You found the "
            "secret shortcut to a working submission."
        ),
        "ending": "secret",
    },
}


def available_choices(scene, inventory):
    """Return choices whose required items are present."""
    return [
        choice
        for choice in scene.get("choices", [])
        if choice.get("requires") is None or choice["requires"] in inventory
    ]


def play(input_fn=input, output_fn=print):
    """Play the adventure until an ending or the player quits."""
    current = "entrance"
    inventory = set()

    while True:
        scene = STORY[current]
        output_fn(f"\n{scene['text']}")
        if scene.get("ending"):
            output_fn(f"Ending: {scene['ending']}")
            return

        if inventory:
            output_fn(f"Inventory: {', '.join(sorted(inventory))}")

        choices = available_choices(scene, inventory)
        for number, choice in enumerate(choices, start=1):
            output_fn(f"{number}. {choice['text']}")

        valid_numbers = {
            str(number): choice for number, choice in enumerate(choices, start=1)
        }
        while True:
            answer = input_fn("Choose a number (or q to quit): ").strip().lower()
            if answer == "q":
                output_fn("You quit the adventure.")
                return
            if answer in valid_numbers:
                choice = valid_numbers[answer]
                break
            output_fn("Invalid choice. Enter one of the listed numbers or q.")

        if "gives" in choice:
            inventory.add(choice["gives"])
        current = choice["next"]


def main():
    play()


if __name__ == "__main__":
    main()
