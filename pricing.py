import numpy as np
import pandas as pd


def gompertz_makeham_survival(age, t, A, B, c):

    integral = (
        A * t
        + B * (c ** age) * (c ** t - 1) / np.log(c)
    )

    return np.exp(-integral) # this is the equation tPx = exp[-At - frac{Bc**x(c**t - 1)}{log c}

def price_survival_benefit(
    age,
    term,
    benefit,
    interest_rate,
    A,
    B,
    c
):

    survival = gompertz_makeham_survival(
        age,
        term,
        A,
        B,
        c
    )

    discount = 1 / (1 + interest_rate) ** term

    price = benefit * survival * discount

    return price     # PV = S * frac{tPx}{(1+i)**t} A person aged 40 receives £100,000 at the end of 20 years if they aint dead




def price_historical_models(
        gm_results,
        sex,
        age,
        term,
        benefit,
        interest_rate
    ):
    results = []

    sex_models = gm_results[
        gm_results['sex'] == sex
    ]
    for _,row in sex_models.iterrows():

        price = price_survival_benefit(
            age,
            term,
            benefit,
            interest_rate,
            A=row['A'],
            B=row['B'],
            c=row['c'],
        )
        results.append({
            'period': row['period'],
            'start_year': row['start_year'],
            'sex': row['sex'],
            'price': price
        })

    return pd.DataFrame(results)