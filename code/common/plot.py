#!/usr/bin/env python3

"""
Python file containing all common and frequently
ran code for the analysis of the Caribbean data.
--------------------------------------------------
Created on 04/03/2023. Last updated on 04/03/2023.
Written by Andrei Pascu, Yale College '23.
--------------------------------------------------
"""

import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm

# Display a pre-pandemic trendline to predict variable
# outcomes in the absence of the 2020 pandemic in order
# to highlight the impact of COVID-19.
def gen_did_plot(
    df: pd.DataFrame,
    y_name: str,
    x_name: str = 'yr',
    x0: int = 2010,
    x1: int = 2021,
    primary_color: str = '#1f77b4',
    secondary_color: str = 'lightblue',
    trendline_color: str = 'darkblue',
    show_trendline: bool = True,
    bar_width: float = 0.8,
    bar_offset: float = 0,
):
    # Add difference-in-differences vertical line
    plt.axvline(x=2019.51, color='black')

    # Determine pre-pandemic trendline using OLS
    x = df.loc[df[x_name] < 2020, x_name]
    y = df.loc[df[x_name] < 2020, y_name]
    reg = sm.OLS(y, sm.add_constant(x)).fit()
    alpha, beta = reg.params.const, reg.params[x_name]
    predict = lambda _x: alpha + beta * _x

    # Add pre-pandemic trendline to plot
    if show_trendline:
        x = pd.DataFrame(range(x0 - 1, 2020))
        plt.plot(x, predict(x), color=trendline_color)
        x = pd.DataFrame(range(2019, x1 + 2))
        plt.plot(x, predict(x), color=trendline_color, linestyle='dashed')

    # Display post-2020 predictions in the absence of COVID-19
    x = df.loc[df['yr'] >= 2020, x_name]
    y = df.loc[df['yr'] >= 2020, y_name]
    plt.bar(x + bar_offset, predict(x), color=secondary_color, edgecolor='black', width=bar_width)
    # for i in range(len(x)):
    #     plt.text(
    #         2020 + i + bar_offset, y.iloc[i] + text_offset,
    #         '{:,.0f}'.format(predict(2020 + i) - y.iloc[i]),
    #         ha='center', rotation='vertical',
    #     )

    # Show data
    plt.bar(df[x_name] + bar_offset, df[y_name], color=primary_color, edgecolor='black', width=bar_width)
