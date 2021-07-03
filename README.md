# Repository Usage
This serves as the Policy-as-Code repository. All code developed in TeamCity, AWS CodePiplines and Github Actions for UAL exists within this repository for ease-of-access and future usability. All script elements have been dockerized within the provided Dockerfile in this repository. This allows for management to minimize matineince, and gives the ability to update in one place and affect several pipelines. When the project is run, it will use CloudFormation Guard to scan a given github repository with a given ruleset. Results from that run will then (optionally) be sent to a provided Microsoft Teams webhook.

This repository contains several useful elements for PaC:
1. Set-up for TeamCity is located [here](/TeamCity-Setup).
2. Set-up for GitHub Actions is located [here](/GithubAction-Setup).
3. Set-up for AWS CodePipelines is located [here](/CodePipeline-Setup).

Additionally, all the source-code can be found under [/docker-scripts] for any extensibility. The Dockerfile in which all the CI/CD build steps run in is located [here](/Dockerfile).

## TeamCity Usage
#### Overview
The following serves as a high-level flowchart of the component source files as organized in TeamCity. It should be noted that two types of scripting files are utilized in this project - bash and python scripts. All steps here are contained within the Docker image, with the exception of the inputs.

![alt text](https://github.com/jstmcneil/Github-Action/blob/main/res/pac-flow-readme.png)

### Inputs 
**CFM REPO**: a link to the repository where your CloudFormation templates live.

**Webhook URL**: the link to the Microsoft Teams webhook where your output will be sent.

**Ruleset File**: the link to the Microsoft Teams webhook where your output will be sent.the link to the Microsoft Teams webhook where your output will be sent.
