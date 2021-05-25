FROM python:latest
# Downloads Relevant Python Libraries
RUN pip install pymsteams
RUN pip install pyyaml

# Installs CFN-GUARD
RUN wget https://github.com/aws-cloudformation/cloudformation-guard/releases/download/1.0.0/cfn-guard-linux-1.0.0.tar.gz
RUN tar -xvf cfn-guard-linux-1.0.0.tar.gz
RUN cp -R cfn-guard-linux/cfn-guard /usr/sbin

# Grabs Execution Scripts
RUN mkdir scripts
COPY docker-scripts/env-var-condition.sh /scripts/env-var-condition.sh
COPY docker-scripts/failed-check-teams.py /scripts/failed-check-teams.py
COPY docker-scripts/passed-check-teams.py /scripts/passed-check-teams.py
COPY docker-scripts/python-checkforcfn.py /scripts/python-checkforcfn.py
COPY docker-scripts/run-cfn-binary.sh /scripts/run-cfn-binary.sh
chmod -R 777 scripts

# Grab Ruleset
COPY global_policies.ruleset /global_policies.ruleset

# Entrypoint to The Script(s)
ENTRYPOINT ["/scripts/run-cfn-binary.sh"]
