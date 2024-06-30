import re
def filter_text_to_out_file(input_text_file, output_text_file, regex_phrase):
    with open(input_text_file) as input:
        lines = input.readlines()

        #print(re.search(regex_phrase, lines[0]))

        with open(output_text_file, 'r+') as output:
            for line in lines:
                if(re.search(regex_phrase, line)):
                    if('\n' in line):
                        output.write(line)
                    else:
                        output.write(line + "\n")
                    
def remove_matching_lines(input_file, regex_phrase):
    with open(input_file,'r+') as input:
        lines = input.readlines()

        # https://stackoverflow.com/questions/2769061/how-to-erase-the-file-contents-of-text-file-in-python
        input.seek(0)
        input.truncate(0)

        for line in lines:
            if not(re.search(regex_phrase,line)):
                if('\n' in line):
                    input.write(line)
                else:
                    input.write(line + "\n")

search_term = "program"
filter_text_to_out_file("saved_post.txt", "deleted_post.txt", search_term)
filter_text_to_out_file("saved_post.txt", "deleted_posts.txt", search_term)
remove_matching_lines("saved_post.txt", search_term)