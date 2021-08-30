import pandas as pd
import json
import os


def analyzedata(query):
    # keep track of the different scores
    # results can be explained here: https://github.com/IUNetSci/botometer-python
    overall = []
    astroturf = []
    fake_follower = []
    financial = []
    other = []
    self_declared = []
    spammer = []

    # to generate the average score
    count = 0
    overnum = 0
    astronum = 0
    fakenum = 0
    finnum = 0
    othnum = 0
    selfnum = 0
    spamnum = 0

    filenames = os.listdir("data/" + query)

    for filename in filenames: 
        with open("data/{}/{}".format(query, filename)) as infile:
            data = json.load(infile)

            for item in data:
                # append each score
                overall.append(item['overall'])
                astroturf.append(item['astroturf'])
                fake_follower.append(item['fake_follower'])
                financial.append(item['financial'])
                other.append(item['other'])
                self_declared.append(item['self_declared'])
                spammer.append(item['spammer'])

                # generate the average score for each bot score
                count = count + 1
                overnum = overnum + float(item['overall'])
                astronum = astronum + float(item['astroturf'])
                fakenum = fakenum + float(item['fake_follower'])
                finnum = finnum + float(item['financial'])
                othnum = othnum + float(item['other'])
                selfnum = selfnum + float(item['self_declared'])
                spamnum = spamnum + float(item['spammer'])

    # calculate the average
    aveover = overnum / count
    aveastro = astronum / count
    avefake = fakenum / count
    avefin = finnum / count
    aveoth = othnum / count
    aveself = selfnum / count
    avespam = spamnum / count

    info = [overall, astroturf, fake_follower, financial, other, self_declared, spammer]
    print(info)
    df = pd.DataFrame(info)

    print(df)



    print("\nThe average overall bot score is: " + str(round(aveover, 3)))
    print("\nThe average astroturf bot score is: " + str(round(aveastro, 3)))
    print("\nThe average fake follower bot score is: " + str(round(avefake, 3)))
    print("\nThe average financial bot score is: " + str(round(avefin, 3)))
    print("\nThe average other bot score is: " + str(round(aveoth, 3)))
    print("\nThe average self delcared bot score is: " + str(round(aveself, 3)))
    print("\nThe average spammer bot score is: " + str(round(avespam, 3)))  