FROM python:3
# SET PROXY/CERT INFO
ENV HTTP_PROXY="http://gatewayndc.ual.com:80"
ENV HTTPS_PROXY="http://gatewayndc.ual.com:80"

# Downloads Relevant Python Libraries
RUN pip3 install --proxy=http://gatewayndc.ual.com:80 pymsteams
RUN pip3 install --proxy=http://gatewayndc.ual.com:80 pyyaml
RUN pip3 install --proxy=http://gatewayndc.ual.com:80 tabulate

# Installs CFN-GUARD
RUN wget -e use_proxy=yes -e HTTPS_PROXY="http://gatewayndc.ual.com:80" https://github.com/aws-cloudformation/cloudformation-guard/releases/download/1.0.0/cfn-guard-linux-1.0.0.tar.gz
RUN tar -xvf cfn-guard-linux-1.0.0.tar.gz
RUN cp -R cfn-guard-linux/cfn-guard /usr/sbin

# Grabs Execution Scripts
RUN mkdir scripts
COPY docker-scripts/env-var-condition.sh /scripts/env-var-condition.sh
COPY docker-scripts/failed-check-teams.py /scripts/failed-check-teams.py
COPY docker-scripts/passed-check-teams.py /scripts/passed-check-teams.py
COPY docker-scripts/python-checkforcfn.py /scripts/python-checkforcfn.py
COPY docker-scripts/run-cfn-binary.sh /scripts/run-cfn-binary.sh
RUN chmod -R 777 scripts

# Grab Ruleset
COPY global_policies.ruleset /global_policies.ruleset
COPY metrics.json /metrics.json

# Entrypoint to The Script(s)
ENTRYPOINT ["/scripts/run-cfn-binary.sh"]