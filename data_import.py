import pandas as pd
import os
import re

def load_csv_skip_junk(file_path):
    # Open the file and find the header row
    with open(file_path, 'r', encoding='utf-8') as file:
        for line_number, line in enumerate(file):
            if 'Time' in line:  # Replace with a known header name
                header_row = line_number
                break
        else:
            raise ValueError("No valid header found in the file.")
    
    # Load the CSV using pandas, skipping junk lines
    df = pd.read_csv(file_path, skiprows=header_row)
    return df

def rename_file(original_name):
    rename_mapping = {
        "reaction_from_qp": "qp_reaction",
        "joint_velocity": "joint_velocity",
        "power": "joint_mech_power",
        "torques": "joint_torque",
        "foot_contact_forces": "foot_forces",
        "energy": "joint_energy"
    }
    # Remove the timestamp prefix using regex
    match = re.match(r"^\d+_(.*)\.csv$", original_name)
    if match:
        base_name = match.group(1)
    else:
        base_name = original_name.replace(".csv", "")
    
    return rename_mapping.get(base_name, base_name)

def load_all_csv_in_directory(directory):
    dataframes = {}
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            file_path = os.path.join(directory, file)
            new_name = rename_file(file)
            try:
                df = load_csv_skip_junk(file_path)
                dataframes[new_name] = df
                print(f"Loaded: {file}")
            except Exception as e:
                print(f"Error loading {file}: {e}")
    return dataframes

if __name__ == "__main__":
    # Example usage
    directory_path = "data"  # Replace with your actual directory path
    df_dict = load_all_csv_in_directory(directory_path)

    # Example: Print first few rows of each dataframe
    for file_name, df in df_dict.items():
        print(f"\n{file_name}:")
        print(df.head())
