from scipy.ndimage import zoom
from scipy.io import loadmat
import numpy as np
import nibabel as nib
import glob

name = "s1_bravo_recon_bravo"
mdict = loadmat(name+".mat")
data = mdict["reconImg"]

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

px, py, pz = data.shape
qx, qy, qz = (512, 512, 284)
zoom_data = zoom(data, (qx/px, qy/py, qz/pz))

print("Old dim:", data.shape)
print("New dim:", zoom_data.shape)

sino_file = nib.Nifti1Image(zoom_data, affine=file_affine, header=file_header)
nib.save(sino_file, "./"+name+".nii")