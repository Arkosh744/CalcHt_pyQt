'''Заметки о коде
Т - температура, t - время - ну не получается у меня их назвать другими буквами
i - шаги по пространству, k - шаги по времени
Файл с веществом гружу в память, потому что его надо только читать и всё, в моей постановке нужен importlib, шикарная библиотека
'''

# Данные от юзера
b = 0.050  # м - толщина сляба
T_ini = 25  # градусов цельсия, начальная температура материала

T_up = 500  # градусов цельсия, температура сверху
alpha_up = 150  # вт/м2К коэффициент теплоотдачи сверху
T_down = 500  # градусов цельсия, температура снизу
alpha_down = 30  # вт/м2К коэффициент теплоотдачи снизу

t_comm = 100  # секунд - время процесса

substance = 'test'  # имя материала

# Продвинутые настройки, есть значения по умолчанию
k = 10  # число слоев
dt = 0.1  # секунд, шаг по времени

import importlib


def prop(T, list1):
    '''функция для определения свойств материала от температуры'''
    # функция на вход получает список величин и Температуру

    # Проверка вхождения в массив, если не входит, то возвращает крайние значения
    if T >= list1[0][0]:
        return list1[0][1]
    if T <= list1[len(list1) - 1][0]:
        return list1[len(list1) - 1][1]

    # Поиск нужного значения

    # Иницианизация начальных значений индекса
    index_begin = 0
    index_end = len(list1) - 1

    while True:
        search_index = (index_end + index_begin) // 2
        if list1[search_index][0] < T:
            index_end = search_index
        elif list1[search_index + 1][0] > T:
            index_begin = search_index
        elif list1[search_index + 1][0] == T:
            return list1[search_index][1]
        else:
            dT = list1[search_index][0] - list1[search_index + 1][0]
            dF = list1[search_index][1] - list1[search_index + 1][1]
            return list1[search_index][1] + (T - list1[search_index][0]) * dF / dT


def value_prop(T, mat):
    '''возвращает кортеж из плотности, теплопроводности и теплоемкости при данной температуре'''
    dens = prop(T, mat.density)
    cond = prop(T, mat.conductivity)
    cp = prop(T, mat.specific_heat)
    return dens, cond, cp


# %%

