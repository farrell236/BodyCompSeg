import os

import numpy as np
import pandas as pd
import SimpleITK as sitk

from sklearn.metrics import cohen_kappa_score

from glob import glob
from tqdm import tqdm


a=1


cases = sorted(map(os.path.basename, glob('/raid/houbb/saros-dataset/data/case_*')))

y_true_root = '/raid/houbb/saros-dataset/data'
ts_pred_root = '/raid/houbb/scratch/ts_tissue_types'
jf_pred_root = '/raid/houbb/scratch/jianfei/BodyCompositionSegmentator/preds'


a=1


def calculate_kappa_score(rater1, rater2, region):

    rater1 = rater1[region != 0].ravel()
    rater2 = rater2[region != 0].ravel()

    return cohen_kappa_score(rater1, rater2)


results = []


for case in tqdm(cases):

    y_mask = sitk.ReadImage(f'{y_true_root}/{case}/body-parts.nii.gz')
    ts_pred = sitk.ReadImage(f'{ts_pred_root}/{case}.nii.gz')
    jf_pred = sitk.ReadImage(f'{jf_pred_root}/{case}.nii.gz')

    y_mask = (sitk.GetArrayFromImage(y_mask) == 1).astype('uint')

    # Subcutaneous Fat
    ts_pred_1 = (sitk.GetArrayFromImage(ts_pred) == 1).astype('uint')
    jf_pred_1 = (sitk.GetArrayFromImage(jf_pred) == 2).astype('uint')
    kappa_score_1 = calculate_kappa_score(ts_pred_1, jf_pred_1, y_mask)

    # Muscle
    ts_pred_2 = (sitk.GetArrayFromImage(ts_pred) == 3).astype('uint')
    jf_pred_2 = (sitk.GetArrayFromImage(jf_pred) == 3).astype('uint')
    kappa_score_2 = calculate_kappa_score(ts_pred_2, jf_pred_2, y_mask)

    # Visceral Fat
    ts_pred_3 = (sitk.GetArrayFromImage(ts_pred) == 2).astype('uint')
    jf_pred_3 = (sitk.GetArrayFromImage(jf_pred) == 1).astype('uint')
    kappa_score_3 = calculate_kappa_score(ts_pred_3, jf_pred_3, y_mask)

    results.append({
        'case': case,
        'subcutaneous_fat': kappa_score_1,
        'muscle': kappa_score_2,
        'visceral_fat': kappa_score_3,
    })


results_df = pd.DataFrame(results)
results_df.to_csv('cohen_kappa.csv', index=False)


a=1

#           Subcutaneous Fat    Muscle      Visceral Fat
# SAROS     1                   2           -
# Jianfei   2                   3           1
# TS        1                   3           2