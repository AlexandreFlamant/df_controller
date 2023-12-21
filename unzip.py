import os
import zipfile

def unzip_and_delete_zip_files(folder_path):
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' not found.")
        return False

    zip_files = [f for f in os.listdir(folder_path) if f.endswith('.zip')]

    if not zip_files:
        print("No zip files found to unzip.")
        return False

    for zip_file in zip_files:
        zip_path = os.path.join(folder_path, zip_file)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                # Extract the file with a new name
                new_file_name = f"{os.path.splitext(zip_file)[0]}_{file}"
                new_file_path = os.path.join(folder_path, new_file_name)
                with open(new_file_path, 'wb') as f:
                    f.write(zip_ref.read(file))
                print(f"Extracted '{new_file_name}' from '{zip_file}'.")

        os.remove(zip_path)
        print(f"Deleted '{zip_file}'.")

    return True

def main():
    folder_path = os.path.join(os.getcwd(), 'CSV_files')
    return unzip_and_delete_zip_files(folder_path)

if __name__ == "__main__":
    success = main()
    if not success:
        print("No new zip files were processed.")
