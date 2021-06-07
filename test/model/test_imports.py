import unittest

from model.imports import check_if_lower_version, check_imports


class TestImports(unittest.TestCase):
    """
    Just a dummy test
    """
    def setUp(self) -> None:
        pass

    #useless because the test depend of the user
    """
    def test_imports(self) -> None:
        result = check_imports()
        self.assertTrue(result)
    """
    def test_true_check_if_lower_version(self):
        res = check_if_lower_version("1.5.17")
        self.assertTrue(res)

    def test_false_check_if_lower_version(self):
        res = check_if_lower_version("1.6.2")
        self.assertFalse(res)


if __name__ == "__main__":
    suite = unittest.makeSuite(TestImports)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
