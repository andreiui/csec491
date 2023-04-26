#!/usr/bin/env python3

"""
Python file containing all common and frequently
ran code for the analysis of the Caribbean data.
--------------------------------------------------
Created on 04/03/2023. Last updated on 04/24/2023.
Written by Andrei Pascu, Yale College '23.
--------------------------------------------------
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Display a pre-pandemic trendline to predict variable
# outcomes in the absence of the 2020 pandemic in order
# to highlight the impact of COVID-19
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
    show_confidence: bool = True,
    bar_width: float = 0.8,
    bar_offset: float = 0,
) -> tuple[float, float]:
    df = pd.DataFrame(df)

    # Add post-pandemic indicator variable
    df['ind_post'] = (df['yr'] >= 2020)

    # Add difference-in-differences vertical line
    plt.axvline(x=2019.5, color='black')

    # Determine pre-pandemic trendline using OLS
    reg = smf.ols(f"{y_name} ~ {x_name} + ind_post", data=df).fit()
    effect, stderr = reg.params['ind_post[T.True]'], reg.bse['ind_post[T.True]']
    predict = lambda _x: reg.params['Intercept'] + reg.params[x_name] * _x

    # Display post-2020 predictions in the absence of COVID-19
    x = df.loc[df[x_name] >= 2020, x_name]
    plt.bar(x + bar_offset, predict(x), color=secondary_color, width=bar_width)

    # Show data
    plt.bar(df[x_name] + bar_offset, df[y_name], color=primary_color, width=bar_width)

    if show_trendline:
        # Show hypothetical trendline in the absence of COVID-19
        x = list(range(x0 - 1, 2020)) + [2019.5]
        plt.plot(x, [predict(_x) for _x in x], color=trendline_color)
        x = [2019.5] + list(range(2020, x1 + 2))
        plt.plot(x, [predict(_x) for _x in x], color=trendline_color, linestyle='dotted')

        # Show pandemic impact
        plt.plot(x, [predict(_x) for _x in x] + effect, color=trendline_color)

        # Show confidence band
        if show_confidence:
            plt.fill_between(
                x,
                [predict(_x) for _x in x] + effect + stderr,
                [predict(_x) for _x in x] + effect - stderr,
                color=trendline_color,
                alpha=0.1,
            )

    return effect, stderr

# Performs an OLS regression on the given economic variable
def run_covid19_regression(
    df: pd.DataFrame,
    y_name: str,
    log_level: bool = False,
):
    df = pd.DataFrame(df)
    yr_ind_str = ''

    # Add post-pandemic year indicator variables for use in OLS regression
    for yr in filter(lambda _x: _x >= 2021, df['yr']):
        df[f'ind_{yr}'] = [1 if _x == yr else 0 for _x in df['yr']]
        yr_ind_str += f'ind_{yr} + '
    yr_ind_str = yr_ind_str[:-3]

    # Transform to dependent variable to log for marginal interpretation
    if log_level:
        df[f'log_{y_name}'] = np.log(df[y_name])

    # Run OLS regression for COVID-19 cases, deaths and mortality rates
    for x_name in ('covid19_cases', 'covid19_deaths', 'covid19_mortality'):
        # Create indicators for formula 
        indicator_str = (
            f' + {x_name}:({yr_ind_str})'
            if yr_ind_str != ''
            else ''
        )

        # Construct appropriate OLS formula
        formula = f'{y_name} ~ yr + {x_name}{indicator_str}'
        if log_level:
            formula = 'log_' + formula

        # Output regression summary
        print(smf.ols(formula, df,).fit().summary(), '\n')
