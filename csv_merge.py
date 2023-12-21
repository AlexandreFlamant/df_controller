import pandas as pd
import os
from datetime import datetime

def merge_spreadsheets():
    folder_name = "CSV_files"
    script_directory = os.path.dirname(os.path.realpath(__file__))
    folder_path = os.path.join(script_directory, folder_name)

    files_to_merge = [f for f in os.listdir(folder_path) if f.endswith('.csv') or f.endswith('.xlsx')]
    
    if not files_to_merge:
        print("No new CSV or Excel files to merge.")
        return False

    merged_df = pd.DataFrame()

    for file in files_to_merge:
        file_path = os.path.join(folder_path, file)
        if file.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        merged_df = pd.concat([merged_df, df], ignore_index=True)

    merged_df['Verdict'] = pd.NA  # Add an empty 'Verdict' column

    current_date = datetime.now().strftime("%Y_%m_%d")
    output_file = os.path.join(script_directory, f'merged_data_{current_date}.csv')
    merged_df.to_csv(output_file, index=False)

    # Delete the processed files
    for file_path in files_to_merge:
        os.remove(os.path.join(folder_path, file_path))
        print(f"Deleted '{file_path}'")

    print("Merging completed successfully.")
    return True  # Ensuring this is True after successful merging

def main():
    success = merge_spreadsheets()
    if success:
        print("Merging process successful.")
        return True
    else:
        print("Merging process was skipped as there were no new files.")
        return False

if __name__ == "__main__":
    main()
