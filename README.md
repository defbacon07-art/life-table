# life-table
lifetable -> contract pricing project

data-loader takes in lifetable data from an excel sheet and exports it as a data sheet in pandas, with the capacity to have data extracted by sex or period
lifetable takes this data sheet and calculates dx, px, qx, ux and ex, and fits gompertz-makeham parameters to the model
pricing then prices a contract to pay an (age) year old £100 000 if they survive to 60, given by PV = S * frac{tPx}{(1+i)**t} where t is the term (40), i is the interest rate, assumed to be 4% and tx is given by tPx = exp[-At - frac{Bc**x(c**t - 1)}{log c} where A B and C are gompertz-makeham parameters
Analysis then takes these prices and plots a graph of price on time for males and females since 1983
