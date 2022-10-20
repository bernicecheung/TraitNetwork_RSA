"""
This script is for running regressions of event-related beta on self-ratings for each trait across runs. 
"""

import os
import glob
import pandas as pd
from nltools.data import Brain_Data

# set directories
root_dir = '/Users/BerniceCheung/Dropbox (University of Oregon)/ResearchProject/socialContext'
reorder_beta_dir = os.path.join(root_dir, 'RSA', 'inputs')
beta_regress_output_dir = os.path.join(root_dir, 'RSA', 'beta_regression','outputs')

# load condition file
conDf = pd.read_csv(os.path.join(root_dir, 'RSA', 'inputs', 'condition.txt'), sep=" ",
                    header=None)

# rename the columns
conDf.columns = ["subjectID", "runNum", "condition"]

# load the trait list
traitDf = pd.read_csv(os.path.join(root_dir, 'RSA', 'inputs', 'traitList.csv'))

# extract the trait as the reference order
ref_order = traitDf['Trait'].tolist()

# load the re-ordered trait rating with repetition
rating_repeatDf = pd.read_csv(os.path.join(root_dir, 'RSA', 'inputs', 'ratingDf_reorder_repeat.csv'))

# extract the subject ID list 
sub_list = ["{:02}".format(num) for num in rating_repeatDf['participant'].unique()]

# initialize a list of brain maps with beta regression coeffiicents for each subject
beta_regress_list = []

print("Complete the initiation.")
# loop through each subject
for sub in sub_list: 

    print(f"Start with subject {sub}")

    # extract all re-ordered beta files
    beta_fileList = glob.glob(os.path.join(reorder_beta_dir, f'sub-{sub}*.nii.gz'))
    beta_fileList.sort()

    # concatenate beta maps in the order of friend-1, friend-2, school-1, school-2
    beta_files_all = Brain_Data(beta_fileList)

    # extract the corresponding ratins
    rating_repeat = rating_repeatDf['response'][(rating_repeatDf['participant'] == int(sub))]

    # regress the beta onto the trait ratings across 4 runs
    beta_files_all.X = pd.DataFrame(rating_repeat)
    regression_output = beta_files_all.regress()

    # append and write the output
    beta_output = regression_output['beta']
    beta_output.write(os.path.join(beta_regress_output_dir, f'sub-{sub}_beta_regress.nii.gz'))
    beta_regress_list.append(beta_output)

    print(f"Complete with subject {sub}.")

beta_regress_allSub = Brain_Data(beta_regress_list)
beta_regress_allSub.write(os.path.join(beta_regress_output_dir, f'beta_regress_allSub.nii.gz')) 

print("complete with concatinating all subject beta regression images.")