from lingpy import convert, get_wordlist
import pandas as pd

sem_wordlist = get_wordlist('semitic_cognates_long.csv', col="Language", row="Concept")

convert.strings.write_nexus(sem_wordlist, mode="BEAST", filename='semitic_cognates.nex', ref="value", missing="?")

### Modify the nexus file manually as it doesn't display missing data properly
with open('semitic_cognates.nex', 'r') as nexus_file:
    nexus_text = nexus_file.readlines()

df = pd.read_csv('semitic_cognates_long.csv')
df['Concept'] = df['Concept'].str.replace('(', '').str.replace(')', '').str.replace(',', '').str.replace(".", "")
df['Concept'] = df['Concept'].str.replace(' ', '_')
df["Language"] = df["Language"].str.replace('_', '').str.replace("'", "")

matrix_begin = nexus_text.index('MATRIX\n') + 1
matrix_end = nexus_text.index("END;\n") - 1

chars_begin = nexus_text.index('    CHARSTATELABELS\n') + 1
chars_end = matrix_begin - 2

concepts_ints = list(map(lambda x: x.strip().rstrip(",").split(), nexus_text[chars_begin:chars_end]))

map_concept_ints = {}
for integer, concept in concepts_ints:
    if concept not in map_concept_ints.keys():
        map_concept_ints[concept] = [integer]
    else:
        map_concept_ints[concept].append(integer)

for i in range(matrix_begin, matrix_end):
    lang_name, ints = nexus_text[i].split()
    missing_vals = df[(df.Language == lang_name) & (df.Value == "?")]["Concept"]
    new_ints = ints
    for concept in missing_vals:
        for integer in map_concept_ints[concept]:
            integer = int(integer)
            integer -= 1 # for 0-indexing
            new_ints = new_ints[:integer] + "?" + new_ints[integer+1:]
    print(len(new_ints))
    nexus_text[i] = f"{lang_name}             {new_ints}\n"


with open('semitic_cognates.nex', 'w') as nexus_file:
    nexus_file.write("".join(nexus_text))
