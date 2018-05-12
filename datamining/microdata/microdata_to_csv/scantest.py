import time

start = time.time()

file = open('../Amostra_Pessoas_35_outras.txt', 'r')

line_counter = 0

for line in file:
    x = str(line)


file.close()

end = time.time()
print(end - start)