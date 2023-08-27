"""Definition of transforms sequence for data preparation.
"""
import torchvision


MNIST_TRANSFORM_STEPS = {
    "train": torchvision.transforms.Compose(
        [
            torchvision.transforms.Resize(32),
            torchvision.transforms.RandomCrop((28, 28)),
            torchvision.transforms.ToTensor(),
            torchvision.transforms.Normalize((0.5,), (0.5,)),
        ]
    ),
    "test": torchvision.transforms.Compose(
        [
            torchvision.transforms.Resize(32),
            torchvision.transforms.CenterCrop((28, 28)),
            torchvision.transforms.ToTensor(),
            torchvision.transforms.Normalize((0.5,), (0.5,)),
        ]
    ),
}
