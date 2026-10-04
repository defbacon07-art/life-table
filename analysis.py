import pandas as pd
import matplotlib.pyplot as plt

from data_loader import load_historical_life_data
from life_table import life_table
from pricing import price_historical_models

# Load all historical data
data = load_historical_life_data("life_table_data.xlsx")


def fit_all_gompertz_models(data):  

    results = [] 

    sexes = ["Male", "Female"]
    periods = data["period"].unique()

    for sex in sexes:

        for period in periods:   # selects one sex and period

                period_data = data[
                (data["sex"] == sex) &
                (data["period"] == period)
            ]

            # Create the life table
            table = life_table(
                period_data["lx"],
                period_data["age"]
            )

            # Fit Gompertz-Makeham
            table.fit_gompertz_makeham(
                start_age=20,
                end_age=90
            )

            # Extract fitted parameters
            A, B, c = table.gm_params

            # Store result
            results.append({
                "period": period,
                'start_year': int(period[:4]),
                "sex": sex,
                "A": A,
                "B": B,
                "c": c
            })

    return pd.DataFrame(results)


gm_results = fit_all_gompertz_models(data)

prices_male = price_historical_models(
    gm_results,
    sex='Male',
    age=40,
    term=40,
    benefit=100000,
    interest_rate=0.04
)



prices_female = price_historical_models(
    gm_results,
    sex="Female",
    age=40,
    term=40,
    benefit=100000,
    interest_rate=0.04
)

prices = pd.concat(
    [prices_male, prices_female],
    ignore_index=True
)

plt.figure(figsize=(10, 6))

for sex in ["Male", "Female"]:

    subset = prices[
        prices["sex"] == sex
    ].sort_values("start_year")

    plt.plot(
        subset["start_year"],
        subset["price"],
        marker="o",
        label=sex
    )

plt.xlabel("Start year")
plt.ylabel("Contract value (£)")
plt.title("Historical Mortality Impact on Contract Value")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "historical_contract_prices.png",
    dpi=300
)

plt.show()