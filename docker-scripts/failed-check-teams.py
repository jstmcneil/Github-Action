import pymsteams
import os
import sys
import re
from tabulate import tabulate

# Intializes pymsteams card for a template.
def createCard(filename, count: int, total: int, webhook: str, listOfBad: list, listOfGood: list):
  myTeamsMessage = pymsteams.connectorcard(webhook)
  myMessageSection = pymsteams.cardsection()
  component_name = filename.split(".")
  raw_file_name = component_name[0] + "." + component_name[1]
  myTeamsMessage.text("**[" + str(count) + "/" + str(total) + "] CFN-GUARD REPORT FOR:** _" + raw_file_name + "_")
  if (os.stat('results/' + filename).st_size != 0):
    print("\n\033[0mErrors for \033[37m[" + raw_file_name + "]\033[0m CloudFormation Template:")
    print("\033[37m---------------------\033[0m")
    myTeamsMessage.color("#FF6347")
    # Creating Section
    totalIssues = pymsteams.cardsection()
    # Constructing the body of the message
    body = "❌  Your template has failed some baseline policies. The issues are listed below:\n"

    with open('results/' + filename, 'r') as program:
      data = program.readlines()

    with open('results/' + filename, 'w') as program:
      for (number, line) in enumerate(data):
        if (number != (len(data) - 1)):
          program.write('%d.  %s\n' % (number + 1, line))
          myMessageSection.addFact(number + 1, line)
          line = re.sub(r'\[(.*?)\]', r'\033[37m\g<0>\033[0m', line.rstrip())
          print('\033[0m%d.  %s' % (number + 1, line))
        else:
          program.write('\n%s' % (line))
          print('%s' % (line))
          toAdd = "**" + line.rstrip() + "**"
          totalIssues.activityText(toAdd)
          listOfBad.append((raw_file_name, line.split(":")[1]))
    myMessageSection.activityText(body)
    myTeamsMessage.addSection(myMessageSection)
    myTeamsMessage.addSection(totalIssues)
    print("\033[37m---------------------\033[0m")

  else:
    myTeamsMessage.color("#00FF00")
    body = "✔ Your code templates have passed all configuration checks!"
    myMessageSection.activityText(body)
    myTeamsMessage.addSection(myMessageSection)
    listOfGood.append((raw_file_name, "0"))
  myTeamsMessage.send()

# Generates a Teams card summary that lists which
# CloudFormation files passed/failed their checks.
def generateSummaryCard(webhook: str, total: str, listOfBad: list, listOfGood: list):
  myTeamsMessage = pymsteams.connectorcard(webhook)
  myTeamsMessage.color("#0000FF")
  myTeamsMessage.text("**[" + str(i) + "/" + str(total) + "] CFN-GUARD DIGEST & SUMMARY**")
  if listOfBad:
    badSection = pymsteams.cardsection()
    badSection.activityText("❌ The following templates have failed baseline checks:")
    j = 1
    for (name, issues) in listOfBad:
      toAdd =  "_" + name + "_ failed _" + str(issues) + "_ policy checks."
      badSection.addFact(j, toAdd)
      j = j + 1
    myTeamsMessage.addSection(badSection)
  if listOfGood:
    goodSection = pymsteams.cardsection()
    goodSection.activityText("✔ The following code templates have passed all configuration checks!")
    j = 1
    for (name, issues) in listOfGood:
      toAdd = "_" + name + "_ passed all policy checks."
      goodSection.addFact(j, toAdd)
      j = j + 1
    myTeamsMessage.addSection(goodSection)
  myTeamsMessage.send()

# Outputs results to stdout.
def onlyCommandLine(filename, count: int, total: int, listOfBad: list, listOfGood: list):
  component_name = filename.split(".")
  raw_file_name = component_name[0] + "." + component_name[1]
  if (os.stat('results/' + filename).st_size != 0):
    print("\n\033[0mErrors for \033[37m[" + raw_file_name + "]\033[0m CloudFormation Template:")
    print("\033[37m---------------------\033[0m")

    with open('results/' + filename, 'r') as program:
      data = program.readlines()

    with open('results/' + filename, 'w') as program:
      for (number, line) in enumerate(data):
        if (number != (len(data) - 1)):
          program.write('%d.  %s\n' % (number + 1, line))
          line = re.sub(r'\[(.*?)\]', r'\033[37m\g<0>\033[0m', line.rstrip())
          print('\033[0m{:<3s} {:>7s}'.format(str(number+1)+".", line))
        else:
          program.write('\n%s' % (line))
          print('%s' % (line))
          listOfBad.append((raw_file_name, line.split(":")[1]))
    print("\033[37m---------------------\033[0m")
  else:
    listOfGood.append((raw_file_name, "0"))


# Driver Program
i, tot = 1, len(os.listdir('results/')) + 1
good, bad = [], []
for file in os.listdir('results/'):
  if (len(sys.argv) > 1):
    createCard(file, i, tot, sys.argv[1], bad, good)
  else:
    onlyCommandLine(file, i, tot, bad, good)
  i = i + 1
if (len(sys.argv) > 1):
  generateSummaryCard(sys.argv[1], tot, bad, good)
combined = bad + good
print("\n\u001b[31m✖ Failed:\u001b[0m Some of your code templates failed policy checks.")
print(tabulate(combined, headers=['CloudFormation File', 'Failures'], tablefmt="grid"))
print("FAILED-CODE-PYTHON")
