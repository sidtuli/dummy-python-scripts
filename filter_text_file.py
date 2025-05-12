import re
import json

def filter_text_to_out_file(input_text_file, output_text_file, regex_phrase):
    with open(input_text_file) as input:
        lines = input.readlines()

        #print(re.search(regex_phrase, lines[0]))

        with open(output_text_file, 'r+') as output:
            for line in lines:
                if(re.search(regex_phrase, line)):
                    output.write(line.rstrip() + '\n')
                    #if('\n' in line):
                    #    output.write(line)
                    #else:
                    #    output.write(line + "\n")
                    
def remove_matching_lines(input_file, regex_phrase):
    with open(input_file,'r+') as input:
        lines = input.readlines()

        # https://stackoverflow.com/questions/2769061/how-to-erase-the-file-contents-of-text-file-in-python
        input.seek(0)
        input.truncate(0)

        for line in lines:
            if not(re.search(regex_phrase,line)):
                input.write(line.rstrip() + '\n')
                #if('\n' in line):
                    #input.write(line)
                #else:
                    #input.write(line+ "\n")

def flag_non_unique_lines(textLines):
    linesDict={}

    for line in textLines:
        line = line.rstrip()
        if line in linesDict:
            linesDict[line] += 1
        else:
            linesDict[line] = 1
    # lineKeys = []
    # for key in linesDict:
    #     lineKeys.append(key)

    # for lineKey in lineKeys:
    #     if linesDict[lineKey] <= 1:
    #         del linesDict[lineKey]
    #     else:
    #         print(lineKey)
    
    return linesDict


def filterNonUniqueLines(textFile, outFile):
    lines = []
    with open(textFile) as f:
        lines = f.readlines()
    
    nonUniqueLinesDict = flag_non_unique_lines(lines)

    with open(outFile, 'w+') as fp:
        json.dump(nonUniqueLinesDict, fp)

    with open(textFile, "w+") as testFile:
        for key in nonUniqueLinesDict:
            testFile.write(key + "\n")



search_term = ""
#filter_text_to_out_file("jojo.txt", "filter_saved.txt", search_term)
#filter_text_to_out_file("filter_saved.txt", "deleted_posts.txt", search_term)
#filter_text_to_out_file("saved_post.txt", "filter_saved.txt", search_term)
#remove_matching_lines("saved_post.txt", search_term)

filterNonUniqueLines("jojo.txt", "jojo_dups.json")

