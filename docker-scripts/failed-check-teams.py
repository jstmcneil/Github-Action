import pymsteams
import os
import sys
import re
from tabulate import tabulate


# Takes in two possible parameters:
# p1: format type (github, teamcity, default) --> (mandatory)
# p2: webhook URL --> (optional)
# Call is like: python3 failed-check-teams.py p1 p2

# Sets output colors scheme for command line output.
def colorSchemeIntialize():
  if len(sys.argv) < 2:
    print("\n\033[31m" + "ERROR: " + "\033[0m" + "please provide a scheme color as your first parameter.")
    print("Options include: '{0}dark{1}', '{0}light{1}', or '{0}default{1}'.\n".format("\033[33m", "\033[0m"))
    exit(1)
  elif sys.argv[1] not in ['dark', 'light', 'default']:
    print("\n\033[31m" + "ERROR: " + "\033[0m" + "non-selectable color scheme provided as first parameter.")
    print("Options include: '{0}dark{1}', '{0}light{1}', or '{0}default{1}'.".format("\033[33m", "\033[0m"))
    print("Use command: python3 failed-check-teams.py <{0}color-scheme{1}> <{0}optional-webhook{1}>\n".format("\033[33m", "\033[0m"))
    exit(1)
  elif sys.argv[1] == 'dark':
    MAIN_COLOR  = "\033[0m"   #WHITE
    OFF_COLOR   = "\033[37m"  #GRAY
  elif sys.argv[1] == 'light':
    MAIN_COLOR  = "\033[30m"  #BLACK
    OFF_COLOR   = "\033[36m"  #CYAN
  elif sys.argv[1] == 'default':
    MAIN_COLOR  = "\033[0m"   #WHITE
    OFF_COLOR   = "\033[36m"  #CYAN
  return MAIN_COLOR, OFF_COLOR

# Intializes pymsteams card for a template.
def createCard(filename, count: int, total: int, webhook: str, listOfBad: list, listOfGood: list):
  myTeamsMessage = pymsteams.connectorcard(webhook)
  myMessageSection = pymsteams.cardsection()
  component_name = filename.split(".")
  raw_file_name = component_name[0] + "." + component_name[1]
  myTeamsMessage.text("**[" + str(count) + "/" + str(total) + "] CFN-GUARD REPORT FOR:** _" + raw_file_name + "_")
  if (os.stat('results/' + filename).st_size != 0):
    header = ("{}Errors for {}[".format(MAIN_COLOR, OFF_COLOR) + raw_file_name + "]{} CloudFormation Template:".format(MAIN_COLOR))
    myTeamsMessage.color("#FF6347")
    # Creating Section
    totalIssues = pymsteams.cardsection()
    # Constructing the body of the message
    body = "❌  Your template has failed some baseline policies. The issues are listed below:\n"

    with open('results/' + filename, 'r') as program:
      data = program.readlines()

    with open('results/' + filename, 'w') as program:
      output = ""
      for (number, line) in enumerate(data):
        if (number != (len(data) - 1)):
          program.write('%d.  %s\n' % (number + 1, line))
          myMessageSection.addFact(number + 1, line)
          line = re.sub(r'\[(.*?)\]', r'{}'.format(OFF_COLOR) + '\g<0>' + '{}'.format(MAIN_COLOR), line.rstrip())
          output = output + ('{}{:<3s} {:>7s}\n'.format(MAIN_COLOR, str(number+1)+".", line))
        else:
          program.write('\n%s' % (line.rstrip()))
          footer = ('%s' % (line.rstrip()))
          toAdd = "**" + line.rstrip() + "**"
          totalIssues.activityText(toAdd)
          listOfBad.append((raw_file_name, line.split(":")[1]))
    myMessageSection.activityText(body)
    myTeamsMessage.addSection(myMessageSection)
    myTeamsMessage.addSection(totalIssues)
    print("{}".format(MAIN_COLOR) + tabulate({header: [output, footer]}, headers="keys", tablefmt="fancy_grid"), "\n")

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
  myTeamsMessage.text("**[" + str(total) + "/" + str(total) + "] CFN-GUARD DIGEST & SUMMARY**")
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
    header = ("{}Errors for {}[".format(MAIN_COLOR, OFF_COLOR) + raw_file_name + "]{} CloudFormation Template:".format(MAIN_COLOR))
    with open('results/' + filename, 'r') as program:
      data = program.readlines()

    with open('results/' + filename, 'w') as program:
      output = ""
      for (number, line) in enumerate(data):
        if (number != (len(data) - 1)):
          program.write('%d.  %s\n' % (number + 1, line))
          line = re.sub(r'\[(.*?)\]', r'{}'.format(OFF_COLOR) + '\g<0>' + '{}'.format(MAIN_COLOR), line.rstrip())
          output = output + ('{}{:<3s} {:>7s}\n'.format(MAIN_COLOR, str(number+1)+".", line))
        else:
          program.write('\n%s' % (line))
          footer = ('%s' % (line.rstrip()))
          listOfBad.append((raw_file_name, line.split(":")[1]))
    print("{}".format(MAIN_COLOR) + tabulate({header: [output, footer]}, headers="keys", tablefmt="fancy_grid"), "\n")
  else:
    listOfGood.append((raw_file_name, "0"))

# Utility sort method.
def sort_tuple_list(tup):
  tup.sort(key = lambda x: -int(x[1])) 
  return tup 

# Utility function for coloring.
def sorround_color(string: str):
  return "{}".format(OFF_COLOR) + string + "{}".format(MAIN_COLOR)

## Global Fields
MAIN_COLOR, OFF_COLOR = colorSchemeIntialize()

def main():
  good, bad = [], []
  i, tot = 1, len(os.listdir('results/')) + 1
  for file in os.listdir('results/'):
    if (len(sys.argv) > 2):
      createCard(file, i, tot, sys.argv[2], bad, good)
    else:
      onlyCommandLine(file, i, tot, bad, good)
    i = i + 1
  if (len(sys.argv) > 2):
    generateSummaryCard(sys.argv[2], tot, bad, good)
  bad = sort_tuple_list(bad)
  combined = bad + [("TOTAL", str(sum(int(i[1]) for i in bad)))]
  print("\n\033[31m✖ Failed:\033[0mTemplates failed policy checks.")
  print("{}".format(MAIN_COLOR) + tabulate(combined, headers=[sorround_color('CloudFormation File'), sorround_color('Failures')], tablefmt="fancy_grid"))
  print("FAILED-CODE-PYTHON")

if __name__ == '__main__':
    main()