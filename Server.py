"""# *************************************************************
#                           2018
# *************************************************************
#
#                           SERVER
#
# *************************************************************"""


# Import function from socket module
# from socket import *
import socket
from threading import Thread


fileNameUsers = "users.txt"
fileOrganisations = "organisations.txt"
listUsers = []
listOrganisations = []
menu = ("\n\n*****************************" + \
        "\n             MENU: " + \
        "\n*****************************" + \
        "\n1. Get domain name and IP" + \
        "\n2. Get statistics" + \
        "\n3. Sort data" + \
        "\n4. Add organisation" + \
        "\n5. Remove organisation" + \
        "\n6. Quit" + \
        "\n\n*****************************" + \
        "\n\nEnter an option: ")


# FUNCTION: Receive from the socket and return decode the message
def commRX(socket):
    print("TCP/IP:\t\t...Waiting for a response")
    message = socket.recv(bufsize)
    print("TCP/IP:\t\t...Dencoding de message")
    coded = message.decode(code)
    print("CLIENT:\t\t\tResponded.............", coded)
    return coded


# FUNCTION: Transmision of any message
def commTX(message, socket):
    print("TCP/IP:\t\t...Sending message")
    coded = message.encode(code)
    print("TCP/IP:\t\t...Encoding message")
    socket.send(coded)


# FUNCTION: Send a message and wait the response from the client
def sendWait(message, socket):
    commTX(message, socket)
    msg = commRX(socket)
    return msg


# FUNCTION: Open file TXT
def openFile(fileTxt):
    print("SERVER:\t\tOpening file= ", fileTxt)
    try:
        listOfList = []
        file = open(fileTxt, 'r')
        for line in file:
            list1 = line.rstrip("\n")
            list1 = list1.split()
            listOfList.append(list1)
        print("LIST  :\t\tOpening file= ", listOfList)
        file.close()
    except IOError:
        print("ERROR:\t\t\t\tError opening the file")
    else:
        return listOfList


# FUNCTION: Write file TXT
def writeFile(fileTxt, newLine):
    print("SERVER:\t\tWriting file= ", fileTxt)
    try:
        file = open(fileTxt, 'a')
        file.write(newLine + "\n")
        file.close()
    except IOError:
        print("ERROR:\t\t\t\tError opening the file...")


# FUNCTION: Create a new file
def writeFileAll(fileTxt, listOfList):
    print("SERVER:\t\tWriting file= ", fileTxt)
    try:
        file = open(fileTxt, 'w')
        for sublist in listOfList:
            # print(sublist)
            nLt = ' '.join(sublist)
            file.write(nLt + "\n")
        file.close()
    except IOError:
        print("ERROR:\t\t\t\tError opening the file...")


# FUNCTION: only one client should be able to use any given
# username and password pair
def onlyOneClientPerName(listOfList):
    for sublist in listOfList:
        sublist.append("0")
    # print(listOfList)
    return listOfList


def chkValidUser(user, passW, onlyOne, client):
    print("SERVER:\t\tChecking valid user")
    allow = False
    global listUsers
    for sublist in listUsers:
        if sublist[0] == user and sublist[1] == passW and sublist[2] != onlyOne:
            allow = True
            sublist[2] = onlyOne
        elif sublist[0] == user and sublist[1] == passW and sublist[2] == onlyOne:
            #sendWait(("User is already taken \n" + "Press [ENTER] to continue"), client)
            print("SERVER:\t\tUser is already taken")
    return allow


def findOrg(listOfList, nameOrganisation):
    print("SERVER:\t\tFinding organisation........", nameOrganisation)
    count = 0
    nameOrg = []
    for sublist in listOfList:
        if sublist[0] == nameOrganisation:
            nameOrg = sublist[0], sublist[1], sublist[2], sublist[3]
            count += 1
    if count == 0:
        nameOrg = "Unknow Organisation", "Unknow Organisation", "Unknow Organisation", "Unknow Organisation"
    return nameOrg


def getStatistics(listOfList):
    print("SERVER:\t\tGetting statistics")
    newList = []
    average = 0.0
    for sublist in listOfList:
        average = average + int(sublist[3])
        listOfList[listOfList.index(sublist)][3] = int(sublist[3])
    average = average / len(listOfList)
    listOfList.sort(key=takeSort)
    newList = (listOfList[0], listOfList[len(listOfList)-1], average)
    return newList


