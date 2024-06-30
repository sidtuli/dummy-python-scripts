import csv

def process_CSV_file(csv_file_path, column, out_file_path):
    try:
        with open(csv_file_path) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            print(csv_reader)
            with open(out_file_path, 'w+') as out_file:
                for row in csv_reader:
                    print(row[column])
                    out_file.write(row[column] + "\n")

            

    except:
        print("Failure")

process_CSV_file("saved_posts.csv", "permalink", "saved_post.txt")