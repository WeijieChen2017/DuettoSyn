from scipy.ndimage import binary_erosion, binary_dilation
from scipy.io import savemat
from nibabel import processing
import nibabel as nib
import numpy as np
import glob
import os

nii_list = glob.glob("./RSZP/*.nii")
nii_list.sort()
for nii_path in nii_list:
    print(nii_path)
    nii_file = nib.load(nii_path)
    nii_data = nii_file.get_fdata()
    print(nii_data.shape)
    
    mdic = {"data": nii_data}
    nii_name = os.path.basename(nii_path)
    nii_group = nii_name[1:3]
    save_name = "./RSZP_mat/"+nii_group+"/"
    if not os.path.exists(save_name):
        os.makedirs(save_name)
    save_name += nii_name[:-4]+".mat"
    savemat(save_name, mdic)
    print("Mat:", save_name)

    save_file = nib.Nifti1Image(nii_data, affine=nii_file.affine, header=nii_file.header)
    smoothed_file = processing.smooth_image(save_file, fwhm=3, mode='nearest')
    save_name = "./RSZP_f3/"+nii_name
    nib.save(smoothed_file, save_name)
    print("F3:", save_name)
    print("--------------------------------------")