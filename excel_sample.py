import pandas as pd

data = {
    'Easting_36M': [500000, 600000, 700000],
    'Northing_36M': [4649776, 4749776, 4849776]
}

df = pd.DataFrame(data)
df.to_excel('sample_input_coords.xlsx', index=False)