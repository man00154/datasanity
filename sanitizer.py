import pandas as pd


def sanitize_data(data: pd.DataFrame, ranges: pd.DataFrame):
    """
    Sanitise data based on parameter min/max ranges.
    Rows with any invalid value are flagged as bad data.
    """

    # ===============================
    # NORMALIZE RANGE COLUMNS
    # ===============================
    ranges = ranges.copy()
    ranges.columns = (
        ranges.columns
        .astype(str)
        .str.strip()
        .str.lower()
    )

    required_cols = {"parameter", "min", "max"}
    missing = required_cols - set(ranges.columns)

    if missing:
        raise ValueError(
            f"Range file missing required columns: {missing}. "
            f"Expected columns: parameter, min, max"
        )

    # ===============================
    # BUILD RANGE MAP
    # ===============================
    range_map = {}

    for _, r in ranges.iterrows():
        param = str(r["parameter"]).strip()

        if param == "" or pd.isna(param):
            continue

        try:
            min_val = float(r["min"])
            max_val = float(r["max"])
        except Exception:
            continue  # skip invalid range rows safely

        range_map[param] = (min_val, max_val)

    # ===============================
    # SANITIZE DATA
    # ===============================
    clean_rows = []
    bad_rows = []

    for _, row in data.iterrows():
        row_issues = []

        for param, (min_val, max_val) in range_map.items():
            if param not in data.columns:
                row_issues.append(f"{param}: column missing")
                continue

            value = row[param]

            if pd.isna(value):
                row_issues.append(f"{param}: missing value")
            elif not isinstance(value, (int, float)):
                row_issues.append(f"{param}: non-numeric")
            elif value < min_val or value > max_val:
                row_issues.append(
                    f"{param}: {value} outside [{min_val}, {max_val}]"
                )

        if row_issues:
            bad_row = row.copy()
            bad_row["issues"] = "; ".join(row_issues)
            bad_rows.append(bad_row)
        else:
            clean_rows.append(row)

    clean_df = pd.DataFrame(clean_rows)
    bad_df = pd.DataFrame(bad_rows)

    return clean_df, bad_df
