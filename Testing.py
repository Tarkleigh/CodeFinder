import unittest
import CodeFinder


class ParserTests(unittest.TestCase):
    """Test class for CodeFinder.py."""

    def test_find_label(self):
        testString = "cardgen/src/main/java"
        label = CodeFinder.find_label(testString)
        self.assertEqual("cardgen", label)


if __name__ == '__main__':
    unittest.main()
