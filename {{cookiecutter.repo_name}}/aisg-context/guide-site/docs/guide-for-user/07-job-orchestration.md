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
a job using that image to Run:ai\:

=== "Linux/macOS"

    ```bash
    $ runai submit \
        --job-name-prefix <YOUR_HYPHENATED_NAME>-data-prep \
        -i {{cookiecutter.harbor_registry_project_path}}/data-prep:0.1.0 \
        --working-dir /<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/{{cookiecutter.repo_name}} \
        --pvc <NAME_OF_DATA_SOURCE>:/<NAME_OF_DATA_SOURCE> \
        --cpu 2 \
        --memory 4G \
        --command -- '/bin/bash -c "source activate {{cookiecutter.repo_name}} && python src/process_data.py process_data.raw_data_dir_path=/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/data/mnist-pngs-data-aisg process_data.processed_data_dir_path=/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/data/processed/mnist-pngs-data-aisg-processed"'
    ```

=== "Windows PowerShell"

    ```powershell
    $ runai submit `
        --job-name-prefix <YOUR_HYPHENATED_NAME>-data-prep `
        -i {{cookiecutter.harbor_registry_project_path}}/data-prep:0.1.0 `
        --working-dir /<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/{{cookiecutter.repo_name}} `
        --pvc <NAME_OF_DATA_SOURCE>:/<NAME_OF_DATA_SOURCE> `
        --cpu 2 `
        --memory 4G `
        --command -- "/bin/bash -c 'source activate {{cookiecutter.repo_name}} && python src/process_data.py process_data.raw_data_dir_path=/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/data/mnist-pngs-data-aisg process_data.processed_data_dir_path=/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/data/processed/mnist-pngs-data-aisg-processed'"
    ```

After some time, the data processing job should conclude and we can
proceed with training the predictive model.
The processed data is exported to the directory
`/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/data/processed/mnist-pngs-data-aisg-processed`.
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
    $ docker push {{cookiecutter.harbor_registry_project_path}}/model-training:0.1.0
    ```

Now that we have the Docker image pushed to the registry,
we can run a job using it:

=== "Linux/macOS"

    ```bash
    $ runai submit \
        --job-name-prefix <YOUR_HYPHENATED_NAME>-train \
        -i {{cookiecutter.harbor_registry_project_path}}/model-training:0.1.0 \
        --working-dir /home/aisg/{{cookiecutter.repo_name}} \
        --pvc <NAME_OF_DATA_SOURCE>:/<NAME_OF_DATA_SOURCE> \
        --cpu 2 \
        --memory 4G \
        -e AWS_ACCESS_KEY_ID=SECRET:s3-credentials,accessKeyId \
        -e AWS_SECRET_ACCESS_KEY=SECRET:s3-credentials,secretAccessKey \
        -e MLFLOW_S3_ENDPOINT_URL="https://necs.nus.edu.sg" \
        -e MLFLOW_TRACKING_USERNAME=<YOUR_MLFLOW_USERNAME> \
        -e MLFLOW_TRACKING_PASSWORD=<YOUR_MLFLOW_PASSWORD> \
        --command -- '/bin/bash -c "source activate {{cookiecutter.repo_name}} && python src/train_model.py train_model.data_dir_path=/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/data/processed/mnist-pngs-data-aisg-processed train_model.setup_mlflow=true train_model.mlflow_tracking_uri=<MLFLOW_TRACKING_URI> train_model.mlflow_exp_name=<NAME_OF_DEFAULT_MLFLOW_EXPERIMENT> train_model.model_checkpoint_dir_path=/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/{{cookiecutter.repo_name}}/models train_model.epochs=3"'
    ```

=== "Windows PowerShell"

    ```powershell
    $ runai submit `
        --job-name-prefix <YOUR_HYPHENATED_NAME>-train `
        -i {{cookiecutter.harbor_registry_project_path}}/model-training:0.1.0 `
        --working-dir /home/aisg/{{cookiecutter.repo_name}} `
        --pvc <NAME_OF_DATA_SOURCE>:/<NAME_OF_DATA_SOURCE> `
        --cpu 2 `
        --memory 4G `
        -e AWS_ACCESS_KEY_ID=SECRET:s3-credentials,accessKeyId `
        -e AWS_SECRET_ACCESS_KEY=SECRET:s3-credentials,secretAccessKey `
        -e MLFLOW_S3_ENDPOINT_URL="https://necs.nus.edu.sg" `
        -e MLFLOW_TRACKING_USERNAME=<YOUR_MLFLOW_USERNAME> `
        -e MLFLOW_TRACKING_PASSWORD=<YOUR_MLFLOW_PASSWORD> `
        --command -- "/bin/bash -c 'source activate {{cookiecutter.repo_name}} && python src/train_model.py train_model.data_dir_path=/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/data/processed/mnist-pngs-data-aisg-processed train_model.setup_mlflow=true train_model.mlflow_tracking_uri=<MLFLOW_TRACKING_URI> train_model.mlflow_exp_name=<NAME_OF_DEFAULT_MLFLOW_EXPERIMENT> train_model.model_checkpoint_dir_path=/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/{{cookiecutter.repo_name}}/models train_model.epochs=3'"
    ```

