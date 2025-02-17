from {{cookiecutter.src_package_name}} import data_prep


def test_datasets_hdbdataset():
    """Test for HdbDataset class."""
    
    dataset = data_prep.datasets.HdbDataset(
        data_dir_path="./src/tests/sample_hdb_data_for_tests"
    )
    data = dataset.load_data().copy()

    assert len(data) == 7 and data.iloc[3][9] == "62 years 02 months"