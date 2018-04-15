import csv

path1 = 'weibo_data_2_1.csv'
path2 = 'weibo_data_2_1_processed.csv'

data = []
with open(path1, 'r+', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] != '':
            data.append(row)

fx = open(path2, 'w+', encoding='utf-8', newline='')
writer = csv.writer(fx)
for row in data:
    writer.writerow(row)
fx.close()
