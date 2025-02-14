# Data Storage & Versioning

## Sample Data

While you may have your own project data to work with, for the purpose
of following through with this template guide, let's download the 
sample data for the [sample problem statement][prob] at hand within our 
VSCode server workspace.

[prob]: ../setting-up/02-preface.md#guides-problem-statement

=== "Coder Workspace Terminal"

    ```bash
    mkdir -p ./data/raw && cd "$_"
    wget https://storage.googleapis.com/aisg-mlops-pub-data/kapitan-hull/ResaleflatpricesbasedonregistrationdatefromJan2017onwards.csv
    ```

!!! info
    The sample data for this guide's problem statement is made
    accessible to the public. Hence any team or individual can download
    it. It is highly likely that your project's data is not publicly
    accessible and neither should it be, especially if it is a 100E
    project.


In the next section, we will work towards processing this set of raw
data and eventually 'training' a resale price prediction model.
