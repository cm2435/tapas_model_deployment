# Tapas model deployment to sagemaker with basic CI CD 
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Heres a brief project to show the deployment of a NLP model to sagemaker inference servers using a custom bring your own container format with GPU, tests, logging and more.
## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Permissions](#permissions)
  - [Installation](#installation)
- [Running the Tests](#running-the-tests)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python (3.7+)
- Conda

### Permissions. 
The local development of the API requires no special CSP provider permissions. That being said, CI CD must be run with an IAM role that has 
write acess to ECR and full sagmaker deployment permissions


### Installation

1. Clone the repository:

```bash
git clone https://github.com/cm2435/tapas_model_deployment
```

2. Create a new conda environment with needed dependancies:
```bash
conda create --name project_env python=3.9
conda activate project_env
pip install -r requirements-dev.txt
```

### Running tests
Tests are stored under ./api/tests .

Unit tests can be run with pytest. 
```python
 pytest ./api/tests/unit/
```
Model performance tests can be run in a similar fashion: 
```python
 pytest ./api/tests/performance
```
Integration testing is done as a script and is runnable simply a a python file 
```python
python api/tests/integration/load_test.py 
```