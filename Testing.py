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

    def test_get_fully_qualified_name(self):
        expected_name = "org.tarkleigh.Finder"
        current_path = ("home" + os.sep + "user" + os.sep + "development" + os.sep + "codefinder" + os.sep
                        + "main" + os.sep + "src" + os.sep + "java" + os.sep + "org" + os.sep + "tarkleigh" + os.sep + "Finder.java")
        qualified_name = CodeFinder.get_fully_qualified_name(current_path)
        self.assertEqual(expected_name, qualified_name)

    def test_get_fully_qualified_name_without_package_marker(self):
        current_path = ("home" + os.sep + "user" + os.sep + "development" + os.sep + "codefinder" + os.sep
                        + "main" + os.sep + "src" + os.sep + "org" + os.sep + "tarkleigh" + os.sep + "Finder.java")
        qualified_name = CodeFinder.get_fully_qualified_name(current_path)
        self.assertEqual(current_path, qualified_name)


if __name__ == '__main__':
    unittest.main()
