import sqlite3
con = sqlite3.connect("ledger.db")
cur = con.cursor()
repeat = True
name = "user"
def_name = "user"
myphone = int(input("Input your phone number "))
cur.execute("INSERT INTO phonebook (pnumber, name) VALUES (?, ?)",(myphone,name))
con.commit()

def trace_back(numfrom):
    finaltransindex = 0
    def_name_arr = []
    coponding_arr = []
    res40 = cur.execute("SELECT type FROM transact ")
    types = res40.fetchall()
    for i in range(0,len(types)):
        if types[i][0]== def_name:
            def_name_arr.append(i)
            #print(def_name_arr)

    res41 = cur.execute("SELECT recipient FROM transact ")
    therecipients = res41.fetchall()
    for i in range(0, len(def_name_arr)):
        if therecipients[len(def_name_arr)-1-i][0]==numfrom:
            finaltransindex = len(def_name_arr)-1-i
            #print("FINALINDEX", finaltransindex)
    coponding = 0
    res42 = cur.execute("SELECT sender FROM transact ")
    thesenders = res42.fetchall()
    while coponding != myphone:
        coponding = thesenders[finaltransindex][0]
        coponding_arr.append(coponding)
        #print("coponding is", coponding)
        del def_name_arr[finaltransindex]
        for i in range(0, len(def_name_arr)):
            if therecipients[len(def_name_arr)-1-i][0]==coponding:
                finaltransindex = i

    return coponding_arr
    


def find_cores_name(theirphone):
    res6 = cur.execute("SELECT pnumber FROM phonebook ")
    pnumbers = res6.fetchall()
    for i in range (0,len(pnumbers)):
        if pnumbers[i][0]==theirphone:
            pindex = i
        
    res7 = cur.execute("SELECT name FROM phonebook ")
    theirnames = res7.fetchall()
    return theirnames[pindex][0]

while repeat == True:
    tindexes = [] #type indexes (name)
    rindexes = [] #recipient indexes
    findexes = [] #from indexes
    sindexes = [] #sender indexes
    message_indexes = []


    print("here are your messages")
    res4 = cur.execute("SELECT too FROM messages ")
    messagers = res4.fetchall()
    for i in range(0,len(messagers)):
        if messagers[i][0]==myphone:
            message_indexes.append(i)
    res5 = cur.execute("SELECT message FROM messages ")
    messagecontent = res5.fetchall()

    res31 = cur.execute("SELECT fromm FROM messages ")
    whosentit = res31.fetchall()
    for i in range(0,len(message_indexes)):
        numfrom = whosentit[message_indexes[i]][0]
        content = messagecontent[message_indexes[i]][0]
        print(numfrom, content)
        print(trace_back(numfrom))
        

    theirphone = int(input("Who is the recipient "))

    theirname = find_cores_name(theirphone)
                     
    option = int(input("Enter 0 to share your contact and 1 to send a message "))
    if option == 0:
        numbertoshare = int(input("Enter the phone number of the contact you want to share"))
        name = find_cores_name(numbertoshare)
        coins = int(input("How many coins do you want to give them "))
        cur.execute("INSERT INTO transact (sender, recipient, quantity, type) VALUES (?, ?, ?, ?)",(myphone,theirphone, coins, name))
        con.commit()

        
    else:

        #looks for the transactions with the names of the person you want to send to 
        res8 = cur.execute("SELECT type FROM transact ")
        nameid = res8.fetchall()
        for p in range(0, len(nameid)):
            if (nameid[p][0] == theirname):
                tindexes.append(p)
        print(tindexes)

        
        res = cur.execute("SELECT recipient FROM transact ")
        recipients = res.fetchall()
        for n in range(0, len(tindexes)):
            if (recipients[tindexes[n]][0] == myphone):
                rindexes.append(tindexes[n])
        print(rindexes)
                
        #res2 = cur.execute("SELECT sender FROM transact ")
        #senders = res2.fetchall()
        #for i in range (0, len(rindexes)):
            #if (senders[rindexes[i]][0]== theirphone):
                #findexes.append(rindexes[i])
        #print(findexes)

        res3 = cur.execute("SELECT quantity FROM transact ")
        coins = res3.fetchall()
        pluscoins = 0
        mycoins = 0
        for x in rindexes: #change rindexes to findexes if above code is uncommented
            pluscoins += coins[x][0]

        res21 = cur.execute("SELECT sender FROM transact ")
        senders = res21.fetchall()
        for n in range(0, len(tindexes)):
            if (senders[tindexes[n]][0] == myphone):
                sindexes.append(tindexes[n])
        print(sindexes)

        res22 = cur.execute("SELECT quantity FROM transact ")
        coins = res22.fetchall()
        minuscoins = 0
        for x in sindexes: #change rindexes to findexes if above code is uncommented
            minuscoins += coins[x][0]

        mycoins = pluscoins-minuscoins

        print("you have ", mycoins, " coins to send to ", theirphone)

        if (mycoins >= 1):
            message = input("What is your message? ")
            cur.execute("INSERT INTO messages (fromm, too, message) VALUES (?, ?, ?)",(myphone,theirphone, message))
            con.commit()


    exit = input("do you want to exit? ")
    if exit == "yes" or exit == "Yes":
        repeat = False
        
    
cur.close()
con.close()

