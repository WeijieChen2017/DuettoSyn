clear
duettoPath = '/data/data_mrcv2/MCMILLAN_GROUP/10_software/duetto/duetto_v02.06_Mar2020';
addpath(genpath(duettoPath));

files = dir(fullfile("./", '*.mat'));
for k=1:22
name = files(k).name(1:7)
img = load(strcat(name,'.mat'));
img = img.data;

reconAlgorithm = 'OSEM-PSF';
userConfig = ptbUserConfig(reconAlgorithm);
userConfig.nX = size(img,1);
userConfig.radialFov = 240;

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

fprintf('Forward projecting\n');
sino = ptbForwardProject(imageFrame, subsetSino, scanner, reconParams.fwdProjFunc);
% save(strcat(name+'_sino_bravo.mat', 'sino'))

fprintf('Applying PSF to sinogram\n');
psfMatrix = ptbReadFile(reconParams.corrOptions.psfOptions.sinoRadialFilename);
sino = ptbApplySinoSpacePsf(sino, subsetSino, psfMatrix, ...
    reconParams.corrOptions.psfOptions, reconParams.fwdProjFunc);

sinoFile = strcat(name, '_emission_bravo.sav');
fprintf('Writing sinogram to %s\n', sinoFile);
ptbWriteSaveFile(sino, sinoFile);

reconAlgorithm = 'OSEM-PSF';
userConfig = ptbUserConfig(reconAlgorithm);

userConfig.nX = 256;        % number of image columns
userConfig.radialFov = 240; % radial FOV in mm for image

userConfig.nSubsets = 28;
userConfig.nIterations = 4;
userConfig.decayCorrFlag = 0;
userConfig.durationCorrFlag = 0;
userConfig.randomsCorrFlag = 0;
userConfig.scatterCorrFlag = 0;
userConfig.attenCorrFlag = 0;
userConfig.normDtPucCorrFlag = 0;
userConfig.postFilterFwhm = 4;
userConfig.verbosity = PtbVerboseEnum.VERBOSE;
sinoFile = strcat(name, '_emission_bravo.sav');

%% Create necessary parameter structures
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
ftrParams.ftrCorrFlag = 0;
ftrParams.ftrDetectFlag = 0;
ftrMask = [];
filenames.emission = sinoFile;
initialImg = ptbMakeReconImageMask(reconParams.nX, reconParams.nZ);

%%
fprintf('Running recon\n');
reconImg = ptbOsem(initialImg, filenames, generalParams, ...
    reconParams, sinoParams, ftrParams, ftrMask, scanner);

%%
reconFile = strcat(name, '_recon_OP.sav');
reconMat = strcat(name, '_recon_OP.mat');
fprintf('Writing recon to %s\n', reconFile);
ptbWriteSaveFile(reconImg, reconFile);
save(strcat(name, '_reconParams.par'), 'generalParams', 'reconParams')
save(reconMat, 'reconImg')

end