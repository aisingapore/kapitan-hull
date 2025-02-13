# Data Storage & Versioning

## HDB Resale Price Data

While you may have your own project data to work with, for the purpose
of following through with this template guide, let's download the 
HDB esale prices data for the [problem statement][prob] at hand within our 
Coder workspace.

[prob]: ../setting-up/02-preface.md#guides-problem-statement
=== "Linux/macOS"

    ```bash
    mkdir -p ./data/raw && cd "$_"
    wget https://tinyurl.com/hdbresalecsv -O ResaleflatpricesbasedonregistrationdatefromJan2017onwards.csv
    ```

=== "Windows Powershell"

    ```powershell 
    New-Item -ItemType Directory -Force -Path "data/raw" | Out-Null
    Set-Location -Path "data/raw"
    Invoke-WebRequest -Uri "https://tinyurl.com/hdbresalecsv" -OutFile "ResaleflatpricesbasedonregistrationdatefromJan2017onwards.csv"
    ```

In the next section, we will work towards processing this set of raw
data and eventually 'training' a resale price prediction model.
