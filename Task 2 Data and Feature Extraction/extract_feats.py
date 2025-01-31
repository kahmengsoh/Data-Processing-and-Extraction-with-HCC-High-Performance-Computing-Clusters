#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import os
import os.path as osp
import zipfile
import shutil
import argparse

dataPath = "/common/wanglab/jojo/datasets/ADNI/derivatives/fmriprep"

def extract_zip(zip_path, extract_to):
    """Extract the zip file to the specified directory."""
    if not osp.exists(extract_to):
        os.makedirs(extract_to)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def read_stats_aparc(statsPath):
    if not osp.exists(statsPath):
        raise ValueError(f"stats path does not exist: {statsPath}")
    statFiles = ["lh.aparc.stats", "rh.aparc.stats"]
    featList = ['StructName', 'NumVert', 'SurfArea', 'GrayVol', 'ThickAvg', 'ThickStd', 'MeanCurv', 'GausCurv', 
                'FoldInd', 'CurvInd']
    dfs = []
    for statFile in statFiles:
        df = pd.read_csv(osp.join(statsPath, statFile), comment='#', header=None, delimiter=r"\s+")
        df.columns = featList
        df.set_index('StructName', inplace=True)
        dfs.append(df)
    n_rows = 34
    assert dfs[0].shape[0] == dfs[1].shape[0] == n_rows, f"Either of {statFiles} has lines not equal {n_rows} "
    df = pd.concat(dfs, keys=statFiles, axis=1, join='inner')
    return df.unstack()

def read_stats_a2009s(statsPath):
    if not osp.exists(statsPath):
        raise ValueError(f"stats path does not exist: {statsPath}")
    statFiles = ["lh.aparc.a2009s.stats", "rh.aparc.a2009s.stats"]
    featList = ['StructName', 'NumVert', 'SurfArea', 'GrayVol', 'ThickAvg', 'ThickStd', 'MeanCurv', 'GausCurv', 
                'FoldInd', 'CurvInd']
    dfs = []
    for statFile in statFiles:
        df = pd.read_csv(osp.join(statsPath, statFile), comment='#', header=None, delimiter=r"\s+")
        df.columns = featList
        df.set_index('StructName', inplace=True)
        dfs.append(df)
    n_rows = 74
    assert dfs[0].shape[0] == dfs[1].shape[0] == n_rows, f"Either of {statFiles} has lines not equal {n_rows} "
    df = pd.concat(dfs, keys=statFiles, axis=1, join='inner')
    return df.unstack()

def read_stats_DKTatlas(statsPath, subName, sesName):
    if not osp.exists(statsPath):
        raise ValueError(f"stats path does not exist: {statsPath}")
    statFiles = ["lh.aparc.DKTatlas.stats", "rh.aparc.DKTatlas.stats"]
    featList = ['StructName', 'NumVert', 'SurfArea', 'GrayVol', 'ThickAvg', 'ThickStd', 'MeanCurv', 'GausCurv', 'FoldInd', 'CurvInd']
    dfs = []
    for statFile in statFiles:
        df = pd.read_csv(osp.join(statsPath, statFile), comment='#', header=None, delimiter=r"\s+")
        df.columns = featList
        df.set_index('StructName', inplace=True)
        index_to_delete = 'temporalpole'
        if index_to_delete in df.index:
            df.drop('temporalpole', inplace=True)
        dfs.append(df)

    n_rows = 31
    assert dfs[0].shape[0] == dfs[1].shape[0] == n_rows, f"Either of {statFiles} has lines not equal {n_rows}: ID {subName} @ {sesName} "
    df = pd.concat(dfs, keys=statFiles, axis=1, join='inner')
    return df.unstack()

def read_stats_pial(statsPath):
    if not osp.exists(statsPath):
        raise ValueError(f"stats path does not exist: {statsPath}")
    statFiles = ["lh.aparc.pial.stats", "rh.aparc.pial.stats"]
    featList = ['StructName', 'NumVert', 'SurfArea', 'GrayVol', 'ThickAvg', 'ThickStd', 'MeanCurv', 'GausCurv', 'FoldInd', 'CurvInd']
    dfs = []
    for statFile in statFiles:
        df = pd.read_csv(osp.join(statsPath, statFile), comment='#', header=None, delimiter=r"\s+")
        df.columns = featList
        df.set_index('StructName', inplace=True)
        dfs.append(df)

    n_rows = 34
    assert dfs[0].shape[0] == dfs[1].shape[0] == n_rows, f"Either of {statFiles} has lines not equal {n_rows}: lh-> {dfs[0].shape[0]} rh-> {dfs[1].shape[0]} "
    df = pd.concat(dfs, keys=statFiles, axis=1, join='inner')
    return df.unstack()

