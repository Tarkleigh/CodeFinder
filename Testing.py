import os
import unittest
import CodeFinder


class ParserTests(unittest.TestCase):
    """Test class for CodeFinder.py."""

    def test_find_label_with_src_folder(self):
        test_directory_path = "finder" + os.sep + "src"
        label = CodeFinder.find_label(test_directory_path)
        self.assertEqual("finder", label)

    def test_find_label_without_src_folder(self):
        test_directory_path = "finder" + os.sep + "main" + os.sep + "java"
        label = CodeFinder.find_label(test_directory_path)
        self.assertEqual("java", label)

    def test_find_label_without_separator(self):
        test_directory_path = "finder"
        label = CodeFinder.find_label(test_directory_path)
        self.assertEqual("finder", label)


if __name__ == '__main__':
    unittest.main()
