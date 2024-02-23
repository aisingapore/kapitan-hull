import shutil
import os


PROBLEM_TEMPLATE = "{{cookiecutter.default_problem_template}}"
SUB_DIRS = ["src", "conf", "notebooks"]


def populate_problem(problem_domain: str) -> None:
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

    global PROBLEM_TEMPLATE

    match PROBLEM_TEMPLATE.lower():
        case "cv":
            populate_problem("cv")
        case "nlp":
            populate_problem("nlp")
        case "tabular":
            populate_problem("tabular")
        case _:
            for subdir in SUB_DIRS:
                os.makedirs(subdir, exist_ok=True)
    shutil.rmtree(os.path.join(os.getcwd(), "problem-templates"))

if __name__ == "__main__":
    generate_template_scripts()
