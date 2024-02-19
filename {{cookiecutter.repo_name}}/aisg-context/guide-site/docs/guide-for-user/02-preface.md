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
    a simple problem statement and once you've grasp what this template
    has to offer, you can deviate from it as much as you wish and
    customise it to your needs.

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
[readme]: https://github.com/aisingapore/ml-project-cookiecutter-onprem-runai/blob/main/README.md
[aisg-gitlab]: https://gitlab.aisingapore.net/
[cr8-proj]: https://docs.gitlab.com/ee/user/project/working_with_projects.html#create-a-project
[gitlab-page]: ./03-mlops-components-platform.md#gitlab

## Guide's Problem Statement

For this guide, we will work towards building a neural network that is
able to classify handwritten digits, widely known as the MNIST use-case.
The model is then to be deployed through a REST API and used for batch
inferencing as well.  
The raw dataset to be used is obtainable through a Google Cloud Storage
bucket; instructions for downloading the data into your development
environment are detailed under ["Data Storage & Versioning"][data-page],
to be referred to later on.

!!! info
    __License:__ Yann LeCun and Corinna Cortes hold the copyright of MNIST
    dataset. MNIST dataset is made available under the terms of the
    [Creative Commons Attribution-Share Alike 3.0 license][cc-sa3.0].

[data-page]: ./06-data-storage-versioning.md
[cc-sa3.0]: https://creativecommons.org/licenses/by-sa/3.0/