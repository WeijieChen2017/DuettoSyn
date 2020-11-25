from scipy.ndimage import zoom
from scipy.io import loadmat
import numpy as np
import nibabel as nib
import glob
import os

Prefix = "PVC2x"
exper_count = 0

def maxmin_norm(data, pMax=99.9, pMin=0.00):
    # MAX = np.amax(data)
    # MIN = np.amin(data)
    MAX = np.percentile(data, q=pMax)
    # MIN = np.percentile(data, q=pMin)
    MIN = 0
    data = (data - MIN)/(MAX-MIN)
    return data

def process_data(data):
    (values,counts) = np.unique(data,return_counts=True)
    ind = np.argmax(counts)
    th = values[ind]
    print("background: ", th)
    data[data<th] = 0
    # data[data>1] = 1
    px, py, pz = data.shape
    qx, qy, qz = (256, 256, 89)
    zoom_data = zoom(data, (qx/px, qy/py, qz/pz))
    print("Old dim:", data.shape)
    print("New dim:", zoom_data.shape)

    zoom_data = maxmin_norm(zoom_data)
    return zoom_data

leah_list = glob.glob("./pet/*.mat")
for leah_name in leah_list:
    exper_count += 1
    name = leah_name
    mdict = loadmat(name)

    try:
        data = mdict["reconImg"]
    except Exception:
        pass  # or you could use 'continue'

    try:
        data = mdict["data"]
    except Exception:
        pass  # or you could use 'continue'

    tmpl_name = "./recon/example.nii"
    file_nii = nib.load(tmpl_name)
    file_data = file_nii.get_fdata()
    file_header = file_nii.header
    file_affine = file_nii.affine

    save_data = process_data(data)
    save_file = nib.Nifti1Image(save_data, affine=file_affine, header=file_header)
    save_name = os.path.basename(name)[:-17]+"_ori.nii"
    nib.save(save_file, save_name)
    print(save_name)

    # # pure_dir = "./recon/"+expername+"/pure/"
    # # blur_dir = "./recon/"+expername+"/blur/"
    # # test_dir = "./recon/"+expername+"/test/"    

    # # os.system("mkdir "+pure_dir)
    # # os.system("mkdir "+blur_dir)
    # # os.system("mkdir "+test_dir)

    # filename = os.path.basename(name)[:-17]
    # new_dataname = filename+"_op_z89_xy512_f4.nii"
    # nib.save(sino_file, blur_dir+new_dataname)
    # nib.save(sino_file, test_dir+new_dataname)
    # os.system("mv ./data/"+filename+".nii "+pure_dir+new_dataname)
    # os.system("zip -r "+expername+"zip "+expername)
