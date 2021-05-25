import pymsteams
import os
import sys

# You must create the connectorcard object with the Microsoft Webhook URL
i = 1
tot = len(os.listdir('results/')) + 1
good = []
bad = []
for filename in os.listdir('results/'):
  myMessageSection = pymsteams.cardsection()
  myTeamsMessage = pymsteams.connectorcard(sys.argv[1])
  myTeamsMessage.text("**[" + str(i) + "/" + str(tot) + "] CFN-GUARD REPORT FOR:** _" + filename.split(".")[0] + ".json_")
  if (os.stat('results/' + filename).st_size != 0):
    myTeamsMessage.color("#FF6347")
    # Creating Section
    totalIssues = pymsteams.cardsection()
    # Constructing the body of the message
    body = "❌ Your template has failed some baseline policies. The issues are listed below:\n"

    with open('results/' + filename, 'r') as program:
      data = program.readlines()

    with open('results/' + filename, 'w') as program:
      for (number, line) in enumerate(data):
        if (number != (len(data) - 1)):
          program.write('%d.  %s\n' % (number + 1, line))
          myMessageSection.addFact(number + 1, line)
        else:
          program.write('\n%s' % (line))
          toAdd = "**" + line.rstrip() + "**"
          totalIssues.activityText(toAdd)
          bad.append((filename, line.rstrip()))
    myMessageSection.activityText(body)
    myTeamsMessage.addSection(myMessageSection)
    myTeamsMessage.addSection(totalIssues)

  else:
    myTeamsMessage.color("#00FF00")
    body = "✔ Your code templates have passed all configuration checks!"
    myMessageSection.activityText(body)
    myTeamsMessage.addSection(myMessageSection)
    good.append(filename)

  # send the message.
  myTeamsMessage.send()
  i = i + 1

myTeamsMessage = pymsteams.connectorcard(sys.argv[1])
myTeamsMessage.color("#0000FF")
myTeamsMessage.text("**[" + str(i) + "/" + str(tot) + "] CFN-GUARD DIGEST & SUMMARY**")
if bad:
  badSection = pymsteams.cardsection()
  badSection.activityText("❌ The following templates have failed baseline checks:")
  j = 1
  for (name, issues) in bad:
    toAdd =  "_" + name + "_ failed _" + str(issues).split(":")[1].strip() + "_ policy checks."
    badSection.addFact(j, toAdd)
    j = j + 1
  myTeamsMessage.addSection(badSection)
if good:
  goodSection = pymsteams.cardsection()
  goodSection.activityText("✔ The following code templates have passed all configuration checks!")
  j = 1
  for name in good:
    toAdd = "_" + name + "_ passed all policy checks."
    goodSection.addFact(j, toAdd)
    j = j + 1
  myTeamsMessage.addSection(goodSection)
myTeamsMessage.send()
# Warn instead of fail here.
#if %warn-instead-of-fail%:
#  print("FAILED-CODE-PYTHON")
