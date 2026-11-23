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