#Documentation Generation API 

##  The Central Repo for the deployment of ML products at Documatic that create documentation 
-Contains the codebase for all all ML projects deployed into Documatic, along with ultility code for ML engineering such as Dockerfiles, example deployments for specific usecases ect.

-Repo does not include model artefacts, those can be found at the respective S3 URI's in the processing and training job tabs on sagemaker.

##  Current list of Projects in this repo-
1. Automatic Documentation : Codebase for the exploration, training and deployment of a live T5 model to summerize code to a sagemaker API endpoint.

2. Code Search: Using Machine learning, namely bi-encoder models to do code-to-code and query-to-code search 

## Useful Sagemaker tutorials and documentation 
Example of normal BYOC sagemaker deployment--
https://sagemaker-examples.readthedocs.io/en/latest/advanced_functionality/tensorflow_bring_your_own/tensorflow_bring_your_own.html#Part-1:-Packaging-and-Uploading-your-Algorithm-for-use-with-Amazon-SageMaker

## Setup

To find codebases to update codesearch indices for,
and to add information to the database,
you need to connect to the platform database.
In our database we store installation ids for the GitHub app
users connect to their codebases,
which allows us to access code.
We use Github App authentication to create a fresh,
temporary,
access token whenever we need to access something
(e.g. cloning the repository).

To run:

1. Username, database name and port are hardcoded as default parameters in the scripts, but get from AWS secrets if any changes
2. Create a `.env` file in project root. **DO NOT ADD TO GIT**
3. Get AWS account with S3, sagemaker, and database access
4. Add `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` for your AWS user to `.env`
5. Add `DOCUMATIC_DB_PASSWORD=<password>` to `.env`. The password can be retrieved from AWS secrets manager
6. Add `DOCUMATIC_DB_HOST=<host>` to `.env`. Host can be found on AWS (host of DB, not proxy)
7. Get a private key file for the github add and copy it locally. This is passed as an argument to `main.py`

To run on an individual repository:
1. Get an access token for the repository and set it as `DOCUMATIC_GITHUB_TOKEN` in `.env`
1. Run `orchestration_pipeline/script_processing/src/serving/index_codebase.py`, setting the ID and project url as command line parameters

To run on all codesearch enabled repositories:
1. Run `orchestration_pipeline/script_processing/src/main.py`

If the language grammar file does not work on the machine,
delete it and a correct grammar will be created the next time
the scripts are run.

**Note** by default the scripts run in dry mode -
the database is **not** updated and files are **not** uploaded to S3.
When behaviour has been validated,
run in prod mode by adding the `--prod` command line argument.

## ROADMAP-- 
1.  Carry on implimenting codesearch via the paper (Papers with Code - Text and Code Embeddings by Contrastive Pre-Training)
2.  Impliment type hinting prediction for python using a weak supervision module on the python AST. 
3.  Increase quality of predictions 

## Testing

Unit testing (no intergration/database/cloud usage)
is run with `pytest` in [`tests/`](./tests/).\
Run
```
python -m pytest tests
```
to invoke unit tests.
