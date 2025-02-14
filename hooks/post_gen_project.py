import os
import shutil


def populate_problem(problem_domain: str) -> None:
    working_dir = os.getcwd()
    src_dir = os.path.join(working_dir, "problem-templates", problem_domain)
    shutil.copytree(src_dir, working_dir, dirs_exist_ok=True)
    if problem_domain == "hdb":
        os.remove(os.path.join(working_dir, "src/batch_infer.py"))


def generate_template_scripts() -> None:
    PROBLEM_TEMPLATE = "{{cookiecutter.problem_template}}"

    match PROBLEM_TEMPLATE:
        case "base":
            pass
        case "cv":
            populate_problem("cv")
        case "hdb":
            populate_problem("hdb")
        case _:
            raise ValueError(f"{PROBLEM_TEMPLATE} is not a valid problem template.")
    shutil.rmtree(os.path.join(os.getcwd(), "problem-templates"))


def remove_redundant_files() -> None:
    PLATFORM = "{{cookiecutter.platform}}"
    ORCH = "{{cookiecutter.orchestrator}}"

    BANNER_PATH = os.path.join(os.getcwd(), "aisg-context", "guide-site", "docs")
    BANNERS = [
        "kapitan-hull-eptg-gcp-runai-banner.png",
        "kapitan-hull-eptg-onprem-runai-banner.png",
    ]

    # Remove all banners that doesn't have both PLATFORM and ORCH
    for path, item in zip([BANNER_PATH], [BANNERS]):
        [
            os.remove(os.path.join(path, x))
            for x in item
            if not (PLATFORM in x and ORCH in x)
        ]

    # Remove runai yaml files if ORCH != runai
    RUNAI_YAML_PATH = os.path.join(os.getcwd(), "aisg-context", "runai")
    if ORCH != "runai":
        shutil.rmtree(RUNAI_YAML_PATH)


if __name__ == "__main__":
    generate_template_scripts()
    remove_redundant_files()
