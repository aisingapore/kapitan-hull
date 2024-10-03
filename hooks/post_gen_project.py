import shutil
import os


def populate_problem(problem_domain: str) -> None:

    working_dir = os.getcwd()
    src_dir = os.path.join(working_dir, "problem-templates", problem_domain)
    shutil.copytree(src_dir, working_dir, dirs_exist_ok=True)


def generate_template_scripts() -> None:

    PROBLEM_TEMPLATE = "{{cookiecutter.problem_template}}"

    match PROBLEM_TEMPLATE:
        case "base":
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
        BANNER_PATH, 'setting-up', 'assets'
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
    
    # Remove runai yaml files if ORCH != runai
    RUNAI_YAML_PATH = os.path.join(
        os.getcwd(), "aisg-context", "runai"
    )
    if ORCH != 'runai':
        shutil.rmtree(RUNAI_YAML_PATH)


if __name__ == "__main__":
    generate_template_scripts()
    remove_redundant_files()