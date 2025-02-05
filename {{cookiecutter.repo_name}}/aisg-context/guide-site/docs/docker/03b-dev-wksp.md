# Development Workspace

You can run VSCode in Docker if you feel like doing so. The 
`code-server` image used is similar to the normal VSCode, but can be
hosted online if you know how.

## VSCode

### Spinning the Docker container up

The Docker image we are using has special user permissions to UID 2222
and GID 2222. As such, we would create a new folder named `workspaces`
to copy the codebase inside and interact with it.
(Only affects Linux)

You can spin the Docker container up as such:

=== "Linux"

    ```bash
    docker run -it --name code-server -p 127.0.0.1:8080:8080 \
      -v "$HOME:/home/coder" \
      -u "$(id -u):$(id -g)" \
      -e "DOCKER_USER=$USER" \
      asia-southeast1-docker.pkg.dev/machine-learning-ops/pub-images/code-server:latest
    ```

=== "macOS"

    ```bash
    docker run -it --name code-server -p 127.0.0.1:8080:8080 \
      -v "$HOME:/home/coder" \
      -e "DOCKER_USER=$USER" \
      asia-southeast1-docker.pkg.dev/machine-learning-ops/pub-images/code-server:latest
    ```

=== "Windows PowerShell"

    ```powershell
    docker run -it --name code-server -p 127.0.0.1:8080:8080 `
      -v "${Env:USERPROFILE}:/home/coder" `
      -e "DOCKER_USER=$Env:USERNAME" `
      asia-southeast1-docker.pkg.dev/machine-learning-ops/pub-images/code-server:latest
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
[jy-vscode]: ./04b-virtual-env.md#jupyter-kernel-for-vscode
