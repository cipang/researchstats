import pandas as pd

from anova import do_anova
from func import get_data_file_path

csv = pd.read_csv(get_data_file_path("maplike_treemap_ease_helpful.csv"))

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

# Run ANOVA on different partitions of data.
groups = ["A", "B", "C", "D"]
results = do_anova("Ease All", data_ease, "vis_type", "value")
for g in groups:
    results = results.append(do_anova(f"Ease {g}", data_ease[data_ease.group == g], "vis_type", "value"))
print(results.to_string())

print()
results = do_anova("Help All", data_helpful, "vis_type", "value")
for g in groups:
    results = results.append(do_anova(f"Help {g}", data_helpful[data_helpful.group == g], "vis_type", "value"))
print(results.to_string())
