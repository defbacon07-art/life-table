from data_loader import load_historical_life_data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
data_file = SCRIPT_DIR / "life_table_data.xlsx"


def gompertz_makeham(x, A, B, c):
    return A + B * np.power(c,  x)  


class life_table: # this acts on a list of lx data to calculate dx, qx, px, and ex values
    def __init__(self, lx, age):
        self.lx = lx.reset_index(drop=True)  # Reset index to ensure it starts from 0
        self.age = age.reset_index(drop=True)  # Reset index to ensure it starts from 0
        self.dx = self.convert_lx_to_dx()
        self.qx = self.calculate_qx()
        self.px = self.calculate_px()
        self.ux = self.calculate_ux()   
        self.ex = self.calculate_ex()
        self.gm_params = None
        self.gm_cov = None

    def convert_lx_to_dx(self):   # as dx is defined as the difference between lx at age x and lx at age x+1, this function calculates dx from lx
        dx = pd.Series(index=range(len(self.lx) - 1), dtype=float)
        for i in range (len(self.lx) - 1):
            dx[i] = self.lx.iloc[i] - self.lx.iloc[i+1]
        return dx
    def calculate_qx(self): # qx is defined as the ratio of dx to lx, this function calculates qx from dx and lx
        qx = pd.Series(index=range(len(self.dx)), dtype=float)

        for i in range(len(self.dx)):
            qx.iloc[i] = self.dx.iloc[i] / self.lx.iloc[i]

        return qx

    def calculate_px(self): # px is the survival probability, defined as 1 - qx, this function calculates px from qx
        return(1-self.qx)
    def calculate_ex(self): # ex is the expected number of years lived at age x, defined as the sum of px from age x to the last age, this function calculates ex from px using the acturial relation 
        ex = pd.Series(index=range(len(self.lx)), dtype=float)
        ex.iloc[-1] = 0
        for i in range(len(self.lx) - 2, -1, -1):
            ex.loc[i] = self.px.iloc[i] * (ex.iloc[i + 1] + 1)
        return ex
    def calculate_ux(self): # this is the force of mortality, defined as -ln(1-qx), this function calculates ux from qx
        return -np.log(1-self.qx)
    def fit_gompertz_makeham(self, start_age=20, end_age=90):

        mask = self.age.iloc[:-1].between(start_age, end_age) # this returns true or false if the number is in our range or not 

        ages = self.age.iloc[:-1][mask].to_numpy() # this returns the ages we want
        ux = self.ux[mask].to_numpy() # this returns the force of mortality at the index we need 
        popt, pcov = curve_fit(   # this runs the non-linear regressions, with p0 as estimators and then fits to the best model possible 
            gompertz_makeham,
            ages,
            ux,
            p0=[0.0005, 0.0001, 1.09],
            maxfev=10000
        )
        self.gm_params = popt # this stores the parameters within the self 
        self.gm_cov = pcov
    def gompertz_makeham_fit(self):

        if self.gm_params is None:
            raise ValueError('Fit the model first')
        A, B, c = self.gm_params

        ages = self.age.iloc[:-1].to_numpy()

        return gompertz_makeham(ages, A, B, c) # this runs the model 




class GompertzMakeham:

    def __init__(self, A, B, C):
        self.A = A
        self.B = B
        self.C = C 

    def force_of_mortality(self, age):
        return(
            self.A + self.B * np.power(self.C, age)
        )
    def survival_probability(self, age, t):

        integral = (
            self.A * t
            + (
                self.B * np.power(self.C, age) * (np.poower(self.C, t) -1)
                / np.log(self.C)
            )
        )
        return np.exp(-integral)  # this gives us the probability that an 'age' year old survives 't' more years

    




#df = pd.read_excel(data_file, sheet_name=input('What years?\n'), skiprows=input('Skip how many rows?\n'))
#
#
#
#male = life_table(df["lx"], df["age"])
#
#
#
#ages = male.age.iloc[:-1]
#observed = male.ux
#male.fit_gompertz_makeham()
#fitted = male.gompertz_makeham_fit()
#
#fit_ages = male.age.iloc[:-1].between(20, 90)
#
#print("Starting plot...")
#
#plt.figure(figsize=(10, 6))
#
#plt.scatter(
#    male.age.iloc[:-1],
#    male.ux,
#    label="Observed",
#    s=15
#)
#
#plt.plot(
#    male.age.iloc[:-1][fit_ages],
#    fitted[fit_ages.to_numpy()],
#    label="Gompertz-Makeham",
#    linewidth=2
#)
#
#plt.yscale("log")
#plt.xlabel("Age")
#plt.ylabel("Force of mortality")
#plt.title("Male Mortality: Gompertz-Makeham Fit")
#plt.legend()
#plt.grid(True, which="both", alpha=0.3)
#plt.tight_layout()
#
#output_file = Path(__file__).parent / "gompertz_mortality.png"
#
#plt.savefig(output_file, dpi=300)
#
#print(f"Graph saved to: {output_file}")
#
#plt.show()
#print("Finished")