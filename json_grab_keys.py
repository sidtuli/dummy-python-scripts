import json

def readJson(jsonFileName, outFile):
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



readJson("result.json", "result_json_keys.txt")