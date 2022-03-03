
############ helper functions ############

def fill_array():
    numComp = int(input('How many competitors? '))
    print('Enter competitors and their totals one by one: ')
    names = []
    totals = []
    for i in range(1, numComp + 1):
        values = input("Competitor " + str(i) + ": ")
        names.append(values.split(" ")[0])
        totals.append(int(values.split(" ")[1]))
    return [names, totals]

def print_array(arr):
    for item in arr:
        print(item)


def sum_array(arr) -> int:
    sum = 0
    for item in arr:
        sum += item
    return sum


def leftover(original, team1):
    copy = team1.copy()
    result = []
    for x in original:
        if (x not in copy):
            result.append(x)
        else:
            copy.remove(x)
    return result

############ end helper functions ############


############ main sorting functions ############

def best_split1(names, totals, length, half):
    best_diff = 2*half
    team1 = []
    total1 = 0
    for i in range (length):    # find the best 1vX split
        curr = abs(half - totals[i]) * 2
        if (curr < best_diff):
            best_diff = curr
            team1 = [names[i]]
            total1 = totals[i]
    team2 = leftover(names, team1)
    total2 = int((half*2) - total1)
    diff = abs(total1 - total2)
    return [team1, total1, team2, total2, diff]
    
###################################################

def best_split2(names, totals, length, half):
    best_diff = 2*half
    team1 = []
    total1 = 0
    for i in range (length):    # find the best 2vX split
        for j in range (i+1, length):
            curr = abs(half - totals[i] - totals[j]) * 2
            if (curr < best_diff):
                best_diff = curr
                team1 = [names[i], names[j]]
                total1 = totals[i] + totals[j]        
    team2 = leftover(names, team1)
    total2 = int((half*2) - total1)
    diff = abs(total1 - total2)
    return [team1, total1, team2, total2, diff]

###################################################

def best_split3(names, totals, length, half):
    best_diff = 2*half
    team1 = []
    total1 = 0
    for i in range (length):    # find the best 3vX split
        for j in range (i+1, length):
            for k in range (j+1, length):
                curr = abs(half - totals[i] - totals[j] - totals[k]) * 2
                if (curr < best_diff):
                    best_diff = curr
                    team1 = [names[i], names[j], names[k]]
                    total1 = totals[i] + totals[j] + totals[k]               
    team2 = leftover(names, team1)
    total2 = int((half*2) - total1)
    diff = abs(total1 - total2)
    return [team1, total1, team2, total2, diff]

###################################################

def best_split4(names, totals, length, half):
    best_diff = 2*half
    team1 = []
    total1 = 0
    for i in range (length):    # find the best 4vX split
        for j in range (i+1, length):
            for k in range (j+1, length):
                for f in range (k+1, length):
                    curr = abs(half - totals[i] - totals[j] - totals[k] - totals[f]) * 2
                    if (curr < best_diff):
                        best_diff = curr
                        team1 = [names[i], names[j], names[k], names[f]]
                        total1 = totals[i] + totals[j] + totals[k] + totals[f]              
    team2 = leftover(names, team1)
    total2 = int((half*2) - total1)
    diff = abs(total1 - total2)
    return [team1, total1, team2, total2, diff]

############ end main sorting functions ############

############ main function ############

def arrange_teams():
    info = fill_array()
    names = info[0]
    totals = info[1]
    length = len(names)
    half = sum_array(totals) / 2

    ######## CALCULATION ########    returns [team1, total1, team 2, total2, diff]

    # WORKS WITH 2 OR 3 COMPETITORS
    if (length > 1):    
        best_teams = best_split1(names, totals, length, half)
    # WORKS WITH 4 OR 5 COMPETITORS
    if(length > 3):
        maybe_best_teams = best_split2(names, totals, length, half)
        if (maybe_best_teams[4] < best_teams[4]):
            best_teams = maybe_best_teams
    # WORKS WITH 6 OR 7 COMPETITORS
    if(length > 5):
        maybe_best_teams = best_split3(names, totals, length, half)
        if (maybe_best_teams[4] < best_teams[4]):
            best_teams = maybe_best_teams
    # WORKS WITH 8 OR 9 COMPETITORS
    if(7 < length < 10):
        maybe_best_teams = best_split4(names, totals, length, half)
        if (maybe_best_teams[4] < best_teams[4]):
            best_teams = maybe_best_teams

    ######## CALCULATION ########

    ##### PRINT RESULTS #####

    print("--------------- ~~CALCULATING~~ ---------------\n")
    print("Team 1 Total = " + str(best_teams[1]))
    print_array(best_teams[0])
    print("\n------------------------------\n")
    print("Team 2 Total = " + str(best_teams[3]))
    print_array(best_teams[2])
    print("\n------------------------------\n")
    print("Difference Between Team Totals: " + str(best_teams[4]))
    print("\n")

    ##### PRINT RESULTS #####

    return [best_teams]

############ end main function ############
