import pandas as pd

books_df = pd.read_csv("dishes.csv")
for title in books_df["Title"]:
    print(f'"{title}",')