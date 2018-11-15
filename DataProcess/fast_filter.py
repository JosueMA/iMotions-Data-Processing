# Given a data frame we need to return only the desired subset
# according to a user-specified list of rules. To maintain performance,
# each filter will return a boolean index, and the boolean indices assembled
# into the final boolean index which will determine the output data frame.
from typing import Callable, List
import pandas as pd

# A FilterRule should return a boolean index denoting which rows of the dataframe
# should be included.
FilterRule = Callable[[pd.DataFrame], pd.Series]


def fast_filter(df, include=None, exclude=None, columns=None) -> pd.DataFrame:
    """
Filters df rows according to the provided inclusion and exclusion filters.

A row in the dataframe is included if any of the include rules mark the row as True,
unless one or more exclusion rules mark the row as True. Exclusion rules override
inclusion rules.

    :param df: Dataframe to filter
    :type df: pd.DataFrame
    :param include:
    :type include: List[FilterRule]
    :param exclude:
    :type exclude: List[FilterRule]
    :param columns: List of columns to include. None returns all columns
    :return:
    """
    if exclude is None:
        exclude = []
    if include is None:
        include = []

    include_indices = []
    for rule in include:
        include_indices.append(rule(df))

    include_rows = pd.concat(include_indices, axis=1).any(axis=1)

    exclude_indices = []
    for rule in exclude:
        exclude_indices.append(rule(df))

    exclude_rows = pd.concat(exclude_indices, axis=1).any(axis=1)

    if columns:
        return df.loc[include_rows & ~ exclude_rows, columns]
    else:
        return df[include_rows & ~ exclude_rows]