def calc_plast3r(b, T_ini, T_up, alpha_up, T_down, alpha_down, t_comm, substance, k, dt):
    '''расчет пластины с гу 3 рода сверху и снизу'''

    mat = importlib.import_module('materials.' + substance)

    # инициализация начальных значений
    T = []  # массив температур
    E = []  # вспомогательный множитель
    F = []  # вспомогательный сдвиг
    a = []  # температуропроводность

    # дискретизация
    k_sum = int(t_comm // dt) + 1  # уточняем шаг по времени, +1 чтобы точно уложиться без всяких if
    dt = t_comm / k_sum  # скорректированный шаг по времени
    dx = b / k  # размер ячейки

    # нулевые массивы температур и температуропроводности
    for i in range(k):
        T.append(T_ini)
        E.append(0)
        F.append(0)
        dens, cond, cp = value_prop(T_ini, mat)
        a.append(cond / dens / cp)
    time = 0  # счетчик времени
    iteration = 0  # счетчик итераций, пользователю нафиг не нужен, я им отлаживаю

    while time <= t_comm:
        # собственно тут начинается магия итераций по времени

        # нужные начальные вычисления, чтобы пальцы не дрогнули печатая длинную формулу
        cond0 = prop(T[0], mat.conductivity)  # теплопроводность в нулевой точке
        B0 = 1 + 2 * dt / dx * a[0] / cond0 * (alpha_up + cond0 / dx)

        E[0] = 2 * a[0] * dt / dx ** 2 / B0
        F[0] = (T[0] + 2 * a[0] / cond0 * dt / dx * alpha_up * T_up) / B0

        # Заполение массива E и F
        for i in range(1, k - 1):
            AC = a[i] * dt / dx ** 2  # вспомогательный множитель
            E[i] = (AC / (1 + 2 * AC - AC * E[i - 1]))
            F[i] = ((T[i] + AC * F[i - 1]) / (1 + 2 * AC - AC * E[i - 1]))

        # Определение температуры в последнем узле, выпадает из цикла из-за особенностей вычисления
        cond_end = prop(T[-1], mat.conductivity)
        B_end = 1 + 2 * dt / dx * a[-1] / cond_end * (alpha_down + cond_end / dx)
        D_end = T[-1] + 2 * a[-1] / cond_end * dt / dx * alpha_down * T_down
        T[-1] = (D_end + 2 * a[-1] * dt / dx ** 2 * F[-2]) / (B_end - 2 * a[-1] * dt / dx ** 2 * E[-2])

        # Определяем оставшиеся температуры
        for i in range(k - 1):
            l = k - 2 - i
            T[l] = E[l] * T[l + 1] + F[l]
        # Определяем температуропроводность для следующего шага
        for i in range(k):
            dens, cond, cp = value_prop(T[i], mat)
            a.append(cond / dens / cp)
        # Перещелкиваем время и счетчик итераций
        time += dt
        iteration += 1

    print(T, iteration)

    # на выходе нужно только Т, его можно не принт, а return



calc_plast3r(b, T_ini, T_up, alpha_up, T_down, alpha_down, t_comm, substance, k, dt)


'''Начальные данные для задачи с 4 зонами'''

b = 0.245  # м - толщина сляба
T_ini = 25  # градусов цельсия, начальная температура материала

T_up = [1047, 1256, 1250, 1238]  # градусов цельсия, температура сверху - сколько зон столько и температур
T_down = [1047, 1256, 1250, 1238]  # градусов цельсия, температура снизу

t_comm = [1, 1, 1, 1]  # секунд - время процесса

substance = 'sh400'  # имя материала

# Продвинутые настройки, есть значения по умолчанию
k = 10  # число слоев
dt = 0.2  # секунд, шаг по времени


# %%

def calc_plast4r(b, T_ini, T_up, T_down, t_comm, substance, k, dt):
    '''расчет пластины с гу 4 рода сверху и снизу и передачей начальных значений'''

    mat = importlib.import_module('materials.' + substance)
    air = importlib.import_module('materials.air')
    # инициализация начальных значений
    T = []  # массив температур

    temp_res = []  # итоговый массив температур

    # Создание начального массива значений температур и шагов по сетке, для его передачи в итерации.
    dx_air = [0.5, 0.25, 0.12, 0.06, 0.03, 0.015, 0.008, 0.004, 0.002, 0.001, 0.0005]
    dx_comm = [b / k for i in range(k)]

    dx = dx_air + dx_comm + dx_air[
                            ::-1]  # требуемые температуры сидят с 11 по 21 элементы по правилам питона (21 элемент выпадает)

    cpro = [0 for i in dx]  # произведение теплоемкости на плотность
    cond = [0 for i in dx]  # теплопроводность

    T = [T_up[0] for i in range(11)] + [T_ini for i in range(k)] + [T_down[0] for i in
                                                                    range(11)]  # массив температур начальный
    E = [0 for i in range(len(T))]  # вспомогательный множитель
    F = [0 for i in range(len(T))]  # вспомогательный сдвиг

    for m, time_zone in enumerate(t_comm):
        time = 0
        #         temp_res.append(T[11:(11+k)])

        k_sum = int(t_comm[m] // dt) + 1
        dt = t_comm[m] / k_sum

        while time <= t_comm[m]:

            for i in range(len(dx)):
                if i > 10 and i < 11 + k:
                    dens1, cond1, cp1 = value_prop(T[i], mat)
                    cpro[i] = dens1 * cp1
                    cond[i] = cond1
                else:
                    dens1, cond1, cp1 = value_prop(T[i], air)
                    cpro[i] = dens1 * cp1
                    cond[i] = cond1

            E[0] = 0
            F[0] = T_up[m]

            # Заполение массива E и F
            for i in range(1, len(dx) - 1):
                AC = cond[i] / cpro[i] * dt / dx[i] ** 2  # вспомогательный множитель
                E[i] = (AC / (1 + 2 * AC - AC * E[i - 1]))
                F[i] = ((T[i] + AC * F[i - 1]) / (1 + 2 * AC - AC * E[i - 1]))
                # Идем снизу вверх, заполняя температуры

            T[-1] = T_down[m]
            for i in range(len(dx) - 1):
                l = len(dx) - 2 - i
                T[l] = E[l] * T[l + 1] + F[l]

            # Перещелкиваем время
            time = time + dt

        temp_res.append(T[11:(11 + k)])

    for i in temp_res:
        print(i)


calc_plast4r(b, T_ini, T_up, T_down, t_comm, substance, k, dt)

air = importlib.import_module('materials.air')
dens, cond, cp = value_prop(25, air)
cp

