import pandas as pd
import os

# Print out current working directory
# os.chdir("PhD Papers/na_phylogeny")
# Open the CSV file

data = pd.read_csv('semitic_cognates.csv', encoding='utf-8')
data.columns = ['Language'] + list(data.columns[1:])

# Melt the DataFrame from wide to long format
long_df = data.melt(id_vars='Language', var_name='Concept', value_name='Value')

num_concepts = len(long_df['Concept'].unique())
# Create a dictionary to map the original concepts to unique integers
concept_num = {concept: i for i, concept in zip(range(0, num_concepts*101, 100), long_df['Concept'].unique())}

# Apply the mapping to the 'Concept' column
long_df['Value'] = long_df['Value'].fillna(0)

long_df['Value'] = long_df.apply(
    lambda row: str(int(row['Value']) + concept_num[row['Concept']]), 
    axis=1)

concept_num_str = [str(i) for i in concept_num.values()]

long_df.loc[long_df["Value"].isin(concept_num_str), "Value"] = "?"

long_df.to_csv('semitic_cognates_long.csv', index=False, encoding='utf-8')

