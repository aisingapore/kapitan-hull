# Prerequisites

## Software & Tooling Prerequisites

Aside from an internet connection, you would need the following to
follow through with the guide:

- PC with the following installed:
    - If your machine is with a Windows OS, use [__PowerShell__][pshell]
      instead of the default Command (`cmd.exe`) shell. Best if you
      resort to [Windows Terminal][winterm].
    - __Web browser__
    - __Terminal__
    - __[Git][git]__
    - __[Rancher Desktop][rancher]__ or __[Docker Engine][docker]:__
      Client-server application for containerising applications as well
      as interacting with the Docker daemon.
        - For Linux users, you may install the Docker Engine (Docker 
          daemon) directly.
        - For Windows or macOS users, the Docker daemon can be installed
          through [Rancher Desktop][rancher].
    - __[miniconda][mcond]:__ for Python virtual environment management.
    - __[`kubectl`][kubectl]:__ CLI for Kubernetes.
{%- if cookiecutter.platform == 'onprem' %}  
    - __[AWS CLI][awscli]:__ CLI for AWS services.
        - You may choose to just use [`boto3`][boto3], the Python SDK 
          for AWS instead, to interact with the ECS service within a 
          Python environment. However, this does not fall under the 
          scope of this guide.
{%- elif cookiecutter.platform == 'gcp' %}
    - __[`gcloud` CLI][gcloud]:__ CLI for interacting with GCP services.
{%- endif %}
    - *(Optional)* __[`helm`][helm]:__ CLI for Kubernetes' package 
      manager.
{%- if cookiecutter.orchestrator == 'runai' %}  
- Access to a project on a Run:ai cluster.  
  See [here][runai-page] for more information.
{%- elif cookiecutter.orchestrator == 'noorch' %}  
{%- endif %}
{%- if cookiecutter.platform == 'onprem' %}  
- Credentials for an S3-compatible service (MinIO, etc).  
  See [here][ecs-page] for more information.
- Credentials for a Docker registry.  
  See [here][harbor-page] for more information.
{%- elif cookiecutter.platform == 'gcp' %}
- Access to a project on [Google Cloud Platform][gcp].  
  See [here][gcp-page] for more information.
{%- endif %}
- Credentials for an MLflow Tracking server.  
  See [here][mlflow-page] for more information.

!!! info
    Wherever relevant, you can toggle between the different commands
    that need to be executed for either Linux/macOS or the Windows 
    environment (PowerShell). See below for an example:

    === "Linux/macOS"

        ```bash
        # Get a list of files/folders in current directory
        $ ls -la
        ```

    === "Windows PowerShell"

        ```powershell
        # Get a list of files/folders in current directory
        $ Get-ChildItem . -Force
        ```

    !!! warning
        If you are on Windows OS, you would need to ensure that the 
        files you've cloned or written on your machine be with `LF` line
        endings. Otherwise, issues would arise when Docker containers 
        are being built or run. See [here][lf-set] on how to configure 
        consistent line endings for a whole folder or workspace using 
        VSCode.

[pshell]: https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.2
[winterm]: https://docs.microsoft.com/en-us/windows/terminal/
[git]: https://git-scm.com/downloads
[rancher]: https://rancherdesktop.io
[docker]: https://docs.docker.com/engine/install
[mcond]: https://conda.io/projects/conda/en/latest/user-guide/install/index.html
[kubectl]: https://kubernetes.io/docs/tasks/tools/
[helm]: https://helm.sh/docs/intro/install/
[mlflow-page]: https://lighthouse.aisingapore.net/Platforms/MLOps&LLMOps/HelmCharts/MLflow
[lf-set]: https://stackoverflow.com/questions/48692741/how-can-i-make-all-line-endings-eols-in-all-files-in-visual-studio-code-unix
{% if cookiecutter.platform == 'onprem' -%}  
[awscli]: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
[boto3]: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html
[ecs-page]: https://lighthouse.aisingapore.net/Platforms/InfraOps/ECS
[harbor-page]: https://lighthouse.aisingapore.net/Platforms/InfraOps/Harbor
{% elif cookiecutter.platform == 'gcp' -%}
[gcloud]: https://cloud.google.com/sdk/docs/install
[gcp]: https://console.cloud.google.com
[gcp-page]: https://lighthouse.aisingapore.net/tools-and-tech/gcp#gcp-project
{% endif %}
{%- if cookiecutter.orchestrator == 'runai' -%}  
[runai-page]: https://lighthouse.aisingapore.net/tools-and-tech/runai
{%- elif cookiecutter.orchestrator == 'noorch' -%}  
{% endif %}

## Tips and Tricks

- If you're using Rancher Desktop, you might encounter issues with 
  regards to the lack of CPU and memory.
    - For Mac/Linux users, from the main window, click on the gear 
      button on the top right.  
      Then, proceed to the Virtual Machines section and increase your 
      CPU and memory resources directly.
    - For Windows users, create a `.wslconfig` file user 
      `%UserProfile%` with the following content:
      ```toml
      [wsl2]
      memory=8GB
      ```
      Change the amount of memory to something you're comfortable with 
      giving up to build Docker images.
- For Windows users, if you have both Rancher and Docker Desktop 
  installed, you may need to disable the networking tunnel:
    - From the gear button on the top right, go to the WSL section 
      under the Network tab. From there, uncheck the `Enable networking 
      tunnel`.
