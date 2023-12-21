import csv_merge
import data_filter
import profile_verdict
from unzip import main as unzip_main

def run_data_processing():
    # Extracting CSV files from ZIP archives
    print("Extracting CSV files from ZIP archives...")
    unzip_successful = unzip_main()

    if unzip_successful:
        # If new files are unzipped, proceed with merging and filtering
        print("\nStarting data merging process...")
        merge_successful = csv_merge.main()
        print(f"Merge Successful: {merge_successful}")  # Debugging statement

        if merge_successful:
            print("\nStarting data filtering process...")
            data_filter.main()
        else:
            print("\nSkipping data filtering as no new data was merged.")
    else:
        print("\nSkipping data merging and filtering as no new zip files were found.")

    # Starting profile verdict process
    print("\nStarting profile verdict process...")
    profile_verdict.main()

if __name__ == "__main__":
    run_data_processing()
