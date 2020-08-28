name = 'mri89FOV240';

reconAlgorithm = 'OSEM';
userConfig = ptbUserConfig(reconAlgorithm);

userConfig.nX = 512;        % number of image columns
userConfig.radialFov = 240; % radial FOV in mm for image

userConfig.nSubsets = 28;
userConfig.nIterations = 4;
userConfig.decayCorrFlag = 0;
userConfig.durationCorrFlag = 0;
userConfig.randomsCorrFlag = 0;
userConfig.scatterCorrFlag = 0;
userConfig.attenCorrFlag = 0;
userConfig.normDtPucCorrFlag = 0;
userConfig.verbosity = PtbVerboseEnum.VERBOSE;
sinoFile = strcat(name, '_emission.sav');

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
reconFile = strcat(name, '_recon.sav');
reconMat = strcat(name, '_recon.mat');
fprintf('Writing recon to %s\n', reconFile);
ptbWriteSaveFile(reconImg, reconFile);
save(strcat(name, '_reconParams.par'), 'generalParams', 'reconParams')
save(reconMat, 'reconImg')
