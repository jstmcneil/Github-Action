# Repository Usage
This serves as the Policy-as-Code repository. All code developed in Refactr, TeamCity and Github Actions for UAL exists within this repository for ease-of-access and future usability. All script elements have been dockerized within the provided Dockerfile in this repository. This allows for management to minimize matineince, and gives the ability to update in one place and affect several pipelines. When the project is run, it will use CloudFormation Guard to scan a given github repository with a given ruleset. Results from that run will then be sent to a provided Microsoft Teams webhook.

This repository contains several useful elements for PaC:
1. The action.yml file allows for the Dockerfile present here to be consumed via GitHub actions in seperate repositories.
2. An exported TeamCity project, which contains the build steps required for consumption.
3. A seperate GitHub action that will auto-deploy the Docker image to Dockerhub if any pushes are made to the repository. This means that if any scripts, rulesets, or other files are changed, the docker image will be recreated and automatically usable across all pipelines. 

## TeamCity Usage
#### Overview
The following serves as a high-level flowchart of the component source files as organized in TeamCity. It should be noted that two types of scripting files are utilized in this project - bash and python scripts. All steps here are contained within the Docker image, with the exception of the inputs.

![alt text](https://github.com/jstmcneil/Github-Action/blob/main/res/pac-flow-readme.png)

#### Inputs
# Repository Usage
This serves as the Policy-as-Code repository. All code developed in Refactr, TeamCity and Github Actions for UAL exists within this repository for ease-of-access and future usability. All script elements have been dockerized within the provided Dockerfile in this repository. This allows for management to minimize matineince, and gives the ability to update in one place and affect several pipelines. When the project is run, it will use CloudFormation Guard to scan a given github repository with a given ruleset. Results from that run will then be sent to a provided Microsoft Teams webhook.

This repository contains several useful elements for PaC:
1. The action.yml file allows for the Dockerfile present here to be consumed via GitHub actions in seperate repositories.
2. An exported TeamCity project, which contains the build steps required for consumption.
3. A seperate GitHub action that will auto-deploy the Docker image to Dockerhub if any pushes are made to the repository. This means that if any scripts, rulesets, or other files are changed, the docker image will be recreated and automatically usable across all pipelines. 

## TeamCity Usage
### Overview
The following serves as a high-level flowchart of the component source files as organized in TeamCity. It should be noted that two types of scripting files are utilized in this project - bash and python scripts. All steps here are contained within the Docker image, with the exception of the inputs.

![alt text](https://github.com/jstmcneil/Github-Action/blob/main/res/pac-flow-readme.png)

### Inputs 
**CFM REPO**: a link to the repository where your CloudFormation templates live.

**CFM Credentials**: the credentials (user/pass) for authorization to the above repository.

**Webhook URL**: the link to the Microsoft Teams webhook where your output will be sent.

**Ruleset File**: the link to the Microsoft Teams webhook where your output will be sent.the link to the Microsoft Teams webhook where your output will be sent.

### Import
For direct usage within TeamCity, either clone this repo or download the [Project Import Zip](TeamCity-PaC-Dockerized.zip). Then, as an TeamCity adminstrator/super-user, do the following (relevant documentation for each step is linked):
1. Navigate to the Adminstration page on TeamCity.

![alt text](/res/admin-page-gif.gif)

2. Click on Project Import & select the download .zip as the source.

![alt text](/res/project-import.gif)

3. Fill out import scope.

![alt text](/res/actual-import.gif)
