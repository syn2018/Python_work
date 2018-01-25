from sys import argv # argument vector - might need this ... 
import os # we have the open() function here 
import re # regex 
from collections import Counter, OrderedDict, defaultdict
import operator 
import itertools # to loop through multiple dimension arrays 
from itertools import product 

# Data modules
from tabulate import tabulate # tabulate module 
import pandas as pd # pandas module
import numpy as np # numpy module 
import matplotlib.pyplot as plt # data visualization module 

dir = '/home/noh/Desktop/Program/Python/Eigen/testdocs/txt' # Directory containing the paragraph/essays. This can be changed as needed
final_table = {}

for root, dirs, filenames in os.walk(dir): # looping over each txt 
    for f in filenames: # loop over each file 
        log = open(os.path.join(root, f), 'r') 
        doc_text = log.read() # Commit the text to a variable. Call on 'doc_text'
        #        print doc_text, f  # print to make sure we are printing out text from all the .txt files
        ## Find all the words 
        words = re.findall(r'\w+', doc_text) # This finds words in each file, whilst still in the .txt loop, using simple regex
        word_counts = Counter(words) # counts the number each time a word appear
        ordered = OrderedDict(sorted(word_counts.items(), key=lambda x: x[1])) ## Now, this is an ordered dict with the word and the frequency
        # Now, loop through the ordered dict
        for key, value in ordered.iteritems():
            # print key, value, f
            text = str(key) # stringify the text, for use in regex if needed, and to search for it in the text  
            single_element = {text: [f, [s+ '.' for s in doc_text.split('.') if text in s]]} # The dict input we want, as this is compatible with pandas module for tabular output as well 
            final_table.update(single_element) # update the 'global' scope dict with the single_element dicts

# To merge the same words (or keys) in the final_table dict 
result = defaultdict(list)
for key, value in final_table.iteritems():
    result[key].append(value)

text_table = []
# Testing this worked, through a simple print procedure
for key,value in result.iteritems():
    key1 = result[key]
#    print key, key1[0][0], key1[0][1] # Access each element of the dictionary key element. The key is a 1d-array with a 2d-array inside it, so
    # we need to specifify the 0th column and then the 0th and first column to get the document.txt file and the sentence
    text_table.append([key,key1[0][0],key1[0][1]]) # append to the final_table 
    # Convert into pandas dataframe

print tabulate(text_table) # we use the tabulate module to print out our result. 
# Not quite perfect, I understand, but I was constrained for time 

# -------------------------------------#
# TODO
#data = pd.DataFrame(data = text_table)
#print tabulate(data) 
# -------------------------------------# 
        
