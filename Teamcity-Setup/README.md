Table of Contents
=================
<!--ts-->
   * [Table of Contents](#table-of-contents)
   * [TeamCity Setup](#TeamCity-Setup)
      * [Import Project](#stdin)
      * [Manually Add Steps](#local-files)
   * [Running The Pipeline](#Running-The-Pipeline)
     * [Inputs](#local)
     * [Output](#public)
<!--te-->

# TeamCity Setup
Setting up the CFN-Guard binary in TeamCity is a relatively simple process. In short, there are two options for importing the process.
1. Import the projct directly.
2. Manually add the steps.

In terms of time required, the first option is shorter, but may not be avaialble to all team members. If the project is already imported by another team, you may be able to reuse it as an asset. Otherwise, you can use the second option to import the build steps manually in order adapt it directly to your existing pipeline structures.

## Import Project

## Manually Add Steps
There are several pages that need to be setup for the given build-step/project: _version-control settings_, _build-steps_, _failure-conditions_, and _parameters_. The below steps show all the required information for each of these settings.
### Version Control Settings
Connect the VCS-Root that houses all of your CloudFormation templates. The scan will check all CloudFormation scripts in this repository for issues. Set up the root as you normally would.

![VCS Root](/res/manual-vcs-root.png)

No other specific details are needed for this step.

### Build-Step
Since the solution/scripts are entirely localized to a docker image, only a single build step is needed. Create a command-line build-step which will be used to call the docker-run command. There are certain parameters referenced in this step, as shown below. It's important to maintain the **order** in which the arguments are passed to the docker command. If you do not want to utilize a Teams webhook (descibed in inputs), then just leave the parameter itself empty.

![Build Step](/res/manual_import_build_step.png)

Make sure you pull the correct image. For easy copy/paste, the image is below:
```
artifactory.ual.com/oetdevops/security-images/cfn-guard-pac:2.0
```
The docker image will handle the remainder of the scripting implementation.

### Parameters
Below is a screenshot of the list of parameters required by the build-step. For a description of how to fill these out, or what they're used for, please seek out the [Inputs]() section. This section merely describes what parameters are needed/what defaults to set.

![Paremeters](/res/manual-parameter.png)

#### Customization Info:
These values are for implementation-specific information.
- app-key-CI: no default.
- color-scheme: default should be light.
- webhook-url: default should be empty.
- ruleset-file: default should be global_policies.ruleset.

#### GitHub Info (optional):
You can input these if you want to be able to quickly switch the VCS-Root. Essentially, you are paramtarizing the username/repo/password values in the VCS-Root section. This is purely for quality of life and has nothing to do with CFN-Guard.
- github-cfm-repo
- github-repo-password
- github-repo-username

### Failure Conditions
There are two failure conditions to add to the build. However, these are optional in the event that you only want your build to _warn_ you instead of failing outright. For both failures, a screenshot and the resulting Kotlin DSL is shown. From these, you should be able to replicate the enviroment.
#### Policy Failures
This failure results from your CloudFormation scripts not passing the policies.
##### Screenshot:

![Failure-Cond-Policy](/res/manual-failure-baseline.png)

##### Kotlin DSL:
``` Kotlin
failOnText {
    id = "BUILD_EXT_1"
    conditionType = BuildFailureOnText.ConditionType.CONTAINS
    pattern = "FAILED-CODE-PYTHON"
    failureMessage = "Policies did not pass baseline requirements."
    reverse = false
    stopBuildOnFailure = true
}
```
Essentially, the docker container will output a "FAILED-CODE-PYTHON" message upon policies failing. This failure rule will trigger a build failure.
#### Ruleset Failures
If you are using alternate rulesets (only one is provided at this time), then the build can be failed in the instance that the ruleset is unable to be found.
##### Screenshot:

![Failure-Cond-Ruleset](/res/manual-failure-ruleset.png)

##### Kotlin DSL:
``` Kotlin
failOnText {
    id = "BUILD_EXT_2"
    conditionType = BuildFailureOnText.ConditionType.CONTAINS
    pattern = "No rule-file found w/ %ruleset-file% name."
    failureMessage = "No rule-file could be found with the supplied name."
    reverse = false
    stopBuildOnFailure = true
}
```
The docker container will post the "No rule-file found w/ %ruleset-file% name" message in the instance the ruleset cannot be found; thus, failing the build.

# Running The Pipeline
