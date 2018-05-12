import csv
import copy
from pprint import pprint
import json



def processNum(num):
    if not num.isdigit():
        return 0
    else:
        return int(num)

filename = "Layout_Microdados_Pessoas.csv"


out_file = open("out.json", 'w+')
layout_file = open(filename, 'r', encoding="utf8")
spamreader = csv.reader(layout_file, delimiter=';', quotechar='|')






answ = []

line_count = 0



for row in spamreader:
    print(", ".join(row))
    element_count = 0

    line_holder = ({
    "varid": "",
    "varname":"",
    "initpos": -1,
    "endpos": -1,
    "intpartsize": -1,
    "decpartsize": -1,
    "type": "",

    "dictText": "",
    "dict" : {},

    "columnConfigs": {
        "valid": True
    }
    })

    for element in row:
        element = str(element).strip()
        if line_count >= 2:
            if element_count == 0:
                line_holder['varid'] = str(element)

            if element_count == 1:
                pass
                elem_split = element.split('\n')
                line_holder['varname'] = elem_split[0].split(' –')[0].strip().replace(':', '')

                if len(elem_split) > 1:
                    if elem_split[1].split('-')[0].strip().isdigit():
                        tmp_dict = {}
                        for dict_line in elem_split[1:]:
                            line_division = dict_line.split('-')

                            code = line_division[0].strip()

                            if len(line_division) > 1:
                                value = dict_line.split('-')[1].strip().replace('\n', '')
                            else:
                                value = code
                                code = ''

                            #tmp_dict.append({code, value})
                            tmp_dict[code] = value
                        line_holder['dict'] = tmp_dict
                    else:
                        line_holder['dictText'] = ' '.join(elem_split).replace('\n', ' ')

                else:
                   line_holder['dictText'] = elem_split[0]



            if element_count == 7:
                '''initial pos'''
                line_holder['initpos'] = processNum(element)

            if element_count == 8:
                '''end pos'''
                line_holder['endpos'] = processNum(element)

            if element_count == 9:
                '''int part'''
                line_holder['intpartsize'] = processNum(element)

            if element_count == 10:
                '''dec part'''
                line_holder['decpartsize'] = processNum(element)
                pass

            if element_count == 11:
                '''type'''
                line_holder['type'] = str(element)

        element_count += 1
    line_count += 1

    if line_count > 2:
        answ.append(copy.deepcopy(line_holder))




pprint(answ)


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

string = json.dumps(answ, default=set_default)

out_file.write(string)

out_file.close()
layout_file.close()