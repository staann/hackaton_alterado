import csv
csv_path = 'departamentos_unb_2.csv'
count = 0
with open(csv_path,'r') as file:
    csv_reader = csv.reader(file)
    data_lista = []
    for row in csv_reader:
        #x = row
        count +=1
        if (row[0]=='ï»¿id'):
            print('excessao')

        elif (int(row[0])==0):
            print('excessao')

        
        else:
            data_lista.append(int(row[0]))



print(data_lista)