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

    def test_convert_found_data_to_csv(self):
        data_to_concert = dict()
        source_label = "Cardgen"
        target_label = "Codefinder"

        first_dependency = "XMLParser"
        second_dependency = "CardGen"

        first_usage = "Main"
        second_usage = "InputReader"
        third_usage = "OutputWriter"

        data_to_concert[first_dependency] = [first_usage, second_usage]
        data_to_concert[second_dependency] = [third_usage]

        converted_data = CodeFinder.convert_found_data_to_csv(data_to_concert, source_label, target_label)

        self.assertEqual(4, len(converted_data))

        # Table header will be covered by another test method
        first_data_line = converted_data[1]
        self.assertEqual(first_data_line[0], source_label)
        self.assertEqual(first_data_line[1], first_dependency)
        self.assertEqual(first_data_line[2], target_label)
        self.assertEqual(first_data_line[3], first_usage)

        second_data_line = converted_data[2]

        self.assertEqual(second_data_line[0], source_label)
        self.assertEqual(second_data_line[1], first_dependency)
        self.assertEqual(second_data_line[2], target_label)
        self.assertEqual(second_data_line[3], second_usage)

        third_data_line = converted_data[3]

        self.assertEqual(third_data_line[0], source_label)
        self.assertEqual(third_data_line[1], second_dependency)
        self.assertEqual(third_data_line[2], target_label)
        self.assertEqual(third_data_line[3], third_usage)

    def test_convert_found_data_to_csv_with_empty_dict(self):
        data_to_concert = dict()

        source_label = "Cardgen"
        target_label = "Codefinder"

        converted_data = CodeFinder.convert_found_data_to_csv(data_to_concert, source_label, target_label)

        self.assertEqual(1, len(converted_data))

        header_line = converted_data[0]
        self.assertEqual(header_line[0], "Source Module")
        self.assertEqual(header_line[1], "Used Class")
        self.assertEqual(header_line[2], "Target Module")
        self.assertEqual(header_line[3], "Consuming Class")

if __name__ == '__main__':
    unittest.main()
