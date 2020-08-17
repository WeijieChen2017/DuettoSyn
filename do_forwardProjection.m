
% Add the following to your Matlab path
%   /data/data_mrcv2/MCMILLAN_GROUP/10_software/duetto/duetto_v02.06_Mar2020

% Load an image
img = ptbReadSaveFile('/path/to/image.sav');

%% Set up a basic recon 
% Set the radial FOV to match your image.
% The code will assume that your image has 89 planes with a plane
%   separation of 2.78 mm. Make sure this is the case.
% The transaxial pixel size will be set according to what you set as the
%   radialFOV below.
reconAlgorithm = 'OSEM-PSF';
userConfig = ptbUserConfig(reconAlgorithm);
userConfig.nX = size(img,1);
userConfig.radialFov = 300; % radial FOV in mm for image

%% Perform forward projection
% This should just run as is, you shouldn't need to change anything
% Create necessary parameter structures
% Create bare RDF structure
rdf.sharc_rdf_pet_exam_data.scannerDesc = 'SIGNA PET/MR';
rdf.sharc_rdf_sys_geo_data.axialBlocksPerModule = 5;
sysConfig = ptbSystemConfig(rdf);
scanner = PtbScanner(sysConfig.name);
scanner = config(scanner, sysConfig);
scanner.calParams = config(scanner.calParams, userConfig);
sinoParams = PtbSinogram;
sinoParams = config(sinoParams, sysConfig);
generalParams = ptbInitGeneralParams(userConfig);
reconParams = ptbInitReconParams(scanner, sysConfig, userConfig, generalParams);

nSubsets = 1;
iSubset = 1;
subsetLut = ptbGenSubsetLut(nSubsets, sinoParams.nPhi, ...
    reconParams.subsetSelectionScheme, reconParams.subsetAngleOffset);
subsetSino = sinoParams;
subsetSequence = ptbGenSubsetSequence(nSubsets, sinoParams.nPhi);
subsetAngles = subsetLut(:, subsetSequence(iSubset));
subsetSino.phiAngles = subsetAngles;

imageFrame = reconParams.imParams;
imageFrame.data = img;

tic
sino = ptbForwardProject(imageFrame, subsetSino, scanner, reconParams.fwdProjFunc);
toc

% If you add the following to your Matlab path 
%   /data/data_mrcv2/MCMILLAN_GROUP/10_software/duetto/lmDuetto_v02.06.beta_Jul2020
%   then you can view the sinogram like this:
% ximage(sino)


