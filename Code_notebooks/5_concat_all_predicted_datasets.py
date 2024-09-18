import os
import pandas as pd
import glob


csv_files = glob.glob('dataset_part_*.csv')


csv_files.sort()


dfs = []


for file in csv_files:
    print(f"Processing file: {file}")
    df = pd.read_csv(file)
    dfs.append(df)


merged_df = pd.concat(dfs, ignore_index=True)


output_file = 'merged_dataset.csv'
merged_df.to_csv(output_file, index=False)

print(f"\nMerged {len(csv_files)} CSV files into '{output_file}'")
print("Processed files:")
for file in csv_files:
    print(f"- {file}")
