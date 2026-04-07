import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def plot_two_categorical(df, column1, column2, plot_type='barplot'):
    """
    Plot the relationship between two categorical variables using a bar plot or heatmap.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the data.
    column1 : str
        The name of the first categorical column.
    column2 : str
        The name of the second categorical column.
    plot_type : str, optional
        The type of plot to create: 'barplot' or 'heatmap'. Default is 'barplot'.

    Returns
    -------
    fig : plotly.graph_objs._figure.Figure
        The Plotly figure object representing the plot.
    """
    # Create a crosstab to count occurrences
    crosstab = pd.crosstab(df[column1], df[column2]).reset_index()

    if plot_type == 'barplot':
        # Melt the crosstab for better plotting
        crosstab_melted = crosstab.melt(id_vars=column1, value_vars=crosstab.columns[1:])
        
        # Bar plot using Plotly
        fig = px.bar(crosstab_melted, x=column1, y='value', color=column2, barmode='group',
                     labels={'value':'Count'}, title=f'Counts of {column1} and {column2} Combinations')
        
    elif plot_type == 'stacked_barplot':
        crosstab_percentage = pd.crosstab(df[column1], df[column2], normalize='index').reset_index()
        crosstab_melted = crosstab_percentage.melt(id_vars=column1, value_vars=crosstab_percentage.columns[1:])
        
        # 100% Stacked bar plot using Plotly
        fig = px.bar(crosstab_melted, x=column1, y='value', color=column2, barmode='stack',
                     labels={'value':'Percentage'}, title=f'100% Stacked Barplot of {column1} and {column2} Combinations')
    
    elif plot_type == 'heatmap':
        # Create a crosstab without resetting index for heatmap
        crosstab = pd.crosstab(df[column1], df[column2])
        
        # Heatmap using Plotly
        fig = px.imshow(crosstab, text_auto=True, color_continuous_scale=['#CBE2B5', '#86AB89'],
                        labels={'color':'Count'}, title=f'Heatmap of {column1} and {column2} Combinations')
    else:
        raise ValueError("plot_type must be either 'barplot' or 'heatmap'")
    return fig



def plot_count_plot(df: pd.DataFrame, column_name: str, color_column: str = None) -> go.Figure:
    """
    Generate a count plot for a specified column in the DataFrame using Plotly.
    If an additional column is provided, use it for facet differentiation; otherwise, generate a single plot.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the data.
    column_name : str
        The name of the column for which to create the count plot.
    color_column : str, optional
        The name of the column used for facet differentiation. Default is None.

    Returns
    -------
    plotly.graph_objs._figure.Figure
        The Plotly figure object representing the count plot.
    """
    category_order = df[column_name].value_counts().index.tolist()
    
    if color_column is None:
        fig = px.histogram(df, x=column_name, title=f'Count Plot of {column_name}', category_orders={column_name: category_order})
    else:
        print(color_column)
        unique_values = df[color_column].unique()
        num_plots = len(unique_values)

        # Create subplots
        fig = make_subplots(rows=1, cols=num_plots, shared_yaxes=False, subplot_titles=[str(val) for val in unique_values])

        # Add traces to subplots
        for i, value in enumerate(unique_values):
            filtered_df = df[df[color_column] == value]
            fig.add_trace(
                go.Histogram(x=filtered_df[column_name], name=str(value)),
                row=1, col=i+1
            )

        # Update layout to synchronize x-axes order
        for i in range(num_plots):
            fig.update_xaxes(categoryorder='array', categoryarray=category_order, row=1, col=i+1)

        fig.update_layout(title_text=f'Count Plot of {column_name} by {color_column}')
    
    return fig

def plot_histogram(df: pd.DataFrame, column_name: str, color_column: str = None) -> go.Figure:
    """
    Generate a histogram for a specified column in the DataFrame using Plotly.
    If an additional column is provided, use it for facet differentiation; otherwise, generate a single plot.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the data.
    column_name : str
        The name of the column for which to create the histogram.
    color_column : str, optional
        The name of the column used for facet differentiation. Default is None.

    Returns
    -------
    plotly.graph_objs._figure.Figure
        The Plotly figure object representing the histogram.
    """
    if color_column is None:
        fig = px.histogram(df, x=column_name, title=f'Histogram of {column_name}')
    else:
        unique_values = df[color_column].unique()
        num_plots = len(unique_values)

        # Create subplots
        fig = make_subplots(rows=1, cols=num_plots, shared_yaxes=False, subplot_titles=[str(val) for val in unique_values])

        # Add traces to subplots
        for i, value in enumerate(unique_values):
            filtered_df = df[df[color_column] == value]
            fig.add_trace(
                go.Histogram(x=filtered_df[column_name], name=str(value)),
                row=1, col=i+1
            )

        fig.update_layout(title_text=f'Histogram of {column_name} by {color_column}')
    
    return fig


def plot_dataframe(df: pd.DataFrame, color_column: str = None) -> None:
    """
    Generate and display count plots or histograms for all columns in the DataFrame.
    For numeric columns, generate histograms.
    For categorical columns, generate count plots.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the data.

    Returns
    -------
    None
    """
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            fig = plot_histogram(df, column, color_column)
        elif pd.api.types.is_object_dtype(df[column]):
            fig = plot_count_plot(df, column, color_column)
        else:
            continue
        fig.show()

def plot_observed_vs_expected(array1, array2):
    chi2, p, dof, expected, contingency_table = chi_square(array1, array2)
    
    # Convert expected to a DataFrame with the same index and columns as the contingency table
    expected_df = pd.DataFrame(expected, index=contingency_table.index, columns=contingency_table.columns)
    
    # Melt the DataFrames for easier plotting with Seaborn
    observed_melted = contingency_table.reset_index().melt(id_vars=contingency_table.index.name)
    expected_melted = expected_df.reset_index().melt(id_vars=expected_df.index.name)
    
    # Add a column to distinguish between observed and expected
    observed_melted['Type'] = 'Observed'
    expected_melted['Type'] = 'Expected'
    
    # Combine the melted DataFrames
    combined_df = pd.concat([observed_melted, expected_melted])
    
    # Plotting
    plt.figure(figsize=(12, 8))
    sns.barplot(x='index', y='value', hue='Type', data=combined_df, ci=None)
    plt.xlabel(array1.name if array1.name else 'Variable 1')
    plt.ylabel('Frequency')
    plt.title('Observed vs Expected Frequencies')
    plt.legend(title='Type')
    plt.show()
