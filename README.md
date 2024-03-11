# Kapitan Hull

![AI Singapore's Kapitan Hull EPTG Onprem Run:ai Banner](./assets/kapitan-hull-banner.png)

## Table of Contents

- [Kapitan Hull](#kapitan-hull)
  - [Table of Contents](#table-of-contents)
  - [Preface](#preface)
  - [Usage](#usage)
    - [Input Parameters](#input-parameters)
    - [Version Control](#version-control)

## Preface

This repository contains the [`cookiecutter`][ccutter] template for 
generating a repository that provides boilerplates touching on the 
differing components of an end-to-end ML project. 

For now, this template is dedicated for AI Singapore's on-premise 
environment, and where Run:ai is used as the MLOps platform. Other 
platforms and orchestrators would be integrated to this repository in
the near future.

[ccutter]: https://cookiecutter.readthedocs.io/en/stable/

## Usage

### Creating new repository

To use the template and create a repository, you would need to install
the `cookiecutter` CLI, say within a virtual environment and pass the
URL of this template as an argument, like such:

```bash
$ pip install "cookiecutter>=2.2"
$ cookiecutter https://github.com/aisingapore/kapitan-hull
```

If you want to run a specific version of Kapitan Hull for compatibility 
reasons, you can specify the `-c` parameter for the specific tag/branch
we have:

```bash
$ cookiecutter https://github.com/aisingapore/kapitan-hull -c <tag>
```

You will then be prompted to provide inputs. These inputs will be used 
to populate different parts of the repository to be generated by
`cookiecutter`.

### Updating your repository

If you want to update the repository with updated utilities, 
***push all your changes in your repository first***. After that, you 
can run this command in the repository:

```bash
# Add `-c <tag>` for the specific tag/branch
$ cookiecutter --replay-file cookiecutter.json \
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
| `orchestrator`           | The orchestrator the project is using. (Choose between "Run:AI", "Polyaxon" or "No orchestrator")                                | `runai`, `polyaxon` or `none`                                               | NIL                                                                                         |
| `proj_name`              | The project name used in by the repository. If you're using Run:AI, this will be the Run:AI project name used by the repository. | `sample-project`                                                            | NIL                                                                                         |
| `registry_project_path`  | Path of the registry repository for your container images to be located under. Cannot end with a slash character.                | `registry.domain.tld/sample-project/my-project`                             | [Link](https://github.com/aisingapore/kapitan-hull/blob/main/hooks/pre_gen_project.py#L22) 	|
| `problem_template`       | Initialise the repository with a default problem statement                                                                       | `base`, `cv`, `nlp` or `tabular`                                            | NIL                                                                                         |
| `author_name`            | Your alias or project team's name. Relatively arbitrary. No hyphens are allowed.                                                 | `AISG`                                  	                                  | [Link](https://github.com/aisingapore/kapitan-hull/blob/main/hooks/pre_gen_project.py#L25) 	|

### Version Control

Following the creation of your repository, initialise it with Git, push 
it to a remote, and follow its `README.md` document for a full guide on 
its usage.

## Note on AMD GPUs

Those who plan to use AMD GPUs and RoCM can check the `rocm` folder and
copy the contents into the `{{cookiecutter.repo_name}}` folder before 
populating your template. This is experimental, so official support for 
this should not be expected any time soon. This is also not added to
the main template to reduce the confusion of having multiple file 
variants for the users.