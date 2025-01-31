#!/bin/bash
#SBATCH --job-name=fMRIprep
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=5
#SBATCH --time=0-00:15:00
#SBATCH --mem=16gb
#SBATCH --output=/common/wanglab/kahmengsoh/Azzam_Model_Data_Extraction_And_Prediction/Task1_Data_Extraction/scripts_outputs/fMRIprep.%J.out
#SBATCH --error=/common/wanglab/kahmengsoh/Azzam_Model_Data_Extraction_And_Prediction/Task1_Data_Extraction/scripts_outputs/fMRIprep.%J.err

module load anaconda
conda activate charlie95
python collect_sublists_all.py