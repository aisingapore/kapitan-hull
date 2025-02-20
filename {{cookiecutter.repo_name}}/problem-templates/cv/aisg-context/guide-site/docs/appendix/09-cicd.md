# Continuous Integration & Deployment

This template presents users with a base configuration for a GitLab
 CI/CD pipeline. In this section, the guide aims to provide readers
with some basic understanding of the pipeline defined in the
configuration file `.gitlab-ci.yml`.

That being said, readers would certainly benefit from reading up on
[introductory CI/CD concepts][cicd-intro] as introduced by GitLab's 
Docs.

<div class="video-wrapper">
  <iframe width="1280" height="720" src="https://www.youtube.com/embed/l5705U8s_nQ?start=392" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

[cicd-intro]: https://docs.gitlab.com/ee/ci/introduction/

## GitHub Flow

The defined pipeline assumes a GitHub flow which only relies on feature 
branches and a `main` (default) branch.

![AISG's GitHub Flow Diagram](assets/images/github-flow-aisg-diagram.png)

With reference to the diagram above, we have the following pointers:

- We make use of feature branches (`git checkout -b <NAME_OF_BRANCH>`) 
  to introduce changes to the source.
- Merge requests are made when we intend to merge the commits made to a
  feature branch to `main`.
- While one works on a feature branch, it is recommended that changes
  pushed to the `main` are pulled to the feature branch itself on a
  consistent basis. This allows the feature branch to possess the
  latest changes pushed by other developers through their own feature
  branches. In the example above, commits from the `main` branch
  following a merge of the `add-hidden-layer` branch are pulled into
  the `change-training-image` branch while that branch still expects
  further changes.
- The command `git pull` can be used to pull and sync these changes. 
  However, it's recommended that developers make use of `git fetch` and 
  `git log` to observe incoming changes first rather than pulling in 
  changes in an indiscriminate manner.
- While it's possible for commits to be made directly to the `main` 
  branch, it's recommended that they are kept minimal, at least for 
  GitHub flow _(other workflows might not heed such practices)_.

For more information on Gitlab CI pipeline, you can refer [here][lighthouse].

[lighthouse]: (https://lighthouse.aisingapore.net/tools-and-tech/Gitlab-CICD)


## Environment Variables

Before we can make use of the GitLab CI pipeline, we would have to
define the following variable(s) for the pipeline beforehand:
{%- if cookiecutter.platform == 'onprem' %}

- `HARBOR_ROBOT_CREDS_JSON`: A JSON formatted value that contains
  encoded credentials for a robot account on Harbor. This is to allow
the pipeline to interact with the Harbor server. See the next section 
  on how to generate this value/file.
{%- elif cookiecutter.platform == 'gcp' %}

- `GCP_SERVICE_ACCOUNT_KEY`: A JSON formatted value that contains 
  encoded credentials for a service account on your GCP project. This 
  is to allow the pipeline to interact with the Google Artifact 
  Registry. See [here][gcp-sa] on how to generate this file.

  After you've generated the json file, please encode the file content using `base64 -i <file>`. Afterwhich, copy paste the encoded value and define it as a CI/CD variable. 
{%- endif %}

To define CI/CD variables for a project (repository), follow the steps
listed [here][cicd-var]. 
{%- if cookiecutter.platform == 'onprem' %}
The environment variable `HARBOR_ROBOT_CREDS_JSON` needs to be a `variable` 
type.
{%- elif cookiecutter.platform == 'gcp' %}
The environment variable `GCP_SERVICE_ACCOUNT_KEY` needs to be a `variable`
type.
{%- endif %}

[cicd-var]: https://docs.gitlab.com/ee/ci/variables/#define-a-cicd-variable-in-the-ui
{%- if cookiecutter.platform == 'gcp' %}
[gcp-sa]: https://cloud.google.com/iam/docs/keys-create-delete
{%- endif %}
{%- if cookiecutter.platform == 'onprem' %}

### Docker Configuration File for Accessing Harbor

The variable `HARBOR_ROBOT_CREDS_JSON` will be used to populate the
files `/kaniko/.docker/config.json` and `/root/.docker/config.json` for
`kaniko` and `crane` to authenticate themselves before communicating
with AI Singapore's Harbor registry. You may create the JSON file like
so:

=== "Linux/macOS"

    ```bash
    echo -n <HARBOR_USERNAME>:<HARBOR_PASSWORD> | base64
    ```

=== "Windows PowerShell"

    ```powershell
    $Env:cred = "<HARBOR_USERNAME>:<HARBOR_PASSWORD>"
    $Env:bytes = [System.Text.Encoding]::ASCII.GetBytes($cred)
    $Env:base64 = [Convert]::ToBase64String($bytes)
    echo $base64
    ```

Using the output from above, copy and paste the following content
into a CI/CD environment variable of type `File`
(under `Settings` -> `CI/CD` -> `Variables` -> `Add variable`):

```json
{
    "auths": {
        "registry.aisingapore.net": {
            "auth": "<ENCODED_OUTPUT_HERE>"
        }
    }
}
```

![GitLab UI - Set File Variable under CI/CD Settings](assets/screenshots/gitlab-settings-cicd-set-file-var.png)

??? info "Reference Link(s)"

    - [GitLab Docs - GitLab CI/CD variables](https://docs.gitlab.com/ee/ci/variables/)
    - [Docker Docs - Configuration files](https://docs.docker.com/engine/reference/commandline/cli/#configuration-files)
{%- endif %}

After defining the Ci/CD Variables for the project, your pipeline should be able to pass. If not, re-run the pipeline. 

## Moving Forward

The stages and jobs defined in this default pipeline is rudimentary at
best as there is much more that could be done with GitLab CI. Some
examples off the top:

- automatically generate reports for datasets that arrive in regular
  intervals
- submit model training jobs following triggers invoked by the same
  pipeline
- automate the deployment of the FastAPI servers to Kubernetes clusters

There's much more that can be done but whatever has been shared thus 
far is hopefully enough for one to get started with CI/CD. 

Maintaining Ci/Cd pipelines requires extensive effort from developers. To reduce the effort required from developers, MLOps team has written a set of templates in which dev teams can implement - plug and play with [CICD Components][cicd components].

[cicd components]: (https://lighthouse.aisingapore.net/Platforms/MLOps&LLMOps/CICD-Components)
