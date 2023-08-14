import pandas as pd
import numpy as np

"""
Read Data
"""
df = pd.read_csv("asterank_exo.csv")

"""
Added filter according to PER data, which is responsible for the indicator of the direction of rotation of the planet.
Filtered to show planets spinning clockwise instead of counterclockwise
"""
df = df[df["PER"] > 0]

# Data from column koi will be shown as int value
df["KOI"] = df["KOI"].astype(int, errors="ignore")

# Creating a StarSize column that contains a broken RSTAR column into "small", "similar", "bigger"
bins = [0, 0.8, 1.2, 100]
names = ["small", "similar", "bigger"]
df["StarSize"] = pd.cut(df["RSTAR"], bins, labels=names)

# Creating selection options for the dropdown menu
options = []
for s in names:
    options.append({"label": s, "value": s})

"""
Requirements for a habitable planet
"""
# Temperature
tp_bins = [0, 200, 400, 500, 5000]
tp_labels = ["low", "optimal", "high", "extreme"]
df["Temp"] = pd.cut(df["TPLANET"], tp_bins, labels=tp_labels)

# Size and Gravity
rp_bins = [0, 0.5, 2, 4, 100]
rp_labels = ["low", "optimal", "high", "extreme"]
df["Gravity"] = pd.cut(df["RPLANET"], rp_bins, labels=rp_labels)

# Set object status
# np.where((condition), wether true, or else)
df["status"] = np.where((df["Temp"] == "optimal") & (df["Gravity"] == "optimal"), "promising", None)

"""
What is loc
loc is responsible for data usage. in-place : can be a sheet with indexes or values. 
In the use case, we are extracting the range rows
"""
df.loc[:, "status"] = np.where((df["Temp"] == "optimal") & (df["Gravity"].isin(["low", "high"])),
                               "challenging", df["status"])
df.loc[:, "status"] = np.where((df["Temp"].isin(["low", "high"])) &
                               (df["Gravity"] == "optimal"),
                               "challenging", df["status"])
# fills NaN values in df to "extreme"
df["status"] = df.status.fillna("extreme")

# Relative distance (Distance to the sun / radius of the sun)
df.loc[:, "Relative_dist"] = df["A"] / df["RSTAR"]