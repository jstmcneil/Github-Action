Table of Contents
=================
<!--ts-->
   * [Table of Contents](#table-of-contents)
   * [GitHub Actions Setup](#Github-Actions-Setup)
      * [Duplicate Repository](#Duplicate-Repository)
      * [Retrofit Existing Repository](#Retrofit-Existing-Repository)
   * [Using GitHub Action](#Using-GitHub-Actions)
      * [Inputs](#inputs)
      * [Outputs](#outputs)
      * [Run Types](#run-types) 
<!--te-->

# CodePipeLine Setup
Of all the documentation in this repository, the CodePipeLine will be the most generic. It is difficult to explicitly state exactly what is needed for application team developers since the various AWS accounts configured across UAL are not standardized. In other words, there may be differences in permissions that make it difficult to emulate the exact enviroment that teams will be importing into. As such, the setup portion of this document serves primarily to describe what permissions/roles are required in order to make the CodeBuild and CodePipeline steps usable.

Additionally, a 
