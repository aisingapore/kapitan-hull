# Development Workspace

An advantage presented by orchestration platforms is that you can
utilise the Kubernetes cluster's resources for your development and
engineering works instead of your own resources.

We can make use of [Coder][coder] to spin up VSCode servers with which 
cluster resources can be dedicated.

Ask your administrator on setting up Coder in your Kubernetes cluster.

[coder]: https://coder.com/

## VSCode

### Git from VSCode

To clone or push to Git repositories within the VSCode integrated
terminal, it is recommended that you first disable VSCode's Git
authentication handler:

Git by default is installed in the VSCode server image. One thing to
take note is that as the persistent storage would be accessible by the
rest of your project team members, __you should only use the `HTTPS`
protocol to clone the repository__ as opposed to creating and using an
`SSH` key within the VSCode server.

Now, let's clone your repository from the remote:

```bash
cd /<PVC_LOCATION>/workspaces/<YOUR_HYPHENATED_NAME>
git clone <REMOTE_URL_HTTPS>
cd {{cookiecutter.repo_name}}
```

### Extensions for VSCode

You can install a multitude of extensions for your VSCode service but
there are a couple that would be crucial for your workflow, especially
if you intend to use Jupyter notebooks within the VSCode environment.

- [`ms-python.python`][vsx-python]: Official extension by Microsoft for
  rich support for many things Python.
- [`ms-toolsai.jupyter`][vsx-jy]: Official extension by Microsoft 
  for Jupyter support.

!!! warning "Manual Installation"
    For some clusters, you may need to install the extensions manually
    due to firewall issues. If that is the case, you can download the
    extension(s) through your local machine and upload them to the 
    VSCode terminal. From there, you can make use of the following 
    command:
    ```
    $ code-server --install-extension /path/to/extension.vsix
    ```

!!! warning "Attention"
    Do head over [here][jy-vscode] on how to enable the usage of 
    virtual `conda` environments within VSCode.

[vsx-python]: https://marketplace.visualstudio.com/items?itemName=ms-python.python
[vsx-jy]: https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter
[jy-vscode]: ./05-virtual-env.md#jupyter-kernel-for-vscode

## Using Docker within Kubernetes

!!! caution
    Since these development environments are essentially pods deployed
    within a Kubernetes cluster, using Docker within the pods
    themselves is not feasible by default and while possible, should
    be avoided.

??? info "Reference Link(s)"

    - [Using Docker-in-Docker for your CI or testing environment? Think twice. - jpetazzo](https://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci/)