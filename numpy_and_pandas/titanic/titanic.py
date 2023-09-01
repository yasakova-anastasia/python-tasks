import typing as tp

import pandas as pd


def male_age(df: pd.DataFrame) -> float:
    """
    Return mean age of survived men, embarked in Southampton with fare > 30
    :param df: dataframe
    :return: mean age
    """
    return df.query('Survived == 1 and Sex == "male" and Embarked == "S" and Fare>30')['Age'].mean()


def nan_columns(df: pd.DataFrame) -> tp.Iterable[str]:
    """
    Return list of columns containing nans
    :param df: dataframe
    :return: series of columns
    """
    return {column for column in df.columns if any(pd.isnull(df[column]))}


def class_distribution(df: pd.DataFrame) -> pd.Series:
    """
    Return Pclass distrubution
    :param df: dataframe
    :return: series with ratios
    """
    size = df['Pclass'].value_counts().sum()
    res = pd.Series(data=[df['Pclass'].value_counts()[1] / size,
                          df['Pclass'].value_counts()[2] / size, df['Pclass'].value_counts()[3] / size],
                    index=[1, 2, 3], name="Pclass")
    return res


def families_count(df: pd.DataFrame, k: int) -> int:
    """
    Compute number of families with more than k members
    :param df: dataframe,
    :param k: number of members,
    :return: number of families
    """
    a = {}
    for i in df['Name']:
        val = i.split(',')[0]
        if val not in a:
            a[val] = 1
        else:
            a[val] += 1
    count = 0
    for i in a:
        if a[i] > k:
            count += 1
    return count


def mean_price(df: pd.DataFrame, tickets: tp.Iterable[str]) -> float:
    """
    Return mean price for specific tickets list
    :param df: dataframe,
    :param tickets: list of tickets,
    :return: mean fare for this tickets
    """
    a = df.loc[df['Ticket'].isin(tickets)]
    b = a['Fare'].mean()
    return b


def max_size_group(df: pd.DataFrame, columns: list[str]) -> tp.Iterable[tp.Any]:
    """
    For given set of columns compute most common combination of values of these columns
    :param df: dataframe,
    :param columns: columns for grouping,
    :return: list of most common combination
    """
    pairs = df.groupby(columns)['PassengerId'].count()
    count = 0
    idx = 0
    j = 0
    for i in pairs:
        if i > count:
            idx = j
            count = i
        j += 1
    return pairs.index[idx]


def dead_lucky(df: pd.DataFrame) -> float:
    """
    Compute dead ratio of passengers with lucky tickets.
    A ticket is considered lucky when it contains an even number of digits in it
    and the sum of the first half of digits equals the sum of the second part of digits
    ex:
    lucky: 123222, 2671, 935755
    not lucky: 123456, 62869, 568290
    :param df: dataframe,
    :return: ratio of dead lucky passengers
    """
    def is_lucky(val: str) -> int:
        if len(val) % 2 != 0:
            return 0
        sum1 = 0
        sum2 = 0
        for i in range(len(val) // 2):
            if val[i] in '0123456789':
                sum1 += int(val[i])
            else:
                return 0
            if val[len(val) - 1 - i] in '0123456789':
                sum2 += int(val[len(val) - 1 - i])
            else:
                return 0
        if sum1 == sum2:
            return 1
        else:
            return 0

    df['lucky'] = df['Ticket'].apply(is_lucky)
    size = df['lucky'].value_counts()[1]
    df = df.query('Survived == 0')
    return df['lucky'].value_counts()[1] / size
