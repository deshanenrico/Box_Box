import pandas as pd


def prepare_lap_data(df):
    """
    Keep only the columns required for analysis.
    """

    cols = [
        "drv",
        "lap",
        "time",
        "compound",
        "life",
        "stint",
        "pos",
        "team",
        "pin",
        "pout",
        "status",
    ]

    clean_df = df[cols].copy()

    numeric_cols = [
        "time",
        "pos",
        "lap",
        "life",
        "stint",
    ]

    for col in numeric_cols:
        clean_df[col] = pd.to_numeric(
            clean_df[col],
            errors="coerce"
        )

    clean_df["pin"] = clean_df["pin"].replace(
        "None",
        pd.NA
    )

    clean_df["pout"] = clean_df["pout"].replace(
        "None",
        pd.NA
    )

    return clean_df


def remove_pit_laps(df):
    """
    Remove pit-in and pit-out laps.
    """

    result = df.copy()

    result = result[
        result["pin"].isna()
    ]

    result = result[
        result["pout"].isna()
    ]

    return result


def remove_neutralised_laps(
    df,
    laps_to_remove
):
    """
    Remove Safety Car and VSC laps.
    """

    result = df[
        ~df["lap"].isin(laps_to_remove)
    ].copy()

    return result


def add_fuel_correction(
    df,
    total_laps,
    initial_fuel=100
):
    """
    Calculate fuel-corrected lap times.
    """

    result = df.copy()

    result["remaining_fuel"] = (
        initial_fuel *
        (1 - result["lap"] / total_laps)
    )

    result["fuel_effect"] = (
        result["remaining_fuel"] * 0.03
    )

    result["corrected_time"] = (
        result["time"]
        - result["fuel_effect"]
    )

    return result