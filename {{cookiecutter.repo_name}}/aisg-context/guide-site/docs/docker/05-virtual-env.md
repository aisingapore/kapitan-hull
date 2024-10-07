# Virtual Environments

!!! warning "Incompatibility issues"

    This method is not recommended as it may have unintended
    consequences on user and group permissions. It is highly
    recommended to [run locally][local-env] instead. This section is
    to provide a complimentary section as a means of a technical
    possibility, especially should you require debugging within the
    Docker container.

[local-env]: ../local/05-virtual-env.md

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