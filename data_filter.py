import pandas as pd
import os
import re
import glob

def load_exclusion_list():
    keywords_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'keywords.csv')
    try:
        keywords_df = pd.read_csv(keywords_file, delimiter=',', encoding='utf-8')
    except UnicodeDecodeError:
        keywords_df = pd.read_csv(keywords_file, delimiter=',', encoding='iso-8859-1')
    exclusion_list = keywords_df['Exclude Tag'].dropna().tolist()
    return exclusion_list

def find_latest_merged_file():
    list_of_files = glob.glob('merged_data_*.csv') 
    if not list_of_files:
        raise FileNotFoundError("No merged CSV files found in the directory.")
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def filter_data(input_file):
    df = pd.read_csv(input_file, dtype={'Verdict': str})

    # Check if the file has already been filtered
    if 'Filtered' in df.columns and df['Filtered'].all():
        print(f"File {input_file} has already been filtered.")
        return False

    initial_row_count = len(df)

    # Remove duplicates
    df = df.drop_duplicates()
    duplicates_removed = initial_row_count - len(df)

    # Apply filters
    pre_filter_row_count = len(df)
    df = df[(df['Region'].isin(['United States', 'Europe'])) & 
            (df['Signal Type'] == 'New Company') & 
            (df['Signal Type'] != 'HR')]
    rows_filtered = pre_filter_row_count - len(df)

    # Exclude based on keywords
    exclusion_list = load_exclusion_list()
    pre_exclusion_count = len(df)
    if exclusion_list:
        pattern = '|'.join([re.escape(word) for word in exclusion_list])
        df = df[~df['New Company Tagline'].str.contains(pattern, na=False, case=False)]
    rows_excluded = pre_exclusion_count - len(df)

    final_row_count = len(df)  # Final number of rows after all processing

    # Mark the file as filtered
    df['Filtered'] = True

    # Overwrite the original file
    df.to_csv(input_file, index=False)

    return (f"Data filtered and saved back to {input_file}\n"
            f"Initial rows: {initial_row_count}\n"
            f"Duplicates removed: {duplicates_removed}\n"
            f"Rows removed by filtering: {rows_filtered}\n"
            f"Rows removed by exclusion list: {rows_excluded}\n"
            f"Final number of rows: {final_row_count}")

def main():
    try:
        input_csv = find_latest_merged_file()
        print(f"Processing file: {input_csv}")
        result = filter_data(input_csv)
        if result:
            print(result)
        else:
            print("No new data to filter.")
    except FileNotFoundError as e:
        print(e)

if __name__ == "__main__":
    main()
