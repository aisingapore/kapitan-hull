# Virtual Environments

While the Docker images you will be using to run experiments on Run:ai
would contain the `conda` environments you would need, you can also
create these virtual environments within your development environment,
and have it be persisted. The following set of commands allows you to
create the `conda` environment and store the packages within your own
workspace directory:

- First, have VSCode open the repository that you have cloned
  previously by heading over to the top left hand corner, selecting
  `File > Open Folder...`, and entering the path to the repository.
  In this case, you should be navigating to the folder
  `/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/{{cookiecutter.repo_name}}`.

- Now, let's initialise `conda` for the bash shell, and create
  the virtual environment specified in
  `{{cookiecutter.repo_name}}-conda-env.yaml`.

=== "VSCode Server Terminal"

    ```bash
    # Usually this is fine
    conda env create -f {{cookiecutter.repo_name}}-conda-env.yaml
    # However, if your configuration doesn't point towards the PVC source, you can use this instead
    # Consult the MLOps team if you're unsure.
    conda env create \
        -f {{cookiecutter.repo_name}}-conda-env.yaml \
        -p /<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/conda_envs/{{cookiecutter.repo_name}}
    ```

??? warning "If you're using the 2nd `conda env create` option"
    After creating the `conda` environment, you can create a permanent 
    alias for easy activation.

    === "VSCode Server Terminal"

        ```bash
        echo 'alias {{cookiecutter.repo_name}}-conda="conda activate /<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/conda_envs/{{cookiecutter.repo_name}}"' >> ~/.bashrc
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
  `/<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/{{cookiecutter.repo_name}}`.

- Install the VSCode extensions [`ms-python.python`][py-ext] and
  [`ms-toolsai.jupyter`][jy-ext]. After installation of these 
  extensions, restart VSCode by using the shortcut `Ctrl + Shift + P`, 
  entering `Developer: Reload Window` in the prompt and pressing 
  `Enter` following that.

!!! warning "Manual Installation"
    For some clusters, you may need to install the extensions manually
    due to firewall issues. If that is the case, you can download the
    extension(s) through your local machine and upload them to the 
    VSCode terminal. From there, you can make use of the following 
    command:
    ```
    $ code-server --install-extension /path/to/extension.vsix
    ```

- Ensure that you have [`ipykernel`][ipyk] installed in the `conda` 
  environment that you intend to use. This template by default lists 
  the library as a dependency under `requirements.txt`. You can check
  for the library like so:

=== "VSCode Server Terminal"

    ```bash
    # Usually this is fine
    conda activate {{cookiecutter.repo_name}}
    # If you're using the 2nd option
    conda activate /<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/conda_envs/{{cookiecutter.repo_name}}
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