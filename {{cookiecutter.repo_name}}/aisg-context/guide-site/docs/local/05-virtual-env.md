# Virtual Environments

We can create a virtual environment that will contain all the 
dependencies required for this guide.

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