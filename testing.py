"""Contains unit tests for code_finder.py."""
import os
import unittest
import code_finder


class ParserTests(unittest.TestCase):
    """Test class for code_finder.py."""

    def test_find_label_with_src_folder(self):
        """Test label finding with Gradle-style path"""
        test_directory_path = "finder" + os.sep + "src" + os.sep + "java"
        label = code_finder.find_label(test_directory_path)
        self.assertEqual("finder", label)

    def test_find_label_without_src_folder(self):
        """Test label finding with regular path"""
        test_directory_path = "finder" + os.sep + "main" + os.sep + "java"
        label = code_finder.find_label(test_directory_path)
        self.assertEqual("java", label)

    def test_find_label_without_separator(self):
        """Test label finding with single directory"""
        test_directory_path = "finder"
        label = code_finder.find_label(test_directory_path)
        self.assertEqual("finder", label)

    def test_find_label_without_folder_above_src(self):
        """Test label finding with low entry-level"""
        test_directory_path = "src" + os.sep + "java"
        label = code_finder.find_label(test_directory_path)
        self.assertEqual("src", label)

    def test_find_label_without_folder_above_src_and_no_sub_directory(self):
        """Test label finding with isolated src folder"""
        test_directory_path = "src"
        label = code_finder.find_label(test_directory_path)
        self.assertEqual("src", label)

    def test_convert_found_data_to_csv(self):
        """Test conversion of found data to CSV"""
        data_to_concert = {}
        source_label = "Cardgen"
        target_label = "code_finder"

        first_dependency = "XMLParser"
        second_dependency = "CardGen"

        first_usage = "Main"
        second_usage = "InputReader"
        third_usage = "OutputWriter"

        data_to_concert[first_dependency] = [first_usage, second_usage]
        data_to_concert[second_dependency] = [third_usage]

        converted_data = code_finder.convert_found_data_to_csv(data_to_concert, source_label,
                                                               target_label)
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
        """Test conversion of data to CSV with no usages found"""
        data_to_concert = {}

        source_label = "Cardgen"
        target_label = "code_finder"

        converted_data = code_finder.convert_found_data_to_csv(data_to_concert, source_label,
                                                               target_label)

        self.assertEqual(1, len(converted_data))

        header_line = converted_data[0]
        self.assertEqual(header_line[0], "Source Root")
        self.assertEqual(header_line[1], "Used Class")
        self.assertEqual(header_line[2], "Target Root")
        self.assertEqual(header_line[3], "Consuming Class")

    def test_search_source_code_for_dependency_usages(self):
        """Test finding usages of dependencies in the source code"""
        first_dependency = "tarkleigh.code_finder.code_finder"
        second_dependency = "tarkleigh.code_finder.DataFormatter"
        file = "CardGenerator" + os.extsep + "java"

        possible_dependencies = set()
        possible_dependencies.add(first_dependency)
        possible_dependencies.add(second_dependency)

        usages = {second_dependency: ["tarkleigh.coding.cardgen.XMLParser"]}

        source_code = ["package tarkleigh.coding.cardgen" + os.linesep, os.linesep,
                       "import java.util.List;" + os.linesep,
                       "import " + first_dependency + ";" + os.linesep,
                       "import " + second_dependency + ";" + os.linesep, os.linesep,
                       "class CardGenerator"]

        code_finder.search_source_code_for_dependency_usages(file, source_code,
                                                             possible_dependencies, usages)
        self.assertEqual(len(usages[first_dependency]), 1)
        self.assertEqual(len(usages[second_dependency]), 2)

        usage_first_dependency = usages[first_dependency][0]
        self.assertEqual("tarkleigh.coding.cardgen.CardGenerator", usage_first_dependency)

        first_usage_second_dependency = usages[second_dependency][0]
        second_usage_second_dependency = usages[second_dependency][1]
        self.assertEqual("tarkleigh.coding.cardgen.XMLParser", first_usage_second_dependency)
        self.assertEqual("tarkleigh.coding.cardgen.CardGenerator", second_usage_second_dependency)

    def test_extract_class_name(self):
        """Test extracting the class name from a Java file"""
        test_file_name = "CardGenerator" + os.extsep + "java"
        label = code_finder.extract_class_name(test_file_name)
        self.assertEqual("CardGenerator", label)

    def test_extract_class_name_with_wrong_file_type(self):
        """Test extracting the class name from invalid file"""
        test_file_name = "CardGenerator" + os.extsep + "py"
        label = code_finder.extract_class_name(test_file_name)
        self.assertEqual(test_file_name, label)

    def test_search_line_for_package_name(self):
        """Test extracting the package name from a line of source code"""
        # Using a somewhat usual formatting to test all cases
        test_line = "  package" + " org.tarkleigh.foundation" + " ;"
        package_name = code_finder.search_line_for_package_name(test_line, 2)
        self.assertEqual("org.tarkleigh.foundation", package_name)

    def test_search_line_unix_line_ending_handling(self):
        """Test extracting the package name from a line of source code with unix line handling"""
        test_line = "package" + "org.tarkleigh.foundation" + ";\r"
        package_name = code_finder.search_line_for_package_name(test_line, 0)
        self.assertEqual("org.tarkleigh.foundation", package_name)

    def test_search_line_windows_line_ending_handling(self):
        """Test extracting the package name from a line of source code with Windows line handling"""
        test_line = "package" + "org.tarkleigh.foundation" + ";\r\n"
        package_name = code_finder.search_line_for_package_name(test_line, 0)
        self.assertEqual("org.tarkleigh.foundation", package_name)


if __name__ == '__main__':
    unittest.main()
