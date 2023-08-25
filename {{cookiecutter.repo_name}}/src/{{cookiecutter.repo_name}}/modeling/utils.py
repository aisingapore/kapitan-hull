"""
Utilities for model training and experimentation workflows.
"""
import torch

import {{cookiecutter.src_package_name}} as {{cookiecutter.src_package_name_short}}


def train(args, model, device, train_loader, optimiser, epoch, mlflow_init_status):
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

    return test_loss
