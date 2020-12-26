import os

for idx in range(369):
	idx_str = "{0:0>3}".format(idx)
	print(idx_str)
	cmd_1 = "3dresample -dxyz 1.172 1.172 2.78 -prefix z"+idx_str+" -inset BraTS20_Training_"+idx_str"_t1_inv.nii"
	cmd_2 = "3dZeropad -I 16 -S 17 -A 25 -P 26 -L 25 -R 26 z"+idx_str+"+orig"
	cmd_3 = "3dAFNItoNIFTI -prefix z"+idx_str+" zeropad+orig"
	cmd_4 = "rm -f zeropad+orig.BRIK"
	cmd_5 = "rm -f zeropad+orih.HEAD"
	cmd_6 = "mv z"+idx_str+" ../inv_RSZP"
	for cmd in [cmd_1, cmd_2, cmd_3, cmd_4, cmd_5, cmd_6]
		os.system(cmd_6)
# 3dresample -dxyz 1.172 1.172 2.78 -prefix test -inset BraTS20_Training_001_t1_inv.nii
# 3dZeropad -I 16 -S 17 -A 25 -P 26 -L 25 -R 26 Z001+orig -prefix 123
# 3dAFNItoNIFTI -prefix test test+orig