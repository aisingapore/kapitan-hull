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

    # Remove all banners that doesn't have both PLATFORM and ORCH
    [os.remove(
        os.path.join(BANNER_PATH, x)) for x in BANNERS
        if not (PLATFORM in x and ORCH in x
    )]
    

if __name__ == "__main__":
    generate_template_scripts()
    remove_redundant_files()