# Preface

## Repository Setup

This repository intend to provide an end-to-end template for AI 
Singapore's AI engineers to onboard their AI projects. Instructions for 
generating this template is detailed in the [`cookiecutter`][ccutter] 
template's repository's [`README.md`][readme].

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
__ensure that this repository is pushed to a remote__.  
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

[ccutter]: https://github.com/cookiecutter/cookiecutter
[readme]: https://github.com/aisingapore/kapitan-hull/blob/main/README.md
