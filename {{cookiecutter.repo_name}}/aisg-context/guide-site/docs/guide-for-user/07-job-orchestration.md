# Job Orchestration

Even though we can set up development workspaces to execute jobs and
workflows, these environments often have limited access to resources.
To carry out heavier workloads, we encourage the usage of job
orchestration features that Run:ai offers.

Jobs are submitted to the Kubernetes cluster through Run:ai and executed
within Docker containers. Using the images specified upon job
submission, Kubernetes pods are spun up to execute the entry points or
commands defined, tapping on to the cluster's available resources.

Any jobs that are submitted to Run:ai can be tracked and monitored
through Run:ai's dashboard.

## Pipeline Configuration

In this template, Hydra is the configuration framework of choice for the
data preparation and model training pipelines (or any
pipelines that doesn't belong to the model serving aspects).

The configurations for logging, pipelines and hyperparameter tuning
can be found under `conf/base`. These YAML files are then referred to
by Hydra or general utility functions
(`src/{{cookiecutter.src_package_name}}/general_utils.py`)
for loading of parameters
and configurations. The defined default values can be overridden through
the CLI.

!!! attention
    It is recommended that you have a basic understanding of
    [Hydra](https://hydra.cc/)'s
    concepts before you move on.

__Reference(s):__

- [Hydra Docs - Basic Override Syntax](https://hydra.cc/docs/advanced/override_grammar/basic/)

## Data Preparation & Preprocessing

To process the sample raw data, we will be spinning up a job on Run:ai,
using the CLI. This job will be using a Docker image that will be built
from a Dockerfile (`docker/{{cookiecutter.src_package_name}}-data-prep.Dockerfile`)
provided in this template:

=== "Linux/macOS"

    ```bash
    $ docker build \
        -t {{cookiecutter.harbor_registry_project_path}}/data-prep:0.1.0 \
        -f docker/{{cookiecutter.repo_name}}-data-prep.Dockerfile \
        --platform linux/amd64 .
    $ docker push {{cookiecutter.harbor_registry_project_path}}/data-prep:0.1.0
    ```

=== "Windows PowerShell"

    ```powershell
    $ docker build `
        -t {{cookiecutter.harbor_registry_project_path}}/data-prep:0.1.0 `
        -f docker/{{cookiecutter.repo_name}}-data-prep.Dockerfile `
        --platform linux/amd64 .
    $ docker push {{cookiecutter.harbor_registry_project_path}}/data-prep:0.1.0
    ```

Now that we have the Docker image pushed to the registry, we can submit
a job using that image to Run:ai:

=== "Linux/macOS"

    ```bash
    $ runai submit \
        --job-name-prefix <YOUR_NAME>-data-prep \
        -i {{cookiecutter.harbor_registry_project_path}}/data-prep:0.1.0 \
        --working-dir /<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_NAME>/{{cookiecutter.repo_name}} \
        --pvc <NAME_OF_DATA_SOURCE>:/<NAME_OF_DATA_SOURCE> --cpu 2 --memory 4G \
        --command -- '/bin/bash -c "source activate {{cookiecutter.repo_name}} && python src/process_data.py process_data.raw_data_dir_path=/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_NAME>/data/mnist-pngs-data-aisg" process_data.processed_data_dir_path=/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_NAME>/data/processed/mnist-pngs-data-aisg-processed'
    ```

=== "Windows PowerShell"

    ```powershell
    $ runai submit `
        --job-name-prefix <YOUR_NAME>-data-prep `
        -i {{cookiecutter.harbor_registry_project_path}}/data-prep:0.1.0 `
        --working-dir /<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_NAME>/{{cookiecutter.repo_name}} `
        --pvc <NAME_OF_DATA_SOURCE>:/<NAME_OF_DATA_SOURCE> --cpu 2 --memory 4G `
        --command -- '/bin/bash -c "source activate {{cookiecutter.repo_name}} && python src/process_data.py process_data.raw_data_dir_path=/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_NAME>/data/mnist-pngs-data-aisg" process_data.processed_data_dir_path=/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_NAME>/data/processed/mnist-pngs-data-aisg-processed'
    ```

After some time, the data processing job should conclude and we can
proceed with training the predictive model.
The processed data is exported to the directory
`/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_NAME>/data/processed/mnist-pngs-data-aisg-processed`.
We will be passing this path to the model training workflows.

## Model Training

Now that we have processed the raw data, we can look into training the
sentiment classification model. The script relevant for this section
is `src/train_model.py`. In this script, you can see it using
some utility functions from
`src/{{cookiecutter.src_package_name}}/general_utils.py`
as well, most notably the functions for utilising MLflow utilities
for tracking experiments. Let's set up the tooling for experiment
tracking before we start model experimentation.

### Experiment Tracking

In the module `src/{{cookiecutter.src_package_name}}/general_utils.py`,
the functions `mlflow_init` and `mlflow_log` are used to initialise
MLflow experiments as well as log information and artifacts relevant
for a run to a remote MLflow Tracking server.
An MLflow Tracking server is usually set up within the Run:ai project's
namespace for projects that requires model experimentation.
Artifacts logged through the MLflow API can be
uploaded to ECS buckets, assuming the client is authorised for access to
ECS.

!!! note
    The username and password for the MLflow Tracking server
    can be retrieved from the MLOps team or your team lead.

To log and upload artifacts to ECS buckets through MLflow, you need to
ensure that the client has access to the credentials of an account that
can write to a bucket.

__Reference(s):__

- [MLflow Docs - Tracking](https://www.mlflow.org/docs/latest/tracking.html#)
- [MLflow Docs - Tracking (Artifact Stores)](https://www.mlflow.org/docs/latest/tracking.html#artifact-stores)

### Container for Experiment Job

Before we submit a job to Run:ai to train our model,
we need to build the Docker image to be used for it:

=== "Linux/macOS"

    ```bash
    $ docker build \
        -t {{cookiecutter.harbor_registry_project_path}}/model-training:0.1.0 \
        -f docker/{{cookiecutter.repo_name}}-model-training.Dockerfile \
        --platform linux/amd64 .
    $ docker push {{cookiecutter.harbor_registry_project_path}}/model-training:0.1.0
    ```

=== "Windows PowerShell"

    ```powershell
    $ docker build `
        -t {{cookiecutter.harbor_registry_project_path}}/model-training:0.1.0 `
        -f docker/{{cookiecutter.repo_name}}-model-training.Dockerfile `
        --platform linux/amd64 .
    $ docker push {{cookiecutter.harbor_registry_project_path}}/model-train:0.1.0
    ```

Now that we have the Docker image pushed to the registry,
we can run a job using it:

=== "Linux/macOS"

    ```bash
    $ runai submit \
        --job-name-prefix <YOUR_NAME>-train \
        -i {{cookiecutter.harbor_registry_project_path}}/model-training:0.1.0 \
        --working-dir /home/aisg/{{cookiecutter.repo_name}} \
        --pvc <NAME_OF_DATA_SOURCE>:/<NAME_OF_DATA_SOURCE> \
        -e AWS_ACCESS_KEY_ID=SECRET:s3-credentials,accessKeyId \
        -e AWS_SECRET_ACCESS_KEY=SECRET:s3-credentials,secretAccessKey \
        -e MLFLOW_S3_ENDPOINT_URL="https://necs.nus.edu.sg" \
        -e MLFLOW_TRACKING_USERNAME=<YOUR_MLFLOW_USERNAME> \
        -e MLFLOW_TRACKING_PASSWORD=<YOUR_MLFLOW_PASSWORD> \
        --command -- '/bin/bash -c "source activate {{cookiecutter.repo_name}} && python src/train_model.py train_model.data_dir_path=/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_NAME>/data/processed/mnist-pngs-data-aisg-processed train_model.setup_mlflow=true train_model.mlflow_tracking_uri=<MLFLOW_TRACKING_URI> train_model.mlflow_exp_name=<NAME_OF_DEFAULT_MLFLOW_EXPERIMENT> train_model.model_checkpoint_dir_path=/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_NAME>/{{cookiecutter.repo_name}}/models train_model.epochs=3"'
    ```

=== "Windows PowerShell"

    ```powershell
    $ runai submit `
        --job-name-prefix <YOUR_NAME>-train `
        -i {{cookiecutter.harbor_registry_project_path}}/model-training:0.1.0 `
        --working-dir /home/aisg/{{cookiecutter.repo_name}} `
        --pvc <NAME_OF_DATA_SOURCE>:/<NAME_OF_DATA_SOURCE> `
        -e AWS_ACCESS_KEY_ID=SECRET:s3-credentials,accessKeyId `
        -e AWS_SECRET_ACCESS_KEY=SECRET:s3-credentials,secretAccessKey `
        -e MLFLOW_S3_ENDPOINT_URL="https://necs.nus.edu.sg" `
        -e MLFLOW_TRACKING_USERNAME=<YOUR_MLFLOW_USERNAME> `
        -e MLFLOW_TRACKING_PASSWORD=<YOUR_MLFLOW_PASSWORD> `
        --command -- '/bin/bash -c "source activate {{cookiecutter.repo_name}} && python src/train_model.py train_model.data_dir_path=/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_NAME>/data/processed/mnist-pngs-data-aisg-processed train_model.setup_mlflow=true train_model.mlflow_tracking_uri=<MLFLOW_TRACKING_URI> train_model.mlflow_exp_name=<NAME_OF_DEFAULT_MLFLOW_EXPERIMENT> train_model.model_checkpoint_dir_path=/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_NAME>/{{cookiecutter.repo_name}}/models train_model.epochs=3"'
    ```

### Hyperparameter Tuning

> TO BE FILLED IN...

__Reference(s):__

- [Hydra Docs - Optuna Sweeper Plugin](https://hydra.cc/docs/plugins/optuna_sweeper/)
- [MLflow Docs - Search Syntax](https://www.mlflow.org/docs/latest/search-syntax.html)
