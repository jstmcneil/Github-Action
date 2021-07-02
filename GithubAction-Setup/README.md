Table of Contents
=================
<!--ts-->
   * [Table of Contents](#table-of-contents)
   * [GitHub Actions Import](#TeamCity-Setup)
      * [Duplicate Repository](#TeamCity-Setup)
      * [Retrofit Existing Repository](#TeamCity-Setup)
   * [Using GitHub Action]()
      * [Inputs]()
      * [Outputs]()
      * [Run Types]() 
<!--te-->

# Github Actions Setup
The GitHub actions setup should be relatively easy for United Application developers. Like TeamCity, there are two primary options for setup.
1. Duplicate an already set-up repository which includes the GitHub action files.
2. Retrofit an existing repository to include the GitHub action files.

The second option is also ideal for projects that already have GitHub actions configured.

## Duplicate Repository
Start by navigating to this [directory](https://github.ual.com/V838688/Policy-as-Code-GitHub-Action).
1. Click the "Use this template" button at the top of the page.
2. Name your new repository, and provide a description as you would normally.

That's it! Everything should be set-up for usage now.

## Retrofit Existing Repository
There is a slight difference between projects that already have GitHub actions configured, and those that do not.
#### No Existing Actions:
1. Click the _"Actions"_ tab on your repository's splash screen.
2. Following this, click the _"Set up this workflow"_ button.
3. Copy and paste the contents of [policy-as-code.yml]() (located in this folder) over the pre-generated contents.
4. Rename the file to policy-as-code.yml.

#### Existing Actions:
Simply copy the [policy-as-code.yml]() contents into your existing workflows, or place the file directly into your repository's /.github/workflows/ directory. If you are an advanced user, please feel free to look at the [actions.yml]() file that hosts the actual GitHub Dockerized Action content.

# Using GitHub Actions
There are few parameters that need to be changed in order to ensure the application is run correctly for your repository. Additionally, there are considerations for when the policy scan should be run, as well as how to read/extract output.
## Inputs
In order to actually change parameters/inputs, you must navigate to the _policy-as-code.yml_ file that you setup in the previous section(s). Open the file and note the tail-end of the script.

![GitHub Action Edit](/res/github-action-inputs.png)

### Required:
_app_CI_key:_ this input should be your specific 3-letter Application ID. This input is utilized in the output process in order for cleaner build logs. Without this set, the application will fail.

_rule-file-name:_ The default value should be "global_policies.ruleset". This input marks the specific ruleset file being used to check your CloudFormation templates against. At this time, there is only one ruleset, which is "global_policies.ruleset". As such, this should be the value in all runs at this time.

_color_style:_ The default should be "dark". This input affects the coloring of the output sent to the build log. The available options are: "default", "light", and "dark". Light should be used in instances of a "light"-colored UI. Dark should be used when the UI is comprised of a darker color scheme. Default is used primarily for testing purposes.

### Optional:
_ms-teams-webhook:_ This input is a link to a webhook connector on Teams. The Python script will format card-based message(s) containing the errors in your CloudFormation scripts. The resulting messages will to send to your webhook and will show up in your Teams channel. This is optional, and will only be done if this parameter is set. Leave it blank, like shown above, if you do not want to use this functionality. 

## Outputs
Defaulty, output will always be sent to the build log. If the user configured the webhook parameter, then output will be sent there also.
#### Build Log
Every file in the output will have a corresponding table containing its policy failures. Policies with no failures will not be included.

![Failure-Ex](/res/failure-example.png)

At the top, the path of the CloudFormation script relative to the VCS Root repository is shown. Each line in the table is a single policy failure. The specific rule is mentioned there, which can be used to trace back the required properties. 

Additionally, a summary table containing a count of all the failures for each file is included.

![Failure-Summary](/res/summary-table.png)

This can be used to prioritize remediation efforts for each CloudFormation script.

#### Teams Webhook
The Teams output is very similar to that of the build log. A card is generated for every CloudFormation file that the CFN-Guard build-step scanned. Then, like the build log, the output provides the specific policy infringements for that failed check.

![Webhook-Ex](/res/webhook_ex.png)

Finally, a summary table is printed that shows which files failed and which ones passed. It will also provide details on the number of policy failures for each file. This can be utilized as some form of objective remediation prioritization.

![Webhook-Summary](/res/webhook_summary.png)

These resources should provide an iterative feedback loop which allows developers to quickly make the required security changes.
