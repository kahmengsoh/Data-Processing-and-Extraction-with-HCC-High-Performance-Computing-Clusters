#!/bin/bash
#SBATCH --job-name=fMRIprep
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=5
#SBATCH --time=0-23:00:00
#SBATCH --mem=16gb
#SBATCH --output=/common/wanglab/kahmengsoh/Extract_ADNI_nii_json/scripts_outputs/fMRIprep.%J.out
#SBATCH --error=/common/wanglab/kahmengsoh/Extract_ADNI_nii_json/scripts_outputs/fMRIprep.%J.err

module load anaconda
conda activate charlie95
python Extract_ADNI_nii_json.py