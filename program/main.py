import getdata
import analyzedata
import botometer
import tweepy

full = True
while full:
    print(
        "\nWould you like to...\n A.) Gather more data\n B.) Analyze a topic\n C.) exit"
    )
    answer = input()
    if answer == "A" or answer == "a":
        # take an input of the desired search
        print("Enter requested topic search: ")
        query = input()
        print("Enter requested sample size: ")
        size = int(input())
        print(
            "Enter requested subheader for data (press enter if no subheader desired): "
        )
        sub = input()
        getdata.getdata(query, size, sub)
        full = False
    elif answer == "B" or answer == "b":
        print("Enter data folder name: ")
        query = input()
        analyzedata.analyzedata(query)
        full = False
    elif answer == "C" or answer == "c":
        full = False
    else:
        print("\nInvalid response!")