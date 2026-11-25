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

    # Create a copy containing only useful columns.
    clean_df = df[cols].copy()

    # Convert lap times to numeric values. Some are stored as text.
    clean_df["time"] = pd.to_numeric(
        clean_df["time"],
        errors="coerce"
    )

    # Convert race position to numeric.
    clean_df["pos"] = pd.to_numeric(
        clean_df["pos"],
        errors="coerce"
    )

    # Convert string "None" values to proper missing values for .isna() to work correctly.
    clean_df["pin"] = clean_df["pin"].replace("None", pd.NA)
    clean_df["pout"] = clean_df["pout"].replace("None", pd.NA)

    return clean_df

def add_fuel_correction(
    df,
    total_laps=52,
    initial_fuel=100
):
    """
    Estimate fuel-corrected lap times.

    WHY:
    Cars become lighter throughout the race.
    Later laps are naturally faster due to
    reduced fuel load.

    Fuel correction attempts to isolate tyre
    performance from fuel-weight effects.
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
        result["time"] -
        result["fuel_effect"]
    )

    return result


def add_pace_loss(df):
    """
    pace_loss = lap_time - fastest_stint_lap
    """

    # Group by driver and stint & Find the fastest lap within each stint.
    fastest = (
        df.groupby(
            ["drv", "stint"]
        )["corrected_time"]
        .transform("min")
    )

    # Create a copy so we don't modify the original dataframe.
    result = df.copy()

    # Calculate the pace loss.
    result["corrected_pace_loss"] = (
    result["corrected_time"] - fastest
    )

    return result


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
    Remove laps affected by
    Safety Car or Virtual Safety Car.
    """

    result = df[
        ~df["lap"].isin(
            laps_to_remove
        )
    ].copy()

    return result
