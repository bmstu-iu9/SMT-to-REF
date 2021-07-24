def insertNot(data):
        t = data[len(data) - 1]
        s = list(["expr", "(", "not", ")"])
        s.insert(3, t)
        a = len(data) - 1
        data[a] = s
        if (len(data) > 2):
            data[1] = insertNot(list(data[1]))
        return data

def throwNot(data):
     if (len(data) > 3 and data[2] == "not" and len(data[3]) > 2 and data[3][2] == "not"):
        data = list(data[3][3])
     elif (data[2] == "not" and data[3][1][0] != "pred"):
        data = list(data[3])
        if (len(data) > 2):
            if (data[2] == "or"):
                data.remove("or")
                data.insert(2, "and")
                data[3] = insertNot(list(data[3]))
            elif (data[2] == "and"):
                data.remove("and")
                data.insert(2, "or")
                data[3] = insertNot(list(data[3]))
        else:
            data.insert(1,"(")
            data.insert(2,"not")
            data.insert(4,")")

     return data


def predCreate(data,preds):
    if (data[2] == "str.contains"):
        preds.append(("p" + str(len(preds)),(data[3]),data[2],data[3],data[4]))
    else:
        preds.append(("p" + str(len(preds)),(data[3],data[4]),data[2], data[3], data[4]))
        del data[2]
        del data[2]
        del data[2]
        data.insert(2,"p" + str(len(preds)))
    return data,preds


def createPredAndDelNot(data, preds):
    if data[0] != "pred":
        for i in range(1,len(data)):
            t = data[i]
            if t == "not":
                data = throwNot(list(data))

        for i in range(1,len(data)):
            t = data[i]
            if (type(t) == list or type(t) == tuple):
                data[i], preds = createPredAndDelNot(list(t), list(preds))
    else:
        data,preds = predCreate(list(data),preds)
    return data,preds


def distrCheak(cheak,distr_mass,data):
    if (len(data) > 2):
        if (len(data[2]) > 2 and data[2][2] == "and"):
            cheak = True
            distr_mass.append(data[2][3])
        else:
            distr_mass[0].append(data[2])
        cheak,distr_mass = distrCheak(cheak,list(distr_mass),list(data[1]))
        return cheak,distr_mass
    else:
        if (len(data[1]) > 2 and data[1][2] == "and"):
            cheak = True
            distr_mass.append(data[1][3])
        else:
            distr_mass[0].append(data[1])
        return cheak,distr_mass


def packSimple(pack,i,data):
    pack.append("exprs")
    pack.append(data[i])
    if (len(data)-1 > i):
        pack.insert(1,list())
        pack[1] = packSimple(list(),i+1,data)
    return pack


def cheakList(mass,choiseList,index):
    choiseList[index] = choiseList[index] + 1
    if (choiseList[index] >= len(mass[index])):
        choiseList[index] = 0
        if (index -1 > 0):
            choiseList = cheakList(mass,choiseList,index - 1)
    return choiseList


def packFromChoiseList(i,pack, distr_mass, choiseList):
    if (len(pack) > 2):
        pack[1] = packFromChoiseList(i,pack[1],distr_mass,choiseList)
    else:
        pack.insert(1,list())
        pack[1].append("exprs")
        pack[1].append(distr_mass[i][choiseList[i]])
        if (i+1 < len(choiseList)):
            pack.insert(1,packFromChoiseList(i+1,pack[1],distr_mass,choiseList))
    return pack


def packD(pack,data,distr_mass, choiseList):
    data.append("exprs")
    data.append(list())
    data[1].append("expr")
    data[1].append("(")
    data[1].append("or")
    data[1].append(list())
    data[1].append(")")
    data[1] = packFromChoiseList(0,pack,distr_mass,choiseList)
    choiseList = cheakList(distr_mass,choiseList,len(choiseList)-1)
    data.insert(1,packD(pack,data[1],distr_mass,choiseList))
    return data


def app(data,distr_mass):
    data[2] = "and"
    if (len(distr_mass[0]) > 0):
        pack= list()
        pack = packSimple(pack,0,list(distr_mass[0]))
    choiseList = list()
    for i in range(1,len(distr_mass)):
        choiseList.append(0)
    data[3] = packD(pack,data[3],distr_mass,choiseList)
    pass


def distrAppication(data):
        for i in range(1, len(data)):
            t = data[i]
            if (t == "or"):
                distr_mass = ()
                distr_mass = list(distr_mass)
                distr_mass.append(list())
                cheak,distr_mass = distrCheak(False,list(distr_mass),list(data[3]))
                if (cheak):
                    data = app(list(data),list(distr_mass))

        for i in range(1, len(data)):
            t = data[i]
            if (type(t) == list or type(t) == tuple):
                data[i] = distrAppication(list(t))
        return data,


def translateToCNF(data):
    preds = []
    for i in range(1,len(data)):
        t = data[i]
        if t[0] == "asserts":
            data[i],preds = createPredAndDelNot(list(t), list(preds))
          #  data[i] = distrAppication(list(data[i]))

    return data,preds