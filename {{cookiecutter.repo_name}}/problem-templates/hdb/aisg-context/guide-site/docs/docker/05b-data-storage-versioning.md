# Data Storage & Versioning

## Sample Data

While you may have your own project data to work with, for the purpose
of following through with this template guide, let's download the 
sample data for the [sample problem statement][prob] at hand within our 
VSCode server workspace.

=== "Linux/macOS"

    ```bash
    mkdir -p ./data/raw && cd "$_"
    wget 
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
