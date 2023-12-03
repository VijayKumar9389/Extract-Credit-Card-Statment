import datetime
import pdfplumber
import csv
import os

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

def tt(date):
    date_format = '%b/%d/%Y'

    try:
        datetime.datetime.strptime(date, date_format)
        return True
    except ValueError:
        return False



def scanString(string):

    tmp = string[-5:]

    if verify(tmp):
        return True
    else:
        return False

def matchFiles(fileName):

    result = []

    if fileName.__contains__("Credit Card"):
        tmp = fileName.split("-")
        result.append(["WestJet RBC® World Elite Mastercard", tmp[2]])
    if fileName.__contains__("TD_CASH_BACK_VISA_INFINITE_CARD"):
        tmp = fileName.split("_")
        year = tmp[8].split("-")
        result.append(["`TD Cash Back Infinite Visa`", year[1][:-4]])
    if fileName.__contains__("TD_EVERY_DAY_A_BUSINESS_PLAN"):
        tmp = fileName.split("_")
        plan = tmp[6][-4:]
        year = tmp[10].split(".")
        result.append(["TD Every Day Business", year[0]])
    if fileName.__contains__("TD_FIRST_CLASS_TRAVEL_VISA_INFINITE_CARD"):
        tmp = fileName.split("_")
        year = tmp[9].split("-")
        result.append(["TD First Class Travel Visa Infinite Card", year[1][:4]])
    if fileName.__contains__("US_DOLLAR_CARD"):
        tmp = fileName.split("-")
        year = tmp[1].split(".")
        result.append(["TD US Dollar Card", year[0]])


    return result

def formatDate(date):
    tmp = date[:3] + "/" + date[3:]
    return tmp

def interpretTDInvoice(line, year):

    length = len(line)
    date = ''
    amount = ''
    desc = ''

    #Grabs the date
    if verify(line[-1]):
        date = formatDate(line[-1]) +"/"+ year
    if scanString(line[-1]):
        date = formatDate(line[-1][-5:]) +"/"+ year
    else:
        for word in line:
            if scanString(word):
                date = formatDate(word[-5:])+"/"+ year
                line.pop(length - 1)

    for word in line:
        if not word.isdigit() and isfloat(word):
            amount = "$" + word
        if scanString(word) and len(word) > 5:
            amount = "-" + amount[:-5]

    for word in line:
        if not isfloat(word) and not scanString(word):
            desc = desc + word + " "

    tmp = [date, desc, amount]

    if amount != '' and desc != '' and date != '':
        record.append(tmp)

def stripTDInvoice(line, year):
    if verify(line[0]):
        # print(line)

        if (formatDate(line[0]).upper().__contains__("JAN")):
            print((formatDate(line[0])))
            # year = int(year) - 1
            # year = str(year)

        date = formatDate(line[0]) + "/" + year
        desc = line[2]

        if line[3][-2:].isdigit() and line[3].__contains__("$"):
            amount = line[3]
        else:
            amount = line[4]

        tmp = [date, desc, amount]
        print(tmp)
        record.append(tmp)





pdfFile = 'C:\\Users\\vijay\\OneDrive\\Desktop\\invoi\\'
fileName = ''
files = os.listdir("C:\\Users\\vijay\\OneDrive\\Desktop\\invoi")
record = []
count = files.__len__()

for file in files:

    print(file)

    statementInfo = matchFiles(file)


    fileName = statementInfo[0][0]
    with pdfplumber.open(pdfFile + file) as pdf:

        total_Pages = len(pdf.pages)

        for i in range(0, total_Pages):
            page = pdf.pages[i]
            text = page.extract_text()

            for row in text.split('\n'):
                line = row.split(" ")


                stripTDInvoice(line, statementInfo[0][1])


record = sorted(record, key=lambda t: datetime.datetime.strptime(t[0], '%b/%d/%Y'))

with open('C:\\Users\\vijay\\OneDrive\\Desktop\\Invoice.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Date", "Description", "Cheque/Debit", "Deposit/Credit"])

    for item in record:
        if item[2].__contains__('-'):
            writer.writerow([item[0], item[1], "", item[2][1:]])
        else:
            writer.writerow([item[0], item[1], item[2], ""])

files = os.listdir("C:\\Users\\vijay\\OneDrive\\Desktop\\Invoice")


