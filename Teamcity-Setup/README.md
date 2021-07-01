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


