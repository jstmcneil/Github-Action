Table of Contents
=================
<!--ts-->
   * [Table of Contents](#table-of-contents)
   * [GitHub Actions Setup](#TeamCity-Setup)
      * [Duplicate Repository](#TeamCity-Setup)
      * [Retrofit Existing Repository](#TeamCity-Setup)
   * [GitHub Action Setup]
      * [Inputs]
      * [Outputs]
      * [Run Types] 
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
