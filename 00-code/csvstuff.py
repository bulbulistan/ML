import csv
import time
import json

t = time.process_time()

queryResults = [('ܕܫܒܬܐ', 0.8489677309989929),
 ('ܠܠܝܐ', 0.8186253309249878),
 ('ܕܝܘܡܐ', 0.7990292906761169),
 ('ܐܝܡܡܐ', 0.7648172378540039),
 ('ܒܝܘܡܐ', 0.7487006187438965),
 ('ܪܡܫܐ', 0.7345137596130371),
 ('ܫܒܬܐ', 0.7199773788452148),
 ('ܐܚܪܝܐ', 0.7182391881942749),
 ('ܘܐܝܡܡܐ', 0.7158458232879639),
 ('ܥܕܢܐ', 0.7127423286437988)]


allWords = {}

with open("x:\\data\\Simtho-gensim\\model\\simtho999-10-25.csv", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=",")
    next(reader)
    for x in reader:        
        allWords[x[0]] = [float(x[1]), float(x[2])]
    
queryResults = dict(queryResults)


for key in queryResults:    
    x = allWords[key]    
    x.append(queryResults[key])
    queryResults[key] = x

print(queryResults)

print("Done, the processing took " + str(time.process_time() - t) + " seconds")

json.dumps(queryResults)