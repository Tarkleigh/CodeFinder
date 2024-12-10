import os
import csv
import subprocess
import argparse
import tkinter
import sys

from argparse import Namespace
from tkinter.filedialog import askdirectory
from typing import AnyStr

JAVA_FILE_TYPE = os.extsep + "java"


def find_label(root_directory: str) -> str:
    index = root_directory.find("src")
    if index != -1:
        # Use the directory above src for the label
        before_src = root_directory[:index - 1]
        former_seperator = before_src.rfind(os.sep)
        label = before_src[former_seperator + 1:]
        return label
    else:
        # Use the current directory as label
        former_seperator = root_directory.rfind(os.sep)
        label = root_directory[former_seperator + 1:]
        return label


def find_possible_dependencies(root_directory: str, possible_dependencies: set[str]):
    root_dir = os.path.abspath(root_directory)

    for item in os.listdir(root_dir):
        item_full_path = os.path.join(root_dir, item)
        if item.endswith(JAVA_FILE_TYPE):
            class_name = extract_class_name(item)
            package_name = extract_package_name(item_full_path)
            fully_qualified_name = package_name + "." + class_name
            possible_dependencies.add(fully_qualified_name)

        if os.path.isdir(item_full_path):
            find_possible_dependencies(item_full_path, possible_dependencies)


def extract_class_name(item: str) -> str:
    file_ending_index = item.find(JAVA_FILE_TYPE)
    if file_ending_index == -1:
        return item
    else:
        return item[:file_ending_index]


def extract_package_name(item_full_path: str) -> str:
    with open(item_full_path, encoding='utf-8') as java_file:
        for line in java_file:
            package_index = line.find("package")
            if package_index != -1:
                package_name = search_line_for_package_name(line, package_index)
                return package_name

        # Since every Java file has a package, we should never come here unless we open the wrong kind of file
        return ""


def search_line_for_package_name(line: str, package_index: int) -> str:
    # Ignore everything before package and the package keyword itself
    start_index = package_index + len("package")
    line_without_package_keyword = line[start_index:]
    line_without_semi_colon = line_without_package_keyword.replace(";", "")
    line_without_line_ending = line_without_semi_colon.rstrip('\r\n')
    package_name = line_without_line_ending.replace(" ", "")
    return package_name


def find_usages(item_full_path: str, item, possible_dependencies: set[str], usages: dict[str, list[str]]):
    with open(item_full_path, encoding='utf-8') as source_file:
        source_code = source_file.readlines()
        search_source_code_for_usages(item, source_code, possible_dependencies, usages)


def search_source_code_for_usages(item: str, source_code: list[AnyStr], possible_dependencies: set[str],
                                  usages: dict[str, list[str]]):
    import_section_reached = False
    package_name = ""
    for line in source_code:
        if line.strip() == "":
            continue

        package_index = line.find("package")
        if package_index != -1:
            package_name = search_line_for_package_name(line, package_index)

        if line.find("import ") != -1:
            import_section_reached = True
            semicolon_index = line.find(";")

            # Extract the class by removing the "import " string and the terminating semicolon and line ending character
            imported_class = line[7: semicolon_index]
            if imported_class in possible_dependencies:
                class_name = extract_class_name(item)
                consuming_class = package_name + "." + class_name
                usages.setdefault(imported_class, []).append(consuming_class)
        elif import_section_reached:
            # Done with import section, rest of the file can be ignored
            break


def search_target_repo(root_dir: str, possible_dependencies: set[str], usages: dict[str, list[str]]):
    root_dir = os.path.abspath(root_dir)
    print("Checking for usages in " + root_dir)

    for item in os.listdir(root_dir):
        item_full_path = os.path.join(root_dir, item)
        if item.endswith(JAVA_FILE_TYPE):
            find_usages(item_full_path, item, possible_dependencies, usages)

        if os.path.isdir(item_full_path):
            search_target_repo(item_full_path, possible_dependencies, usages)


def convert_found_data_to_csv(found_usages: dict[str, list[str]], source_label: str, target_label: str) -> list[
    list[str]]:
    data = [["Source Module", "Used Class", "Target Module", "Consuming Class"]]
    for key in found_usages.keys():
        usages_of_key = found_usages[key]
        for usage in usages_of_key:
            data_row = [source_label, key, target_label, usage]
            data.append(data_row)

    return data


def create_and_open_csv_file(data: list[list[str]]):
    # File path for the CSV file
    csv_file_path = 'dependency_usages.csv'
    # Open the file in write mode
    with open(csv_file_path, 'w') as file:
        # Create a csv.writer object
        writer = csv.writer(file)
        # Write data to the CSV file
        writer.writerows(data)

    if sys.platform == "win32":
        os.startfile(csv_file_path)
    elif sys.platform == "darwin":  # mac
        subprocess.call(["open", csv_file_path])
    else:  # linux
        subprocess.call(["xdg-open", csv_file_path])


def get_root_directory(directory_from_command_line: str, dialogue_title: str) -> (str, bool):
    if directory_from_command_line is None:
        tkinter.Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
        tkinter.messagebox.showinfo(dialogue_title, dialogue_title)
        root_directory = askdirectory(title=dialogue_title)
        return root_directory, True
    else:
        return directory_from_command_line, False


def get_command_line_arguments() -> Namespace:
    parser = argparse.ArgumentParser(
        prog='CodeFinder',
        description='Finds the usages of code from the source repo in the target repo')
    parser.add_argument("--source_root", required=False)
    parser.add_argument("--target_root", required=False)
    parser.add_argument("--skip_confirm", required=False)
    return parser.parse_args()


def main():
    args = get_command_line_arguments()

    source_root, source_from_dialogue = get_root_directory(args.source_root, "Please select source root directory")
    target_root, target_from_dialogue = get_root_directory(args.target_root, "Please select target root directory")

    # Root directories were chosen via Tkinter dialogue. This can be confusing, so we should let the user confirm
    if source_from_dialogue or target_from_dialogue:
        confirm_message = ("Source Root set to " + source_root + os.linesep + "---" + os.linesep +
                           "Target Root set to " + target_root + os.linesep + "---" + os.linesep + "Continue?")
        result = tkinter.messagebox.askokcancel("Confirm", confirm_message)
        if result is False:
            sys.exit("Search cancelled")

    source_label = find_label(source_root)
    target_label = find_label(target_root)

    possible_dependencies = set()
    usages = dict()

    find_possible_dependencies(source_root, possible_dependencies)
    print(str(len(possible_dependencies)) + " possible dependencies found in source repository")

    print("Starting to scan target repository for code from the source repository")
    search_target_repo(target_root, possible_dependencies, usages)
    print("Usages of " + str(len(usages.keys())) + " classes found")

    print("Converting found usages to CSV format")
    converted_data = convert_found_data_to_csv(usages, source_label, target_label)
    create_and_open_csv_file(converted_data)


if __name__ == '__main__':
    main()
