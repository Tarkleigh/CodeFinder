import os
import csv
import subprocess
import argparse
import tkinter

from tkinter.filedialog import askdirectory

JAVA_FILE_TYPE = os.extsep + "java"

collected_dependencies = set()
usages = dict()


def find_label(root_directory):
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


def find_import_strings(root_directory, dependencies):
    root_dir = os.path.abspath(root_directory)

    for item in os.listdir(root_dir):
        item_full_path = os.path.join(root_dir, item)
        if item.endswith(JAVA_FILE_TYPE):
            package_string = get_package_string(item_full_path)
            dependencies.add(package_string)

        if os.path.isdir(item_full_path):
            find_import_strings(item_full_path, dependencies)


def get_package_string(item_full_path):
    package_index = item_full_path.find("java" + os.sep)
    package_string = item_full_path[package_index + 5:-5]
    package_string = package_string.replace(os.sep, ".")
    return package_string


def check_for_dependencies(item_full_path, dependencies):
    import_section_reached = False

    with open(item_full_path) as f:
        for line in f.readlines():
            if line == '\n':
                continue

            if line.find("import ") != -1:
                import_section_reached = True
                import_string = line[7: -2]
                if import_string in dependencies:
                    package_string = get_package_string(item_full_path)
                    usages.setdefault(import_string, []).append(package_string)
            elif import_section_reached:
                # Done with import section
                break


def search_target_repo(root_dir, dependencies):
    root_dir = os.path.abspath(root_dir)
    print("Checking for dependencies in " + root_dir)

    for item in os.listdir(root_dir):
        item_full_path = os.path.join(root_dir, item)
        if item.endswith(JAVA_FILE_TYPE):
            check_for_dependencies(item_full_path, dependencies)

        if os.path.isdir(item_full_path):
            search_target_repo(item_full_path, dependencies)


def convert_found_data_to_csv(usages):
    data = [["Source Module", "Used Class", "Target Module", "Consuming Class"]]
    for key in usages.keys():
        usages_of_key = usages[key]
        for usage in usages_of_key:
            data_row = [source_label, key, target_label, usage]
            data.append(data_row)

    return data


def create_and_open_csv_file(data):
    # File path for the CSV file
    csv_file_path = 'dependency_usages.csv'
    # Open the file in write mode
    with open(csv_file_path, 'w') as file:
        # Create a csv.writer object
        writer = csv.writer(file)
        # Write data to the CSV file
        writer.writerows(data)
    subprocess.call(["open", csv_file_path])


def get_root_directory(directory_from_command_line, dialogue_title):
    if directory_from_command_line is None:
        tkinter.Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
        return askdirectory(title=dialogue_title)  # show an "Open" dialog box and return the path to the selected file
    else:
        return directory_from_command_line


def main():
    parser = argparse.ArgumentParser(
        prog='CodeFinder',
        description='Finds the usages of code from the source repo in the target repo')
    parser.add_argument("--source_root", required=False)
    parser.add_argument("--target_root", required=False)

    args = parser.parse_args()

    source_root = get_root_directory(args.source_root, "Select source repository")
    target_root = get_root_directory(args.target_root, "Select target repository")

    source_label = find_label(source_root)
    target_label = find_label(target_root)

    find_import_strings(source_root, collected_dependencies)
    print(str(len(collected_dependencies)) + " possible dependencies found in source repository")

    print("Starting to scan target repository for code from the source repository")
    search_target_repo(target_root, collected_dependencies)
    print("Usages of " + str(len(usages.keys())) + " classes found")

    print("Converting found usages to CSV format")
    converted_data = convert_found_data_to_csv(usages)
    create_and_open_csv_file(converted_data)


if __name__ == '__main__':
    main()
