import csv




storeinput = input("Enter a list of stores seperated by a single space and/or commas, or enter the file path to a CSV file with all stores listed in the first column: ")

if ".csv" in storeinput:
    with open('storelist.csv',encoding='utf-8-sig') as storelist_file:
        storelist = []
        csv_reader = csv.reader(storelist_file,delimiter=',')
        for row in csv_reader:
            storelist.append(row[0])
elif ", " in storeinput:
    storelist = storeinput.split(", ")
elif "," in storeinput:
    storelist = storeinput.split(",")
else:
    storelist = storeinput.split(" ")
print(storelist)
