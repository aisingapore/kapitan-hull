"""Dataset classes for defining how datasets are to be loaded.
"""
import os
import pandas as pd
from PIL import Image
import torch.utils.data as torch_data
import torchvision


class MNISTDataset(torch_data.Dataset):
    """MNIST dataset class."""

    def __init__(
        self,
        data_dir_path,
        anno_file_name,
        to_grayscale=False,
        to_tensor=False,
        transform=None,
    ):
        self.data_dir_path = data_dir_path
        anno_file_path = os.path.join(data_dir_path, anno_file_name)
        self.anno_df = pd.read_csv(anno_file_path)
        self.to_grayscale = to_grayscale
        self.to_tensor = to_tensor
        self.transform = transform

    def __len__(self):
        return len(self.anno_df)

    def __getitem__(self, index):
        image_file_name = self.anno_df["filepath"][index]
        image_path = os.path.join(self.data_dir_path, self.anno_df["filepath"][index])
        image = Image.open(image_path)
        if self.to_grayscale:
            image = torchvision.transforms.functional.to_grayscale(image)
        if self.to_tensor:
            image = torchvision.transforms.functional.to_tensor(image)
        if self.transform:
            image = self.transform(image)

        label = self.anno_df["label"][index]

        return image_file_name, image, label
