from scipy.ndimage import zoom
from scipy.io import loadmat
import numpy as np
import nibabel as nib
import glob
import os

Prefix = "PVC2x"
exper_count = 0

def process_data(data):
    
    px, py, pz = data.shape
    qx, qy, qz = (256, 256, 89)
    zoom_data = zoom(data, (qx/px, qy/py, qz/pz))
    
    (values,counts) = np.unique(zoom_data,return_counts=True)
    ind = np.argmax(counts)
    th_min = values[ind]
    print("background: ", th_min)
    zoom_data[zoom_data<th_min] = 0
    th_max = np.percentile(zoom_data, q=99.9)
    zoom_data[zoom_data>th_max] = th_max
    zoom_data = zoom_data / th_max
    print("Max: ", np.amax(zoom_data))
    print("Min: ", np.amin(zoom_data))


    print("Old dim:", data.shape)
    print("New dim:", zoom_data.shape)

    return zoom_data

tmpl_name = "./test_data/zeros_PET.nii"
tmpl_nii = nib.load(tmpl_name)
tmpl_header = tmpl_nii.header
tmpl_affine = tmpl_nii.affine

mat_list = glob.glob("./pet/*.mat")
mat_list.sort()
for mat_name in mat_list:
    print("-----------------------------------------------")
    exper_count += 1
    mdict = loadmat(mat_name)

    try:
        mat_data = mdict["reconImg"]
    except Exception:
        pass  # or you could use 'continue'

    try:
        mat_data = mdict["data"]
    except Exception:
        pass  # or you could use 'continue'

    save_data = process_data(mat_data)
    save_file = nib.Nifti1Image(save_data, affine=tmpl_affine, header=tmpl_header)
    save_name = os.path.basename(mat_name)[:-17]+"_ori.nii"
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
