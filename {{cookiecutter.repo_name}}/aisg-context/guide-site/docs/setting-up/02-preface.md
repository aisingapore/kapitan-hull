# Preface

## Repository Setup

This repository provides an end-to-end template for AI engineers to 
onboard their AI projects. Instructions for generating this template is 
detailed in the [`cookiecutter`][ccutter] template's repository's 
[`README.md`][readme].

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
{%- if cookiecutter.aisg %}
__ensure that this repository is pushed to a remote__. Most probably you 
will be resorting to [AI Singapore's GitLab instance][aisg-gitlab] as
the remote. Refer to [this section][cr8-proj] on creating a blank remote 
_repository_ (or _project_ using GitLab's terminology).  
{%- else %}
__ensure that this repository is pushed to a remote__.  
{%- endif %}
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
{%- if cookiecutter.aisg %}

Go to [this section][gitlab-page] for more information on interacting 
with the on-premise GitLab instance.
{%- endif %}

[ccutter]: https://github.com/cookiecutter/cookiecutter
[readme]: https://github.com/aisingapore/kapitan-hull/blob/main/README.md
{%- if cookiecutter.aisg %}
[aisg-gitlab]: https://gitlab.aisingapore.net/
[cr8-proj]: https://docs.gitlab.com/ee/user/project/
[gitlab-page]: https://lighthouse.aisingapore.net/Platforms/InfraOps/Gitlab
{%- endif %}
