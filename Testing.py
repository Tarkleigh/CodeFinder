import os
import unittest
import CodeFinder


class ParserTests(unittest.TestCase):
    """Test class for CodeFinder.py."""

    def test_find_label_with_src_folder(self):
        test_directory_path = "finder" + os.sep + "src" + os.sep + "java"
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

    def test_find_label_without_folder_above_src(self):
        test_directory_path = "src" + os.sep + "java"
        label = CodeFinder.find_label(test_directory_path)
        self.assertEqual("src", label)

    def test_find_label_without_folder_above_src_and_no_sub_directory(self):
        test_directory_path = "src"
        label = CodeFinder.find_label(test_directory_path)
        self.assertEqual("src", label)

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
        self.assertEqual(header_line[0], "Source Root")
        self.assertEqual(header_line[1], "Used Class")
        self.assertEqual(header_line[2], "Target Root")
        self.assertEqual(header_line[3], "Consuming Class")

    def test_search_source_code_for_usages(self):
        first_dependency = "tarkleigh.codefinder.Codefinder"
        second_dependency = "tarkleigh.codefinder.DataFormatter"
        file = "CardGenerator" + os.extsep + "java"

        possible_dependencies = set()
        possible_dependencies.add(first_dependency)
        possible_dependencies.add(second_dependency)

        usages = dict()
        usages[second_dependency] = ["tarkleigh.coding.cardgen.XMLParser"]

        source_code = list()
        source_code.append("package tarkleigh.coding.cardgen" + os.linesep)
        source_code.append(os.linesep)
        source_code.append("import java.util.List;" + os.linesep)
        source_code.append("import " + first_dependency + ";" + os.linesep)
        source_code.append("import " + second_dependency + ";" + os.linesep)
        source_code.append(os.linesep)
        source_code.append("class CardGenerator")

        CodeFinder.search_source_code_for_usages(file, source_code, possible_dependencies, usages)
        self.assertEqual(len(usages[first_dependency]), 1)
        self.assertEqual(len(usages[second_dependency]), 2)

        usage_first_dependency = usages[first_dependency][0]
        self.assertEqual("tarkleigh.coding.cardgen.CardGenerator", usage_first_dependency)

        first_usage_second_dependency = usages[second_dependency][0]
        second_usage_second_dependency = usages[second_dependency][1]
        self.assertEqual("tarkleigh.coding.cardgen.XMLParser", first_usage_second_dependency)
        self.assertEqual("tarkleigh.coding.cardgen.CardGenerator", second_usage_second_dependency)

    def test_extract_class_name(self):
        test_file_name = "CardGenerator" + os.extsep + "java"
        label = CodeFinder.extract_class_name(test_file_name)
        self.assertEqual("CardGenerator", label)

    def test_extract_class_name_with_wrong_file_type(self):
        test_file_name = "CardGenerator" + os.extsep + "py"
        label = CodeFinder.extract_class_name(test_file_name)
        self.assertEqual(test_file_name, label)

    def test_search_line_for_package_name(self):
        # Using a somewhat usual formatting to test all cases
        test_line = "  package" + " org.tarkleigh.foundation" + " ;"
        package_name = CodeFinder.search_line_for_package_name(test_line, 2)
        self.assertEqual("org.tarkleigh.foundation", package_name)

    def test_search_line_unix_line_ending_handling(self):
        # Using a somewhat usual formatting to test all cases
        test_line = "package" + "org.tarkleigh.foundation" + ";\r"
        package_name = CodeFinder.search_line_for_package_name(test_line, 0)
        self.assertEqual("org.tarkleigh.foundation", package_name)

    def test_search_line_windows_line_ending_handling(self):
        # Using a somewhat usual formatting to test all cases
        test_line = "package" + "org.tarkleigh.foundation" + ";\r\n"
        package_name = CodeFinder.search_line_for_package_name(test_line, 0)
        self.assertEqual("org.tarkleigh.foundation", package_name)


if __name__ == '__main__':
    unittest.main()
