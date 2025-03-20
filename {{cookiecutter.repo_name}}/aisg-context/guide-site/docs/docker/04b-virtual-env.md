# Virtual Environments

!!! warning "Incompatibility issues"

    This method is not recommended as it may have unintended
    consequences on user and group permissions. It is highly
    recommended to [run locally][local-env] instead. This section is
    to provide a complimentary section as a means of a technical
    possibility, especially should you require debugging within the
    Docker container.

[local-env]: ../local/04a-virtual-env.md

!!! info "Creating Virtual Environments"

    If you're planning to use the `code-server` development workspace
    written in the [previous section](03b-dev-wksp.md), you should start
    reading [here](#using-virtual-conda-environments-within-vscode) 
    instead.

## Docker Image Debugging
{%- if cookiecutter.aisg %}

While we will be making use of AI Singapore's remote infrastructure
{%- else %}

While you might be making use of your own remote infrastructure
{%- endif %}
to carry out some workflows, we can still make use of our local
machine to execute some of the steps of the end-to-end machine learning
workflow. Hence, we can begin by creating a virtual environment
that will contain all the dependencies required for this guide. This
requires the Docker image to be built from a Dockerfile
(`docker/{{cookiecutter.src_package_name}}-cpu.Dockerfile`)
provided in this template:

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

!!! info "Using GPUs in Docker"

    You can build the `gpu` variant by replacing the `cpu` in the above
    commands to `gpu`, i.e.:

    - `{{cookiecutter.registry_project_path}}/cpu` to
      `{{cookiecutter.registry_project_path}}/gpu`
    - `docker/{{cookiecutter.repo_name}}-cpu.Dockerfile` to
      `docker/{{cookiecutter.repo_name}}-gpu.Dockerfile`

Spin up your Docker image by running:

=== "Linux"

    !!! info
        Add `--gpus=all` for Nvidia GPUs in front of the image name.  
        Add `--device=nvidia.com/gpu=all` for Nvidia GPUs using Podman
        instead of Docker.  
        Add `--device=/dev/kfd --device=/dev/dri --group-add` video for
        AMD GPUs in front of the image name.

    ```bash
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
        GPU passthrough only works with Docker Desktop or Podman 
        Desktop at the time this section is written.  
        For Nvidia GPUs, you would need to add `--gpus=all` in front of
        the image name, or `--device=nvidia.com/gpu=all` if Podman is
        used.  
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

### Using Virtual Conda Environments Within VSCode

While it is possible for VSCode to make use of different virtual Python
environments, some other additional steps are required for the VSCode
server to detect the `conda` environments that you would have created.

- Ensure that you are in a project folder which you intend to work
  on. You can open a folder through `File > Open Folder...`.

- Install the VSCode extensions [`ms-python.python`][py-ext] and
  [`ms-toolsai.jupyter`][jy-ext]. After installation of these 
  extensions, restart VSCode. If you wish to restart VSCode in-place,
  you can do so by using the shortcut `Ctrl + Shift + P`, entering 
  `Developer: Reload Window` in the prompt and pressing `Enter` 
  following that.

- Ensure that you have [`ipykernel`][ipyk] installed in the `conda` 
  environment that you intend to use. This template by default lists 
  the library as a dependency under  `requirements.txt`. You can check
  for the library like so:

    === "Linux/macOS"

        ```bash
        conda activate {{cookiecutter.repo_name}}
        conda list | grep "ipykernel"
        ```
  
    === "Windows PowerShell"

        ```powershell
        conda activate {{cookiecutter.repo_name}}
        conda list | Select-String "ipykernel"
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
