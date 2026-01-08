import os
import zipfile


# ===========================================
def list_files_by_extension_in_directory(directory):
    file_dict = {}
    for root, _, files in os.walk(directory):
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext:
                if ext not in file_dict:
                    file_dict[ext] = []
                file_dict[ext].append(os.path.join(root, file))
    return file_dict


def list_files_by_extension_in_zip(zip_file):
    file_dict = {}
    with zipfile.ZipFile(zip_file, "r") as z:
        for file in z.namelist():
            ext = os.path.splitext(file)[1]
            if ext:
                if ext not in file_dict:
                    file_dict[ext] = []
                file_dict[ext].append(file)
    return file_dict


# ===========================================
def list_file_extensions_in_directory(directory):
    extensions = set()
    for root, _, files in os.walk(directory):
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext:
                extensions.add(ext)
    return extensions


def list_file_extensions_in_zip(zip_file):
    extensions = set()
    with zipfile.ZipFile(zip_file, "r") as z:
        for file in z.namelist():
            ext = os.path.splitext(file)[1]
            if ext:
                extensions.add(ext)
    return extensions


# ===========================================


def main():
    print("FILE EXTENSION VIEWER")
    while True:
        path = input("Enter the directory path or zip file path: ")
        if path.startswith('"') and path.endswith('"'):
            path = path[1:-1]
        elif path.startswith("'") and path.endswith("'"):
            path = path[1:-1]

        # Find all available file extensions
        if os.path.isdir(path):
            file_dict = list_files_by_extension_in_directory(path)
        elif zipfile.is_zipfile(path):
            file_dict = list_files_by_extension_in_zip(path)
        else:
            print(f"Error: '{path}' is neither a directory nor a valid zip file.")
            return

        # List all available file extensions
        if file_dict:
            print("Available file extensions:")
            for ext in sorted(file_dict):
                print(ext)
        else:
            print("No files found with extensions.")
            return

        # Main loop to ask for file extensions
        while True:
            ext = (
                input("Enter a file extension (e.g., .txt, .py) or 'exit' to search another directory: ")
                .strip()
                .lower()
            )
            if ext == "exit":
                break
            elif not ext.startswith("."):
                ext = "." + ext

            if ext in file_dict:
                print(f"Files with the '{ext}' extension:")
                for file in file_dict[ext]:
                    print(file)
            else:
                print(f"No files found with the '{ext}' extension.")


if __name__ == "__main__":
    main()
