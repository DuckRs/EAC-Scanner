import os
import winreg
import tqdm
import subprocess

# Set the root directory to scan
root_dir = "C:\\"

# Set the list of file extensions to search for
file_extensions = [".exe", ".dll", ".sys", ".log"]

# Set the list of folder names to search for
folder_names = ["EasyAntiCheat", "EAC"]

# Set the list of registry keys to search for
registry_keys = ["EasyAntiCheat", "EAC"]

# Set the list of registry hives to search in
registry_hives = [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]

# Create an empty list to store the results
results = []

# Iterate over all files in the root directory and its subdirectories
print("Scanning files...")
for root, dirs, files in tqdm.tqdm(os.walk(root_dir)):
    for file in files:
        # Check if the file extension is in the list of extensions to search for
        if any(file.endswith(ext) for ext in file_extensions):
            # Check if the file is in a folder with a name in the list of names to search for
            if any(folder in root for folder in folder_names):
                # The file is a match, so add it to the list of results
                results.append(os.path.join(root, file))

# Iterate over all registry hives
print("Scanning registry keys...")
for hive in registry_hives:
    # Open the hive
    with winreg.OpenKey(hive, "", 0, winreg.KEY_ALL_ACCESS) as root_key:
        # Iterate over all subkeys in the hive
        index = 0
        while True:
            try:
                # Get the name of the subkey
                subkey_name = winreg.EnumKey(root_key, index)
                # Check if the subkey name is in the list of names to search for
                if any(key in subkey_name for key in registry_keys):
                    # The subkey is a match, so add it to the list of results
                    results.append(subkey_name)
                else:
                    # The subkey is not a match, so move on to the next one
                    index += 1
            except OSError:
                # There are no more subkeys, so break out of the loop
                break

# Open the text file for writing
with open("EasyAntiCheat_files_and_registry_keys.txt", "w") as f:
    # Write the results to the text file
    for result in results:
        f.write(result + "\n")

# Open the text file using the default program for its file type
file_path = "EasyAntiCheat_files_and_registry_keys.txt"
directory = os.path.dirname(file_path)
subprocess.Popen(["start", file_path], cwd=directory, shell=True)

print("Finished writing EasyAntiCheat files and registry keys to text file.")