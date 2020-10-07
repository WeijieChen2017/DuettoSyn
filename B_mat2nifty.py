from scipy.ndimage import zoom
from scipy.io import loadmat
import numpy as np
import nibabel as nib
import glob

leah_list = glob.glob("./leah/recon/*.mat")
for leah_name in leah_list:
    name = leah_name
    mdict = loadmat(name)
    data = mdict["reconImg"]

    tmpl_name = "./data/mri_89.nii"
    file_nii = nib.load(tmpl_name)
    file_data = file_nii.get_fdata()
    file_header = file_nii.header
    file_affine = file_nii.affine

    # data[data<0] = 0
    # data[data>1] = 1

    px, py, pz = data.shape
    qx, qy, qz = (512, 512, 284)
    zoom_data = zoom(data, (qx/px, qy/py, qz/pz))

    print("Old dim:", data.shape)
    print("New dim:", zoom_data.shape)

    sino_file = nib.Nifti1Image(zoom_data, affine=file_affine, header=file_header)
    nib.save(sino_file, name[:-4]+".nii")