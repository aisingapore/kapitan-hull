# Kapitan Hull

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

![AI Singapore's Kapitan Hull EPTG Onprem Run:ai Banner](./assets/kapitan-hull-banner.png)

A cookiecutter template for end-to-end ML projects with MLOps best practices.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Creating a New Repository](#creating-a-new-repository)
  - [Updating Your Repository](#updating-your-repository)
  - [Input Parameters](#input-parameters)
  - [Version Control](#version-control)
- [Development](#development)
  - [Applying Diff Patch](#applying-diff-patch)
  - [Creating Diff Patch](#creating-diff-patch)
- [AMD GPU Support](#note-on-amd-gpus)

## Overview

This repository contains the [`cookiecutter`](https://cookiecutter.readthedocs.io/en/stable/) template for 
generating a repository that provides boilerplates touching on the 
differing components of an end-to-end ML project. 

For now, this template is dedicated for AI Singapore's on-premise 
environment, and where Run:ai is used as the MLOps platform. Other 
platforms and orchestrators would be integrated to this repository in
the near future.

## Features

- End-to-end ML project structure
- MLOps best practices
- Run:ai integration
- Problem-specific templates
- Docker configuration

## Installation

```bash
# Ensure that python>=3.10
pip install "cookiecutter>=2.2" unidiff
```

> For macOS users who encounter issues with the `cookiecutter` CLI installation, 
> you can use `conda install` (if using Conda), or follow the instructions on the
> [cookiecutter guide site](https://cookiecutter.readthedocs.io/en/stable/README.html#installation) using `pipx`.

## Usage

### Creating a New Repository

To use the template and create a repository:

```bash
cookiecutter https://github.com/aisingapore/kapitan-hull
```

For a specific version of Kapitan Hull:

```bash
cookiecutter https://github.com/aisingapore/kapitan-hull -c <tag>
```

You will be prompted to provide inputs that will populate different parts of the generated repository.

### Updating Your Repository

To update your repository with the latest utilities:

1. First, commit and push all your changes
2. Run:

```bash
# Add `-c <tag>` for the specific tag/branch
cookiecutter --replay-file cookiecutter.json \
    https://github.com/aisingapore/kapitan-hull \
    -o .. -f
```

### Input Parameters

| Parameter                | Detail                                                                                                                           | Default                                                                     | Regex Reference                                                                             |
|------------------------- |--------------------------------------------------------------------------------------------------------------------------------- |---------------------------------------------------------------------------- |-------------------------------------------------------------------------------------------- |
| `project_name`           | Name of project that will be the header for the `README.md`. Input to start with alphabet. Only whitespace as separators.        | My Project                                                                  | [Link](https://github.com/aisingapore/kapitan-hull/blob/main/hooks/pre_gen_project.py#L8)  	|
| `description`            | A short description of the project that will be populated in `README.md`. Max of 72 characters.                                  | A short description of the project.                                         | NIL                                                                                        	|
| `repo_name`              | Name of the repository folder. Input to start with alphabet characters. No whitespaces or underscores are allowed.               | `project_name` where whitespaces and underscores are replaced with hyphens. | [Link](https://github.com/aisingapore/kapitan-hull/blob/main/hooks/pre_gen_project.py#L13) 	|
| `src_package_name`       | Name of the source code's package under `src`. Input to start with alphabet characters. No whitespaces or hyphens are allowed.   | `repo_name` where hyphens are replaced with underscores.                    | [Link](https://github.com/aisingapore/kapitan-hull/blob/main/hooks/pre_gen_project.py#L16) 	|
| `src_package_name_short` | The alias for the source code's package. Input to start with alphabet characters. No whitespaces or hyphens are allowed.         | `src_package_name`                                                          | [Link](https://github.com/aisingapore/kapitan-hull/blob/main/hooks/pre_gen_project.py#L19) 	|
| `platform`               | The platform the project is running on. (Choose between "on-premise" or "Google Cloud Platform")                                 | `onprem` or `gcp`                                                           | NIL                                                                                         |
| `orchestrator`           | The orchestrator the project is using. (Choose between "Run:ai" or "No orchestrator")                                            | `runai` or `none`                                                           | NIL                                                                                         |
| `proj_name`              | The project name used in by the repository. If you're using Run:ai, this will be the Run:ai project name used by the repository. | `sample-project`                                                            | NIL                                                                                         |
| `registry_project_path`  | Path of the registry repository for your container images to be located under. Cannot end with a slash character.                | `registry.domain.tld/sample-project/my-project`                             | [Link](https://github.com/aisingapore/kapitan-hull/blob/main/hooks/pre_gen_project.py#L22) 	|
| `problem_template`       | Initialise the repository with a default problem statement                                                                       | `base` or `cv`                                                              | NIL                                                                                         |
| `aisg`                   | Choose whether to add AISG context                                                                                               | `true` or `false`                                                           | NIL                                                                                         |
| `author_name`            | Your alias or project team's name. Relatively arbitrary. No hyphens are allowed.                                                 | `AISG`                                  	                                  | [Link](https://github.com/aisingapore/kapitan-hull/blob/main/hooks/pre_gen_project.py#L25) 	|

### Version Control

Following the creation of your repository, initialise it with Git, push 
it to a remote, and follow its `README.md` document for a full guide on 
its usage.

## Development

To reduce the size and check the explicit changes between the base
template and the various problem templates, we opt for the use of diff
files within Kapitan Hull to store the differences within the 
repository. As such it is essential that developers would know how to 
apply patches for development, and regenerate the diff files to commit 
those changes.

### Applying Diff Patch

You can apply a specific patch as such:

```bash
python hooks/pre_prompt.py apply <diff_file>
```

### Creating Diff Patch

You can create a specific patch as such:

```bash
python extras/generate_diffs.py create <alt_file>
```

This `<alt_file>` refers to the file that is to be committed as a diff
file in the `problem-templates/<template>` folder.

> Note: When creating a diff patch, ensure that the base file and the
>       other file have an extra newline at the end to avoid patching
>       issues using the scripts.

## Note on AMD GPUs

Those who plan to use AMD GPUs and RoCM can check the `extras/rocm` 
folder and copy the contents into the `{{cookiecutter.repo_name}}` 
folder before populating your template. This is experimental, so 
official support for this should not be expected any time soon. This is 
also not added to the main template to reduce the confusion of having 
multiple file variants for the users.
