#!/usr/bin/env python3

"""
Python file containing all common and frequently
ran code for the analysis of the Caribbean data.
--------------------------------------------------
Created on 04/03/2023. Last updated on 04/15/2023.
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
    # Add post-pandemic indicator variable
    df['ind_postpand'] = (df['yr'] >= 2020)

    # Add difference-in-differences vertical line
    plt.axvline(x=2019.5, color='black')

    # Determine pre-pandemic trendline using OLS
    reg = smf.ols(f"{y_name} ~ {x_name} + ind_postpand", data=df).fit()
    effect, stderr = reg.params['ind_postpand[T.True]'], reg.bse['ind_postpand[T.True]']
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

def run_covid19_interaction(
    df: pd.DataFrame,
    y_name: str,
):
    # Add year indicators
    df = pd.DataFrame(df)
    df[f"ind_2020"] = (df["yr"] == 2020)
    df[f"ind_2021"] = (df["yr"] == 2021)
    df[f"ind_postpand"] = (df["yr"] >= 2020)

    reg = smf.ols(
        formula=f"{y_name} ~ covid19_cases + covid19_deaths",
        data=df,
    ).fit()
    print(reg.summary())
    
    reg = smf.ols(
        formula=f"{y_name} ~ covid19_mortality",
        data=df,
    ).fit()
    print(reg.summary())
