import os
import json

# Название файла свойств
mat_name = 'X70'

path = os.path.join(os.path.dirname(os.path.realpath(__file__)), f'materials\\{mat_name}')

# Файлы со свойствами из JmatPro
# Формат файлов .dat (первые 2 строчки с названиями обязательны)

# Specific heat (J/(g K))
#  'T (C)'	'CP'
# 1200.0	0.66166
# ...

# !!! .dat файлы должны находится в директории \materials относительно исполняемого скрипта !!!

link_1_cond = f'{path}_cond.dat'
link_2_cp = f'{path}_sh.dat'
link_3_dens = f'{path}_dens.dat'

data1_cond, data2_cp, data3_dens = [], [], []


def prepare_data(link, data):
    with open(link, 'r') as file:
        file.readline()
        file.readline()
        for row in file:
            current_data = row.splitlines()[0].split('\t')
            if current_data[0] != '':
                [*float_data] = map(float, current_data)
                data.append(float_data)


def write_data(path):
    with open(f'{path}.py', 'a') as file_w:
        file_w.write(f'density = ')
        json.dump(data3_dens, file_w)
        file_w.write('\n')
        file_w.write(f'conductivity = ')
        json.dump(data1_cond, file_w)
        file_w.write('\n')
        file_w.write(f'specific_heat = ')
        json.dump(data2_cp, file_w)
        file_w.write('\n')


prepare_data(link_1_cond, data1_cond)
prepare_data(link_2_cp, data2_cp)
prepare_data(link_3_dens, data3_dens)

for row in range(len(data3_dens)):
    data3_dens[row][1] = data3_dens[row][1] * 1000
for row in range(len(data2_cp)):
    data2_cp[row][1] = data2_cp[row][1] * 1000


if os.path.exists(f'{path}.py'):
    print(f'Вы перезаписали файл {path}')
    os.remove(f'{path}.py')
    write_data(path)
    os.remove(link_1_cond)
    os.remove(link_2_cp)
    os.remove(link_3_dens)
else:
    print(f'Создан новый файл {path}')
    write_data(path)
    os.remove(link_1_cond)
    os.remove(link_2_cp)
    os.remove(link_3_dens)



