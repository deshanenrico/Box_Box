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


def add_pace_loss(df):
    """
    pace_loss = lap_time - fastest_stint_lap
    """

    # Group by driver and stint & Find the fastest lap within each stint.
    fastest = (
        df.groupby(
            ["drv", "stint"]
        )["time"]
        .transform("min")
    )

    # Create a copy so we don't modify the original dataframe.
    result = df.copy()

    # Calculate the pace loss.
    result["pace_loss"] = (
        result["time"] - fastest
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


def remove_neutralised_laps(df):
    """
    Remove laps affected by VSC and Safety Car.
    # - Virtual Safety Car (laps 20-22)
    # - Virtual Safety Car (laps 36-39)
    # - Safety Car (laps 45-52)
    """

    neutralised_laps = [
        20, 21, 22,
        36, 37, 38, 39,
        45, 46, 47, 48, 49, 50, 51, 52
    ]

    result = df[
        ~df["lap"].isin(neutralised_laps)
    ].copy()

    return result