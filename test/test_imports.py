import unittest

from model.imports import check_imports


class TestImports(unittest.TestCase):
    """
    Just a dummy test
    """
    def setUp(self) -> None:
        pass

    def test_imports(self) -> None:
        result = check_imports()
        self.assertTrue(result)


if __name__ == "__main__":
    suite = unittest.makeSuite(TestImports)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
