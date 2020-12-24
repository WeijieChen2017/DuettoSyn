from scipy.ndimage import binary_erosion, binary_dilation
import nibabel as nib
import numpy as np
import glob
import os

nii_list = glob.glob("../../BraTS20T/*.nii.gz")
nii_list.sort()
for nii_path in nii_list:
    print(nii_path)
    nii_file = nib.load(nii_path)
    nii_data = nii_file.get_fdata()
    print(nii_data.shape)
    
    mask_data = np.zeros(nii_data.shape)
    mask = [nii_data == 0]
    mask_data[tuple(mask)] = 1
    mask_data = binary_dilation(mask_data, iterations=2)
    mask = np.asarray(mask_data, dtype=bool)
    
    value_max = np.amax(nii_data)
    nii_data = value_max - nii_data
    nii_data[mask_data] = 0
    
    norm_data = nii_data / value_max
    norm_data = norm_data ** 1.75
    norm_data = norm_data * value_max
    
    save_file = nib.Nifti1Image(norm_data, affine=nii_file.affine, header=nii_file.header)
    save_name = "./BraTS20T_m2/"+os.path.basename(nii_path)[:-7]+"_e3p175.nii"
    nib.save(save_file, save_name)
    print(save_name)
    print("--------------------------------------")