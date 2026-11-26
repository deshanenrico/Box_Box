import pandas as pd
from scipy.stats import linregress



def tyre_degradation_rate(driver_df, compound):
    """
    Estimate tyre degradation directly from
    fuel-corrected lap times.

    WHY:
    This avoids using the stint's fastest lap
    as a reference point.

    The slope represents seconds lost per lap
    of tyre age.
    """

    compound_df = driver_df[
        driver_df["compound"] == compound
    ]

    fit = linregress(
        compound_df["life"],
        compound_df["corrected_time"]
    )

    return {
        "compound": compound,
        "laps": len(compound_df),
        "slope": fit.slope,
        "stderr": fit.stderr,
        "r_squared": fit.rvalue ** 2,
        "intercept": fit.intercept
    }


def compare_driver_compounds(driver_name, driver_df):
    """
    Compare tyre degradation results
    across compounds for one driver.
    """

    results = []

    for compound in driver_df["compound"].unique():

        result = tyre_degradation_rate(
            driver_df,
            compound
        )

        results.append({
            "driver": driver_name,
            **result
        })

    return pd.DataFrame(results)