def read_stats_BA_exvivo(statsPath):
    if not osp.exists(statsPath):
        raise ValueError(f"stats path does not exist: {statsPath}")
    statFiles = ["lh.BA_exvivo.stats", "rh.BA_exvivo.stats"]
    featList = ['StructName', 'NumVert', 'SurfArea', 'GrayVol', 'ThickAvg', 'ThickStd', 'MeanCurv', 'GausCurv', 'FoldInd', 'CurvInd']
    dfs = []
    for statFile in statFiles:
        df = pd.read_csv(osp.join(statsPath, statFile), comment='#', header=None, delimiter=r"\s+")
        df.columns = featList
        df.set_index('StructName', inplace=True)
        dfs.append(df)

    n_rows = 14
    assert dfs[0].shape[0] == dfs[1].shape[0] == n_rows, f"Either of {statFiles} has lines not equal {n_rows}"
    df = pd.concat(dfs, keys=statFiles, axis=1, join='inner')
    return df.unstack()

def read_stats_wg(statsPath):
    if not osp.exists(statsPath):
        raise ValueError(f"stats path does not exist: {statsPath}")
    statFiles = ["lh.w-g.pct.stats", "rh.w-g.pct.stats"]
    featList = ['Index', 'SegId', 'NVertices', 'Area_mm2', 'StructName', 'Mean', 'StdDev', 'Min', 'Max', 'Range', 'SNR']
    dfs = []
    for statFile in statFiles:
        df = pd.read_csv(osp.join(statsPath, statFile), comment='#', header=None, delimiter=r"\s+")
        df.columns = featList
        df.set_index('StructName', inplace=True)
        if 'unknown' in df.index:
            df.drop('unknown', inplace=True)
        dfs.append(df)
    n_rows = 34
    assert dfs[0].shape[0] == dfs[1].shape[0] == n_rows, f"Either of {statFiles} has lines not equal {n_rows}: lh-> {dfs[0].shape[0]} rh-> {dfs[1].shape[0]}"
    df = pd.concat(dfs, keys=statFiles, axis=1, join='inner')
    return df.unstack()

def read_stats_aseg(statsPath):
    if not osp.exists(statsPath):
        raise ValueError(f"stats path does not exist: {statsPath}")
    statFile = "aseg.stats"
    featList = ['Index', 'SegId', 'NVoxels', 'Volume_mm3', 'StructName', 'normMean', 'normStdDev', 'normMin', 'normMax', 'normRange']
    df = pd.read_csv(osp.join(statsPath, statFile), comment='#', header=None, delimiter=r"\s+")
    n_rows = 45
    assert df.shape[0] == n_rows, "{statFile} has rows not equal to {n_rows}"
    df.columns = featList
    df.set_index('StructName', inplace=True)
    df.columns = df.columns.map(lambda col: (statFile, col))
    df = df.unstack()
    return df

def read_stats_wmparc(statsPath):
    if not osp.exists(statsPath):
        raise ValueError(f"stats path does not exist: {statsPath}")
    statFile = "wmparc.stats"
    featList = ['Index', 'SegId', 'NVoxels', 'Volume_mm3', 'StructName', 'normMean', 'normStdDev', 'normMin', 'normMax', 'normRange']
    df = pd.read_csv(osp.join(statsPath, statFile), comment='#', header=None, delimiter=r"\s+")
    n_rows = 70
    assert df.shape[0] == n_rows, "{statFile} has rows not equal to {n_rows}"
    df.columns = featList
    df.set_index('StructName', inplace=True)
    df.columns = df.columns.map(lambda col: (statFile, col))
    df = df.unstack()
    return df

def find_stats_folder(extract_path):
    """Recursively search for the 'stats' folder within the extracted directory."""
    for root, dirs, files in os.walk(extract_path):
        if 'stats' in dirs:
            return osp.join(root, 'stats')
    return None

