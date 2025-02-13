# Data Storage & Versioning

## Sample Data

We can generate some sample data to use to test the different 
components of Kapitan Hull.

=== "Linux/macOS"

    ```bash
    mkdir -p ./data/raw && cd "$_"
    echo "Test1" > data1.txt
    echo "Test2" > data2.txt
    echo "Test3" > data3.txt
    ```

=== "Windows Powershell"

    ```powershell
    New-Item -ItemType Directory -Path .\data\raw -Force | Out-Null
    Set-Location -Path .\data\raw
    Set-Content -Path .\data1.txt -Value "Test1"
    Set-Content -Path .\data2.txt -Value "Test2"
    Set-Content -Path .\data3.txt -Value "Test3"
    ```

In the next section, we will work towards processing this set of raw
data and eventually 'training' a dummy model.
