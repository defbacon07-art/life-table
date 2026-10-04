import pandas as pd 
import re
def load_historical_life_data(file_path): # takes an excel file and outputs a data sheet

    excel_file = pd.ExcelFile(file_path)

    Life_table_sheets = [
        sheet 
        for sheet in excel_file.sheet_names
        if re.fullmatch(r"\d{4}-\d{4}", sheet)
    ]
    all_tables = []  

    for sheet in Life_table_sheets:    
        male = pd.read_excel(
            file_path,   
            sheet_name=sheet,
            skiprows=5,
            usecols='A:F'         # takes just the male bits 
        )

        male['period'] = sheet    # tells you what year the thing is in 
        male['sex'] = 'Male'

        female = pd.read_excel(
            file_path,
            sheet_name=sheet,
            skiprows=5,
            usecols="H:M"
        )

        female.columns = [
            "age",
            "mx",
            "qx",
            "lx",
            "dx",
            "ex"
        ]

        female["period"] = sheet
        female["sex"] = "Female"

        

        all_tables.append(male)              
        all_tables.append(female)


    historical_data = pd.concat(    # stacks all the dataframes together 
        all_tables,
        ignore_index = True    # resets the index each sheet 
    )

    historical_data = historical_data[
        [
            "period",
            "sex",
            "age",
            "mx",
            "lx",
            "dx",
            "qx",
            "ex"
        ]
    ]

    numeric_columns = [
        "age",
        "mx",
        "lx",
        "dx",
        "qx",
        "ex"
    ]

    for column in numeric_columns:
        historical_data[column] = pd.to_numeric(
            historical_data[column],
            errors="coerce"
        )

    historical_data = historical_data.dropna(
        subset=numeric_columns
    )

    historical_data["age"] = historical_data["age"].astype(int)

    historical_data["start_year"] = (
        historical_data["period"]
        .str[:4]
        .astype(int)
    )

    historical_data = historical_data.sort_values(
        ["sex", "start_year", "age"]
    ).reset_index(drop=True)

    return historical_data
