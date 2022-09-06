import SimpleITK as sitk
import numpy as np
from downloaddata import fetch_data as fdata
import os
from config import get_cfg_defaults

cfg = get_cfg_defaults()
cfg.freeze()

img1 = sitk.ReadImage(fdata("training_001_mr_T1.mha"))
img2 = sitk.ReadImage(fdata("training_001_ct.mha"))

outDir = os.path.join(cfg.INPUT.DIRECTORY, 'TestPatientData')
os.makedirs(outDir, exist_ok=True)

sitk.WriteImage(img1, os.path.join(outDir, 'T1.mha'))
sitk.WriteImage(img2, os.path.join(outDir, 'CT.mha'))

stats1 = sitk.StatisticsImageFilter()
stats1.Execute(img1)

stats2 = sitk.StatisticsImageFilter()
stats2.Execute(img2)

print(stats1.GetMinimum(), stats1.GetMaximum())
print(stats2.GetMinimum(), stats2.GetMaximum())

range1 = stats1.GetMaximum() - stats1.GetMinimum()
range2 = stats2.GetMaximum() - stats2.GetMinimum()

binFilt = sitk.BinaryThresholdImageFilter()
binFilt.SetLowerThreshold(stats1.GetMinimum() + range1*.1)
binFilt.SetUpperThreshold(stats1.GetMaximum())
mask1 = binFilt.Execute(img1)

binFilt.SetLowerThreshold(stats2.GetMinimum() + range2*.1)
binFilt.SetUpperThreshold(stats2.GetMaximum())
mask2 = binFilt.Execute(img2)

sitk.WriteImage(mask1, os.path.join(outDir, 'T1_mask.nii.gz'))
sitk.WriteImage(mask2, os.path.join(outDir, 'CT_mask.nii.gz'))