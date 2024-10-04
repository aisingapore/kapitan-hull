# Data Storage & Versioning

## Sample Data

We can generate some sample data to use to test the different 
components of Kapitan Hull.

=== "VSCode Server Terminal"

    ```bash
    mkdir -p /<NAME_OF_DATA_SOURCE>/workspaces/<YOUR_HYPHENATED_NAME>/data/raw && cd "$_"
    echo "Test1" > data1.txt
    echo "Test2" > data2.txt
    echo "Test3" > data3.txt
    ```

In the next section, we will work towards processing this set of raw
data and eventually 'training' a dummy model.