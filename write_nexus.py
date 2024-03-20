from lingpy import *

# you might need to change the working directory using package "os" and command "os.chdir('path_to_file')"
na_wordlist = get_wordlist('na_cognates_long.csv', col="Language", row="Concept")
convert.strings.write_nexus(na_wordlist, mode="BEAST", filename='na_cognates.nex', ref="value")