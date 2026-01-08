# import OS module
import os
import subprocess

print("FAST FILE SEARCHER")

# Get the list of all files and directories
basePath = input("Enter your base directory: ")
# basePath = "C:\\Users\\sampw\\OneDrive\\Code Projects\\Java\\Projects\\XBuilders\\app\\resources\\assets\\textures\\non redistributable\\Jicklus+1.19"


def nameContainsSearch(dirpath, filename, search):
    if filename.lower().__contains__(search.lower()):
        return True


def fileHasSearch(dirpath, filename, search):
    if os.path.isfile(dirpath + "\\" + filename):
        with open(dirpath + "\\" + filename, "rb") as f:
            contents = f.read()
            # If the contents is not a binary file
            if contents.__contains__(search.encode()):
                return True


def openFile(path):
    subprocess.Popen(f"explorer /select,{path}")


results = []
resultIndex = 0

while True:
    search = input("\n\nEnter search query: ").lower().strip()
    print(f'SEARCH RESULTS FOR "{search}":')
    results.clear()

    print('files names containing "' + search + '":')  # First, check all names
    resultIndex = 0
    for dirpath, dirnames, filenames in os.walk(basePath):
        dirpath2 = dirpath.replace(basePath, "")
        for filename in filenames:
            if nameContainsSearch(dirpath, filename, search):
                print(f"({resultIndex}):\t{dirpath2}\\{filename}")
                results.append(dirpath + "\\" + filename)
                resultIndex += 1

    print(f'files containing "{search}":')  # Next check all files
    for dirpath, dirnames, filenames in os.walk(basePath):
        dirpath2 = dirpath.replace(basePath, "")
        for filename in filenames:
            result = dirpath + "\\" + filename
            if result not in results and fileHasSearch(dirpath, filename, search):
                print(f"({resultIndex}):\t{result}")
                results.append(result)
                resultIndex += 1

    print(f"\n({len(results)} results).")
    try:
        while True:
            val = input("\nEnter the file you would like to open (Press x to cancel): ").strip()
            if val == "x":
                break
            else:
                index = int(val)
                if index >= 0 and index < len(results):
                    file = results[index]
                    if os.path.exists(file):
                        print(f"Opening {file}")
                        openFile(file)
                    else:
                        print("Invalid filepath")
                else:
                    print("Invalid input")
    except:
        print("Error")
