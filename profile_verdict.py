import os
import glob
import pandas as pd

def find_latest_file():
    list_of_files = glob.glob('merged_data_*.csv') 
    if not list_of_files:
        raise FileNotFoundError("No merged CSV files found in the directory.")
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def display_progress(df):
    total_rows = len(df)
    if total_rows == 0:
        print("\nNo data available for review.")
        return
    completed_rows = total_rows - df['Verdict'].isna().sum()
    progress_percentage = (completed_rows / total_rows) * 100
    print(f"\nProgress: {completed_rows}/{total_rows} [{progress_percentage:.2f}%]")

def display_card(row):
    # Check if the founder is a repeat founder and add 🔁 after their name if true
    name = row['Name']
    if row.get('Serial Founder') == 'Yes':
        name += " 🔁"

    # Merge the first row and display the name
    print("\n" + "=" * 50)
    print(f"{'Name':<20} | {name:<28}")
    print("-" * 50)

    # Define the categories, excluding 'Name', 'Serial Founder', and 'Past Education'
    categories = ['Location', 'New Position', 'New Company Tagline', 'Past Position', 'Education']

    # Mapping for display names
    display_names = {
        'New Position': 'Current',
        'New Company Tagline': 'Tagline'
    }

    # Fetch data for each category from the row and display in 2x2 chart format
    for category in categories:
        display_category = display_names.get(category, category)

        if category == 'Education':
            education_str = str(row.get('Education') or '')
            past_education_str = str(row.get('Past Education') or '')
            education_data = education_str + ';' + past_education_str
            education_items = [item.strip() for item in education_data.split(';') if item.strip()]
            print(f"{display_category:<20} | ", end="")
            for index, item in enumerate(education_items):
                if index > 0:
                    print(f"{' ':<20} | ", end="")
                print(f"• {item}")
            print(f"{' ':<20} | {' ':<28}")  # Add a vertical space after 'Education'
        elif category == 'Past Position':
            item_data = str(row.get(category) or 'N/A')
            items = [item.strip() for item in item_data.split(';') if item.strip()]
            for index, item in enumerate(items):
                if index == 0:
                    print(f"{display_category:<20} | • {item}")
                else:
                    print(f"{' ':<20} | • {item}")
            print(f"{' ':<20} | {' ':<28}")  # Add a vertical space after 'Past Position'
        else:
            result = str(row.get(category, 'N/A'))
            print(f"{display_category:<20} | {result}")
            if category == 'New Company Tagline':
                print(f"{' ':<20} | {' ':<28}")  # Add a vertical space after 'Tagline'

    print("=" * 50)

def get_user_input():
    while True:
        verdict = input("Enter your verdict (Y/N), 'SAVE' to save, or 'EXIT' to exit without saving: ").strip().upper()
        if verdict in ['Y', 'N', 'SAVE', 'EXIT']:
            return verdict
        else:
            print("Invalid input. Please enter 'Y', 'N', 'SAVE', or 'EXIT'.")

def main():
    print("Starting the review process...")

    try:
        latest_file = find_latest_file()
    except FileNotFoundError as e:
        print(e)
        return

    df = pd.read_csv(latest_file, dtype={'Verdict': str})

    for index, row in df.iterrows():
        if pd.notna(row['Verdict']) and row['Verdict'].strip() != '':
            continue

        display_progress(df)
        display_card(row)
        verdict = get_user_input()
        if verdict == 'SAVE':
            df.to_csv(latest_file, index=False)
            print("Data saved. Exiting...")
            break
        elif verdict == 'EXIT':
            print("Exiting without saving...")
            break
        else:
            df.at[index, 'Verdict'] = verdict

    if df['Verdict'].isna().sum() == 0:
        print("All rows have been reviewed!")
        df.to_csv(latest_file, index=False)
        print("Data saved.")

if __name__ == "__main__":
    main()
