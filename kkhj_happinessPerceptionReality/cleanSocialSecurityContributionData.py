import pandas as pd


# Extract data, make it ready for future instructions
def get_security_contribution():
    df = pd.read_excel("kkhj_happinessPerceptionReality/data/socialSecurityContributions.xlsx")
    df = df.melt(['Country'], var_name='Year', value_name='Social Security Employer Contribution Index')
    # Delete columns if there is any empty cells
    return df[(df != '-').all(1)]


# Convert contribution rates to index (out of 10)
def security_contribution_out_of_10():
    df = get_security_contribution()
    df.loc[:, df.columns == 'Social Security Employer Contribution Index'] = df.loc[:, df.columns == 'Social Security Employer Contribution Index'].div(10)
    return df