import os
import hashlib
import argparse
from datetime import datetime

# Calculates the Blake2 hash of a file
def blake2_hash(filepath):
    hasher = hashlib.blake2b()
    with open(filepath, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

# Traverse filesystem, hash each file, and store metadata
def new_baseline():
    
    # Log file for any access errors
    with open("access_errors.log", "a") as log_file, open("baseline.txt", "w") as metadata_file:

        for dirpath, dirnames, filenames in os.walk("/"):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    # Get file metadata
                    file_hash = blake2_hash(filepath)
                    file_size = os.path.getsize(filepath)
                    file_timestamp = os.path.getmtime(filepath)
                    file_last_modified = datetime.fromtimestamp(file_timestamp).strftime('%Y-%m-%d %H:%M:%S')

                    # Write to metadata file
                    metadata_file.write(f"{filepath}:{file_hash}:{file_size}:{file_last_modified}\n")

                # Handle cases where the file can't be accessed
                except (PermissionError, FileNotFoundError, OSError) as e:
                    # Write to error log
                    log_file.write(f"{datetime.now()} Skipping {filepath}: {e}\n")
                    #print(f"Skipping {filepath}: {e}")

#def start_monitor():

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--new-baseline", help="Create a new system baseline", action="store_false")
    parser.add_argument("-b", "--baseline", help="Run against system baseline", action="store_true")
    
    args = parser.parse_args()

    if args.new_baseline:
        new_baseline()

if __name__ == "__main__":
    main()