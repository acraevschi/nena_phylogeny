import pandas as pd

# Open the CSV file
with open('na_cognates.csv', 'r', encoding="UTF-8") as file:

    data = pd.read_csv('na_cognates.csv', encoding='utf-8')
    data.columns = ['Language'] + list(data.columns[1:])

    # Melt the DataFrame from wide to long format
    long_df = data.melt(id_vars='Language', var_name='Concept', value_name='Value')

    num_concepts = len(long_df['Concept'].unique())
    # Create a dictionary to map the original concepts to unique integers
    concept_num = {concept: i for i, concept in zip(range(0, num_concepts*101, 100), long_df['Concept'].unique())}

    # Apply the mapping to the 'Concept' column
    long_df['Value'] = long_df.apply(lambda row: int(row['Value']) + concept_num[row['Concept']] if row['Concept'] in concept_num and row['Value'] != "?" else row['Value'], axis=1)
    # Write the long format to a new CSV file
    long_df.to_csv('na_cognates_long.csv', index=False, encoding='utf-8')
