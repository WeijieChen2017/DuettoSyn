import nibabel as nib
from scipy.io import loadmat

name = "mri89FOV240_recon"
mdict = loadmat(name+".mat")
data = mdict["reconImg"]
print(data.shape)

import numpy as np
import nibabel as nib
import glob

file_list = glob.glob("./data/*.nii")
file_list.sort()
for file_name in file_list:
    print(file_name)

file_nii = nib.load(file_list[-1])
file_data = file_nii.get_fdata()
file_header = file_nii.header
file_affine = file_nii.affine

data[data<0] = 0
data[data>1] = 1

import numpy as np
sino_file = nib.Nifti1Image(data, affine=file_affine, header=file_header)
nib.save(sino_file, "./"+name+".nii")