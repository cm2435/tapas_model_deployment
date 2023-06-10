#!/bin/bash

# Set docker image variables
docker_image_name="tapas_model_serving_0001"
region="us-east-2"
repository_name="qa_api"

# Read the contents of the ~/.aws/credentials file
credentials=$(cat ~/.aws/credentials)

# Extract the access key ID and secret access key from the file and set them as variables
access_key=$(echo "$credentials" | grep -Po "(?<=aws_access_key_id = ).*")
secret_key=$(echo "$credentials" | grep -Po "(?<=aws_secret_access_key = ).*")

# Set the access key ID and secret access key as environment variables
export AWS_ACCESS_KEY_ID=$access_key
export AWS_SECRET_ACCESS_KEY=$secret_key

# Set the default region
export AWS_DEFAULT_REGION="us-east-2"

# Check if the ECR repository already exists
existing_repository=$(aws ecr describe-repositories --repository-names $repository_name 2>/dev/null)

if [[ -z "$existing_repository" ]]; then
    # Create a new ECR repository
    aws ecr create-repository --repository-name $repository_name --region $region >/dev/null
    echo "Created new ECR repository: $repository_name"
fi

# Run pytest on the subfolder ./tests and store the result in a variable
echo "running unit tests"
pytest_output=$(pytest ./tests 2>&1)

# Check if pytest passed with no errors
if [[ $pytest_output == *"ERROR"* ]]; then
    echo "pytest failed with errors:"
    echo "$pytest_output"
else
    echo "pytest passed with no errors, deploying to ECR..."

    # ECR deployment
    aws ecr get-login-password --region $region | docker login --username AWS --password-stdin 708362204001.dkr.ecr.us-east-2.amazonaws.com

    docker build -t $docker_image_name --build-arg AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID --build-arg AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY ..

    docker tag $docker_image_name:latest 708362204001.dkr.ecr.us-east-2.amazonaws.com/$repository_name:latest

    docker push 708362204001.dkr.ecr.us-east-2.amazonaws.com/$repository_name:latest

    echo "ECR deployment complete."
fi
