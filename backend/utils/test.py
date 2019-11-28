# -*- coding: utf-8 -*-
# author: timor

cp_money = {
    'A': 5000000,
    'B': 20000,
    'C': 3000,
    'D': 200,
    'E': 10,
    'F': 5,
}


def countMoney(red, blue):
    x, y = 6, 3
    n = x * red + y * blue
    if n == 39:
        return 'A'
    elif n == 36:
        return 'B'
    elif n == 33:
        return 'C'
    elif n == 30 or n == 27:
        return 'D'
    elif n == 24 or n == 21:
        return 'E'
    elif n == 15 or n == 9 or n == 3:
        return 'F'
    else:
        return 'G'


def countSsq(lst, ssq):
    ssq_red = ssq[:6]
    ssq_blue = ssq[-1]
    all_cp = []
    all_money = 0
    for l in lst:
        src_red = l[:6]
        src_blue = l[-1]
        red = len([x for x in src_red if x in set(ssq_red)])

        if ssq_blue == src_blue:
            level = countMoney(red, 1)
        else:
            level = countMoney(red, 0)

        if level != 'G':
            all_money += cp_money[level]
            all_cp.append(l)

    return {"all_cp": all_cp, "all_money": all_money}


if __name__ == '__main__':
    lst = [[16, 17, 18, 22, 23, 30, 4], [2, 7, 12, 24, 26, 32, 9], [11, 12, 16, 25, 29, 32, 15]]
    ssq = [2, 3, 6, 8, 14, 22, 4]
    print(countSsq(lst, ssq))