def process_subject_row(row):
    """Process each subject's row: extract zip, process stats, and clean up."""
    sub_name = f"{row['ID']}"
    ses_name = f"ses-{row['ses']}"

    # Ensure we don't duplicate the "sub-" prefix
    if not sub_name.startswith("sub-"):
        zip_file_name = f"sub-{sub_name}.zip"
    else:
        zip_file_name = f"{sub_name}.zip"

    session_path = osp.join(dataPath, ses_name, "sourcedata/freesurfer")
    zip_file_path = osp.join(session_path, zip_file_name)

    # Temporary extraction path
    temp_extract_path = osp.join("/common/wanglab/kahmengsoh/Azzam_Model_Data_Extraction_And_Prediction/Task1_Data_Extraction/cache", sub_name)

    # Check if zip file exists
    if not osp.exists(zip_file_path):
        raise FileNotFoundError(f"Zip file not found: {zip_file_path}")
    
    # Extract the zip file
    print(f"Extracting {zip_file_path} to {temp_extract_path}...")
    extract_zip(zip_file_path, temp_extract_path)

    # Recursively search for the stats folder
    stats_path = find_stats_folder(temp_extract_path)
    
    if stats_path is None:
        print(f"Directory structure under {temp_extract_path}:")
        for root, dirs, files in os.walk(temp_extract_path):
            print(f"Root: {root}")
            print(f"Directories: {dirs}")
            print(f"Files: {files}")
        raise ValueError(f"Stats folder not found in the extracted directory: {temp_extract_path}")
    
    print(f"Stats folder found: {stats_path}")

    # Use existing read_stats_* functions to read stats files
    row_aparc = read_stats_aparc(stats_path)
    row_a2009s = read_stats_a2009s(stats_path)
    row_DKTatlas = read_stats_DKTatlas(stats_path, sub_name, ses_name)
    row_pial = read_stats_pial(stats_path)
    row_BA_exvivo = read_stats_BA_exvivo(stats_path)
    row_wg = read_stats_wg(stats_path)
    row_aseg = read_stats_aseg(stats_path)
    row_wmparc = read_stats_wmparc(stats_path)

    # Combine all the rows into a single dataframe
    combined_stats = pd.concat([row_aparc, row_a2009s, row_DKTatlas, row_pial, 
                                row_BA_exvivo, row_wg, row_aseg, row_wmparc], 
                               axis=0, join='inner', ignore_index=False)

    # Add the subject ID and session as a new column
    combined_stats['ID'] = sub_name
    combined_stats['ses'] = ses_name

    # Clean up: delete the extracted files to avoid clutter
    print(f"Cleaning up: Removing folder {temp_extract_path}")
    shutil.rmtree(temp_extract_path)
    
    return combined_stats

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Freesurfer feature extraction from ADNI dataset')
    parser.add_argument('--input', type=str, default='/common/wanglab/kahmengsoh/Azzam_Model_Data_Extraction_And_Prediction/Task1_Data_Extraction/derivatives/sublists_ADNI_CN.csv',
                        help='CSV file containing subject details like age, ID, and session')
    parser.add_argument('--output', type=str, default='/common/wanglab/kahmengsoh/Azzam_Model_Data_Extraction_And_Prediction/Task1_Data_Extraction/derivatives/ADNI_CN_Data.csv',
                        help='CSV file to store the extracted features and age data')
    
    args = parser.parse_args()
    
    csv_file = args.input
    output_file = args.output

    if not osp.isfile(csv_file):
        raise FileNotFoundError(f"CSV file not found: {csv_file}")

    print(f"Reading CSV file: {csv_file}...")
    df = pd.read_csv(csv_file)
    print("CSV file loaded successfully!")

    print("Extracting features from zip files...")
    df_new = df.apply(process_subject_row, axis=1)

    # Add the age column back to the final dataframe
    df_new['age'] = df['age']

    # Ensuring that the "ID", "ses", and "age" columns are aligned properly without adding extra blank rows
    df_new['ID'] = list(df['ID'])
    df_new['ses'] = list(df['ses'])
    df_new['age'] = list(df['age'])

    print(f"Saving the processed data to {output_file}...")
    df_new.to_csv(output_file, index=False)
    print("Feature extraction and saving completed!")

