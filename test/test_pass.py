import unittest


class TestSuccess(unittest.TestCase):
    """
    Just a dummy test
    """
    def setUp(self) -> None:
        pass

    def test_success(self):
        # print("test_sucess \o/")
        self.assertTrue(True)

    def test_failure(self):
        self.assertFalse(False)


if __name__ == "__main__":
    suite = unittest.makeSuite(TestSuccess)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        exit(0)
    else:
        exit(1)