from scipy.ndimage import zoom
from scipy.io import loadmat
import numpy as np
import nibabel as nib
import glob
import os

def maxmin_norm(data, pMax=99.9, pMin=0.01):
    # MAX = np.amax(data)
    # MIN = np.amin(data)
    MAX = np.percentile(data, q=pMax)
    MIN = np.percentile(data, q=pMin)
    data = (data - MIN)/(MAX-MIN)
    return data

nii_list = glob.glob("./BraTS20T_001_039/finish/*.nii.gz")
nii_list.sort()
for nii_name in nii_list:
    print(nii_name)
    name = nii_name
    data = nib.load(nii_name).get_fdata()

    tmpl_name = "./recon/example.nii"
    file_nii = nib.load(tmpl_name)
    file_data = file_nii.get_fdata()
    file_header = file_nii.header
    file_affine = file_nii.affine

    data[data<0] = 0
    # data[data>1] = 1
    px, py, pz = data.shape
    qx, qy, qz = (256, 256, 89)
    zoom_data = zoom(data, (qx/px, qy/py, qz/pz))

    zoom_data = maxmin_norm(zoom_data)
    save_file = nib.Nifti1Image(zoom_data, affine=file_affine, header=file_header)
    nib.save(save_file, os.path.basename(name)[:-7]+"_ori.nii")
    # px, py, pz = data.shape
    # qx, qy, qz = (px*2, py*2, pz*2)

    # zoom_data = zoom(data, (1, 1, 1))
    # zoom_data = zoom_data / np.sum(zoom_data) * np.sum(data)
    # print("Old dim:", data.shape)
    # print("New dim:", zoom_data.shape)
    # print("Original sum:", np.sum(data))
    # print("2x sum:", np.sum(zoom_data))

    # PVE_data = np.zeros((px, py, pz))
    # for idx in range(px):
    #     for idy in range(py):
    #         for idz in range(pz):
    #             # print("Old sum:", data[idx, idy, idz])
    #             new_sum = np.sum(zoom_data[idx*2:idx*2+2, idy*2:idy*2+2, idz*2:idz*2+2])
    #             # print("New sum:", new_sum)
    #             PVE_data[idx, idy, idz] = new_sum

    # print("PVE sum:", np.sum(PVE_data))

    # sino_file = nib.Nifti1Image(PVE_data, affine=file_affine, header=file_header)
    # nib.save(sino_file, name[:-4] +"_xy256z89_PVE.nii")