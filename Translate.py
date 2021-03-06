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

def EqualExprs(exp1,exp2):
    if (exp1[1][0] == "pred" and exp2[1][0] == "pred"):
        if (exp1[1] == exp2[1]):
            return True
        else:
            return False
    else:
        if (len(exp1) == len(exp2) and exp1[2] == exp2[2]):
            list1 = RecToList(exp1[3],list())
            list2 = RecToList(exp2[3],list())
            if (len(list1) != len(list2)):
                return False
            else:
                cheak =  list()
                cheak2 = list()
                for i in range(0,len(list1)):
                    cheak.append(False)
                    cheak2.append(True)
                for i in range(0,len(list1)):
                    expr1 = list1[i]
                    for j in range(0, len(list2)):
                        expr2 = list2[j]
                        if (EqualExprs(expr1,expr2) and cheak2[j]):
                            cheak[i] = True
                            cheak2[j] = False
                            continue
                flag = True
                for f in cheak:
                    if (not f):
                        flag = False
                if (flag):
                    return True
                else:
                    return False
        else:
            return False

def RecToList(data,list):
    if (len(data) > 2):
        list.append(data[2])
        list = RecToList(data[1],list)
        return list
    else:
        list.append(data[1])
        return list

def ListToRec(lis,data,pos):
    data.append("exprs")
    data.append(lis[pos])
    pos = pos + 1
    if (pos != len(lis)):
        data.insert(1,ListToRec(lis,list(),pos))
    return data


def isPredEq(data, preds):
    for i in range(0,len(preds)):
        p = preds[i]
        if (data[2] == "="):
            if (data[2] == p[2] and ((data[3] == p[3] and data[4] == p[4]) or (data[3] == p[4] and data[4] == p[3]))):
                return True,i
        else:
            if (data[2] ==p[2] and data[3] == p[3] and data[4] == p[4]):
                return True, i
    return False,-1

def predCreate(data,preds):
    flag,pos = isPredEq(data,preds)
    if (not flag):
        if (data[2] == "str.contains"):
            preds.append(("p" + str(len(preds)),(data[3]),data[2],data[3],data[4]))
        else:
            preds.append(("p" + str(len(preds)),(data[3],data[4]),data[2], data[3], data[4]))
        del data[2]
        del data[2]
        del data[2]
        data.insert(2,"p" + str(len(preds)-1))
        return data,preds
    else:
        del data[2]
        del data[2]
        del data[2]
        data.insert(2, "p" + str(pos))
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
    pack.append(list(data[i]))
    if (len(data)-1 > i):
        pack.insert(1,list())
        pack[1] = list(packSimple(list(),i+1,data))
    return pack


def cheakList(mass,choiseList,index):
    cheak = True
    choiseList[index] = choiseList[index] + 1
    if (choiseList[index] >= len(mass[index+1])):
        choiseList[index] = 0
        if (index > 0):
            cheak ,choiseList = cheakList(mass,choiseList,index - 1)
        else:
            return False,choiseList
    return cheak, choiseList



def packFromChoiseList(i,pack, distr_mass, choiseList):
    lis = list(pack)
    if (len(pack) > 2):
        pack[1] = packFromChoiseList(i,list(pack[1]),distr_mass,choiseList)
    else:
        if (len(pack) != 0):
            pack.insert(1,list())
            pack[1] = list(pack[1])
            pack[1].append("exprs")
            pack[1].append(distr_mass[i+1][choiseList[i]])
            if (i+1 < len(choiseList)):
                pack[1]= packFromChoiseList(i+1,list(pack[1]),distr_mass,choiseList)
        else:
            pack.append("exprs")
            pack.append(distr_mass[i + 1][choiseList[i]])
            if (i + 1 < len(choiseList)):
                pack = packFromChoiseList(i + 1, list(pack), distr_mass, choiseList)
    return pack


def reloadMass(distr_mass,lis):
    if (len(distr_mass) > 2):
        lis.append(distr_mass[2])
        lis.append(reloadMass(distr_mass[1],list()))
    else:
        return distr_mass[1]
    return lis


