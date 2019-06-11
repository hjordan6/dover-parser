from tika import parser
import csv

raw = parser.from_file('directory.pdf')
text = raw['content'].split()

file = open("out.csv", "w")
origFile = open("orig.txt", "w")


def out(to_write):
    try:
        if not to_write == '\n':
            file.write(to_write + ',')
        else:
            file.write(to_write)
    except UnicodeEncodeError:
        file.write("Transcription Error,")


def orig(to_write):
    origFile.write(to_write)


# Go through the text from the PDF to get the important info
revised = []
start = False
# skipNext: To use when skipping the next thing in the list after combining two parts of a
# phone number that got separated after the split
skipNext = False
idx = 0

# This for loop parses the data, finding all the important pieces of information

for word in text:
    if not revised.__contains__(word) \
            and not word.startswith('mailto')\
            and not word.startswith('tel:'):
        if skipNext:
            skipNext = False
            idx += 1
            continue
        elif word[-1] == ')' and len(word) == 5:
            hold = word + text[idx + 1]
            newWord = ''
            for c in hold:
                if c.isdigit():
                    newWord += c
            revised.append(newWord)
            idx += 1
            skipNext = True
            continue

        elif word[-1] == ',':
            if word == 'Reserve,':
                idx += 1
                continue
            revised.append('')
            revised.append(text[idx + 1])
            revised.append(word[:-1])
        elif word.__contains__('@'):
            revised.append(word)
        elif len(word) > 10:
            number = ''
            for c in word:
                if c.isdigit():
                    number += c
            if len(number) == 10:
                revised.append(number)

    idx += 1

# Everything after this point has to do with printing the data

# print(revised)

out("First Name,Last Name,Phone,Email,Other")
out("\n")

idx = 0
while idx < len(revised):
    if revised[idx] == '':
        firstName = revised[idx + 1]
        if firstName == 'Jeff':
            print("asdf")
        lastName = revised[idx + 2]
        phone = []
        email = []
        idx += 3
        while idx < len(revised) and revised[idx] != '':
            if revised[idx].__contains__('@'):
                email.append(revised[idx])
            else:
                phone.append(revised[idx])
            idx += 1

        out(firstName)
        out(lastName)

        if len(phone) > 0:
            out(phone[0])
        else:
            out("N/A")

        if len(email) > 0:
            out(email[0])
        else:
            out("N/A")

        for p in phone:
            if p != phone[0]:
                out('phone: ' + p)
        for e in email:
            if e != email[0]:
                out('email: ' + e)

        out('\n')
    else:
        idx += 1

# Output for testing purposes
outputOriginal = True
outputRevised = False

if outputOriginal:
    for word in text:
        try:
            orig(word + '\n')
        except UnicodeEncodeError:
            continue

if outputRevised:
    for word in revised:
        try:
            out(word + '\n')
        except UnicodeEncodeError:
            continue
