# End-to-end Project Template (On-premise Run:ai)

![AI Singapore's Kapitan Hull EPTG Onprem Run:ai Banner](./assets/images/kapitan-hull-eptg-onprem-runai-banner.png)

__Customised for `{{cookiecutter.project_name}}`__.

__Project Description:__ {{cookiecutter.description}}

This template that is also accompanied with an end-to-end guide was
generated and customised using the
following
[`cookiecutter`](https://cookiecutter.readthedocs.io/en/stable/)
template:

> https://github.com/aisingapore/ml-project-cookiecutter-onprem-runai

This `mkdocs` site is for serving the contents of the end-to-end
guide in a more readable manner, as opposed to plain
Markdown views. The contents of this guide have been customised
according to the inputs provided upon generation of this repository
through the usage of the `cookiecutter` CLI,
following instructions detailed
[here](https://github.com/aisingapore/ml-project-cookiecutter-onprem-runai/blob/main/README.md)
.

Inputs provided to `cookiecutter` for the generation of this
template:

- __`project_name`:__ {{cookiecutter.project_name}}
- __`description`:__ {{cookiecutter.description}}
- __`repo_name`:__ {{cookiecutter.repo_name}}
- __`src_package_name`:__ {{cookiecutter.src_package_name}}
- __`src_package_name_short`:__ {{cookiecutter.src_package_name_short}}
- __`harbor_registry_project_path`:__ {{cookiecutter.harbor_registry_project_path}}
- __`author_name`:__ {{cookiecutter.author_name}}

## Overview For User Guide

1. [Prerequisites](./guide-for-user/01-prerequisites.md)
2. [Preface](./guide-for-user/02-preface.md)
3. [MLOps Components & Platform](./guide-for-user/03-mlops-components-platform.md)
4. [Developer Workspace](guide-for-user/04-dev-wksp.md)
5. [Virtual Environment](./guide-for-user/05-virtual-env.md)
6. [Data Storage & Versioning](./guide-for-user/06-data-storage-versioning.md)
7. [Job Orchestration](./guide-for-user/07-job-orchestration.md)
8. [Deployment](./guide-for-user/08-deployment.md)
9. [Batch Inferencing](./guide-for-user/09-batch-inferencing.md)
10. [Continuous Integration & Deployment](./guide-for-user/10-cicd.md)
11. [Documentation](./guide-for-user/11-documentation.md)

## Directory Tree

```tree
{{cookiecutter.repo_name}}
├── aisg-context        <- Folders containing files and assets relevant
│   │                      for works within the context of AISG's
│   │                      development environments.
│   └── guide-site      <- Files relevant for spinning up the `mkdocs`
│                          site to view the end-to-end guide.
├── conf                <- Configuration files associated with the
│                          various pipelines as well as for logging.
├── data                <- Folder to contain any data for the various
│                          pipelines. Ignored by Git except its
│                          `.gitkeep` file.
├── docker              <- Dockerfiles associated with the various
│                          stages of the pipeline.
├── docs                <- A default Sphinx project; see sphinx-doc.org
│                          for details.
├── models              <- Directory for trained and serialised models.
├── notebooks           <- Jupyter notebooks. Suggested naming
│                          convention would be number (for ordering),
│                          the creator's initials, and a short `-`
│                          delimited description, e.g.
│                          `1.0-jqp-initial-data-exploration`.
├── src                 <- Directory containing the source code and
|   |                       packages for the project repository.
│   ├── {{cookiecutter.src_package_name}}
│   │   ^- Package containing modules for all pipelines except
│   │      deployment of API server.
│   ├── {{cookiecutter.src_package_name}}_fastapi
│   │   ^- Package for deploying the predictive models within a FastAPI
│   │      server.
│   └── tests           <- Directory containing tests for the
│                          repository's packages.
├── .dockerignore       <- File for specifying files or directories
│                          to be ignored by Docker contexts.
├── .gitignore          <- File for specifying files or directories
│                          to be ignored by Git.
├── .gitlab-ci.yml      <- AML file for configuring GitLab CI/CD
│                          pipelines.
├── .pylintrc           <- Configurations for `pylint`.
├── {{cookiecutter.repo_name}}-conda-env.yaml
│   ^- The `conda` environment file for reproducing
│      the project's development environment.
└── README.md           <- The top-level README containing the basic
                           guide for using the repository.
```
