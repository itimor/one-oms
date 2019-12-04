# -*- coding: utf-8 -*-
# author: timor


def testrecurse(z, target):
    a = dict()
    a[z] = z
    if z >= target:
        return cc
    return [a] + testrecurse(2 * z, target)


if __name__ == '__main__':
    print(testrecurse(1, 1000))



def setMenuUp(menuMapAll, menuid, menuMap):
    if menuid in menuMapAll:
        mid = menuMapAll[menuid].id
        if mid in menuMap:
            return [menuMap]
        else:
            menuMap[mid] = menuMapAll[menuid]
            return [menuMap] + setMenuUp(menuMapAll, menuMapAll[menuid].parent, menuMap)
