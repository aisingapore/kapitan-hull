# {{cookiecutter.project_name}}

{% if (cookiecutter.platform == 'gcp') and (cookiecutter.orchestrator == 'runai') -%}
![AI Singapore's Kapitan Hull EPTG GCP Run:ai Banner](./kapitan-hull-eptg-gcp-runai-banner.png)

{% elif (cookiecutter.platform == 'gcp') and (cookiecutter.orchestrator == 'none') -%}
![AI Singapore's Kapitan Hull EPTG GCP Banner](./kapitan-hull-eptg-gcp-none-banner.png)

{% elif cookiecutter.platform == 'onprem' and (cookiecutter.orchestrator == 'runai') -%}
![AI Singapore's Kapitan Hull EPTG Onprem Run:ai Banner](./kapitan-hull-eptg-onprem-runai-banner.png)

{% elif cookiecutter.platform == 'onprem' and (cookiecutter.orchestrator == 'none') -%}
![AI Singapore's Kapitan Hull EPTG Onprem Banner](./kapitan-hull-eptg-onprem-none-banner.png)

{% endif -%}

_{{cookiecutter.description}}_

__A project generated using AI Singapore's Kapitan Hull, an end-to-end 
ML project template.__

This template that is also accompanied with an end-to-end guide was
generated and customised using the following [`cookiecutter`][ccutter]
template:

> https://github.com/aisingapore/kapitan-hull

This `mkdocs` site is for serving the contents of the end-to-end guide 
in a more readable manner, as opposed to plain Markdown views. The 
contents of this guide have been customised according to the inputs 
provided upon generation of this repository through the usage of the 
`cookiecutter` CLI, following instructions detailed [here][kh-readme].

Inputs provided to `cookiecutter` for the generation of this template:

- __`project_name`:__ {{cookiecutter.project_name}}
- __`description`:__ {{cookiecutter.description}}
- __`repo_name`:__ {{cookiecutter.repo_name}}
- __`src_package_name`:__ {{cookiecutter.src_package_name}}
- __`src_package_name_short`:__ {{cookiecutter.src_package_name_short}}
- __`platform`:__ {{cookiecutter.platform}}
- __`orchestrator`:__ {{cookiecutter.orchestrator}}
- __`aisg`:__ {{cookiecutter.aisg}}
- __`proj_name`:__ {{cookiecutter.proj_name}}
- __`registry_project_path`:__ {{cookiecutter.registry_project_path}}
{% if cookiecutter.problem_template != 'base' -%}
- __`problem_template`:__ {{cookiecutter.problem_template}}
{% endif -%}
- __`author_name`:__ {{cookiecutter.author_name}}

[ccutter]: https://cookiecutter.readthedocs.io/en/stable/
[kh-readme]: https://github.com/aisingapore/kapitan-hull/blob/main/README.md

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
|   |                      packages for the project repository.
│   ├── {{cookiecutter.src_package_name}}
│   │                   ^- Package containing modules for all pipelines 
│   │                      except deployment of API server.
│   ├── {{cookiecutter.src_package_name}}_fastapi
│   │   ^- Package for deploying the predictive models within a FastAPI
│   │      server.
│   └── tests           <- Directory containing tests for the
│                          repository's packages.
├── .dockerignore       <- File for specifying files or directories
│                          to be ignored by Docker contexts.
├── .gitignore          <- File for specifying files or directories
│                          to be ignored by Git.
├── .gitlab-ci.yml      <- YAML file for configuring GitLab CI/CD
│                          pipelines.
├── .pylintrc           <- Configurations for `pylint`.
├── {{cookiecutter.repo_name}}-conda-env.yaml
│                       ^- The `conda` environment file for reproducing
│                          the project's development environment.
└── README.md           <- The top-level README containing the basic
                           guide for using the repository.
```
