# Repository Usage
This serves as the Policy-as-Code repository. All code developed in Refactr, TeamCity and Github Actions for UAL exists within this repository for ease-of-access and future usability. All script elements have been dockerized within the provided Dockerfile in this repository. This allows for management to minimize matineince, and gives the ability to update in one place and affect several pipelines. When the project is run, it will use CloudFormation Guard to scan a given github repository with a given ruleset. Results from that run will then be sent to a provided Microsoft Teams webhook.

This repository contains several useful elements for PaC:
1. The action.yml file allows for the Dockerfile present here to be consumed via GitHub actions in seperate repositories.
2. An exported TeamCity project, which contains the build steps required for consumption.
3. A seperate GitHub action that will auto-deploy the Docker image to Dockerhub if any pushes are made to the repository. This means that if any scripts, rulesets, or other files are changed, the docker image will be recreated and automatically usable across all pipelines. 

## TeamCity Usage
