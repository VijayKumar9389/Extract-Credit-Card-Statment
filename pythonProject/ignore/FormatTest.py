import datetime
import pdfplumber
import csv
import os
import re

def isfloat(value):

    if scanString(value) and len(value) > 5:
        return True

    tmp = value.replace(",", "")

    try:
        float(tmp)
        return True
    except ValueError:
        return False

def verify(word):
    date_format = '%b%d'

    try:
        datetime.datetime.strptime(word, date_format)
        return True
    except ValueError:
        return False


def scanString(string):

    tmp = string[-5:]

    if verify(tmp):
        return True
    else:
        return False

def interpretTDInvoice(line):

    length = len(line)
    descLength = 0
    date = ''
    amount = ''
    desc = ''

    #Grabs the date from the last word in the line
    if verify(line[-1]):
        date = line[-1]
    #If there is a credit the date is contatinated to the amount
    if scanString(line[-1]):
        date = line[-1][-5:]
    #
    else:
        for word in line:
            if scanString(word):
                date = word[-5:]
                line.pop(length - 1)


    for word in line:
        if not word.isdigit() and isfloat(word):
            amount = "$" + word
        if scanString(word) and len(word) > 5:
            amount = "-" + amount[:-5]


    for word in line:
        if not isfloat(word) and not verify(word):
            desc = desc + word + " "

    tmp = [date, desc, amount]

    if amount != '' and desc !='' and date !='':
        record.append(tmp)

def matchFiles(fileName):

    result = []

    fileName.replace(" (1).pdf", "")

    if fileName.__contains__("Credit Card"):
        tmp = fileName.split("-")
        result.append(["WestJet RBC® World Elite Mastercard", tmp[2]])
    if fileName.__contains__("TD_CASH_BACK_VISA_INFINITE_CARD"):
        tmp = fileName.split("_")
        year = tmp[8].split("-")
        result.append(["TD Cash Back Infinite Visa", year[1][:-4]])
    if fileName.__contains__("TD_EVERY_DAY_A_BUSINESS_PLAN"):
        tmp = fileName.split("_")
        year = tmp[10].split(".")
        result.append(["TD Every Day Business", year[0]])
    if fileName.__contains__("TD_FIRST_CLASS_TRAVEL_VISA_INFINITE_CARD"):
        tmp = fileName.split("_")
        year = tmp[9].split("-")
        result.append(["TD First Class Travel Visa Infinite Card", year[1][:4]])

    return result



pdfFile = 'C:\\Users\\vijay\\OneDrive\\Desktop\\Invoice\\'
files = os.listdir("C:\\Users\\vijay\\OneDrive\\Desktop\\Invoice")
record = []
count = files.__len__()

for file in files:

    info = matchFiles(file)

    if info[0][0] == "TD Every Day Business":












