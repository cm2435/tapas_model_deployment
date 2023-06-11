# Tapas model deployment to sagemaker with basic CI CD 
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A brief description of your project.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Running the Tests](#running-the-tests)
- [API Methods](#api-methods)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python (3.7+)
- Conda

### Installation

1. Clone the repository:

```bash
git clone https://github.com/cm2435/tapas_model_deployment
```

2. Create a new conda environment with needed dependancies:
```bash
conda create --name project_env python=X.X
conda activate project_env
pip install -r requirements-dev.txt
```

### Running tests
Tests are stored under ./api/tests .

Unit tests can be run with pytest. 
```python
 pytest ./api/tests/unit/
```
Model performance tests can be run 