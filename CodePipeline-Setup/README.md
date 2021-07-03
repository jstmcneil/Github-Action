Table of Contents
=================
<!--ts-->
   * [Table of Contents](#table-of-contents)
   * [AWS Pipeline Setup](#AWS-Pipeline-Setup)
      * [CodePipeline](#CodePipeline)
        1. [Setup/Variables](#1-SetupVariables)
        2. [Permissions](#2-Permissions)
      * [CodeBuild](#CodeBuild)
        1. [ECR Setup](#1-ECR-Setup)
        2. [Setup/Variables](#2-SetupVariables)
        3. [Permissions](#3-Permissions)
   * [AWS Pipeline Usage](#AWS-Pipeline-Usage)
      * [Inputs](#inputs)
      * [Outputs](#outputs)
<!--te-->

# AWS Pipeline Setup
Of all the documentation in this repository, the CodePipeLine will be the most generic. It is difficult to explicitly state exactly what is needed for application team developers since the various AWS accounts configured across UAL are not standardized. In other words, there may be differences in permissions that make it difficult to emulate the exact enviroment that teams will be importing into. 

As such, the setup portion of this document serves primarily to describe what permissions/roles are required in order to make the CodeBuild and CodePipeline steps usable. Additionally, in this repository folder lies the CloudFormation script used on my end to spin up the relevant infrastructure. It includes the specific policies/roles required. While it may not be directly consumable, the script should serve as a guiding reference.
## Parameters
Below shows the input parameters that need to be supplied to both the pipeline and build job. It is templatized at the top of the CloudFormation script.
```yaml
Parameters:
  ProjectName:
    Type: String
    Description: >-
      The name of the project being built.  This name will be used on a number
      of resources.
    Default: CFN-Guard
  BucketName:
      Type: String
      Description: >-
        The S3 bucket at which your repository zip live. This S3 bucket should house
        the below zip file of your repository files.
  S3RepoObjectKey:
      Type: String
      Description: >-
        The exact name of your S3 zipped object that lives in the S3 bucket stated
        above. This zip contains all your repository files.
  WebhookURL:
      Type: String
      Description: >-
        The webhook to which your results will be sent to. Leave this blank (default option) if you do not
        want to send your data to a webhook.
      Default: ""
  ApplicationCI:
    Type: String
    Description: >-
      The 3-character application key (or "CI") belonging to your application.
    Default: ""
  RulesetName:
    Type: String
    Description: >-
      Name of the ruleset that your CloudFormation templates are run against.
    Default: "ruleset_migrated.guard"
  ColorScheme:
    Type: String
    Description: >-
      The color scheme in which the build log failures will be printed in.
    AllowedValues:
      - "dark"
      - "light"
      - "default"
    Default: "default"
```
### Pipeline Parameters:
This parameters deal primarily in naming/sourcing your repository files. For this section, you must package your repository files in a .zip, and then place them inside a bucket. For more information, view [this documentation](https://docs.aws.amazon.com/codepipeline/latest/userguide/tutorials-simple-s3.html).

_Project Name:_ this parameter determines the naming scheme of the spun up resources. This allows for ease of tracking.

_Bucket Name:_ this parameter is the bucket name where your source files live. 

_S3RepoObjectKey:_ this paremeter is the name of the .zip file within the previously defined bucket. It should contain all of your repository data/files.

### Customization Parameters:
_ApplicationCI:_ this input should be your specific 3-letter Application ID. This input is utilized in the output process in order for cleaner build logs. Without this set, the application will fail.

_RulesetName:_ the default value should be "global_policies.ruleset". This input marks the specific ruleset file being used to check your CloudFormation templates against. At this time, there is only one ruleset, which is "ruleset_migrated.guard". As such, this should be the value in all runs at this time.

_ColorScheme:_ this input affects the coloring of the output sent to the build log. The available options are: "default", "light", and "dark". Light should be used in instances of a "light"-colored UI. Dark should be used when the UI is comprised of a darker color scheme. Default is used primarily for testing purposes.

### Optional Parameters:
_WebhookURL:_ this input is a link to a webhook connector on Teams. The Python script will format card-based message(s) containing the errors in your CloudFormation scripts. The resulting messages will to send to your webhook and will show up in your Teams channel. This is optional, and will only be done if this parameter is set. Leave it blank, like shown above, if you do not want to use this functionality. 

## CodePipeline
### 1. Setup
Below is the relevant portion of the CloudFormation script that defines the CodePipeline resource.

```yaml
CFNGuardPipeline:
  Type: 'AWS::CodePipeline::Pipeline'
  Properties:
    RoleArn: !GetAtt CodePipelineServiceRole.Arn
    ArtifactStore:
      Type: S3
      Location: codepipeline-us-east-1-218189232283
    Stages:
      - Name: Source
        Actions:
          - Name: Source
            ActionTypeId:
              Category: Source
              Owner: AWS
              Provider: S3
              Version: '1'
            RunOrder: 1
            Configuration:
              PollForSourceChanges: 'false'
              S3Bucket: !Ref BucketName
              S3ObjectKey: !Ref S3RepoObjectKey
            OutputArtifacts:
              - Name: SourceArtifact
            InputArtifacts: []
            Region: us-east-1
            Namespace: SourceVariables
      - Name: Build
        Actions:
          - Name: CodeBuild
            ActionTypeId:
              Category: Build
              Owner: AWS
              Provider: CodeBuild
              Version: '1'
            RunOrder: 1
            Configuration:
              EnvironmentVariables: !Sub >-
                [{"name":"rulesetfile","value":"${RulesetName}","type":"PLAINTEXT"},{"name":"webhookurl","value":"${WebhookURL}","type":"PLAINTEXT"},{"name":"color_scheme","value":"${ColorScheme}","type":"PLAINTEXT"},{"name":"appCI","value":"${ApplicationCI}","type":"PLAINTEXT"}]
              ProjectName: !Ref ProjectName
            OutputArtifacts:
              - Name: BuildArtifact
            InputArtifacts:
              - Name: SourceArtifact
            Region: us-east-1
```
In short, this snippet spins up a CodePipeline resource which grabs the source zip file defined in parameters. Subsequently, it calls the CodeBuild resource defined in the next section. The build output does not occur in the pipeline job, and will only show up in the CodeBuild log.

Note the following:
1. The RoleArn is set to CodePipelineServiceRole.Arn. This role and the corresponding policy are also created in the CloudFormation template, and will be explained in the following section.
2. The following environment variables are defined to be passed to the CodeBuild job: rulesetfile, webhookurl, color_scheme, and appCI. These were all defined previously in the parameters list.
3. Finally, the CodeBuild job is referenced via the ProjectName parameter. This occurs in the **ProjectName: !Red ProjectName** line.

### 2. Permissions
Please view the [CloudFormation source file](./intial-cfn-test-template.yaml) to see the example role and policy: CodePipelineServiceRole & CodePipelineServicePolicy. This section will quickly highlight the permissions that the policy provides.

####S3
There are three S3 statements in this policy:
1. GetBucketVersioning and PutBucketVersioning are applied to the bucket defined in the parameters section.
2. GetObjectVersion and GetObject are applied directly to the S3RepoObjectKey item. This gives the Pipeline the ability to pull down the .zip file.
3. PutObject, GetObject and GetObjectVersion are provided to the bucket codepipeline-us-east-1-* . This wildcard figure at the end matches any bucket that begins with "codepipeline-us-east-1-". In short, this policy allows the pipeline to publish any necessary artifacts.

####CodeBuild: BatchGetBuildBatches, StartBuildBatch, StartBuild, and BatchGetBuilds are provided to the CodePipeline role. This allows the pipeline resource to start builds and retrieve information about them. This access is granted across all CodeBuild resources, however you can lock yours down depending on your pipeline's scope.

####CloudWatch: unrestricted access to CloudWatch is granted in this instance for logging purposes. It is reccomended you employ least privileges and lock down the permissions to provide access only authorized resources.

## CodeBuild
### 1. ECR Setup
Unfortunately, UAL's AWS enviroment does not have the capabilities to route to the artifactory server. As such, the Docker image used to drive this build job must be uploaded directly to ECR. Instruction to do so are located [here](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html).

There are two options for sourcing the image for transferring to ECR:
1. Grab the live image from artifactory.
2. Clone this repository and build the image manually.

For the first option:
```bash
docker pull artifactory.ual.com/oetdevops/security-images/cfn-guard-pac:2.0
```
For the second option, clone this repository and navigate to the root. The Dockerfile downloads the cfn-guard executable and installs the pymsteams and pyyaml python packages for Teams integration. To build this image, navigate to the directory it is placed, and do the following:

```bash
docker build . -t <your-name-for-image>
```
### 2. Setup
Below is the relevant portion of the CloudFormation script that defines the CodeBuild resource.
```yaml
CodeBuildStep:
  Type: 'AWS::CodeBuild::Project'
  Properties:
    Name: !Ref ProjectName
    Source:
      Type: CODEPIPELINE
      BuildSpec: |-
        version: 0.2

        env:
          variables:
            rulesetfile: ""
            webhookurl: ""
            color_scheme: ""
            appCI: ""
        phases:
          build:
            commands:
               - /scripts/run-cfn-binary.sh $rulesetfile $appCI $color_scheme $webhookurl
    Artifacts:
      Type: CODEPIPELINE
    Environment:
      Type: LINUX_CONTAINER
      Image: '437042700033.dkr.ecr.us-east-1.amazonaws.com/cfn-guard-docker:latest'
      ComputeType: BUILD_GENERAL1_SMALL
      EnvironmentVariables: []
      PrivilegedMode: false
      ImagePullCredentialsType: SERVICE_ROLE
    ServiceRole: !GetAtt CodeBuildServiceRole.Arn
    TimeoutInMinutes: 10
    QueuedTimeoutInMinutes: 480
```
This CodeBuild job starts an EC2 instance and attaches our ECR container to it. Then, depending on your input, it'll scan the provided repository (.zip) and post the output. For more information on the output, see the [output](#output) section.

Note the following details:
1. The buildspec file is built into the CloudFormation snippet. This is the portion of code that runs once our jobs starts. In this case, it calls the entrypoint to our container with the relevant parameters attached. While the enviroment variable are intially empty, they won't be once the CodePipeline resource passes its enviroment variables into the build task.
2. The **Image: '437042700033.dkr.ecr.us-east-1.amazonaws.com/cfn-guard-docker:latest'** line shows that we are starting the EC2 instance with our docker image.
3. Finally, note that the ServiceRole is set to CodeBuildServiceRole.Arn. This role and the policy attached will be discussed in the next section.

### 3. Permissions

# AWS Pipeline Usage
## Inputs
## Outputs
