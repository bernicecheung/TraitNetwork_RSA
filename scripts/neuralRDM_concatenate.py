import os
import glob
from nltools.data import Brain_Data
from nltools.mask import expand_mask
from bids import BIDSLayout

# set parameters
root_dir = '/Users/BerniceCheung/Dropbox (University of Oregon)/ResearchProject/socialContext'
reorder_beta_dir = os.path.join(root_dir, 'RSA', 'reorder_beta')
target_roi_idx = list(range(40, 48))
neural_RDM_output_dir = os.path.join(root_dir, 'RSA', 'outputs', 'neuralRDM_concat')

# create a BIDS object
layout = BIDSLayout(os.path.join(root_dir,'bids_data'), derivatives=True)

# return a list of subject IDs
sub_list = layout.get(target='subject', return_type='id')

# load the whole brain parcellation mask
mask = Brain_Data(os.path.join(root_dir, 'brainMask', 'Schaefer2018_100Parcels_7Networks_order_FSLMNI152_2mm.nii.gz'))

# get a list of ROIs
mask_x = expand_mask(mask)

# loop through each subject
for subID in sub_list[0:2]: 
    # concatenate all 4 runs in the following order: friend 1, friend2, school 1, school 2
    sub_beta_file_list = sorted(glob.glob(os.path.join(reorder_beta_dir, f'sub-{subID}_*.nii.gz')))

    sub_beta_concat = Brain_Data(sub_beta_file_list)

    # loop through each PFC ROI, and generate a neural RDM
    for idx, m in enumerate(mask_x[target_roi_idx]):
    # correlation distance ranges from 0-2
    # and subtracting this value from 1 yields similarity scores in the form of pearson correlations
        neural_RDM = 1 - sub_beta_concat.apply_mask(m).distance(metric='correlation')
        roi_idx = idx + 40
        neural_RDM.write(os.path.join(neural_RDM_output_dir, f'sub-{subID}_ROI-{roi_idx}_neuralRDM.csv'), method="square")
