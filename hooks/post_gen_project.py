import shutil
import os


def populate_problem(problem_domain: str) -> None:

    SUB_DIRS = ["src", "conf", "notebooks"]

    for subdir in SUB_DIRS:

        working_dir = os.getcwd()
        src_dir = os.path.join(working_dir, "problem-templates", problem_domain)
        shutil.copytree(
            f"{src_dir}/{subdir}",
            f"{working_dir}/{subdir}",
            dirs_exist_ok=True
        )
        shutil.copy2(
            f"{src_dir}/{{cookiecutter.repo_name}}-conda-env.yaml",
            f"{working_dir}/{{cookiecutter.repo_name}}-conda-env.yaml"
        )


def generate_template_scripts() -> None:

    PROBLEM_TEMPLATE = "{{cookiecutter.problem_template}}"

    match PROBLEM_TEMPLATE:
        case "none":
            pass
        case "cv":
            populate_problem("cv")
        case "nlp":
            populate_problem("nlp")
        case "tabular":
            populate_problem("tabular")
        case _:
            raise ValueError(f"{PROBLEM_TEMPLATE} is not a valid problem template.")
    shutil.rmtree(os.path.join(os.getcwd(), "problem-templates"))


def remove_redundant_files() -> None:

    PLATFORM = "{{cookiecutter.platform}}"
    ORCH = "{{cookiecutter.orchestrator}}"

    BANNER_PATH = os.path.join(
        os.getcwd(), "aisg-context", "guide-site", "docs"
    )
    BANNERS = [
        'kapitan-hull-eptg-gcp-runai-banner.png',
        'kapitan-hull-eptg-onprem-runai-banner.png'
    ]
    WORKFLOW_HTML_PATH = os.path.join(
        BANNER_PATH, 'guide-for-user', 'assets'
    )
    WORKFLOWS_HTML = [
        'aisg-e2e-mlops-gcp-runai-workflow-components_jul2023.html',
        'aisg-e2e-mlops-onprem-runai-workflow-components_jul2023.html',
    ]
    WORKFLOW_PNG_PATH = os.path.join(
        WORKFLOW_HTML_PATH, 'images'
    )
    WORKFLOWS_PNG = [
        'aisg-e2e-mlops-gcp-runai-workflow-components_jul2023.png',
        'aisg-e2e-mlops-onprem-runai-workflow-components_jul2023.png'
    ]

    # Remove all banners that doesn't have both PLATFORM and ORCH
    for path, item in zip(
        [BANNER_PATH, WORKFLOW_HTML_PATH, WORKFLOW_PNG_PATH],
        [BANNERS, WORKFLOWS_HTML, WORKFLOWS_PNG]
    ):
        [os.remove(
            os.path.join(path, x)) for x in item
            if not (PLATFORM in x and ORCH in x
        )]
    

if __name__ == "__main__":
    generate_template_scripts()
    remove_redundant_files()