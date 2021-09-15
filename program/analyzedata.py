import pandas as pd
import json
import os
import math
import matplotlib.pyplot as plt


def mean(arg):
    val = sum(arg)
    return val / len(arg)


def meanlist(arg):
    count = 0
    overnum = 0
    astronum = 0
    fakenum = 0
    finnum = 0
    othnum = 0
    selfnum = 0
    spamnum = 0
    data = []

    for item in arg:
        # generate the average score for each bot score
        count = count + 1
        overnum = overnum + float(item[0])
        astronum = astronum + float(item[1])
        fakenum = fakenum + float(item[2])
        finnum = finnum + float(item[3])
        othnum = othnum + float(item[4])
        selfnum = selfnum + float(item[5])
        spamnum = spamnum + float(item[6])
    # calculate the average
    data.append(overnum / count)
    data.append(astronum / count)
    data.append(fakenum / count)
    data.append(finnum / count)
    data.append(othnum / count)
    data.append(selfnum / count)
    data.append(spamnum / count)

    return data


def variance(arg):
    meanvar = mean(arg)
    num = 0
    for item in arg:
        num += (item - meanvar) ** 2
    den = len(arg) - 1
    return num / den


def variancelist(arg):
    means = []
    data = []
    for item in arg:
        meanvar = mean(item)
        means.append(meanvar)
        num = 0
        for i in item:
            num += (i - meanvar) ** 2
        den = len(item) - 1
        data.append(num / den)
    fulldict = {means[i]: data[i] for i in range(len(means))}
    return data


def standard_deviation(arg):
    data = []
    for item in arg:
        data.append(math.sqrt(variance(item)))
    return data


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

    filenames = os.listdir("data/" + query)

    for filename in filenames:
        with open("data/{}/{}".format(query, filename)) as infile:
            data = json.load(infile)

            for item in data:
                # append each score
                overall.append(item["overall"])
                astroturf.append(item["astroturf"])
                fake_follower.append(item["fake_follower"])
                financial.append(item["financial"])
                other.append(item["other"])
                self_declared.append(item["self_declared"])
                spammer.append(item["spammer"])

    info = [overall, astroturf, fake_follower, financial, other, self_declared, spammer]
    stddev = standard_deviation(info)
    var = variancelist(info)
    ave = meanlist(info)

    names = [
        "Overall",
        "Astroturf",
        "Fake Follower",
        "Financial",
        "Other",
        "Self Declared",
        "Spammer",
    ]

    df = pd.DataFrame(
        {
            "Mean": ave,
            "Variance": var,
            "Standard Deviation": stddev,
        },
        index=names,
    )

    fig1, ax1 = plt.subplots()
    ax1.set_title(query)
    ax1.boxplot(info, showfliers=False, labels=names)

    print(df)
    plt.show()