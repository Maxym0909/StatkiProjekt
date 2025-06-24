import unittest
from game import reset_game_state, Ship  # Import z game.py
from timeit import timeit

class TestGameLogic(unittest.TestCase):
    def setUp(self):
        reset_game_state()
        self.test_ship = Ship((2, 1), (0, 0))

    def test_place_valid_ship(self):
        result = self.test_ship.place((3, 3))
        self.assertTrue(result)
        self.assertTrue(self.test_ship.placed)
        self.assertEqual(len(self.test_ship.cells), 2)

    def test_place_out_of_bounds_ship(self):
        result = self.test_ship.place((9, 9))
        self.assertFalse(result)

    def test_place_overlapping_ship(self):
        self.test_ship.place((2, 2))
        another = Ship((2, 1), (0, 0))
        result = another.place((2, 2))
        self.assertFalse(result)

    def test_place_too_close_ship(self):
        self.test_ship.place((2, 2))
        another = Ship((2, 1), (0, 0))
        result = another.place((3, 2))
        self.assertFalse(result)

    def test_place_ship_performance(self):
        duration = timeit(lambda: Ship((1, 1), (0, 0)).place((0, 0)), number=1000)
        self.assertLess(duration, 0.1)

if __name__ == "__main__":
    unittest.main()