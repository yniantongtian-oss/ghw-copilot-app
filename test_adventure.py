import unittest
from unittest.mock import patch

import adventure


class StoryStructureTests(unittest.TestCase):
    def test_every_choice_points_to_an_existing_scene(self):
        for scene_name, scene in adventure.STORY.items():
            for choice in scene.get("choices", []):
                with self.subTest(scene=scene_name, choice=choice["number"]):
                    self.assertIn(choice["next"], adventure.STORY)

    def test_every_ending_is_reachable(self):
        pending = [("entrance", frozenset())]
        visited = set()
        reachable_endings = set()

        while pending:
            scene_name, inventory = pending.pop()
            state = (scene_name, inventory)
            if state in visited:
                continue
            visited.add(state)
            scene = adventure.STORY[scene_name]
            if "ending" in scene:
                reachable_endings.add(scene["ending"])
                continue

            for choice in adventure.available_choices(scene, inventory):
                next_inventory = set(inventory)
                if "gives" in choice:
                    next_inventory.add(choice["gives"])
                pending.append((choice["next"], frozenset(next_inventory)))

        self.assertTrue({"good", "bad", "secret"}.issubset(reachable_endings))


class GameplayTests(unittest.TestCase):
    def test_inventory_unlocks_choices(self):
        corridor = adventure.STORY["corridor"]
        self.assertNotIn(
            "optics_hall",
            [choice["next"] for choice in adventure.available_choices(corridor, set())],
        )
        self.assertIn(
            "optics_hall",
            [
                choice["next"]
                for choice in adventure.available_choices(corridor, {"lab badge"})
            ],
        )

    def test_invalid_input_reprompts_and_q_quits(self):
        answers = iter(["not a number", "q"])
        output = []

        adventure.play(input_fn=lambda _prompt: next(answers), output_fn=output.append)

        self.assertTrue(any("Invalid choice" in line for line in output))
        self.assertEqual(output[-1], "You quit the adventure.")

    def test_hidden_choice_is_renumbered_and_keeps_its_destination(self):
        answers = iter(["1", "2"])
        output = []

        adventure.play(input_fn=lambda _prompt: next(answers), output_fn=output.append)

        self.assertIn("1. Slip into the darkroom.", output)
        self.assertIn(
            "2. Look for a way through the freight stairs.", output
        )
        self.assertNotIn(
            "3. Look for a way through the freight stairs.", output
        )
        self.assertIn("Ending: bad", output)

    def test_collecting_prism_reaches_good_ending(self):
        # Take the badge at reception, collect the prism, then use both to
        # reach the calibrated hackathon room.
        answers = iter(["2", "1", "1", "1", "2", "3", "1"])
        output = []

        adventure.play(input_fn=lambda _prompt: next(answers), output_fn=output.append)

        self.assertIn("Ending: good", output)


if __name__ == "__main__":
    unittest.main()
