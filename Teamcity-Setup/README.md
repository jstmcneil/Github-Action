Table of contents
=================
<!--ts-->
   * [Table of Contents](#table-of-contents)
   * [TeamCity Setup](#TeamCity-Setup)
      * [Import Project](#stdin)
      * [Manually Add Steps](#local-files)
   * [Running the Steps](#dependency)
     * [Inputs](#local)
     * [Output](#public)
<!--te-->

## TeamCity Setup
Setting up the CFN-Guard binary in TeamCity is a relatively simple process. In short, there are two options for importing the process.
1. Import the projct directly.
2. Manually add the steps.

In terms of time required, the first option is shorter, but may not be avaialble to all team members. If the project is already imported by another team, you may be able to reuse it as an asset. Otherwise, you can use the second option to import the build steps manually in order adapt it directly to your existing pipeline structures.

### Import Project

### Manually Add Steps
There are several pages that need to be setup for the given build-step/project: _version-control settings_, _build-steps_, _failure-conditions_, and _parameters_.
#### Version Control Settings
Connect the VCS-Root that houses all of your CloudFormation templates. The scan will check all CloudFormation scripts in this repository for issues. Set up the root as you normally would.

No other specific details are needed for this step.

#### Build-Step
Since the solution/scripts are entirely localized to a docker image, only a single build step is needed. Create a command-line build-step which will be used to call the docker-run command. There are certain parameters referenced in this step, as shown below. It's important to maintain the **order** in which the arguments are passed to the docker command. If you do not want to utilize a Teams webhook (descibed in inputs), then just leave the parameter itself empty. 
