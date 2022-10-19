# -*- coding: utf-8 -*-
"""Debug code for open issues."""
import shutil

import numpy as np
import pandas as pd

from sktime.classification.dummy import DummyClassifier
from sktime.classification.feature_based import SignatureClassifier
from sktime.datasets import (
    load_from_tsfile,
    load_gunpoint,
    load_japanese_vowels,
    load_plaid,
    load_UCR_UEA_dataset,
    write_dataframe_to_tsfile,
)
from sktime.transformations.panel.shapelet_transform import RandomShapeletTransform
from sktime.transformations.panel.signature_based._signature_method import (
    SignatureTransformer,
)
from sktime.utils._testing.panel import _make_panel_X
from sktime.utils.sampling import stratified_resample

# debug_load_uea_dataset(split="TRAIN")
# debug_load_uea_dataset(split="TEST")
# debug_load_uea_dataset(return_type="numpy3d")


def debug_write_dataframe_to_ts_file(name, extract_path=None):
    """See https://github.com/sktime/sktime/issues/3499."""
    from sktime.datatypes import check_is_scitype

    #    X, y = load_UCR_UEA_dataset(name=name, extract_path="C:\\Temp",
    #                                return_type="numpy3D", split="TRAIN")
    #    print(" series shape  = ",X.shape)
    X, y = load_UCR_UEA_dataset(name=name, extract_path=extract_path)
    X_valid, _, X_metadata = check_is_scitype(X, scitype="Panel", return_metadata=True)
    print(X_metadata)
    series_length = X.iloc[0, 0].size
    print(" series length  = ", series_length)
    write_dataframe_to_tsfile(
        X,
        "C:\\Temp\\WriteTest",
        class_value_list=y,
        equal_length=X_metadata["is_equal_length"],
        problem_name=name,
    )


def debug_load_and_save():
    """Issue?."""
    X1, y1 = load_gunpoint()
    write_dataframe_to_tsfile(
        X1,
        "C:\\Temp\\WriteTest",
        class_value_list=y1,
        equal_length=True,
        problem_name="GunPoint",
    )
    X2, y2 = load_from_tsfile(
        full_file_path_and_name="C:\\Temp\\WriteTest\\GunPoint" "\\GunPoint.ts"
    )
    assert np.array_equal(y1, y2)

    X1, y1 = load_japanese_vowels()
    print("Type of y1 = ", type(y1))
    write_dataframe_to_tsfile(
        X1,
        "C:\\Temp\\WriteTest",
        class_value_list=y1,
        equal_length=False,
        problem_name="JapaneseVowels",
    )
    X2, y2 = load_from_tsfile(
        full_file_path_and_name="C:\\Temp\\WriteTest\\JapaneseVowels"
        "\\JapaneseVowels.ts"
    )
    assert np.array_equal(y1, y2)

    X1, y1 = load_plaid()
    print("Type of y1 = ", type(y1))
    write_dataframe_to_tsfile(
        X1,
        "C:\\Temp\\WriteTest",
        class_value_list=y1,
        equal_length=False,
        problem_name="Fred",
    )
    X2, y2 = load_from_tsfile(
        full_file_path_and_name="C:\\Temp\\WriteTest\\Fred" "\\Fred.ts"
    )
    assert np.array_equal(y1, y2)


from sktime.datasets._data_io import _load_provided_dataset


def debug_testing_load_and_save_3499():
    """Test load and save, related to https://github.com/sktime/sktime/issues/3499."""
    from datasets import write_panel_to_tsfile

    return_type = "nested_univ"
    dataset_name = "ItalyPowerDemand"
    X, y = _load_provided_dataset(dataset_name, split="TRAIN", return_type=return_type)
    write_panel_to_tsfile(data=X, path="./Temp", target=y, problem_name=dataset_name)
    load_path = f"./Temp/{dataset_name}/{dataset_name}.ts"
    newX, newy = load_from_tsfile(
        full_file_path_and_name=load_path, return_data_type=return_type
    )
    assert np.array_equal(y, newy)
    shutil.rmtree("./Temp")


def debug_callibration_2662():
    """Issue 2662 https://github.com/sktime/sktime/issues/2662."""
    import sklearn.calibration
    import sklearn.pipeline

    from sktime.datasets import load_arrow_head, load_basic_motions
    from sktime.transformations.panel import rocket
    from sktime.transformations.panel.padder import PaddingTransformer

    X, y = load_basic_motions(return_X_y=True)
    n_jobs = -1

    featurizer_rocket = rocket.MiniRocket(n_jobs=n_jobs)
    featurizer_rocket = rocket.Rocket(n_jobs=n_jobs)
    featurizer_rocket = rocket.MultiRocket(n_jobs=n_jobs)
    featurizer_rocket = rocket.MiniRocketMultivariate(n_jobs=n_jobs)
    featurizer_rocket = rocket.MultiRocketMultivariate(n_jobs=n_jobs)
    classifier = sklearn.ensemble.HistGradientBoostingClassifier(
        loss="categorical_crossentropy"
    )

    base_estimator = sklearn.pipeline.Pipeline(
        [
            ("featurizer_rocket", featurizer_rocket),
            ("classifier", classifier),
        ],
    )

    calibrated_model = sklearn.calibration.CalibratedClassifierCV(
        base_estimator,
        cv=2,
        n_jobs=n_jobs,
    )

    calibrated_model.fit(X, y)


if __name__ == "__main__":
    debug_callibration_2662()
