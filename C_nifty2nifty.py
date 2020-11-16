from scipy.ndimage import zoom
from scipy.io import loadmat
import numpy as np
import nibabel as nib
import glob

leah_list = glob.glob("../../BraTS20T_001_039/*.nii.gz")
for leah_name in leah_list:
    name = leah_name
    data = nib.load(leah_name).get_fdata()

    tmpl_name = "./data/example.nii"
    file_nii = nib.load(tmpl_name)
    file_data = file_nii.get_fdata()
    file_header = file_nii.header
    file_affine = file_nii.affine

    # data[data<0] = 0
    # data[data>1] = 1

    px, py, pz = data.shape
    qx, qy, qz = (512, 512, 178)
    zoom_data = zoom(data, (qx/px, qy/py, qz/pz))

    print("Old dim:", data.shape)
    print("New dim:", zoom_data.shape)

    sino_file = nib.Nifti1Image(zoom_data, affine=file_affine, header=file_header)
    nib.save(sino_file, name[:-4] +"_xy512z178.nii")