def packD(pack,data,distr_mass, choiseList):
    data.append("exprs")
    data.append(list())
    data[1].append("expr")
    data[1].append("(")
    data[1].append("or")
    data[1].append(list())
    data[1].append(")")
    data[1][3] = packFromChoiseList(0,list(pack),distr_mass,choiseList)
    cheak, choiseList = cheakList(distr_mass,choiseList,len(choiseList)-1)
    if (cheak):
        data.insert(1,packD(pack,list(),distr_mass,choiseList))
    return data


def app(data,distr_mass):
    data[2] = "and"
    pack= list()
    if (len(distr_mass[0]) > 0):
        pack = list()
        pack = packSimple(pack,0,list(distr_mass[0]))
    else:
        pack = list()
    choiseList = list()
    for i in range(1,len(distr_mass)):
        choiseList.append(0)
        distr_mass[i] = reloadMass(distr_mass[i], list());
    data[3] = packD(pack,list(),distr_mass,choiseList)
    return data


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
               # data[i] = list(data[i])
                data[i] = list(distrAppication(list(t)))
        return data


def DelSameElemsForDis(data):
    if (len(data) == 2 and data[0] != "expr"):
        data[1] = DelSameElemsForDis(data[1])
    elif (len(data) == 3):
        data[2] = DelSameElemsForDis(data[2])
        data[1] = DelSameElemsForDis(data[1])
    else:
        if (len(data) != 2 ):
            res = list()
            if (data[2] == "or"):
                list1 = RecToList(data[3],list())
                list2 = list(list1)
                for i in range(0,len(list1)):
                    l = list1[i]
                    flag = True
                    for j in range(0,len(res)):
                        l2 = res[j]
                        if (EqualExprs(l,l2)):
                            flag = False
                    if (flag):
                        res.append(l)
                res = ListToRec(res,list(),0)
                data[3] = res
                if (len(data[3]) == 2):
                    data = data[3]
                    data = DelSameElemsForDis(data)
                else:
                    data[3] = DelSameElemsForDis(data[3])
            else:
                data[3] = DelSameElemsForDis(data[3])
    return data





def DelSameElemsRecForDis(data):
    if (len(data) > 2):
        data[2] = DelSameElemsForDis(data[2])
        data[1][3] = DelSameElemsRecForDis(data[1][3])
    else:
        data[1][3] = DelSameElemsForDis(data[1][3])
    return data


def OposExprs(l, l2):
    if (len(l) > 3 and l[2] == "not"):
        return EqualExprs(l[3],l2)
    elif(len(l2) > 3 and l2[2] == "not"):
        return EqualExprs(l2[3],l)
    else:
        return False


def DelOposLitForDis(data):
    if (len(data) == 2 and data[0] != "expr"):
        data[1] = DelOposLitForDis(data[1])
        if (data[1] == list()):
            return list()
    elif (len(data) == 3):
        data[2] = DelOposLitForDis(data[2])
        if (data[2] == list()):
            data = data[1]
        data[1] = DelOposLitForDis(data[1])
        if (data[1] == list()):
            del data[1]
    else:
        if (len(data) != 2 ):
            res = list()
            if (data[2] == "or"):
                list1 = RecToList(data[3],list())
                list2 = list(list1)
                for i in range(0,len(list1)):
                    l = list1[i]
                    flag = True
                    for j in range(0,len(list2)):
                        l2 = list2[j]
                        if (i !=j and OposExprs(l,l2)):
                            flag = False
                    if (flag):
                        res.append(l)
                if (res == list()):
                    return list()
                else:
                    res = ListToRec(res,list(),0)
                    data[3] = res
                    if (len(data[3]) == 2):
                        data = data[3]
                        data = DelOposLitForDis(data)
                    else:
                        data[3] = DelOposLitForDis(data[3])
            else:
                data[3] = DelOposLitForDis(data[3])
    return data


def DelOposLitRecForDis(data):
    if (len(data) > 2):
        data[2] = DelOposLitForDis(data[2])
        data[1][3] = DelOposLitRecForDis(data[1][3])
    else:
        data[1][3] = DelOposLitForDis(data[1][3])
    return data