def sortData(listOfList, response):
    print("SERVER:\t\tSorting data")
    newList = [] + listOfList
    listToStr = ""
    for sublist in newList:
        newList[newList.index(sublist)][3] = int(sublist[3])
    if (response == "N" or response =="n" or response == "Name" or response == "name" or response == "NAME"):
        newList.sort(key=takeSort1)
        sortBy = "NAME"
        for sublist in newList:
            newList[newList.index(sublist)][3] = str(sublist[3])
            listToStr = listToStr + str(sublist) + "\n"
    elif (response == "M" or response =="m" or response == "Minutes" or response == "minutes" or response == "MINUTES"):
        newList.sort(reverse=True, key=takeSort)
        sortBy = "MINUTES"
        for sublist in newList:
            newList[newList.index(sublist)][3] = str(sublist[3])
            listToStr = listToStr + str(sublist) + "\n"
    else:
        newList = "Value out of range! you can only sort by NAME(N) or MINUTES(M)"
        sortBy = ""
    return listToStr, sortBy


def takeSort(elem):
    return elem[3]


def takeSort1(elem):
    return elem[0]


# Multi-threaded server
# When a clien connects, it creates a clien handler thread object
# and allocated client to it.
class ClientHandler(Thread):
    # __init__(self [,args]) Initializes the thread's name
    # __client -> it's a private datafield
    def __init__(self, client): 
        Thread.__init__(self)
        self.__client = client

    # run(self [,args])
    def run(self):
        try:
            attempts = 0
            global listOrganisations
            while True:
                print("SERVER:\t\tTransmiting WELCOME message")
                user = sendWait(("\nWelcome to the server!" + \
                                 "\nYou must have a valid user and password" + \
                                 "\n\nAttempts: "+ str(attempts+1) + " of 3" + \
                                 "\n\nUser: "), self.__client)
                passW = sendWait("\nPassword: ", self.__client)
                print("SERVER:\t\tUSER...", user, "   PASSWORD...", passW)
                allow = chkValidUser(user, passW, '1', self.__client)
                if allow == True:
                    attempts = 0
                    timesx3 = 0
                    times2x3 = 0
                    nameOrg = []
                    print("SERVER:\t\tCorrect user and password........." + user)
                    while True:
                        print("SERVER:\t\tTransmiting MENU")
                        # print(timesx3, times2x3)
                        if(timesx3 != 3 and times2x3 != 3):
                            # print(timesx3, times2x3)
                            option = sendWait(("\nWELCOME " + user + menu), self.__client)
                        if(option == "6" or timesx3 == 3 or times2x3 == 3):
                            # print(option, " " ,timesx3, " " ,times2x3)
                            print("SERVER:\t\tDisconnecting client.............." + user)
                            allow = chkValidUser(user, passW, '0', self.__client)
                            commTX("6", self.__client) # Send 6 to disconnect the client
                            break
                        elif(option == "1"):
                            print("SERVER:\t\tOPTION 1 SELECTED. Get statistics")
                            response = sendWait("\nOption 1. Get domain name and IP\n\nType the organisation name : ", self.__client)
                            nameOrg = findOrg(listOrganisations, response)
                            flag = sendWait(("\n\nSearching Organisation: " + response + \
                                    "\n\n\n\tOrganisation Name................." + nameOrg[0] + \
                                    "\n\tServer Domain Name................" + nameOrg[1] + \
                                    "\n\tIP Address........................" + nameOrg[2] +\
                                    "\n\n\nPress [ENTER] to continue"), self.__client)
                        elif(option == "2"):
                            print("SERVER:\t\tOPTION 2 SELECTED. Get domain name and IP")
                            print("SERVER:\t\tOption 2. Calculating the mean, minimum and maximum number of minutes")
                            newList = getStatistics(listOrganisations)
                            flag = sendWait(("\nStatistics according of number of minutes of service" + \
                                             "\n\n[MAXIMUM]\n\tOrganisation: " + newList[1][0] + \
                                             " --> Total minutes connected: " + str(newList[1][3]) + \
                                             "\n\n[MINIMUM]\n\tOrganisation: " + newList[0][0] + \
                                             " --> Total minutes connected: " + str(newList[0][3]) + \
                                             "\n\n[AVERAGE]\n\tAll Organisations average minutes connected: " + str(newList[2]) + \
                                             "\n\n\nPress [ENTER] to continue"), self.__client)
                        elif(option == "3"):
                            print("SERVER:\t\tOPTION 3 SELECTED. Sort data")
                            response = sendWait("\nOption 3. Sort data\n\nIf you want to sort the data by NAME(N) or MINUTES(M)? : ", self.__client)
                            newList,sortBy = sortData(listOrganisations, response)
                            flag = sendWait(("\n\n\tSort by " + sortBy + "\n\n" + newList + "\n\n\nPress [ENTER] to continue"), self.__client)
                        elif(option == "4"):
                            print("SERVER:\t\tOPTION 4 SELECTED. Add organisation")
                            newOrg = sendWait("\nOption 4. Add organisation\n\nType the new organisation name : ", self.__client)
                            newDomain = sendWait("\nNew organisation Domain Name : ", self.__client)
                            newIP = sendWait("\nNew organisation IP : ", self.__client)
                            newTime = sendWait("\nNew organisation time of conection (Minutes) : ", self.__client)
                            nameOrg = findOrg(listOrganisations, newOrg)
                            if (nameOrg[0] == "Unknow Organisation"):
                                timesx3 = 0
                                newOrganisation = newOrg + " " + newDomain + " " + newIP + " " + newTime
                                writeFile(fileOrganisations, newOrganisation)
                                listOrganisations = openFile(fileOrganisations)
                                #print(listOrganisations)
                                print("SERVER:\t\tOrganisation added.......", newOrganisation)
                                flag = sendWait(("\n\n\tOrganisation added successfully: " + newOrganisation + \
                                             "\n\n\nPress [ENTER] to continue"), self.__client)
                            else:
                                timesx3 += 1
                                print("SERVER:\t\tThe Organisation is already in the file" + "Attempts: " + str(timesx3))
                                flag = sendWait(("\n\nThe Organisation is already in the file." + "\nAttempts: " + str(timesx3) + " of 3" + "\n\n\nPress [ENTER] to continue"), self.__client)
                        elif(option == "5"):
                            print("SERVER:\t\tOPTION 5 SELECTED. Remove organisation")
                            newOrg = sendWait("\nOption 5. Remove organisation\n\nType the organisation name to be deleted: ", self.__client)
                            nameOrg = findOrg(listOrganisations, newOrg)
                            if (nameOrg[0] != "Unknow Organisation"):
                                #print(nameOrg)
                                times2x3 = 0
                                #print(listOrganisations)
                                listOrganisations.remove(list(nameOrg))
                                writeFileAll(fileOrganisations, listOrganisations)
                                listOrganisations = openFile(fileOrganisations)
                                print("SERVER:\t\tOrganisation removed.......", str(nameOrg))
                                flag = sendWait(("\n\n\tOrganisation deleted successfully: " + str(nameOrg) + \
                                             "\n\n\nPress [ENTER] to continue"), self.__client)
                            else:
                                times2x3 += 1
                                print("SERVER:\t\tThe Organisation is already in the file" + "Attempts: " + str(times2x3))
                                flag = sendWait(("\n\nThe Organisation is NOT in the file." + "\nAttempts: " + str(times2x3) + " of 3" + "\n\n\nPress [ENTER] to continue"), self.__client)
                        else:
                            print("SERVER:\t\tThe user input is out of range")
                            flag = sendWait(("\n\n\tYour input is out if range. \n\tPlease enter a number between 1 to 6, according to the menu. \n\t Press [ENTER] to continue"), self.__client)
                    break
                else:    
                    if(attempts == 2):
                        print("SERVER:\t\tDisconnecting client because it reach maximum wrong attempts")
                        flag = sendWait(("\n\n\tDisconnecting client because it reach maximum wrong attempts. \n\tPress [ENTER] to continue"), self.__client)
                        commTX("6", self.__client)  # 6 is exit in the menu
                        break
                    else:
                        attempts += 1
                        print("SERVER:\t\tWrong user or password. Attempts...", attempts)
                        flag = sendWait(("\n\n\tThis is not a valid user and password. \n\tPress [ENTER] to continue"), self.__client)
        except OSError:
            print("ERROR:\t\t\t\tOS Error")
            sys.exit(1)
        else:
            self.__client.close()

            







code = "utf-8"
listUsers = openFile(fileNameUsers)
listUsers = onlyOneClientPerName(listUsers)                                   #Add 1 user per name restriction
listOrganisations = openFile(fileOrganisations)
host = socket.gethostname()
#host = '192.168.255.255' #Error
port = 6666
address = (host,port)
bufsize = 1024
try:    
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(address)
    server.listen(5)
except OSError:
    print("SERVER:\t\tError open socket. The program will be closed.")
    server.close()
    sys.exit(1)
else:
    while True:
        print("SERVER:\t\tServer is up and waiting for connection.")
        client, address = server.accept()
        print("SERVER:\t\tConnected from......", address)
        handler = ClientHandler(client)
        handler.start()
