# Repository Usage
This repository contains several useful elements for PaC:
1. The action.yml file allows for the Dockerfile present here to be consumed via GitHub actions in seperate repositories.
2. An exported TeamCity project, which contains the build steps required for consumption.
3. A seperate GitHub action that will auto-deploy the Docker image to Dockerhub if any pushes are made to the repository. This means that if any scripts, rulesets, or other files are changed, the docker image will be recreated and automatically usable across all pipelines. 
