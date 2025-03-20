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
data preparation and model training pipelines (or any pipelines that
doesn't belong to the model serving aspects).

The configurations for logging, pipelines and hyperparameter tuning can
be found under the `conf` folder. These YAML files are then referred to 
by Hydra or general utility functions
(`src/{{cookiecutter.src_package_name}}/general_utils.py`)
for loading of parameters and configurations. The defined default 
values can be overridden through the CLI.

!!! attention
    It is recommended that you have a basic understanding of
    [Hydra]'s concepts before you move on.

??? info "Reference Link(s)"

    - [Hydra Docs - Basic Override Syntax](https://hydra.cc/docs/advanced/override_grammar/basic/)

[Hydra]: https://hydra.cc/

## Data Preparation & Preprocessing

To process the sample raw data, there are many ways to do so. We can 
either build within the Coder workspace, or to submit the job through 
Run:ai. You can first update your configuration variables at 
`conf/process_data.yaml`, specifically this section:

```yaml
raw_data_dir_path: "./data/raw"
processed_data_dir_path: "./data/processed"
log_dir: "./logs"  # Optional: Custom directory for log files
```

This requires the Docker image to be built from a Dockerfile 
(`docker/{{cookiecutter.src_package_name}}-cpu.Dockerfile`)
provided in this template:

=== "Coder Workspace Terminal"

    ```bash
    docker build \
        -t {{cookiecutter.registry_project_path}}/cpu:0.1.0 \
        -f $(pwd)/docker/{{cookiecutter.repo_name}}-cpu.Dockerfile \
        $(pwd)
{%- if cookiecutter.platform == 'gcp' %}
    # Run `gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS` 
    # and `gcloud auth configure-docker {{cookiecutter.registry_project_path.split('/')[0]}}`
{%- elif cookiecutter.platform == 'onprem' %}
    # Run `docker login {{cookiecutter.registry_project_path.split('/')[0]}}`
{%- endif %}
    # to authenticate if you have not done so
    docker push {{cookiecutter.registry_project_path}}/cpu:0.1.0
    ```

=== "Using Run:ai"

    ```bash
    # Run `runai login` and `runai config project {{cookiecutter.proj_name}}` first if needed
    # Run this in the base of your project repository, and change accordingly
    khull kaniko --context $(pwd) \
        --dockerfile $(pwd)/docker/{{cookiecutter.repo_name}}-cpu.Dockerfile \
        --destination {{cookiecutter.registry_project_path}}/cpu:0.1.0 \
{%- if cookiecutter.platform == 'gcp' %}
        --gcp \
{%- elif cookiecutter.platform == 'onprem' %}
        --cred-file /path/to/docker/config.json \
{%- endif %}
        -v <pvc-name>:/path/to/pvc/mount
    ```

Now that we have the Docker image built and pushed to the registry, we 
can submit a job using that image to Run:ai\:

=== "Coder Workspace Terminal using Run:ai"

    ```bash
    # Run `runai login` and `runai config project {{cookiecutter.proj_name}}` first if needed
    # Run this in the base of your project repository, and change accordingly
    # Switch working-dir to /<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/{{cookiecutter.repo_name}} to use the repo in the PVC
    runai submit \
        --job-name-prefix <YOUR_HYPHENATED_NAME>-data-prep \
        -i {{cookiecutter.registry_project_path}}/cpu:0.1.0 \
        --working-dir /home/aisg/{{cookiecutter.repo_name}} \
        --existing-pvc claimname=<NAME_OF_DATA_SOURCE>,path=/<NAME_OF_DATA_SOURCE> \
        --cpu 2 --cpu-limit 2 --memory 4G --memory-limit 4G --backoff-limit 1 \
        --command -- /bin/bash -c "python -u src/process_data.py \
            raw_data_dir_path=/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/data/raw \
            processed_data_dir_path=/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/data/processed \
            log_dir=/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/logs"
    ```

After some time, the data processing job should conclude and we can
proceed with training the predictive model.
The processed data is exported to the directory
`/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/data/processed`.
We will be passing this path to the model training workflows.

## Model Training

Now that we have processed the raw data, we can look into training the
sentiment classification model. The script relevant for this section
is `src/train_model.py`. In this script, you can see it using some
utility functions from
`src/{{cookiecutter.src_package_name}}/general_utils.py`
as well, most notably the functions for utilising MLflow utilities for
tracking experiments. Let's set up the tooling for experiment tracking
before we start model experimentation.

{% if cookiecutter.platform == 'onprem' -%}
    {%- set objstg = 'ECS' -%}
{% elif cookiecutter.platform == 'gcp' -%}
    {%- set objstg = 'GCS' -%}
{% endif -%}

!!! info "Experiment Tracking and Logging"

    In the module `src/{{cookiecutter.src_package_name}}/general_utils.py`,
    the functions `mlflow_init` and `mlflow_log` are used to initialise
    MLflow experiments as well as log information and artifacts 
    relevant for a run to a remote MLflow Tracking server. An MLflow 
    Tracking server is usually set up within the Run:ai project's 
    namespace for projects that requires model experimentation. 
    Artifacts logged through the MLflow API can be uploaded to {{objstg}} 
    buckets, assuming the client is authorised for access to {{objstg}}.
    
    The `setup_logging` function now supports a `log_dir` parameter that allows
    you to specify a custom directory for log files. This is useful when you want
    to store logs in a specific location, such as a mounted volume in a container
    environment or a shared directory for team access. When running in Run:ai,
    you might want to set this to a path on your persistent volume.

    To log and upload artifacts to {{objstg}} buckets through MLFlow, 
    you need to ensure that the client has access to the credentials of
    an account that can write to a bucket. This is usually settled by 
    the MLOps team, so you need only interact with MLFlow to download 
    the artifacts without explicitly knowing the {{objstg}} credentials.

    ??? info "Reference Link(s)"

        - [MLflow Docs - Tracking](https://www.mlflow.org/docs/latest/tracking.html#)
        - [MLflow Docs - Tracking (Artifact Stores)](https://www.mlflow.org/docs/latest/tracking.html#artifact-stores)

Before submitting the job to build the Docker image and run the model 
training script, you should update your configuration variables at 
`conf/train_model.yaml` first, especially this section:

```yaml
setup_mlflow: true
mlflow_autolog: false
mlflow_tracking_uri: "./mlruns"
mlflow_exp_name: "{{cookiecutter.src_package_name_short}}"
mlflow_run_name: "train-model"
data_dir_path: "./data/processed"
lr: 1.3
train_bs: 32
test_bs: 100
artifact_dir_path: "./models"
epochs: 5
resume: false
log_dir: "./logs"  # Optional: Custom directory for log files
```

After that, we build the Docker image from the Docker file 
`docker/{{cookiecutter.repo_name}}-gpu.Dockerfile`:

!!! warning "Attention"

    If you're only using CPUs for training, then you can just reuse
    the `{{cookiecutter.repo_name}}/cpu` Docker image instead that was
    built during the previous step.  

=== "Coder Workspace Terminal"

    ```bash
    docker build \
        -t {{cookiecutter.registry_project_path}}/gpu:0.1.0 \
        -f $(pwd)/docker/{{cookiecutter.repo_name}}-gpu.Dockerfile \
        $(pwd)
{%- if cookiecutter.platform == 'gcp' %}
    # Run `gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS` 
    # and `gcloud auth configure-docker {{cookiecutter.registry_project_path.split('/')[0]}}`
{%- elif cookiecutter.platform == 'onprem' %}
    # Run `docker login {{cookiecutter.registry_project_path.split('/')[0]}}`
{%- endif %}
    # to authenticate if you have not done so
    docker push {{cookiecutter.registry_project_path}}/gpu:0.1.0
    ```

=== "Using Run:ai"

    ```bash
    # Run `runai login` and `runai config project {{cookiecutter.proj_name}}` first if needed
    # Run this in the base of your project repository, and change accordingly
    khull kaniko --context $(pwd) \
        --dockerfile $(pwd)/docker/{{cookiecutter.repo_name}}-gpu.Dockerfile \
        --destination {{cookiecutter.registry_project_path}}/gpu:0.1.0 \
{%- if cookiecutter.platform == 'gcp' %}
        --gcp \
{%- elif cookiecutter.platform == 'onprem' %}
        --cred-file /path/to/docker/config.json \
{%- endif %}
        -v <pvc-name>:/path/to/pvc/mount
    ```

Now that we have the Docker image built and pushed to the registry, 
we can run a job using it:

=== "Coder Workspace Terminal using Run:ai"

    ```bash
    # Run `runai login` and `runai config project {{cookiecutter.proj_name}}` first if needed
    # Run this in the base of your project repository, and change accordingly
    # Switch working-dir to /<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/{{cookiecutter.repo_name}} to use the repo in the PVC
    $ runai submit \
        --job-name-prefix <YOUR_HYPHENATED_NAME>-train \
        -i {{cookiecutter.registry_project_path}}/gpu:0.1.0 \
        --working-dir /home/aisg/{{cookiecutter.repo_name}} \
        --existing-pvc claimname=<NAME_OF_DATA_SOURCE>,path=/<NAME_OF_DATA_SOURCE> \
        --cpu 2 --cpu-limit 2 --memory 4G --memory-limit 4G --backoff-limit 1 \
        -e MLFLOW_TRACKING_USERNAME=<YOUR_MLFLOW_USERNAME> \
        -e MLFLOW_TRACKING_PASSWORD=<YOUR_MLFLOW_PASSWORD> \
        --command -- /bin/bash -c "python -u src/train_model.py \
            mlflow_tracking_uri=<MLFLOW_TRACKING_URI> \
            mlflow_exp_name=<NAME_OF_DEFAULT_MLFLOW_EXPERIMENT> \
            data_dir_path=/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/data/processed \
            artifact_dir_path=/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/models \
            log_dir=/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/logs"
    ```

Once you have successfully run an experiment, you may inspect the run
on the MLflow Tracking server. Through the MLflow Tracking server
interface, you can view the metrics and parameters logged for the run,
as well as download the artifacts that have been uploaded to the {{objstg}}
bucket. You can also compare runs with each other.

![MLflow Tracking Server - Inspecting Runs](https://storage.googleapis.com/aisg-mlops-pub-data/images/mlflow-tracking-server-inspect.gif)

!!! tip
    Every job submitted with `runai submit` is assigned a unique ID,
    and a unique job name if the `--job-name-prefix` is used. The
    `mlflow_init` function within the `general_utils.py` module tags
    every experiment name with the job's name and UUID as provided by
    Run:ai, with the tags `job_uuid` and `job_name`. This allows you to
    easily identify the MLflow experiment runs that are associated with 
    each Run:ai job. You can filter for MLflow experiment runs 
    associated with a specific Run:ai job by using MLflow's search 
    filter expressions and API.

    ??? info "Reference Link(s)"

        - [Run:ai Docs - Environment Variables inside a Run:ai Workload](https://docs.run.ai/latest/Researcher/best-practices/env-variables/)
        - [MLflow Docs - Search Runs](https://mlflow.org/docs/latest/search-runs.html)

!!! info
    If your project has GPU quotas assigned to it, you can make use of
    it by specifying the `--gpu` flag in the `runai submit` command. As
    part of Run:ai's unique selling point, you can also specify
    fractional values, which would allow you to utilise a fraction of a
    GPU. This is useful for projects that require a GPU for training,
    but do not require the full capacity of a GPU.

!!! info "Resuming/adding new epochs"

    The training script supports resuming training from a previous 
    checkpoint by setting the `resume` parameter to `true` in the 
    configuration file. When this parameter is enabled, the script will:
    
    1. Check for the latest step logged by MLFlow
    2. Offset the epoch step with the latest step from MLFlow
    3. Continue training from the last saved epoch
    4. Log the continued training as part of the same MLflow run
    
    This is particularly useful when:
    
    - You need to extend training for additional epochs after 
      evaluating initial results
    - Training was interrupted and needs to be continued
    - You want to implement a progressive training strategy with 
      changing parameters
    
    To use this feature, simply set `resume: true` in your 
    `conf/train_model.yaml` file or append `resume=true` during runtime 
    as an override and run the training script as normal.

### Hyperparameter Tuning

For many ML problems, we would be bothered with finding the optimal
parameters to train our models with. While we are able to override the
parameters for our model training workflows, imagine having to sweep
through a distribution of values. For example, if you were to seek for
the optimal learning rate within a log space, we would have to execute
`runai submit` a myriad of times manually, just to provide the training
script with a different learning rate value each time. It is reasonable
that one seeks for ways to automate this workflow.

[Optuna][optuna] is an optimisation framework designed for ML 
use-cases. Its features includes:

- ease of modularity,
- optimisation algorithms for searching the best set of parameters,
- and [parallelisation][parallel] capabilities for faster sweeps.

In addition, Hydra has a plugin for utilising Optuna which further
translates to ease of configuration. To use Hydra's plugin for Optuna,
we have to provide further overrides within the YAML config, and this is
observed in `conf/train_model.yaml`:

```yaml
defaults:
  - override hydra/sweeper: optuna
  - override hydra/sweeper/sampler: tpe

hydra:
  sweeper:
    sampler:
      seed: 55
    direction: ["minimize", "maximize"]
    study_name: "base-template"
    storage: null
    n_trials: 3
    n_jobs: 1
    params:
      lr: range(0.9,1.7,step=0.1)
      train_bs: choice(32,48,64)
```

These fields are used by the Optuna Sweeper plugin to configure the
Optuna study.

!!! attention
    The fields defined are terminologies used by Optuna. Therefore, it is
    recommended that you understand the basics of the tool.
    [This overview video][optuna-vid] covers well on the concepts 
    brought upon by Optuna.

    Here are the definitions for some of the fields:

    - `params` is used to specify the parameters to be tuned, and the 
      values to be searched through
    - `n_trials` specifies the number of trials to be executed
    - `n_jobs` specifies the number of trials to be executed in 
      parallel

As to how the training script would work towards training a model with
the best set of parameters, there are two important lines from two
different files that we have to pay attention to.

`src/train_model.py`
```python
...
    return curr_test_loss, curr_test_accuracy
...
```

`conf/train_model.yaml`
```yaml
...
    direction: ["minimize", "maximize"]
...
```

In the training script the returned variables are to contain values
that we seek to optimise for. In this case, we seek to minimise the 
loss and maximise the accuracy. The `hydra.sweeper.direction` field in 
the YAML config is used to specify the direction that those variables 
are to optimise towards, defined in a positional manner within a list.

An additional thing to take note of is that for each trial where a
different set of parameters are concerned, a new MLflow run has to be
initialised. However, we need to somehow link all these different runs
together so that we can compare all the runs within a single Optuna
study (set of trials). How we do this is that we provide each trial 
with the same tag to be logged to MLflow (`hptuning_tag`) which would
essentially be the date epoch value of the moment you submitted the job
to Run:ai. This tag is defined using the environment value
`MLFLOW_HPTUNING_TAG`. This tag is especially useful if you are
executing the model training job out of the Run:ai platform, as the
`JOB_NAME` and `JOB_UUID` environment variables would not be available
by default.

=== "Coder Workspace Terminal using Run:ai"

    ```bash
    # Run `runai login` and `runai config project {{cookiecutter.proj_name}}` first if needed
    # Run this in the base of your project repository, and change accordingly
    # Switch working-dir to /<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/{{cookiecutter.repo_name}} to use the repo in the PVC
    runai submit \
        --job-name-prefix <YOUR_HYPHENATED_NAME>-train-hp \
        -i {{cookiecutter.registry_project_path}}/gpu:0.1.0 \
        --working-dir /home/aisg/{{cookiecutter.repo_name}} \
        --existing-pvc claimname=<NAME_OF_DATA_SOURCE>,path=/<NAME_OF_DATA_SOURCE> \
        --cpu 2 --cpu-limit 2 --memory 4G --memory-limit 4G --backoff-limit 1 \
        -e MLFLOW_TRACKING_USERNAME=<YOUR_MLFLOW_USERNAME> \
        -e MLFLOW_TRACKING_PASSWORD=<YOUR_MLFLOW_PASSWORD> \
        -e MLFLOW_HPTUNING_TAG=$(date +%s) \
        --command -- /bin/bash -c "python -u src/train_model.py --multirun \
            mlflow_tracking_uri=<MLFLOW_TRACKING_URI> \
            mlflow_exp_name=<NAME_OF_DEFAULT_MLFLOW_EXPERIMENT> \
            data_dir_path=/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/data/processed \
            artifact_dir_path=/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/models"
    ```

![MLflow Tracking Server - Hyperparameter Tuning Runs](../common/assets/screenshots/mlflow-tracking-hptuning-runs.png)

??? info "Reference Link(s)"

    - [Run:ai Docs - Environment Variables inside a Run:ai Workload](https://docs.run.ai/latest/Researcher/best-practices/env-variables/)
    - [Hydra Docs - Optuna Sweeper Plugin](https://hydra.cc/docs/plugins/optuna_sweeper/)
    - [MLflow Docs - Search Syntax](https://www.mlflow.org/docs/latest/search-syntax.html)

[optuna]: https://optuna.readthedocs.io/en/stable/
[parallel]: https://optuna.readthedocs.io/en/stable/tutorial/10_key_features/004_distributed.html
[optuna-vid]: https://www.youtube.com/watch?v=P6NwZVl8ttc
