import pandas as pd
def merge(tables,collumn):
    merged_table=pd.DataFrame(columns=[collumn])
    for table in tables:
        merged_table = pd.merge(merged_table, table, on=collumn, how='outer')
    return merged_table