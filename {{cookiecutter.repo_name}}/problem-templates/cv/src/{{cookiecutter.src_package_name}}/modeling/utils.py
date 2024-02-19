"""Utilities for model training and experimentation workflows.
"""
import torch

import {{cookiecutter.src_package_name}} as {{cookiecutter.src_package_name_short}}


def train(args, model, device, train_loader, optimiser, epoch, mlflow_init_status):
    """Trains model.

    Parameters
    ----------
    args : omegaconf.DictConfig
        An omegaconf.DictConfig object containing arguments from the main function.
    model : `torch.nn.Module` object
        Initialised PyTorch model.
    device : `torch.device` object
        Device type to be used for training.
    train_loader : `torch.utils.data.DataLoader` object
        Iterable that provides batches of data from the training dataset.
    optimiser : `torch.optim.Optimizer` object
        Optimiser algorithm to be used for training.
    epoch : int
        Current epoch value.
    mlflow_init_status : bool
        Boolean value indicative of success of intialising connection
        with MLflow server.

    Returns
    -------
    loss.item() : float
        Average loss value for the training dataset.
    """
    model.train()
    for batch_idx, (_, data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimiser.zero_grad()
        output = model(data)
        loss = torch.nn.functional.nll_loss(output, target)
        loss.backward()
        optimiser.step()
        if batch_idx % args["log_interval"] == 0:
            print(
                "Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}".format(
                    epoch,
                    batch_idx * len(data),
                    len(train_loader.dataset),
                    100.0 * batch_idx / len(train_loader),
                    loss.item(),
                )
            )
            if args["dry_run"]:
                break

    {{cookiecutter.src_package_name_short}}.general_utils.mlflow_log(
        mlflow_init_status,
        "log_metric",
        key="train_loss",
        value=loss.item(),
        step=epoch,
    )

    return loss.item()


def test(model, device, test_loader, epoch, mlflow_init_status):
    """Evaluate model on test dataset.

    Parameters
    ----------
    model : `torch.nn.Module` object
        Initialised PyTorch model.
    device : `torch.device` object
        Device type to be used for training.
    test_loader : `torch.utils.data.DataLoader` object
        Iterable that provides batches of data from the test dataset.
    epoch : int
        Current epoch value.
    mlflow_init_status : bool
        Boolean value indicative of success of intialising connection
        with MLflow server.

    Returns
    -------
    test_loss : float
        Average loss value for the test dataset.
    test_accuracy : float
        Accuracy value for the test dataset.
    """
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for _, data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += torch.nn.functional.nll_loss(
                output, target, reduction="sum"
            ).item()
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)
    test_accuracy = correct / len(test_loader.dataset)

    print(
        "\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n".format(
            test_loss,
            correct,
            len(test_loader.dataset),
            100 * test_accuracy,
        )
    )

    {{cookiecutter.src_package_name_short}}.general_utils.mlflow_log(
        mlflow_init_status, "log_metric", key="test_loss", value=test_loss, step=epoch
    )
    {{cookiecutter.src_package_name_short}}.general_utils.mlflow_log(
        mlflow_init_status,
        "log_metric",
        key="test_accuracy",
        value=test_accuracy,
        step=epoch,
    )

    return test_loss, test_accuracy


def load_model(path_to_model, use_cuda, use_mps):
    """Load PyTorch model state dict.

    A sample utility function to be used for loading a PyTorch model.

    Parameters
    ----------
    path_to_model : str
        Path to a PyTorch checkpoint model.

    Returns
    -------
    loaded_model : `torch.nn.state_dict` object
        Object containing state of predictive model.
    device : `torch.device` object
        Device type to be used for whatever operation will be using this variable.
    """
    if use_cuda and torch.cuda.is_available():
        device = torch.device("cuda")
    elif use_mps and torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")
    loaded_model = {{cookiecutter.src_package_name_short}}.modeling.models.Net().to(device)
    checkpoint = torch.load(path_to_model)
    loaded_model.load_state_dict(checkpoint["model_state_dict"])
    return loaded_model, device
