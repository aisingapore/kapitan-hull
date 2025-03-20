# Virtual Environments

We can create a virtual environment that will contain all the 
dependencies required for this guide.
{%- if cookiecutter.aisg %}
While we will be making use of AI Singapore's remote infrastructure
{%- else %}
While you might be making use of your own remote infrastructure
{%- endif %}
to carry out some workflows, we can still make use of our local
machine to execute some of the steps of the end-to-end machine learning
workflow.

```bash
conda env create -f {{cookiecutter.repo_name}}-conda-env.yaml
```

The Conda YAML configuration file uses the `requirements.txt` to create
a Conda environment. This is so that there is parity between the 
development and deployment environment as the Docker image would use 
`requirements.txt` as the list of packages to be installed.

!!! info "On the use of GPUs"
    Conda environment configured using the YAML file does not take into
    account whether you need extra requirements to use your GPU for
    training/inference. Check the instructions on your ML/AI framework
    of choice to configure your Conda environment to suit your needs.

Activate your environment by running:

```bash
conda activate {{cookiecutter.repo_name}}
```

You can either run `python` or install IPython to run an interactive
shell and write snippets to test within the environment:

```bash
conda install ipython
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
