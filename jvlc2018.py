import os

from scipy import stats
import pandas as pd

csv = pd.read_csv(os.path.join(os.path.dirname(__file__), "data", "maplike_treemap_ease_helpful.csv"))

# Setup a data frame for ease of use.
rows = []
for col_name in ["ut_ease", "nt_ease", "ml_ease"]:
    for _, instance in csv[["group", col_name]].iterrows():
        rows.append((instance["group"], instance[col_name], col_name[0:2].upper()))
data_ease = pd.DataFrame(data=rows, columns=["group", "value", "vis_type"])

# Setup a data frame for helpfulness.
rows = []
for col_name in ["ut_helpful", "nt_helpful", "ml_helpful"]:
    for _, instance in csv[["group", col_name]].iterrows():
        rows.append((instance["group"], instance[col_name], col_name[0:2].upper()))
data_helpful = pd.DataFrame(data=rows, columns=["group", "value", "vis_type"])

del csv

#
# One-way ANOVA for repeated measures.
# Reference: https://www.marsja.se/four-ways-to-conduct-one-way-anovas-using-python/
#
def do_anova(label, data):
    types = pd.unique(data.vis_type).tolist()
    k = len(types)  # number of conditions
    N = len(data.value)  # conditions * participants
    n = data.groupby("vis_type").size()[0]  # Participants in each condition

    DFbetween = k - 1
    DFwithin = N - k
    DFtotal = N - 1

    SSbetween = (sum(data.groupby("vis_type").sum()["value"] ** 2) / n) - (data["value"].sum() ** 2) / N
    sum_y_squared = sum([value ** 2 for value in data["value"].values])
    SSwithin = sum_y_squared - sum(data.groupby("vis_type").sum()["value"] ** 2) / n
    SStotal = sum_y_squared - (data["value"].sum() ** 2) / N
    MSbetween = SSbetween / DFbetween
    MSwithin = SSwithin / DFwithin
    # F = MSbetween / MSwithin
    # p = stats.f.sf(F, DFbetween, DFwithin)

    F, p = stats.f_oneway(*[data["value"][data.vis_type == t] for t in types])
    eta_sqrd = SSbetween / SStotal
    omega_sqrd = (SSbetween - (DFbetween * MSwithin)) / (SStotal + MSwithin)
    sig = "*" if p < 0.05 else " "

    return pd.DataFrame(data=[[sig, DFbetween, DFwithin, F, p, eta_sqrd, omega_sqrd]],
                        columns=["sig.", "DFbetween", "DFwithin", "F", "p", "eta_sqrd", "omega_sqrd"],
                        index=[label])


groups = ["A", "B", "C", "D"]
results = do_anova("Ease All", data_ease)
for g in groups:
    results = results.append(do_anova(f"Ease {g}", data_ease[data_ease.group == g]))
print(results.to_string())

print()
results = do_anova("Help All", data_helpful)
for g in groups:
    results = results.append(do_anova(f"Help {g}", data_helpful[data_helpful.group == g]))
print(results.to_string())
