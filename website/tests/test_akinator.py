import unittest

from controllers.akinator import *


class TestAkinator(unittest.TestCase):

    def setUp(self):
        self.questions = {
            0: 'Is your character fictional',
            1: 'Is your character yellow',
            2: 'Is your character bald',
            3: 'Is your character a man',
            4: 'Is your character short',
            5: 'Is your character blonde'
        }

        self.characters = {
            0: {'name': 'Homer Simpson', 'answers': {0: 1, 1: 1, 2: 1, 3: 1, 4: 0, 5: 0.25}},
            1: {'name': 'SpongeBob', 'answers': {0: 1, 1: 1, 2: 1, 3: 1, 4: 0.75, 5: 0.25}},
            2: {'name': 'Sandy Cheeks', 'answers': {0: 1, 1: 0, 2: 0, 3: 0, 5: 0}},
        }

    def test_supported_characters(self):
        chars = supported_characters()
        self.assertIsInstance(chars, list)
        self.assertTrue(all(isinstance(char, str) for char in chars))
        self.assertNotIn('', chars)
        self.assertNotIn(None, chars)
        self.assertTrue(all([len(char) > 0 for char in chars]))

    def test_calculate_posterior(self):
        Priori((np.array([0.333, 0.333, 0.333]), np.array([0.667, 0.667, 0.667])))

    def test_bayes(self):
        Posterior((np.array([1, 0, 0.5]), np.array([0, 0.5, 1])))


if __name__ == '__main__':
    unittest.main()
