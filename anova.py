import pandas as pd

from scipy import stats


#
# One-way ANOVA for repeated measures.
# Reference: https://www.marsja.se/four-ways-to-conduct-one-way-anovas-using-python/
#
def do_anova(label: str, data: pd.DataFrame, col_group: str, col_value: str) -> pd.DataFrame:
    groups = pd.unique(data[col_group]).tolist()
    k = len(groups)  # number of conditions
    N = len(data[col_value])  # conditions * participants
    n = data.groupby(col_group).size()[0]  # Participants in each condition

    DFbetween = k - 1
    DFwithin = N - k
    DFtotal = N - 1

    SSbetween = (sum(data.groupby(col_group).sum()[col_value] ** 2) / n) - (data[col_value].sum() ** 2) / N
    sum_y_squared = sum([value ** 2 for value in data[col_value].values])
    SSwithin = sum_y_squared - sum(data.groupby(col_group).sum()[col_value] ** 2) / n
    SStotal = sum_y_squared - (data[col_value].sum() ** 2) / N
    MSbetween = SSbetween / DFbetween
    MSwithin = SSwithin / DFwithin
    # F = MSbetween / MSwithin
    # p = stats.f.sf(F, DFbetween, DFwithin)

    F, p = stats.f_oneway(*[data[col_value][data[col_group] == g] for g in groups])
    eta_sqrd = SSbetween / SStotal
    omega_sqrd = (SSbetween - (DFbetween * MSwithin)) / (SStotal + MSwithin)
    sig = "*" if p < 0.05 else " "

    return pd.DataFrame(data=[[sig, DFbetween, DFwithin, F, p, eta_sqrd, omega_sqrd]],
                        columns=["sig.", "DFbetween", "DFwithin", "F", "p", "eta_sqrd", "omega_sqrd"],
                        index=[label])
