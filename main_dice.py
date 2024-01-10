import os

import numpy as np
import pandas as pd
import SimpleITK as sitk

from glob import glob
from tqdm import tqdm


a=1


def calculate_dice_score(prediction, label, region):
    # Apply the region mask
    masked_pred = prediction * region
    masked_label = label * region

    # Calculate true positives, false positives, and false negatives
    TP = np.sum(masked_pred * masked_label)
    FP = np.sum(masked_pred * (1 - masked_label))
    FN = np.sum((1 - masked_pred) * masked_label)

    # Calculate Dice score
    dice_score = 2 * TP / (2 * TP + FP + FN) if (2 * TP + FP + FN) != 0 else 0

    return dice_score


cases = sorted(map(os.path.basename, glob('/raid/houbb/saros-dataset/data/case_*')))

# cases = sorted(map(os.path.basename, glob('/raid/houbb/scratch/jianfei/BodyCompositionSegmentator/preds/*.nii.gz')))
# cases = [x.replace('.nii.gz', '') for x in cases]

y_true_root = '/raid/houbb/saros-dataset/data'
# y_pred_root = '/raid/houbb/scratch/ts_tissue_types'
y_pred_root = '/raid/houbb/scratch/jianfei/BodyCompositionSegmentator/preds'

results = []

for case in tqdm(cases):

    y_mask = sitk.ReadImage(f'{y_true_root}/{case}/body-parts.nii.gz')
    y_true = sitk.ReadImage(f'{y_true_root}/{case}/body-regions.nii.gz')
    y_pred = sitk.ReadImage(f'{y_pred_root}/{case}.nii.gz')

    y_mask = (sitk.GetArrayFromImage(y_mask) == 1).astype('uint')

    # Subcutaneous Fat
    y_true_1 = (sitk.GetArrayFromImage(y_true) == 1).astype('uint')
    y_pred_1 = (sitk.GetArrayFromImage(y_pred) == 2).astype('uint')
    dice_fat = calculate_dice_score(y_pred_1, y_true_1, y_mask)

    # Muscle
    y_true_2 = (sitk.GetArrayFromImage(y_true) == 2).astype('uint')
    y_pred_2 = (sitk.GetArrayFromImage(y_pred) == 3).astype('uint')
    dice_muscle = calculate_dice_score(y_pred_2, y_true_2, y_mask)

    results.append({
        'case': case,
        'dice_fat': dice_fat,
        'dice_muscle': dice_muscle
    })

    # print(f'{case}: {dice_fat:.3f} {dice_muscle:.3f}')

a=1


results_df = pd.DataFrame(results)
results_df.to_csv('jianfei_dice.csv', index=False)

a=1

#           Subcutaneous Fat    Muscle      Visceral Fat
# SAROS     1                   2           -
# Jianfei   2                   3           1
# TS        1                   3           2

