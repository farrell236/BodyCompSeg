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

    image = sitk.ReadImage(f'{y_true_root}/{case}/image.nii.gz')
    y_mask = sitk.ReadImage(f'{y_true_root}/{case}/body-parts.nii.gz')
    y_true = sitk.ReadImage(f'{y_true_root}/{case}/body-regions.nii.gz')
    ts_pred = sitk.ReadImage(f'{ts_pred_root}/{case}.nii.gz')
    jf_pred = sitk.ReadImage(f'{jf_pred_root}/{case}.nii.gz')

    y_mask = (sitk.GetArrayFromImage(y_mask) == 1).astype('uint')
    image = sitk.GetArrayViewFromImage(image) * y_mask

    # Subcutaneous Fat
    y_true_1 = (sitk.GetArrayFromImage(y_true) == 1).astype('uint') * y_mask
    ts_pred_1 = (sitk.GetArrayFromImage(ts_pred) == 1).astype('uint') * y_mask
    jf_pred_1 = (sitk.GetArrayFromImage(jf_pred) == 2).astype('uint') * y_mask

    y_true_mean_hu_1 = np.average(image[y_true_1 != 0])
    ts_pred_mean_hu_1 = np.average(image[ts_pred_1 != 0])
    jf_pred_mean_hu_1 = np.average(image[jf_pred_1 != 0])
    # print(case, y_true_mean_hu_1, ts_pred_mean_hu_1, jf_pred_mean_hu_1)

    # Muscle
    y_true_2 = (sitk.GetArrayFromImage(y_true) == 2).astype('uint') * y_mask
    ts_pred_2 = (sitk.GetArrayFromImage(ts_pred) == 3).astype('uint') * y_mask
    jf_pred_2 = (sitk.GetArrayFromImage(jf_pred) == 3).astype('uint') * y_mask

    y_true_mean_hu_2 = np.average(image[y_true_2 != 0])
    ts_pred_mean_hu_2 = np.average(image[ts_pred_2 != 0])
    jf_pred_mean_hu_2 = np.average(image[jf_pred_2 != 0])
    # print(case, y_true_mean_hu_2, ts_pred_mean_hu_2, jf_pred_mean_hu_2)

    # Visceral Fat
    ts_pred_3 = (sitk.GetArrayFromImage(ts_pred) == 2).astype('uint')
    jf_pred_3 = (sitk.GetArrayFromImage(jf_pred) == 1).astype('uint')

    ts_pred_mean_hu_3 = np.average(image[ts_pred_3 != 0])
    jf_pred_mean_hu_3 = np.average(image[jf_pred_3 != 0])
    # print(case, ts_pred_mean_hu_3, jf_pred_mean_hu_3)

    # case, GT_fat_vol, GT_muscle_vol, Jianfei_fat_vol, Jianfei_muscle_vol, TS_fat_vol, TS_muscle_vol
    results.append({
        'case': case,
        'GT_sub_fat_mean_hu': y_true_mean_hu_1,
        'GT_muscle_mean_hu': y_true_mean_hu_2,
        'JF_sub_fat_mean_hu': jf_pred_mean_hu_1,
        'JF_vis_fat_mean_hu': jf_pred_mean_hu_3,
        'JF_muscle_mean_hu': jf_pred_mean_hu_2,
        'TS_sub_fat_mean_hu': ts_pred_mean_hu_1,
        'TS_vis_fat_mean_hu': ts_pred_mean_hu_3,
        'TS_muscle_mean_hu': ts_pred_mean_hu_2,
    })


results_df = pd.DataFrame(results)
results_df.to_csv('hu_calc.csv', index=False)


a=1

#           Subcutaneous Fat    Muscle      Visceral Fat
# SAROS     1                   2           -
# Jianfei   2                   3           1
# TS        1                   3           2