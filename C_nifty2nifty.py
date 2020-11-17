from scipy.ndimage import zoom
from scipy.io import loadmat
import numpy as np
import nibabel as nib
import glob

leah_list = glob.glob("../../BraTS20T_001_039/*.nii.gz")
leah_list.sort()
for leah_name in leah_list:
    print(leah_name)
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
    zoom_data = zoom_data / np.sum(zoom_data) * np.sum(data)
    print("Old dim:", data.shape)
    print("New dim:", zoom_data.shape)
    print("Original sum:", np.sum(data))
    print("2x sum:", np.sum(zoom_data))

    PVE_data = np.zeros((256, 256, 89))
    for idx in range(256):
        for idy in range(256):
            for idz in range(89):
                print("Old sum:"data[idx, idy, idz])
                new_sum = np.sum(zoom_data[idx*2:idx*2+1, idy*2:idy*2+1, idz*2:idz*2+1])
                print("New sum:", new_sum)
                PVE_data[idx, idy, idz] = new_sum

    print("PVE sum:", np.sum(PVE_data))

    sino_file = nib.Nifti1Image(PVE_data, affine=file_affine, header=file_header)
    nib.save(sino_file, name[:-4] +"_xy256z89_PVE.nii")