import numpy as np
import nibabel as nib
from scipy.io import savemat
import glob
import os

file_list = glob.glob("./data/*.nii")
file_list.sort()
for file_name in file_list:
    print(file_name)

    file_nii = nib.load(file_name)
    file_data = file_nii.get_fdata()
    file_header = file_nii.header
    file_affine = file_nii.affine

    mdic = {"data": file_data}
    savemat(os.path.basename(file_name)[:-4]+".mat", mdic)

    print("---Finished---")