def CheakAssoc(data):
    if (len(data) == 2 and data[0] != "expr"):
        data[1] =CheakAssoc(data[1])
    elif (len(data) == 3):
        data[2] = CheakAssoc(data[2])
        data[1] = CheakAssoc(data[1])
    else:
        if (len(data) != 2):
            res = list()
            if (data[2] == "or"):
                list1 = RecToList(data[3],list())
                for i in range(0,len(list1)):
                    l = list1[i]
                    if (len(l) > 3 and l[2] == "or"):
                        res.append(RecToList(l[3]))
                res.extend(list1)
                res = ListToRec(res,list(),0)
                data[3] = res
                data[3] = CheakAssoc(data[3])
            elif(data[2] == "and"):
                list1 = RecToList(data[3], list())
                for i in range(0, len(list1)):
                    l = list1[i]
                    if (len(l) > 3 and l[2] == "and"):
                        res.extend(RecToList(l[3],list()))
                    else:
                        res.append(l)
                res = ListToRec(res, list(), 0)
                data[3] = res
                data[3] = CheakAssoc(data[3])
            else:
                data[3] = CheakAssoc(data[3])
    return data


def CheakAssocRec(data):
    if (len(data) > 2):
        data[2] = CheakAssoc(data[2])
        data[1][3] = CheakAssocRec(data[1][3])
    else:
        data[1][3] = CheakAssoc(data[1][3])
    return data


def isIncude(l2, l):
    if (len(l2) == 2 or l2[2] == "not"):
        if(EqualExprs(l2,l)):
            return True
        else:
            return False
    else:
        if (len(l) > 3 and l2[2] == l[2]):
            list1 = RecToList(l[3],list())
            list2 = RecToList(l2[3],list())
            cheakList1 = list()
            cheakList2 = list()
            for i in range(0,len(list1)):
                cheakList1.append(False)
            for i in range(0,len(list2)):
                cheakList2.append(False)

            for i in range(0,len(list1)):
                l_1 = list1[i]
                for j in range(0, len(list2)):
                    l_2 = list2[j]
                    if (not cheakList1[i] and not cheakList2[j] and EqualExprs(l_1,l_2)):
                        cheakList2[j] = True
                        cheakList1[i] = True
                        break
            flag = True
            for i in range(0,len(cheakList1)):
                if (cheakList1[i] == False):
                    flag = False
            return flag
        else:
            list2 = RecToList(l2[3])
            for i in range(0, len(list2)):
                l2 = list2[i]
                if (EqualExprs(l2,l)):
                    return  True
            return False

def DelSameSets(data):
    if (len(data) == 2 and data[0] != "expr"):
        data[1] =DelSameSets(data[1])
    elif (len(data) == 3):
        data[2] = DelSameSets(data[2])
        data[1] = DelSameSets(data[1])
    else:
        if (len(data) != 2):
            res = list()
            if (data[2] == "and"):
                list1 = RecToList(data[3],list())
                for i in range(0,len(list1)):
                    l = list1[i]
                    flag = True
                    for j in range(0,len(list1)):
                        l2 = list1[j]
                        if (i != j and isIncude(l2,l)):
                            flag = False
                            break
                    if (flag):
                        res.append(l)
                res = ListToRec(res,list(),0)
                if (len(res) == 2):
                    data = res[1]
                    data = DelSameSets(data)
                else:
                    data[3] = res
                    data[3] = DelSameSets(data[3])
            else:
                data[3] = DelSameSets(data[3])
    return data


def DelSameSetsRec(data):
    if (len(data) > 2):
        data[2] = DelSameSets(data[2])
        data[1][3] = DelSameSetsRec(data[1][3])
    else:
        data[1][3] = DelSameSets(data[1][3])
    return data


