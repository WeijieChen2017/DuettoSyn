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

    px, py, pz = file_data.shape
	qx, qy, qz = (256, 256, 89)
	zoom_data = zoom(data, (qx/px, qy/py, qz/pz))

	print("Old dim:", data.shape)
	print("New dim:", zoom_data.shape)

    mdic = {"data": file_data}
    savemat("./leah/"+os.path.basename(file_name)[:-4]+".mat", mdic)

    pure_file = nib.Nifti1Image(zoom_data, affine=file_affine, header=file_header)
	nib.save(pure_file, "./leah/"+name+".nii")

print("---Finished---")