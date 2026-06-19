import pandas as pd
import random

df = pd.read_csv('/local/scratch/emumic/data/snap_data/soc-Epinions1.csv')

df['Cost'] = [random.randint(1, 10) for _ in range(len(df))]

df.to_csv('/local/scratch/emumic/data/snap_data/soc-Epinions1_cost.csv', index=False)

print("Attached random edge cost to dataset.")