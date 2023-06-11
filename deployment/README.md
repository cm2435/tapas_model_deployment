# Deployments

This folder contains scripts and resources for deploying your API as a SageMaker live endpoint with autoscaling capabilities.

## Files

- **build_and_push.sh**: This bash script builds your API container and pushes it to Amazon Elastic Container Registry (ECR) to make it available for deployment.
- **deployment_notebook.ipynb**: This Jupyter Notebook provides step-by-step instructions on how to deploy the API container from ECR to a SageMaker live endpoint and apply autoscaling policies.

## Usage

1. Run the `build_and_push.sh` script to build your API container and push it to your ECR repository. Make sure to provide the necessary configurations and credentials in the script, such as the ECR repository name and AWS credentials.

2. Open the `deployment_notebook.ipynb` notebook. This notebook provides a guide on deploying the API container to a SageMaker live endpoint, configuring autoscaling policies, and demonstrating the usage of the deployed endpoint.

3. Follow the instructions in the notebook to deploy the API container to SageMaker, configure autoscaling policies based on your requirements, and test the endpoint using provided examples and APIs.

4. Monitor and manage the deployed SageMaker endpoint and autoscaling policies to ensure optimal performance and resource utilization.

## Prerequisites

- Docker: Make sure you have Docker installed on your local machine for building the API container.
- AWS CLI: Ensure you have the AWS CLI configured with appropriate credentials to push the container to ECR and deploy the SageMaker endpoint.
- SageMaker: Familiarize yourself with Amazon SageMaker concepts and workflows to effectively utilize the provided deployment resources.

Note: Modify the scripts and configurations based on your specific project requirements, such as container build steps, environment variables, or additional SageMaker endpoint customization.

Feel free to update this README.md file to provide additional details, specific instructions, or any other relevant information for your project's deployment folder.

Happy deploying!
