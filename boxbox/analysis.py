import pandas as pd
from scipy.stats import linregress


def degradation_regression(driver_df, compound):
    """
    Calculate tyre degradation statistics for a
    specific compound using fuel-corrected pace loss.

    Returns:
    - slope
    - r_squared
    """

    # Keep only laps driven on the selected compound.
    compound_df = driver_df[
        driver_df["compound"] == compound
    ]

    # Fit a linear regression:
    # corrected_pace_loss = a + b * tyre_age
    fit = linregress(
        compound_df["life"],
        compound_df["corrected_pace_loss"]
    )

    return {
        "compound": compound,
        "slope": fit.slope,
        "r_squared": fit.rvalue ** 2,
        "intercept": fit.intercept
    }


def compare_driver_compounds(driver_name, driver_df):
    """
    Compare degradation results
    across compounds for one driver.
    """

    results = []

    for compound in driver_df["compound"].unique():

        result = degradation_regression(
            driver_df,
            compound
        )

        results.append({
            "driver": driver_name,
            **result
        })

    return pd.DataFrame(results)