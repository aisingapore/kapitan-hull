# Preface

## Repository Setup

This repository provides an end-to-end template for AI Singapore's AI 
engineers to onboard their AI projects. Instructions for generating 
this template is detailed in the [`cookiecutter`][ccutter] template's 
repository's [`README.md`][readme].

While this repository provides users with a set of boilerplates, here 
you are also presented with a linear guide on how to use them. The 
boilerplates are rendered and customised when you generated this 
repository using `cookiecutter`.

!!! info
    You can begin by following along the guide as it brings you through
    a simple problem statement and once you've grasped what this
    template has to offer, you can deviate from it as much as you wish
    and customise it to your needs.

Since we will be making use of this repository in multiple environments, 
__ensure that this repository is pushed to a remote__. Most probably you 
will be resorting to [AI Singapore's GitLab instance][aisg-gitlab] as
the remote. Refer to [this section][cr8-proj] on creating a blank remote 
_repository_ (or _project_ using GitLab's terminology).  
After creating the remote repository, retrieve the remote URL and push
the local repository to remote:

```bash
git init
git remote add origin <REMOTE_URL>
git add .
git config user.email "<YOUR_AISG_EMAIL>"
git config user.name "<YOUR_NAME>"
git commit -m "Initial commit."
git push -u origin main
```

Go to [this section][gitlab-page] for more information on interacting 
with the on-premise GitLab instance.

[ccutter]: https://github.com/cookiecutter/cookiecutter
[readme]: https://github.com/aisingapore/kapitan-hull/blob/main/README.md
[aisg-gitlab]: https://gitlab.aisingapore.net/
[cr8-proj]: https://docs.gitlab.com/ee/user/project/
[gitlab-page]: https://lighthouse.aisingapore.net/Platforms/InfraOps/Gitlab

## Guide's Problem Statement

For this guide, we will work towards building a model to that is
able to predict the resale price of a HDB flat upon receipt of inputs 
(e.g. flat type,floor area sqm, area)..  

Here are some criterias that you should strive towards:

- carry out all your EDA and early experimentation work within the Coder 
workspace.
- create unit tests for your data processing steps
- use Run:ai jobs to train your predictive model
- log your experiments on MLflow
- **build Docker images for serving the predictive model through a REST
API server (FastAPI or alternative frameworks)**
- document the aforementioned works within the repository

The list above is not exhaustive but do whatever you can. More than the
completion of this optional exercise, deeper understanding of the
concepts would be of better use for the journey ahead.

The raw dataset to be used is obtainable from Singapore's
open data portal; instructions for downloading the data into your development
environment are detailed under "Data Storage & Versioning" in their
respective sections ([running locally][local-data], with 
[Docker][docker-data], etc.), to be referred to later on.

!!! info
    __License:__ HDB Resale prices dataset is made available under the terms 
    of the [Open Data Licence.][cc-sa3.0].

[local-data]: ../local/05a-data-storage-versioning.md
[docker-data]: ../docker/05b-data-storage-versioning.md
[open-data-license]: https://data.gov.sg/open-data-licence

