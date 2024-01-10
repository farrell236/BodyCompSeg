import os

import numpy as np
import pandas as pd
import SimpleITK as sitk

from sklearn.metrics import cohen_kappa_score

from glob import glob
from tqdm import tqdm

import matplotlib.pyplot as plt

a=1


cases = sorted(map(os.path.basename, glob('/raid/houbb/saros-dataset/data/case_*')))

y_true_root = '/raid/houbb/saros-dataset/data'
ts_pred_root = '/raid/houbb/scratch/ts_tissue_types'
jf_pred_root = '/raid/houbb/scratch/jianfei/BodyCompositionSegmentator/preds'


a=1


results = []


for case in tqdm(cases):

    y_mask = sitk.ReadImage(f'{y_true_root}/{case}/body-parts.nii.gz')
    y_true = sitk.ReadImage(f'{y_true_root}/{case}/body-regions.nii.gz')
    ts_pred = sitk.ReadImage(f'{ts_pred_root}/{case}.nii.gz')
    jf_pred = sitk.ReadImage(f'{jf_pred_root}/{case}.nii.gz')

    y_mask = (sitk.GetArrayFromImage(y_mask) == 1).astype('uint')

    assert ts_pred.GetSpacing() == jf_pred.GetSpacing() == y_true.GetSpacing()

    unit_volume = np.prod(ts_pred.GetSpacing())

    # Subcutaneous Fat
    y_true_1 = (sitk.GetArrayFromImage(y_true) == 1).astype('uint') * y_mask
    ts_pred_1 = (sitk.GetArrayFromImage(ts_pred) == 1).astype('uint') * y_mask
    jf_pred_1 = (sitk.GetArrayFromImage(jf_pred) == 2).astype('uint') * y_mask

    true_volume_1 = np.sum(y_true_1) * unit_volume * 1e-3 # L^3
    ts_pred_volume_1 = np.sum(ts_pred_1) * unit_volume * 1e-3 # L^3
    jf_pred_volume_1 = np.sum(jf_pred_1) * unit_volume * 1e-3 # L^3
    # print(case, true_volume_1, ts_pred_volume_1, jf_pred_volume_1)

    # Muscle
    y_true_2 = (sitk.GetArrayFromImage(y_true) == 2).astype('uint') * y_mask
    ts_pred_2 = (sitk.GetArrayFromImage(ts_pred) == 3).astype('uint') * y_mask
    jf_pred_2 = (sitk.GetArrayFromImage(jf_pred) == 3).astype('uint') * y_mask

    true_volume_2 = np.sum(y_true_2) * unit_volume * 1e-3 # L^3
    ts_pred_volume_2 = np.sum(ts_pred_2) * unit_volume * 1e-3 # L^3
    jf_pred_volume_2 = np.sum(jf_pred_2) * unit_volume * 1e-3 # L^3
    # print(case, true_volume_2, ts_pred_volume_2, jf_pred_volume_2)

    # Visceral Fat
    ts_pred_3 = (sitk.GetArrayFromImage(ts_pred) == 2).astype('uint')
    jf_pred_3 = (sitk.GetArrayFromImage(jf_pred) == 1).astype('uint')

    ts_pred_volume_3 = np.sum(ts_pred_3) * unit_volume * 1e-3 # L^3
    jf_pred_volume_3 = np.sum(jf_pred_3) * unit_volume * 1e-3 # L^3
    # print(case, ts_pred_volume_3, jf_pred_volume_3)

    # case, GT_fat_vol, GT_muscle_vol, Jianfei_fat_vol, Jianfei_muscle_vol, TS_fat_vol, TS_muscle_vol
    results.append({
        'case': case,
        'GT_sub_fat_vol': true_volume_1,
        'GT_muscle_vol': true_volume_2,
        'JF_sub_fat_vol': jf_pred_volume_1,
        'JF_vis_fat_vol': jf_pred_volume_3,
        'JF_muscle_vol': jf_pred_volume_2,
        'TS_sub_fat_vol': ts_pred_volume_1,
        'TS_vis_fat_vol': ts_pred_volume_3,
        'TS_muscle_vol': ts_pred_volume_2,
    })


results_df = pd.DataFrame(results)
results_df.to_csv('vol_calc.csv', index=False)


a=1

#           Subcutaneous Fat    Muscle      Visceral Fat
# SAROS     1                   2           -
# Jianfei   2                   3           1
# TS        1                   3           2