pip install pandas numpy pyreadstat
import numpy as np
import pandas as pd
import pyreadstat

# ====== The parts you need to modify ======
path = r"C:\Users\dingc\Desktop\new.sav"   # SPSS SAV file path
y_col = "BMI"            # continuous variable column names
group_col = "groups"       # grouping variable column names
g1, g2 = 1, 2
B = 5000
seed = 42
# =================================

df, meta = pyreadstat.read_sav(path)

# If the column names do not match completely, uncomment the two lines below to see the actual columns.
# print(df.columns)
# print(df.head())

x1 = df.loc[df[group_col] == g1, y_col].dropna().to_numpy()
x2 = df.loc[df[group_col] == g2, y_col].dropna().to_numpy()

if len(x1) == 0 or len(x2) == 0:
    raise ValueError("No valid data for a particular group: please check whether the grouping variable is 1/2, or whether the BMI values are all missing.")

diff_hat = np.median(x1) - np.median(x2)

rng = np.random.default_rng(seed)
n1, n2 = len(x1), len(x2)

diff_boot = np.empty(B)
for b in range(B):
    xb1 = rng.choice(x1, size=n1, replace=True)
    xb2 = rng.choice(x2, size=n2, replace=True)
    diff_boot[b] = np.median(xb1) - np.median(xb2)

lower = np.percentile(diff_boot, 2.5)
upper = np.percentile(diff_boot, 97.5)

print(f"n1={n1}, n2={n2}")
print(f"median(BMI) Group{g1} = {np.median(x1):.4f}")
print(f"median(BMI) Group{g2} = {np.median(x2):.4f}")
print(f"Median difference (Group{g1} - Group{g2}) = {diff_hat:.4f}")
print(f"95% CI (bootstrap percentile) = [{lower:.4f}, {upper:.4f}]")
