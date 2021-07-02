Table of Contents
=================
<!--ts-->
   * [Table of Contents](#table-of-contents)
   * [AWS Pipeline Setup](#AWS-Pipeline-Setup)
      * [CodePipeline](#CodePipeline)
        1. [Setup/Variables](#Setup/Variables)
        2. [Permissions](#Permissions)
      * [CodeBuild](#CodeBuild)
        1. [ECR Setup](#ECR-Setup)
        2. [Setup/Variables](#Setup/Variables)
        3. [Permissions](#Permissions)
   * [AWS Pipeline Usage](#AWS-Pipeline-Usage)
      * [Inputs](#inputs)
      * [Outputs](#outputs)
<!--te-->

# AWS Pipeline Setup
Of all the documentation in this repository, the CodePipeLine will be the most generic. It is difficult to explicitly state exactly what is needed for application team developers since the various AWS accounts configured across UAL are not standardized. In other words, there may be differences in permissions that make it difficult to emulate the exact enviroment that teams will be importing into. 

As such, the setup portion of this document serves primarily to describe what permissions/roles are required in order to make the CodeBuild and CodePipeline steps usable. Additionally, in this repository folder lies the CloudFormation script used on my end to spin up the relevant infrastructure. It includes the specific policies/roles required. While it may not be directly consumable, the script should serve as a guiding reference.

## CodePipeline
### 1. Setup/Variables
### 2. Permissions

## CodeBuild
### 1. ECR Setup
### 2. Setup/Variables
### 3. Permissions

# AWS Pipeline Usage
## Inputs
## Outputs
