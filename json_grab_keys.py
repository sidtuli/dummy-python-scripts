import json

def grab_keys_from_json(jsonFileName, outFile):
    jsonData = {}
    with open(jsonFileName) as f :
        jsonData = json.load(f)
    
    keys_arr = []
    for key in jsonData.keys():
        keys_arr.append(key)
    #print(keys_arr)

    with open(outFile, "w") as outputFile:
        for line in keys_arr:
            outputFile.write(line + "\n")


