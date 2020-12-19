import numpy as np
import nibabel as nib
from scipy.io import savemat
from scipy.ndimage import zoom
import glob
import os

file_list = glob.glob("../../BraTS20V/*.nii.gz")
# file_list = glob.glob("./mri/*.nii.gz")
file_list.sort()
for file_name in file_list:
    print(file_name)

    file_nii = nib.load(file_name)
    file_data = file_nii.get_fdata()
    file_header = file_nii.header
    file_affine = file_nii.affine

    bg_mask = [file_data == 0]
    value_max = np.amax(file_data)
    file_data = value_max - file_data
    file_data[tuple(bg_mask)] = 0
    file_data[file_data <1] = 0

    px, py, pz = file_data.shape
    qx, qy, qz = (240, 240, 56)
    # zoom_data = zoom(file_data, (qx/px, qy/py, qz/pz))
    zoom_data = file_data

    print("Old dim:", file_data.shape)
    print("New dim:", zoom_data.shape)

    mdic = {"data": zoom_data}
    savemat("./BraTS20V/"+os.path.basename(file_name)[:-7]+".mat", mdic)

    # pure_file = nib.Nifti1Image(zoom_data, affine=file_affine, header=file_header)
    # nib.save(pure_file, "./BraTS20T_001_039/"+os.path.basename(file_name)[:-4]+".nii")

print("---Finished---")