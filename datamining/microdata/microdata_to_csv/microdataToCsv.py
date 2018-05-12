import json
import csv
import time
start = time.time()

disconsider_vars = []
disconsider_lines_with_empty_values = False
process_full_file = True
write_header = True

microdatafilename = '../Amostra_Pessoas_35_outras.txt'
layoutjsonfilename = 'out_discons.json'
outfile = 'out.csv'


jsonfile = open(layoutjsonfilename, 'r')
template = json.load(jsonfile)
micodata = open(microdatafilename, 'r')
outfile = open(outfile, 'w', newline='')
bucket_size = 2048

writer = csv.writer(outfile, delimiter=',', quotechar='\"', quoting=csv.QUOTE_ALL)


print('Counting registers in microdata...')

num_lines = sum(1 for line in micodata)

micodata.seek(0)
#num_lines = 80000

print('Registers found: {}'.format(num_lines))

row = []
rows = []


print('Writing the header on the output file')
for elem in template:
    if elem['columnConfigs']['valid'] == True:
        row.append(elem['varid'])

writer.writerow(row)
print('Done.')


print('Processing the microdata file into the output csv file')
linecount = 0
batchCount = 0
for line in micodata:#iterates over each line in the microdata's file
    #print(linecount,  end='')
    row = []#reser the content of the row array


    for elem in template:#for each element in thhe template file (each var)

        if elem['columnConfigs']['valid'] == False:
            continue


        init = int(elem['initpos']) - 1
        fin = int(elem['endpos'])

        if(fin == init):
            fin += 1

        raw_var = line[init:fin].strip()

        if raw_var.isdigit():#if not empty
            if elem['decpartsize'] != None and elem['decpartsize'] != 0:#if is a decimal number
                intpartsz = int(elem['intpartsize'])
                decpartsz = int(elem['decpartsize'])

                raw_var = float('{}.{}'.format(raw_var[:intpartsz], raw_var[intpartsz + decpartsz:]))
            elif elem['type'] == 'N':#if it's an integer
                raw_var = int(raw_var)
            else:
                raw_var = str(raw_var)
        else:
            raw_var = -1
            #break
        row.append(raw_var)
    #writer.writerow(row)

    rows.append(row)

    if len(rows) > bucket_size or ((num_lines - linecount) < bucket_size and linecount == num_lines):
        batchCount += 1
        print("WRITING BATCH #{:6d}| Current line: {:10d} | {:0.2f}% | {:0.2f}s | {:0.2f}min".format(batchCount, linecount, (linecount * 100)/num_lines, time.time() - start, (time.time() - start)/60))
        writer.writerows(rows)
        rows = []


    if linecount == num_lines+1:break
    linecount += 1

print('Done.')

print('Closing files')
jsonfile.close()
micodata.close()
outfile.close()
print('Done')

end = time.time()

print('Time taken : {:0.2f} s'.format(end - start))
print('Time taken : {:0.2f} min'.format((end - start)/60))
