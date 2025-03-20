# Job Orchestration

We can set up development workspaces to execute jobs and workflows 
locally through Docker containers.

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

To process the sample raw data, there are many ways to do so. One way
is to run through a Docker container. You can first update your configuration
variables at `conf/process_data.yaml`, specifically this section:

```yaml
raw_data_dir_path: "./data/raw"
processed_data_dir_path: "./data/processed"
log_dir: "./logs"  # Optional: Custom directory for log files
```

This requires the Docker image to be built from a Dockerfile 
(`docker/{{cookiecutter.src_package_name}}-cpu.Dockerfile`)
provided in this template:

!!! warning "You may have built the Docker image before"

    If you have followed the section on [virtual environments][venv],
    you would have already built your image. If you have not modified 
    the configuration variables, you can safely skip this step.

[venv]: 04b-virtual-env.md

=== "Linux"

    ```bash
    docker build \
        -t {{cookiecutter.registry_project_path}}/cpu:0.1.0 \
        -f docker/{{cookiecutter.repo_name}}-cpu.Dockerfile .
    ```

=== "macOS"

    ```bash
    docker build \
        -t {{cookiecutter.registry_project_path}}/cpu:0.1.0 \
        -f docker/{{cookiecutter.repo_name}}-cpu.Dockerfile \
        --platform linux/amd64 .
    ```

=== "Windows PowerShell"

    ```powershell
    docker build `
        -t {{cookiecutter.registry_project_path}}/cpu:0.1.0 `
        -f docker/{{cookiecutter.repo_name}}-cpu.Dockerfile .
    ```

After building the image, you can run the script through Docker:

=== "Linux"

    ```bash
    sudo chown 2222:2222 ./data
    docker run --rm \
        -v ./data:/home/aisg/{{cookiecutter.repo_name}}/data \
        -w /home/aisg/{{cookiecutter.repo_name}} \
        {{cookiecutter.registry_project_path}}/cpu:0.1.0 \
        bash -c "python -u src/process_data.py log_dir=./logs"
    ```

=== "macOS"

    ```bash
    docker run --rm \
        -v ./data:/home/aisg/{{cookiecutter.repo_name}}/data \
        -w /home/aisg/{{cookiecutter.repo_name}} \
        {{cookiecutter.registry_project_path}}/cpu:0.1.0 \
        bash -c "python -u src/process_data.py"
    ```

=== "Windows PowerShell"

    ```powershell
    docker run --rm `
        -v .\data:/home/aisg/{{cookiecutter.repo_name}}/data `
        -w /home/aisg/{{cookiecutter.repo_name}} `
        {{cookiecutter.registry_project_path}}/cpu:0.1.0 `
        bash -c "python -u src/process_data.py"
    ```

Once you are satisfied with the Docker image, you can push it to the 
Docker registry:

```bash
docker push {{cookiecutter.registry_project_path}}/cpu:0.1.0
```

## Model Training

Now that we have processed the raw data, we can look into training the
model. The script relevant for this section
is `src/train_model.py`. In this script, you can see it using some
utility functions from
`src/{{cookiecutter.src_package_name}}/general_utils.py`
as well, most notably the functions for utilising MLflow utilities for
tracking experiments. Let's set up the tooling for experiment tracking
before we start model experimentation.

