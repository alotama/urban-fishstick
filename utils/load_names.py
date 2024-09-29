import csv

def load_names(file_path):
    name_list = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            name_list.append(row[1])
    return name_list