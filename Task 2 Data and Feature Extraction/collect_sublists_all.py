import os
import pandas as pd
import os.path as osp
import numpy as np

dataPathDict = {
               'ADNI':'/common/wanglab/jojo/datasets/ADNI/findings',
               'ADHD': '/common/wanglab/jojo/datasets/ADHD/findings',
               'AIBL': '/common/wanglab/jojo/datasets/AIBL/findings',
               'OASIS1': '/common/wanglab/mazzam/datasets/OASIS1/findings',
               'PPMI': '/work/wanglab/jojo/datasets/PPMI/findings',
               'NCANDA': '/common/wanglab/mazzam/datasets/NCANDA/findings',
               'IXI': '/common/wanglab/ziyangxu/datasets/IXI/findings'}


def select_uniform_subjects_ses(df, total_subjects):
    # Define bins for age groups to ensure uniform distribution
    age_bins = np.linspace(7, 96, total_subjects // 10 + 1)
    df['age_group'] = pd.cut(df['age'], bins=age_bins, include_lowest=True)

    # Sort the dataframe to maintain consistent sampling
    df = df.sort_values(by=['ID', 'ses'])

    # Collect unique IDs to ensure no duplicates
    unique_ids = df['ID'].unique()

    selected_ids = set()
    selected_rows = []

    for age_group in df['age_group'].unique():
        for sex in df['sex'].unique():
            subset = df[(df['age_group'] == age_group) & (df['sex'] == sex)]
            if not subset.empty:
                # Select IDs to maintain uniform distribution
                unique_subset_ids = subset['ID'].unique()
                np.random.shuffle(unique_subset_ids)
                sub_count = 0
                for subject_id in unique_subset_ids:
                    if subject_id not in selected_ids:
                        subject_rows = subset[subset['ID'] == subject_id]
                        if len(subject_rows) > 0:
                            selected_ids.add(subject_id)
                            selected_rows.append(subject_rows.iloc[0])  # Select the first entry for each ID
                            sub_count = sub_count + 1
                        if sub_count >= total_subjects // (len(age_bins) - 1) // 2:
                            break
                        # if len(selected_ids) >= total_subjects:
                        #     break
                if len(selected_ids) >= total_subjects:
                    break
        if len(selected_ids) >= total_subjects:
            break

    selected_subjects = pd.DataFrame(selected_rows)
    return selected_subjects

def select_uniform_subjects(df, total_subjects):
    # Define bins for age groups to ensure uniform distribution
    age_bins = np.linspace(7, 96, total_subjects // 3 + 1)
    df['age_group'] = pd.cut(df['age'], bins=age_bins, include_lowest=True)

    # Select unique subjects
    unique_subjects = df.drop_duplicates(subset=['ID'])

    # Stratified sampling to ensure uniform distribution of age and sex
    grouped = unique_subjects.groupby(['age_group', 'sex'])
    selected_unique_subjects = grouped.apply(lambda x: x.sample(n=total_subjects // (len(age_bins) - 1) // 2, replace=False))
    selected_unique_subjects = selected_unique_subjects.reset_index(drop=True)

    # Get the original records of the selected unique subjects
    selected_subjects = df[df['ID'].isin(selected_unique_subjects['ID'])]

    return selected_subjects

if __name__ == '__main__':
    dfs = []
    for dataKey, dataPath in dataPathDict.items():
        print(f"Reading {dataKey} ....")
        csvFilePath = None
        if not osp.isdir(dataPath):
            print(f"Error: No such directory for {dataKey}: {dataPath}")
            continue
        files = os.listdir(dataPath)
        csvFiles = [file for file in files if file.endswith('Desc.csv')]
        if len(csvFiles) == 0:
            print(f"Error: No csv file")
        elif len(csvFiles) == 1:
            csvFile = csvFiles[0]
            csvFilePath = osp.join(dataPath, csvFile)

        elif len(csvFiles) > 1:
            csvNewFiles = [file for file in csvFiles if file.startswith(f"{dataKey}_new")]
            csvNewFile = csvNewFiles[0]
            csvFilePath = osp.join(dataPath, csvNewFile)

        if csvFilePath is not None:
            df = pd.read_csv(csvFilePath)
            df = df[((df['gtype'] == 'CN') & (df['t1w'] == 1) & (~df['age'].isna()))]
            df['dataKey'] = dataKey
            if dataKey == 'ADHD':
                df = df[df['qc_anat'] == 'Pass']
            dfs.append(df)

    df = pd.concat(dfs)
    df = df[df['freesurf'] != 0]
    df = df[df['sex'] !='X'] # removes one subjeect to avoid confusion
    cols = ['dataKey', 'ID', 'sex', 'ses', 'age', 'gtype', 't1w', 'fmriprep', 'freesurf']

    df = df[cols]
    print(f"Shape of collected valid samples: {df.shape}")
    outFile = '/common/wanglab/kahmengsoh/Azzam_Model_Data_Extraction_And_Prediction/Task1_Data_Extraction/derivatives/sublists_all_CN.csv'
    print(f"Saving the collected sample to {outFile} ..... ")
    df.to_csv(outFile, index=False)
    
    n_samples = 1000
    print(f"selecting {n_samples} samples ....")
    df_selected = select_uniform_subjects(df, n_samples)
    print(f"Shape of selected  samples: {df_selected.shape}")
    outFile_selected = '/common/wanglab/kahmengsoh/Azzam_Model_Data_Extraction_And_Prediction/Task1_Data_Extraction/derivatives/sublists_selected_CN.csv'
    print(f"Saving the selected samples to {outFile_selected} ..... ")
#    df_selected.to_csv(outFile_selected, index=False)
     
    print(f"selecting {n_samples} samples with respect to ses....")
    df_selected_ses = select_uniform_subjects_ses(df, n_samples)
    print(f"Shape of selected  samples with ses: {df_selected_ses.shape}")
    outFile_selected_ses = '/common/wanglab/kahmengsoh/Azzam_Model_Data_Extraction_And_Prediction/Task1_Data_Extraction/derivatives/sublists_selected_ses_CN.csv'
    print(f"Saving the selected samples with ses to {outFile_selected_ses} ..... ")
#    df_selected_ses.to_csv(outFile_selected_ses, index=False)
     
    print("Done!")
