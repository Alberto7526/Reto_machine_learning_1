"""
In this module we store prepare the sataset for machine learning experiments.
"""

import typing as t
import typing_extensions as te

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


class DatasetReader(te.Protocol):
    def __call__(self) -> pd.DataFrame:
        ...


SplitName = te.Literal["train", "test"]


def get_dataset(reader: DatasetReader, splits: t.Iterable[SplitName]):
    df = reader()
    # df = clean_dataset(df)

    y = df["y"]
    X = df.drop(columns=["y"])
    X = X.astype({k: str for k in get_categorical_variables_values_mapping().keys()})
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=1
    )
    split_mapping = {"train": (X_train, y_train), "test": (X_test, y_test)}
    return {k: split_mapping[k] for k in splits}


# def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
#     cleaning_fn = _chain(
#         [
#             _fix_unhandled_nulls,
#         ]
#     )
#     df = cleaning_fn(df)
#     return df


# def _chain(functions: t.List[t.Callable[[pd.DataFrame], pd.DataFrame]]):
#     def helper(df):
#         for fn in functions:
#             df = fn(df)
#         return df

#     return helper

# def _fix_unhandled_nulls(df):
#     df.dropna(inplace=True)
#     return df


def get_categorical_column_names() -> t.List[str]:
    return "region".split(",")


def get_binary_column_names() -> t.List[str]:
    return "sex,smoker".split(",")


def get_numeric_column_names() -> t.List[str]:
    return "age,bmi,children".split(",")


def get_column_names() -> t.List[str]:
    return "age,sex,bmi,children,smoker,region".split(",")


def get_categorical_variables_values_mapping() -> t.Dict[str, t.Sequence[str]]:
    return {
        "sex":("female","male"),
        "smoker":("no","yes"),
        "region": ("northeast","southwest","northwest","southeast")       
    }