!!! info "Experiment Tracking and Logging"

    In the module `src/{{cookiecutter.src_package_name}}/general_utils.py`,
    the functions `mlflow_init` and `mlflow_log` are used to initialise
    MLflow experiments as well as log information and artifacts 
    relevant for a run to an `mlruns` local folder. After that, we would 
    use [the MLFlow Docker image][mlflow-docker] for analysis.
    
    The `setup_logging` function now supports a `log_dir` parameter that allows
    you to specify a custom directory for log files. This is useful when you want
    to store logs in a specific location, such as a mounted volume in a container
    environment or a shared directory for team access.

    ??? info "Reference Link(s)"

        - [MLflow Docs - Tracking](https://www.mlflow.org/docs/latest/tracking.html#)

[mlflow-docker]: https://github.com/mlflow/mlflow/pkgs/container/mlflow

Before building the Docker image to run the model training script, you 
should update your configuration variables at `conf/train_model.yaml` 
first, especially this section:

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

!!! warning "You may have built the Docker image before"

    If you have followed the section on [virtual environments][venv],
    you would have already built your image. If you have not modified 
    the configuration variables, you can safely skip this step.

!!! warning "Attention"

    If you're only using CPUs for training, then you can just reuse
    the `{{cookiecutter.repo_name}}/cpu` Docker image instead that was
    built during the previous step.  
    If you're using AMD GPUs for training, you can copy the components
    from the [`rocm`][rocm] folder in the Kapitan Hull repository.

[rocm]: https://github.com/aisingapore/kapitan-hull/tree/main/extras/rocm

=== "Linux"

    ```bash
    docker build \
        -t {{cookiecutter.registry_project_path}}/gpu:0.1.0 \
        -f docker/{{cookiecutter.repo_name}}-gpu.Dockerfile .
    ```

=== "macOS"

    ```bash
    docker build \
        -t {{cookiecutter.registry_project_path}}/gpu:0.1.0 \
        -f docker/{{cookiecutter.repo_name}}-gpu.Dockerfile \
        --platform linux/amd64 .
    ```

=== "Windows PowerShell"

    ```powershell
    docker build `
        -t {{cookiecutter.registry_project_path}}/gpu:0.1.0 `
        -f docker/{{cookiecutter.repo_name}}-gpu.Dockerfile .
    ```

Before we run the model training image, you can run MLFlow in Docker as
well with the following command:

=== "Linux"

    ```bash
    docker run --rm \
        -p 5000:5000 \
        -v ./mlruns:/mlruns \
        ghcr.io/mlflow/mlflow:v2.20.3 \
        mlflow server -h 0.0.0.0
    ```

=== "macOS"

    ```bash
    docker run --rm \
        -p 5000:5000 \
        -v ./mlruns:/mlruns \
        --platform linux/amd64 \
        ghcr.io/mlflow/mlflow:v2.20.3 \
        mlflow server -h 0.0.0.0
    ```

=== "Windows PowerShell"

    ```powershell
    docker run --rm `
        -p 5000:5000 `
        -v .\mlruns:/mlruns `
        ghcr.io/mlflow/mlflow:v2.20.3 `
        mlflow server -h 0.0.0.0
    ```

and connect to http://localhost:5000.

!!! info "Running MLFlow in the background"

    You can run MLFlow in the background by appending `-d` after
    `docker run`, but before the image name. You can also append
    `--restart always` so that it runs every time you boot up your
    machine.

After that, you can run the script through Docker while connecting to
the running MLFlow server:

=== "Linux"

    !!! info
        Add `--gpus=all` for Nvidia GPUs in front of the image name.  
        Add `--device=nvidia.com/gpu=all` for Nvidia GPUs using Podman
        instead of Docker.  
        Add `--device=/dev/kfd --device=/dev/dri --group-add` video for
        AMD GPUs in front of the image name.

    ```bash
    docker run --rm \
        -v ./data:/home/aisg/{{cookiecutter.repo_name}}/data \
        -v ./models:/home/aisg/{{cookiecutter.repo_name}}/models \
        -w /home/aisg/{{cookiecutter.repo_name}} \
        -e MLFLOW_TRACKING_URI=http://localhost:5000 \
        --network=host \
        {{cookiecutter.registry_project_path}}/gpu:0.1.0 \
        bash -c "python -u src/train_model.py mlflow_tracking_uri=\$MLFLOW_TRACKING_URI log_dir=./logs"
    ```

=== "macOS"

    ```bash
    docker run --rm \
        -v ./data:/home/aisg/{{cookiecutter.repo_name}}/data \
        -v ./models:/home/aisg/{{cookiecutter.repo_name}}/models \
        -w /home/aisg/{{cookiecutter.repo_name}} \
        -e MLFLOW_TRACKING_URI=http://localhost:5000 \
        --network=host \
        {{cookiecutter.registry_project_path}}/gpu:0.1.0 \
        bash -c "python -u src/train_model.py mlflow_tracking_uri=\$MLFLOW_TRACKING_URI"
    ```

=== "Windows PowerShell"

    !!! warning
        GPU passthrough only works with Docker Desktop or Podman 
        Desktop at the time this section is written.  
        For Nvidia GPUs, you would need to add `--gpus=all` in front of
        the image name, or `--device=nvidia.com/gpu=all` if Podman is
        used.  
        For AMD GPUs, you can follow this [guide][rocm-wsl].

    ```powershell
    docker run --rm \
        -v .\data:/home/aisg/{{cookiecutter.repo_name}}/data `
        -v .\models:/home/aisg/{{cookiecutter.repo_name}}/models `
        -w /home/aisg/{{cookiecutter.repo_name}} `
        -e MLFLOW_TRACKING_URI=http://localhost:5000 `
        --network=host `
        {{cookiecutter.registry_project_path}}/gpu:0.1.0 `
        bash -c "python -u src/train_model.py mlflow_tracking_uri=\$MLFLOW_TRACKING_URI"
    ```

[rocm-wsl]: https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/howto_wsl.html

Once you are satisfied with the Docker image, you can push it to the 
Docker registry:

```bash
docker push {{cookiecutter.registry_project_path}}/gpu:0.1.0
```

![MLflow Tracking Server - Inspecting Runs](https://storage.googleapis.com/aisg-mlops-pub-data/images/mlflow-tracking-server-inspect.gif)

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
essentially be the date epoch value of the moment you run the Docker 
container. This tag is defined using the environment value
`MLFLOW_HPTUNING_TAG`.

=== "Linux"

    !!! info
        Add `--gpus=all` for Nvidia GPUs in front of the image name.  
        Add `--device=nvidia.com/gpu=all` for Nvidia GPUs using Podman
        instead of Docker.  
        Add `--device=/dev/kfd --device=/dev/dri --group-add` video for
        AMD GPUs in front of the image name.

    ```bash
    docker run --rm \
        -v ./data:/home/aisg/{{cookiecutter.repo_name}}/data \
        -w /home/aisg/{{cookiecutter.repo_name}} \
        -e MLFLOW_HPTUNING_TAG=$(date +%s) \
        -e MLFLOW_TRACKING_URI=http://localhost:5000 \
        --network=host \
        {{cookiecutter.registry_project_path}}/gpu:0.1.0 \
        bash -c "python -u src/train_model.py --multirun mlflow_tracking_uri=\$MLFLOW_TRACKING_URI log_dir=./logs"
    ```

=== "macOS"

    ```bash
    docker run --rm \
        -v ./data:/home/aisg/{{cookiecutter.repo_name}}/data \
        -w /home/aisg/{{cookiecutter.repo_name}} \
        -e MLFLOW_HPTUNING_TAG=$(date +%s) \
        -e MLFLOW_TRACKING_URI=http://localhost:5000 \
        --network=host \
        {{cookiecutter.registry_project_path}}/gpu:0.1.0 \
        bash -c "python -u src/train_model.py --multirun mlflow_tracking_uri=\$MLFLOW_TRACKING_URI"
    ```

=== "Windows PowerShell"

    !!! warning
        GPU passthrough only works with Docker Desktop or Podman 
        Desktop at the time this section is written.  
        For Nvidia GPUs, you would need to add `--gpus=all` in front of
        the image name, or `--device=nvidia.com/gpu=all` if Podman is
        used.  
        For AMD GPUs, you can follow this [guide][rocm-wsl].

    ```powershell
    $Env:MLFLOW_HPTUNING_TAG = [int][double]::Parse((Get-Date).ToUniversalTime().Subtract([datetime]::UnixEpoch).TotalSeconds)
    [System.Environment]::SetEnvironmentVariable("MLFLOW_HPTUNING_TAG", $Env:MLFLOW_HPTUNING_TAG.ToString())
    docker run --rm \
        -v .\data:/home/aisg/{{cookiecutter.repo_name}}/data `
        -w /home/aisg/{{cookiecutter.repo_name}} `
        -e MLFLOW_HPTUNING_TAG=$Env:MLFLOW_HPTUNING_TAG `
        -e MLFLOW_TRACKING_URI=http://localhost:5000 `
        --network=host `
        {{cookiecutter.registry_project_path}}/gpu:0.1.0 `
        bash -c "python -u src/train_model.py --multirun mlflow_tracking_uri=\$MLFLOW_TRACKING_URI"
    ```

![MLflow Tracking Server - Hyperparameter Tuning Runs](../common/assets/screenshots/mlflow-tracking-hptuning-runs.png)

??? info "Reference Link(s)"

    - [Hydra Docs - Optuna Sweeper Plugin](https://hydra.cc/docs/plugins/optuna_sweeper/)
    - [MLflow Docs - Search Syntax](https://www.mlflow.org/docs/latest/search-syntax.html)

[optuna]: https://optuna.readthedocs.io/en/stable/
[parallel]: https://optuna.readthedocs.io/en/stable/tutorial/10_key_features/004_distributed.html
[optuna-vid]: https://www.youtube.com/watch?v=P6NwZVl8ttc
