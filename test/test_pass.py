import unittest


class TestSuccess(unittest.TestCase):
    """
    Just a dummy test
    """
    def setUp(self) -> None:
        pass

    def test_success(self) -> None:
        self.assertTrue(True)

    def test_failure(self) -> None:
        self.assertFalse(False)


if __name__ == "__main__":
    suite = unittest.makeSuite(TestSuccess)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
