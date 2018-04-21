import pandas as pd

from func import get_data_file_path
from anova import do_anova

data = pd.read_csv(get_data_file_path("plant_growth.csv"))
print(do_anova("Plants", data, "group", "weight"))
