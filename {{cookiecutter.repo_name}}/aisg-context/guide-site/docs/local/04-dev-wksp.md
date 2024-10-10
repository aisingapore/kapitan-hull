# Development Workspace

There are many local platforms that can be utilised, of which we favour
[VSCode]/[VSCodium]. In this guide, we would refer both VSCode/VSCodium
as VSCode.

[VSCode]: https://code.visualstudio.com/Download
[VSCodium]: https://github.com/VSCodium/vscodium/releases

## VSCode

### Extensions for VSCode

You can install a multitude of extensions for your VSCode service but
there are a couple that would be crucial for your workflow, especially
if you intend to use Jupyter notebooks within the VSCode environment.

- [`ms-python.python`][vsx-python]: Official extension by Microsoft for
  rich support for many things Python.
- [`ms-toolsai.jupyter`][vsx-jy]: Official extension by Microsoft 
  for Jupyter support.

!!! warning "Attention"
    Do head over [here][jy-vscode] on how to enable the usage of 
    virtual `conda` environments within VSCode.

[vsx-python]: https://marketplace.visualstudio.com/items?itemName=ms-python.python
[vsx-jy]: https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter
[jy-vscode]: ./05-virtual-env.md#using-virtual-conda-environments-within-vscode