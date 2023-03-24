import pandas as pd
def merge(tables):
    merged_table = pd.concat(tables, axis=0, ignore_index=True)
    return merged_table