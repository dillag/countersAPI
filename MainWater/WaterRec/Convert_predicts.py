import time

def convert_answers(result_predict):
    result_predict = [i.split(" ") for i in result_predict]
    result_predict = [g for g in result_predict if g != '']
    new_a = []
    k = 0
    for i in result_predict:
        new_a.append([])
        for j in i:
            if j != '':
                new_a[k].append(j)
        k += 1
    new_a = new_a[1:]
    mass_numbers = {}
    for i in new_a:
        key = int(str(i[3]).split(".")[0])
        mass_numbers[key] = i[-1]
    mass_numbers = dict(sorted(mass_numbers.items()))
    final_answer = "".join(mass_numbers.values())
    return final_answer

def convert_answers1(result_predict):
    result_predict = [i.split(" ") for i in result_predict]
    result_predict = [g for g in result_predict if g != '']
    new_a = []
    k = 0
    for i in result_predict:
        new_a.append([])
        for j in i:
            if j != '':
                new_a[k].append(j)
        k += 1
    new_a = new_a[1:]
    for i in new_a:
        i[3] = int(str(i[3]).split(".")[0])

    index = [int(str(i[3]).split(".")[0]) for i in new_a]
    index.sort()
    final_answer = ""
    for i in range(len(index)):
        for g in new_a:
            if str(g[3]) == str(index[i]):
                final_answer += str(g[-1])
                break
    return final_answer

