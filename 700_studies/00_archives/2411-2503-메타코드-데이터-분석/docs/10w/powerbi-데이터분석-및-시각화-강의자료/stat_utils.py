import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

from scipy.stats import chi2_contingency, ttest_ind, mannwhitneyu, ks_2samp, f_oneway
from sklearn.preprocessing import StandardScaler

def chi_square(array1, array2):
    """
    Perform a Chi-square test for independence between two categorical variables.

    Parameters
    ----------
    array1 : array-like
        The first categorical variable.
    array2 : array-like
        The second categorical variable.

    Returns
    -------
    chi2 : float
        The test statistic.
    p : float
        The p-value of the test.
    dof : int
        The degrees of freedom.
    expected : ndarray
        The expected frequencies in each category.
    contingency_table : pandas.DataFrame
        The contingency table of the observed frequencies.
    """
    contingency_table = pd.crosstab(array1, array2)
    chi2, p, dof, expected = chi2_contingency(contingency_table)
    return chi2, p, dof, expected, contingency_table


def anova_test(df, target_column, var):
    """
    Perform a one-way ANOVA test to compare means of a numerical variable across different categories of a categorical variable.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the data.
    target_column : str
        The name of the categorical target column.
    var : str
        The name of the numerical variable to test.

    Returns
    -------
    f_stat : float
        The test statistic.
    p_value : float
        The p-value of the test.
    """
    groups = [df[df[target_column] == category][var].dropna().values for category in df[target_column].unique()]
    f_stat, p_value = f_oneway(*groups)
    return f_stat, p_value


def numerical_test(array1, array2):
    """
    Perform statistical tests to compare two numerical variables.

    Parameters
    ----------
    array1 : array-like
        The first numerical variable.
    array2 : array-like
        The second numerical variable.

    Returns
    -------
    t_stat : float
        The t-test statistic.
    t_p : float
        The p-value of the t-test.
    ks_stat : float
        The Kolmogorov-Smirnov test statistic.
    ks_p : float
        The p-value of the Kolmogorov-Smirnov test.
    """
    scaler = StandardScaler()
    array = np.concatenate([array1, array2])
    array = scaler.fit_transform(array.reshape(-1, 1)).flatten()

    array1_norm = array[:len(array1)]
    array2_norm = array[len(array1):]

    t_stat, t_p = ttest_ind(array1_norm, array2_norm)
    ks_stat, ks_p = ks_2samp(array1_norm, array2_norm)

    return t_stat, t_p, ks_stat, ks_p

def statistical_tests_step1(df, target_column, analysis_columns):
    """
    Perform statistical tests to identify relevant variables influencing the target variable.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the data.
    target_column : str
        The name of the target column.
    analysis_columns : list of str
        The list of columns to analyze.

    Returns
    -------
    output : dict
        A dictionary containing the results of the statistical tests for each variable.
    relevant_columns : list of str
        A list of columns that are statistically significant.
    """
    output = dict()
    relevant_columns = list()
    target_unique_values = df[target_column].nunique()

    for var in analysis_columns:
        try:
            if pd.api.types.is_numeric_dtype(df[var]):
                if target_unique_values == 2:
                    group1 = df[df[target_column] == df[target_column].unique()[0]][var].values
                    group2 = df[df[target_column] == df[target_column].unique()[1]][var].values
                    t_stat, t_p, ks_stat, ks_p = numerical_test(group1, group2)
                    output[var] = {"t_stat": t_stat, "t_p": t_p, "ks_stat": ks_stat, "ks_p": ks_p}
                    if t_p <= 0.05 and ks_p <= 0.05:
                        print(f"Relevant : {var}")
                        relevant_columns.append(var)
                else:
                    f_stat, p_value = anova_test(df, target_column, var)
                    output[var] = {"f_stat": f_stat, "p_value": p_value}
                    if p_value <= 0.05:
                        print(f"Relevant : {var}")
                        relevant_columns.append(var)

            elif pd.api.types.is_object_dtype(df[var]):
                chi2, p, dof, expected, contingency_table = chi_square(df[var], df[target_column])
                output[var] = {"chi2": chi2, "p": p, "dof": dof, "expected": expected, "contingency_table": contingency_table}
                if p <= 0.05:
                    print(f"Relevant : {var}")
                    relevant_columns.append(var)
            else:
                raise NotImplementedError
        except Exception as e:
            print(f"Error processing {var}: {e}")
            continue

    return output, relevant_columns
