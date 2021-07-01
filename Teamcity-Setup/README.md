Table of contents
=================

<!--ts-->
   * [gh-md-toc](#gh-md-toc)
   * [Table of contents](#table-of-contents)
   * [Installation](#installation)
   * [Usage](#usage)
      * [STDIN](#stdin)
      * [Local files](#local-files)
      * [Remote files](#remote-files)
      * [Multiple files](#multiple-files)
      * [Combo](#combo)
      * [Auto insert and update TOC](#auto-insert-and-update-toc)
      * [GitHub token](#github-token)
      * [TOC generation with Github Actions](#toc-generation-with-github-actions)
   * [Tests](#tests)
   * [Dependency](#dependency)
   * [Docker](#docker)
     * [Local](#local)
     * [Public](#public)
<!--te-->

## TeamCity Setup
Setting up the CFN-Guard binary in TeamCity is a relatively simple process. In short, there are two options for importing the process.
1. Import the projct directly.
2. Manually add the steps.

In terms of time required, the first option is shorter, but may not be avaialble to all team members. If the project is already imported by another team, you may be able to reuse it as an asset. Otherwise, you can use the second option to import the build steps manually in order adapt it directly to your existing pipeline structures.


