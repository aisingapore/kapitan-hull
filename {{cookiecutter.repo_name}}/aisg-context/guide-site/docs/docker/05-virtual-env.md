# Virtual Environments

!!! warning "Incompatibility issues"

    This method is not recommended as it may have unintended
    consequences on user and group permissions. It is highly
    recommended to [run locally][local-env] instead. This section is
    to provide a complimentary section as a means of a technical
    possibility, especially should you require debugging within the
    Docker container.

[local-env]: ../local/05-virtual-env.md

!!! info "Creating Virtual Environments"

    If you're planning to use the `code-server` development workspace
    written in the [previous section](04-dev-wksp.md), you should start
    reading [here](#using-vscode) instead.

## Docker Image Debugging

We would need to build a Docker image to create a virtual environment
that will contain all the dependencies required for this guide. This
requires the Docker image to be built from a Dockerfile
(`docker/{{cookiecutter.src_package_name}}-cpu.Dockerfile`)
provided in this template:

=== "Linux/macOS"

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
        -f docker/{{cookiecutter.repo_name}}-cpu.Dockerfile `
        --platform linux/amd64 .
    ```

!!! info "Using GPUs in Docker"

    You can build the `gpu` variant by replacing the `cpu` in the above
    commands to `gpu`, i.e.:

    - `{{cookiecutter.registry_project_path}}/cpu` to
      `{{cookiecutter.registry_project_path}}/gpu`
    - `docker/{{cookiecutter.repo_name}}-cpu.Dockerfile` to
      `docker/{{cookiecutter.repo_name}}-gpu.Dockerfile`

Spin up your Docker image by running:

=== "Linux"

    ```bash
    # If GPU image variant is used:
    # Add --gpus=all for Nvidia GPUs in front of the image name
    # Add --device=/dev/kfd --device=/dev/dri --group-add video for AMD GPUs in front of the image name
    docker run -it --rm \
        -u $(id -u):$(id -g) \
        -v ./:/home/aisg/{{cookiecutter.repo_name}} \
        {{cookiecutter.registry_project_path}}/cpu:0.1.0 \
        bash
    ```

=== "macOS"

    ```bash
    docker run -it --rm \
        -v ./:/home/aisg/{{cookiecutter.repo_name}} \
        {{cookiecutter.registry_project_path}}/cpu:0.1.0 \
        bash
    ```

=== "Windows PowerShell"

    !!! warning
        GPU passthrough only works with Docker Desktop at the time this
        section is written.
        
        For Nvidia GPUs, you would need to add `--gpus=all` in front of
        the image name.  
        For AMD GPUs, you can follow this [guide][rocm-wsl].

    ```powershell
    docker run -it --rm `
        -v .\:/home/aisg/{{cookiecutter.repo_name}} `
        {{cookiecutter.registry_project_path}}/cpu:0.1.0 `
        bash
    ```

[rocm-wsl]: https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/wsl/howto_wsl.html

You can either run `python` or install IPython to run an interactive
shell and write snippets to test within the environment:

```bash
pip install ipython
```

!!! info "Why use IPython when there is the Python interpreter?"

    There are a number of things IPython does that the Python 
    interpreter lacks:

    - Robust command history with search capabilities, allowing you to
      navigate through previously executed commands easily
    - Auto-completion, syntax highlighting and other development tools
      that make coding easier and faster
    - Enhanced debugging tools and interactive exception handling
    - Able to use hooks and plugins to enhance the IPython experience

## Using VSCode

You can create these virtual environments within your development
environment, and have it be persisted. The following set of commands
allows you to create the `conda` environment and store the packages
within your own workspace directory:

- First, have VSCode open the repository that you have cloned
  previously by heading over to the top left hand corner, selecting
  `File > Open Folder...`, and entering the path to the repository.
  In this case, you should be navigating to the folder
  `/home/coder/<YOUR_WORKSPACE_LOCATION>/{{cookiecutter.repo_name}}`.

- Now, let's initialise `conda` for the bash shell, and create
  the virtual environment specified in
  `{{cookiecutter.repo_name}}-conda-env.yaml`.

=== "VSCode Server Terminal"

    ```bash
    # Usually this is fine
    conda env create -f {{cookiecutter.repo_name}}-conda-env.yaml
    # However, if your environment does not seem to persist, you can
    # use this instead.
    conda env create \
        -f {{cookiecutter.repo_name}}-conda-env.yaml \
        -p /home/coder/<YOUR_WORKSPACE_LOCATION>/conda_envs/{{cookiecutter.repo_name}}
    ```

??? warning "If you're using the 2nd `conda env create` option"
    After creating the `conda` environment, you can create a permanent 
    alias for easy activation.

    === "VSCode Server Terminal"

        ```bash
        echo 'alias {{cookiecutter.repo_name}}-conda="conda activate /home/coder/<YOUR_WORKSPACE_LOCATION>/conda_envs/{{cookiecutter.repo_name}}"' >> ~/.bashrc
        source ~/.bashrc
        {{cookiecutter.repo_name}}-conda
        # conda environment has been activated as ({{cookiecutter.repo_name}})
        ```

!!! tip
    If you encounter issues in trying to install Python libraries,
    do ensure that the amount of resources allocated to the VSCode
    server is sufficient. Installation of libraries from PyPI tends
    to fail when there's insufficient memory. For starters, dedicate
    4GB of memory to the service:

    Another way is to add the flag `--no-cache-dir` for your
    `pip install` executions. However, there's no similar flag for
    `conda` at the moment so the above is a blanket solution.

??? info "Reference Link(s)"

    - [`conda` Docs - Managing environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file)
    - [StackOverflow - "Pip install killed - out of memory - how to get around it?"](https://stackoverflow.com/questions/57058641/pip-install-killed-out-of-memory-how-to-get-around-it)
    - [phoenixNAP - Linux alias Command: How to Use It With Examples](https://phoenixnap.com/kb/linux-alias-command#:~:text=In%20Linux%2C%20an%20alias%20is,and%20avoiding%20potential%20spelling%20errors.)

## Jupyter Kernel for VSCode

While it is possible for VSCode to make use of different virtual Python
environments, some other additional steps are required for the VSCode
server to detect the `conda` environments that you would have created.

- Ensure that you are in a project folder which you intend to work
  on. You can open a folder through `File > Open Folder...`.
  In this case, you should be navigating to the folder
  `/home/coder/<YOUR_WORKSPACE_LOCATION>/{{cookiecutter.repo_name}}`.

- Install the VSCode extensions [`ms-python.python`][py-ext] and
  [`ms-toolsai.jupyter`][jy-ext]. After installation of these 
  extensions, restart VSCode by using the shortcut `Ctrl + Shift + P`, 
  entering `Developer: Reload Window` in the prompt and pressing 
  `Enter` following that.

- Ensure that you have [`ipykernel`][ipyk] installed in the `conda` 
  environment that you intend to use. This template by default lists 
  the library as a dependency under `requirements.txt`. You can check
  for the library like so:

=== "VSCode Server Terminal"

    ```bash
    # Usually this is fine
    conda activate {{cookiecutter.repo_name}}
    # If you're using the 2nd option
    conda activate /home/coder/<YOUR_WORKSPACE_LOCATION>/conda_envs/{{cookiecutter.repo_name}}
    conda list | grep "ipykernel"
    ```

Output should look similar to:

```
ipykernel  X.XX.XX  pypi_0  pypi
```

- Now enter `Ctrl + Shift + P` again and execute 
  `Python: Select Interpreter`. Provide the path to the Python 
  executable within the `conda` environment that you intend to use, 
  something like so: `path/to/conda_env/bin/python`.

- Open up any Jupyter notebook and click on the button that says
  `Select Kernel` on the top right hand corner. You will be presented
  with a selection of Python interpreters. Select the one that
  corresponds to the environment you intend to use.

- Test out the kernel by running the cells in the sample notebook
  provided under `notebooks/sample-pytorch-notebook.ipynb`.

[py-ext]: https://marketplace.visualstudio.com/items?itemName=ms-python.python
[jy-ext]: https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter
[ipyk]: https://ipython.readthedocs.io/en/stable/install/kernel_install.html
