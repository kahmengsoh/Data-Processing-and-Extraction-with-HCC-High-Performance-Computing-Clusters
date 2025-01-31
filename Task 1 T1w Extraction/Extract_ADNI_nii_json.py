import os
import zipfile
import shutil
from pathlib import Path

# Define paths
data_path = "/work/wanglab/jojo/datasets/ADNI/derivatives/fmriprep"
temp_path = "/common/wanglab/kahmengsoh/Extract_ADNI_nii_json/cache"
output_path = "/common/wanglab/kahmengsoh/Extract_ADNI_nii_json/derivatives"

def extract_nii_json(session_path, session_name):
    """Copy specific compressed .nii.gz and .json files to the subject folder."""
    zip_files = [f for f in os.listdir(session_path) if f.endswith('.zip')]
    
    for zip_file in zip_files:
        subject_id = zip_file.split(".")[0]  # e.g., sub-ADNI002S0685
        temp_extract_path = os.path.join(temp_path, subject_id)

        zip_file_path = os.path.join(session_path, zip_file)
        
        # Create temp folder for extraction
        if not os.path.exists(temp_extract_path):
            os.makedirs(temp_extract_path)

        # Extract the zip file
        print(f"Extracting {zip_file_path} to {temp_extract_path}...")
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(temp_extract_path)

        # Locate the anat folder
        anat_path = Path(temp_extract_path) / "common" / "wanglab" / "mazzam" / "datasets" / "ADNI" / "derivatives" / "fmriprep" / session_name / subject_id / session_name / "anat"
        print(f"Looking for anat folder at: {anat_path}")
        if not anat_path.exists():
            print(f"Anat folder not found in {anat_path}. Skipping...")
            shutil.rmtree(temp_extract_path)
            continue

        # Define the specific filenames to copy
        nii_file = anat_path / f"{subject_id}_{session_name}_space-MNI152NLin2009cAsym_desc-preproc_T1w.nii.gz"
        json_file = anat_path / f"{subject_id}_{session_name}_space-MNI152NLin2009cAsym_desc-preproc_T1w.json"

        # Ensure output folder structure exists
        session_output_path = os.path.join(output_path, session_name, subject_id)
        if not os.path.exists(session_output_path):
            print(f"Creating directory: {session_output_path}")
            os.makedirs(session_output_path)

        # Copy the compressed .nii.gz file directly into the subject folder
        if nii_file.exists():
            print(f"Copying compressed NII file {nii_file} to {session_output_path}...")
            shutil.copy(nii_file, session_output_path)
            print(f"Compressed NII file successfully copied to: {session_output_path}")
        else:
            print(f"Compressed NII file NOT FOUND: {nii_file}")

        # Copy the .json file directly into the subject folder
        if json_file.exists():
            print(f"Copying JSON file {json_file} to {session_output_path}...")
            shutil.copy(json_file, session_output_path)
            print(f"JSON file successfully copied to: {session_output_path}")
        else:
            print(f"JSON file NOT FOUND: {json_file}")

        # Clean up temporary extraction folder
        print(f"Cleaning up temporary folder {temp_extract_path}...")
        shutil.rmtree(temp_extract_path)

if __name__ == "__main__":
    # Ensure temp and output directories exist
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Iterate through all session folders
    for session_folder in os.listdir(data_path):
        session_path = os.path.join(data_path, session_folder)
        if os.path.isdir(session_path) and session_folder.startswith("ses-M"):
            print(f"Processing session folder: {session_folder}...")
            extract_nii_json(session_path, session_folder)

    print("Extraction process completed!")