Once you have successfully run an experiment, you may inspect the run
on the MLflow Tracking server. Through the MLflow Tracking server
interface, you can view the metrics and parameters logged for the run,
as well as download the artifacts that have been uploaded to the ECS
bucket. You can also compare runs with each other.

![MLflow Tracking Server - Inspecting Runs](https://storage.googleapis.com/aisg-mlops-pub-data/images/mlflow-tracking-server-inspect.gif)

!!! tip
    Every job submitted with `runai submit` is assigned a unique ID,
    and a unique job name if the `--job-name-prefix` is used.
    The `mlflow_init` function within the `general_utils.py` module
    tags every experiment name with the job's name and UUID as provided
    by Run:ai, with the tags `job_uuid` and `job_name`. This allows you
    to easily identify the MLflow experiment
    runs that are associated with each Run:ai job.
    You can filter for MLflow experiment runs associated with a
    specific Run:ai job by using MLflow's search filter expressions
    and API.

    __Reference(s):__

    - [Run:ai Docs - Environment Variables inside a Run:ai Workload](https://docs.run.ai/v2.9/Researcher/best-practices/env-variables/)
    - [MLflow Docs - Search Runs](https://mlflow.org/docs/latest/search-runs.html)

!!! info
    If your project has GPU quotas assigned to it, you can make use of
    it by specifying the `--gpu` flag in the `runai submit` command.
    As part of Run:ai's unique selling point, you can also specify
    fractional values, which would allow you to utilise a fraction of a
    GPU. This is useful for projects that require a GPU for training,
    but do not require the full capacity of a GPU.

### Hyperparameter Tuning

For many ML problems, we would be bothered with finding the optimal
parameters to train our models with. While we are able to override the
parameters for our model training workflows, imagine having to sweep
through a distribution of values. For example, if you were to seek for
the optimal learning rate within a log space, we would have to execute
`runai submit` a myriad of times manually, just to provide the training
script with a different learning rate value each time. It is reasonable
that one seeks for ways to automate this workflow.

[Optuna](https://optuna.readthedocs.io/en/stable/) is an optimisation
framework designed for ML use-cases.
Its features includes:

- ease of modularity,
- optimisation algorithms for searching the best set of parameters,
- and [paralellisation](https://optuna.readthedocs.io/en/stable/tutorial/10_key_features/004_distributed.html)
  capabilities for faster sweeps.

In addition, Hydra has a plugin for utilising Optuna which further
translates to ease of configuration. To use Hydra's plugin for Optuna,
we have to provide further overrides within the YAML config, and this is
observed in `conf/base/pipelines.yaml`:

```yaml
defaults:
  - override hydra/sweeper: optuna
  - override hydra/sweeper/sampler: tpe

hydra:
  sweeper:
    sampler:
      seed: 55
    direction: ["minimize", "maximize"]
    study_name: "image-classification"
    storage: null
    n_trials: 3
    n_jobs: 1
    params:
      train_model.lr: range(0.9,1.7,step=0.1)
      train_model.gamma: choice(0.7,0.8,0.9)
```

These fields are used by the Optuna Sweeper plugin to configure the
Optuna study.

!!! attention
    The fields defined are terminologies used by Optuna. Therefore, it is
    recommended that you understand the basics of the tool.
    [This overview video](https://www.youtube.com/watch?v=P6NwZVl8ttc)
    covers well on the concepts brought upon by Optuna.

    Here are the definitions for some of the fields:

    - `params` is used to specify the parameters to be tuned, and the values
      to be searched through
    - `n_trials` specifies the number of trials to be executed
    - `n_jobs` specifies the number of trials to be executed in parallel

As to how the training script would work towards training a model with
the best set of parameters, there are two important lines from two
different files that we have to pay attention to.

`src/train_model.py`
```python
...
    return curr_test_loss, curr_test_accuracy
...
```

`conf/base/pipelines.yaml`
```yaml
...
    direction: ["minimize", "maximize"]
...
```

In the training script the returned variables are to contain values
that we seek to optimise for. In this case, we seek to minimise the loss
and maximise the accuracy. The `hydra.sweeper.direction` field
in the YAML config is used to specify the direction that those variables
are to optimise towards, defined in a positional manner within a list.

An additional thing to take note of is that for each trial where a
different set of parameters are concerned, a new MLflow run has to be
initialised. However, we need to somehow link all these different runs
together so that we can compare all the runs within a single Optuna
study (set of trials). How we do this is that we provide each trial with
the same tag to be logged to MLflow (`hptuning_tag`) which would
essentially be the date epoch value of the moment you submitted the job
to Run:ai. This tag is defined using the environment value
`MLFLOW_HPTUNING_TAG`. This tag is especially useful if you are
executing the model training job out of the Run:ai platform, as the
`JOB_NAME` and `JOB_UUID` environment variables would not be available
by default.

=== "Linux/macOS"

    ```bash
    $ runai submit \
        --job-name-prefix <YOUR_HYPHENATED_NAME>-train \
        -i {{cookiecutter.harbor_registry_project_path}}/model-training:0.1.0 \
        --working-dir /home/aisg/{{cookiecutter.repo_name}} \
        --pvc <NAME_OF_DATA_SOURCE>:/<NAME_OF_DATA_SOURCE> \
        --cpu 2 \
        --memory 4G \
        -e AWS_ACCESS_KEY_ID=SECRET:s3-credentials,accessKeyId \
        -e AWS_SECRET_ACCESS_KEY=SECRET:s3-credentials,secretAccessKey \
        -e MLFLOW_S3_ENDPOINT_URL="https://necs.nus.edu.sg" \
        -e MLFLOW_TRACKING_USERNAME=<YOUR_MLFLOW_USERNAME> \
        -e MLFLOW_TRACKING_PASSWORD=<YOUR_MLFLOW_PASSWORD> \
        -e MLFLOW_HPTUNING_TAG=$(date +%s) \
        --command -- '/bin/bash -c "source activate {{cookiecutter.repo_name}} && python src/train_model.py --multirun train_model.data_dir_path=/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/data/processed/mnist-pngs-data-aisg-processed train_model.setup_mlflow=true train_model.mlflow_tracking_uri=<MLFLOW_TRACKING_URI> train_model.mlflow_exp_name=<NAME_OF_DEFAULT_MLFLOW_EXPERIMENT> train_model.model_checkpoint_dir_path=/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/{{cookiecutter.repo_name}}/models train_model.epochs=3"'
    ```

=== "Windows PowerShell"

    ```powershell
    $ runai submit `
        --job-name-prefix <YOUR_HYPHENATED_NAME>-train `
        -i {{cookiecutter.harbor_registry_project_path}}/model-training:0.1.0 `
        --working-dir /home/aisg/{{cookiecutter.repo_name}} `
        --pvc <NAME_OF_DATA_SOURCE>:/<NAME_OF_DATA_SOURCE> `
        --cpu 2 `
        --memory 4G `
        -e AWS_ACCESS_KEY_ID=SECRET:s3-credentials,accessKeyId `
        -e AWS_SECRET_ACCESS_KEY=SECRET:s3-credentials,secretAccessKey `
        -e MLFLOW_S3_ENDPOINT_URL="https://necs.nus.edu.sg" `
        -e MLFLOW_TRACKING_USERNAME=<YOUR_MLFLOW_USERNAME> `
        -e MLFLOW_TRACKING_PASSWORD=<YOUR_MLFLOW_PASSWORD> `
        -e MLFLOW_HPTUNING_TAG=$(Get-Date -UFormat %s -Millisecond 0) `
        --command -- "/bin/bash -c 'source activate {{cookiecutter.repo_name}} && python src/train_model.py --multirun train_model.data_dir_path=/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/data/processed/mnist-pngs-data-aisg-processed train_model.setup_mlflow=true train_model.mlflow_tracking_uri=<MLFLOW_TRACKING_URI> train_model.mlflow_exp_name=<NAME_OF_DEFAULT_MLFLOW_EXPERIMENT> train_model.model_checkpoint_dir_path=/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/{{cookiecutter.repo_name}}/models train_model.epochs=3'"
    ```

![MLflow Tracking Server - Hyperparameter Tuning Runs](assets/screenshots/mlflow-tracking-hptuning-runs.png)

__Reference(s):__

- [Run:ai Docs - Environment Variables inside a Run:ai Workload](https://docs.run.ai/v2.9/Researcher/best-practices/env-variables/)
- [Hydra Docs - Optuna Sweeper Plugin](https://hydra.cc/docs/plugins/optuna_sweeper/)
- [MLflow Docs - Search Syntax](https://www.mlflow.org/docs/latest/search-syntax.html)