def hasOposElems(exp1, exp2):
    if (OposExprs(exp1,exp2)):
        return True,list(),list()
    else:
        list1 = list()
        list2 = list()
        if (len(exp1) > 2 and exp1[2] != "not"):
            list1 = RecToList(exp1[3],list())
        else:
            list1.append(exp1)
        if (len(exp2) > 2 and exp2[2] != "not"):
            list2 = RecToList(exp2[3],list())
        else:
            list2.append(exp2)
        cheak1 = list()
        cheak2 = list()
        for i in range(0, len(list1)):
            cheak1.append(False)
        for i in range(0, len(list2)):
            cheak2.append(False)
        flag = True
        for i in range(0, len(list1)):
            l = list1[i]
            for j in range(0, len(list2)):
                l2 = list2[j]
                if (OposExprs(l,l2)):
                    flag = False
                    cheak1[i] = True
                    cheak2[j] = True
                    break
        if (flag):
            return False,list(),list()
        else:
            res1 = list()
            res2 = list()
            for i in range(0, len(list1)):
                if (not cheak1[i]):
                    res1.append(list1[i])
            for i in range(0, len(list2)):
                if (not cheak2[i]):
                    res2.append(list2[i])
            return True,res1,res2


def createFalsePred(preds):
    pred = list()
    pred.append("p_false")
    pred.append(list())
    pred.append("=")
    pred.append(list())
    pred.append(list())
    pred[3].append("const")
    pred[3].append("a")
    pred[4].append("const")
    pred[4].append("b")
    data = list()
    preds.append(pred)
    data.append("expr")
    data.append(list())
    data[1].append("pred")
    data[1].append("(")
    data[1].append("p_false")
    data[1].append(")")
    return data,preds



def ResolRule(data,preds):
    if (len(data) == 2 and data[0] != "expr"):
        data[1],preds =ResolRule(data[1],preds)
    elif (len(data) == 3):
        data[2],preds = ResolRule(data[2],preds)
        data[1],preds = ResolRule(data[1],preds)
    else:
        if (len(data) != 2):
            res = list()
            if (data[2] == "and"):
                list1 = RecToList(data[3],list())
                cheak1 = list()
                cheak2 = list()
                for i in range(0, len(list1)):
                    cheak1.append(True)
                for i in range(0,len(list1)):
                    l = list1[i]
                    flag = False
                    for j in range(0,len(list1)):
                        l2 = list1[j]
                        if (i != j and cheak1[j] and cheak1[i]):
                            flag = True
                            cheak,l_1,l_2 = hasOposElems(l2,l)
                            if (cheak):
                                if (l_1 != list() and l_2 != list()):
                                    cheak1[i] = False
                                    cheak1[j] = False
                                    flag = False
                                    l_1.extend(l_2)
                                    if (len(l_1) > 1):
                                        midres = list()
                                        midres.append("expr")
                                        midres.append("(")
                                        midres.append("or")
                                        midres.append("(")
                                        midres.append(list())
                                        midres.append(")")
                                        midres[3] = ListToRec(l_1,list(),0)
                                        res.append(midres)
                                    else:
                                        res.append(l_1[0])
                                    break
                                else:
                                    data,preds = createFalsePred(preds)
                                    return data, preds
                    if (flag):
                        res.append(l)

                res = ListToRec(res,list(),0)
                if (len(res) == 2):
                    data = res[1]
                    data,preds = ResolRule(data,preds)
                else:
                    data[3] = res
                    data[3],preds = ResolRule(data[3],preds)
            else:
                data[3],preds = ResolRule(data[3],preds)
    return data,preds


def ResolRuleRec(data,preds):
    if (len(data) > 2):
        data[2],preds = ResolRule(data[2],preds)
        data[1][3],preds = ResolRuleRec(data[1][3],preds)
    else:
        data[1][3],preds = ResolRule(data[1][3],preds)
    return data,preds


def translateToCNF(data):
    preds = []
    for i in range(1,len(data)):
        t = data[i]
        if t[0] == "asserts":
            data[i],preds = createPredAndDelNot(list(t), list(preds))
            data[i] = distrAppication(list(data[i]))
            data[i] = DelSameElemsRecForDis(list(data[i]))
            data[i] = DelOposLitRecForDis(list(data[i]))
            data[i] = CheakAssocRec(list(data[i]))
            data[i],preds = ResolRuleRec(list(data[i]),preds)
            data[i] = DelSameSetsRec(list(data[i]))

    return data,preds
