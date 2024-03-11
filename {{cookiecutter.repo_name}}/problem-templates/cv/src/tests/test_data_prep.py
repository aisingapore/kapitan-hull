from {{cookiecutter.src_package_name}} import data_prep


def test_datasets_mnistdataset():
    """Test for MNISTDataset class."""

    dataset = data_prep.datasets.MNISTDataset(
        data_dir_path="./src/tests/sample_mnist_data_for_tests",
        anno_file_name="sample_data_table.csv",
        to_grayscale=False,
        to_tensor=False,
        transform=data_prep.transforms.MNIST_TRANSFORM_STEPS["train"],
    )

    assert len(dataset) == 3 and dataset[0][0] == "train/0/16585.png"
