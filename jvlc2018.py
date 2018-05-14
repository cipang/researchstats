import pandas as pd
from scipy.stats import ttest_rel

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

# Run t-tests on ease-of-use of all groups.
print()
print("UT/NT", ttest_rel(data_ease["value"][data_ease.vis_type == "UT"],
                         data_ease["value"][data_ease.vis_type == "NT"]))
print("UT/ML", ttest_rel(data_ease["value"][data_ease.vis_type == "UT"],
                         data_ease["value"][data_ease.vis_type == "ML"]))
print("NT/ML", ttest_rel(data_ease["value"][data_ease.vis_type == "NT"],
                         data_ease["value"][data_ease.vis_type == "ML"]))

print()
results = do_anova("Help All", data_helpful, "vis_type", "value")
for g in groups:
    results = results.append(do_anova(f"Help {g}", data_helpful[data_helpful.group == g], "vis_type", "value"))
print(results.to_string())

# Run t-tests on helpfulness of all groups.
print()
print("UT/NT", ttest_rel(data_helpful["value"][data_helpful.vis_type == "UT"],
                         data_helpful["value"][data_helpful.vis_type == "NT"]))
print("UT/ML", ttest_rel(data_helpful["value"][data_helpful.vis_type == "UT"],
                         data_helpful["value"][data_helpful.vis_type == "ML"]))
print("NT/ML", ttest_rel(data_helpful["value"][data_helpful.vis_type == "NT"],
                         data_helpful["value"][data_helpful.vis_type == "ML"]))

# Run ANOVA for speed.
print()
data_speed = pd.read_csv(get_data_file_path("maplike_treemap_speed.csv"))
results = do_anova("Sped All", data_speed, "vis_type", "value")
for g in groups:
    results = results.append(do_anova(f"Sped {g}", data_speed[data_speed.group == g], "vis_type", "value"))
print(results.to_string())

# Run ANOVA for accuracy.
print()
data_accuracy = pd.read_csv(get_data_file_path("maplike_treemap_accuracy.csv"))
results = do_anova("Accy All", data_accuracy, "vis_type", "value")
for g in groups:
    results = results.append(do_anova(f"Accy {g}", data_accuracy[data_accuracy.group == g], "vis_type", "value"))
print(results.to_string())
