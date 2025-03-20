import os
import shutil


def populate_problem(problem_domain: str) -> None:
    if problem_domain == "base":
        shutil.rmtree(os.path.join(os.getcwd(), "problem-templates"))
        return None
    working_dir = os.getcwd()
    src_dir = os.path.join(working_dir, "problem-templates", problem_domain)
    shutil.copytree(src_dir, working_dir, dirs_exist_ok=True)
    if problem_domain == "hdb":
        os.remove(os.path.join(working_dir, "src", "batch_infer.py"))
        os.remove(os.path.join(working_dir, "conf", "batch_infer.yaml"))
    shutil.rmtree(os.path.join(os.getcwd(), "problem-templates"))


def update_mkdocs_yml(mkdocs_path) -> None:
    """
    Update the mkdocs.yml file to remove the Run:ai section.
    """
    if not os.path.exists(mkdocs_path):
        return
        
    with open(mkdocs_path, 'r') as f:
        content = f.readlines()
    
    # Find the start and end of the Run:ai section
    start_idx = None
    end_idx = None
    
    for i, line in enumerate(content):
        if "- Using Run:ai:" in line:
            start_idx = i
        elif start_idx is not None and line.startswith("  - "):
            end_idx = i
            break
    
    # If we found the Run:ai section, remove it
    if start_idx is not None and end_idx is not None:
        content = content[:start_idx] + content[end_idx:]
        
        with open(mkdocs_path, 'w') as f:
            f.writelines(content)


def remove_redundant_files() -> None:
    PLATFORM = "{{cookiecutter.platform}}"
    ORCH = "{{cookiecutter.orchestrator}}"

    DOCS_PATH = os.path.join(os.getcwd(), "aisg-context", "guide-site", "docs")
    BANNERS = [
        "kapitan-hull-eptg-gcp-runai-banner.png",
        "kapitan-hull-eptg-onprem-runai-banner.png",
        "kapitan-hull-eptg-gcp-none-banner.png",
        "kapitan-hull-eptg-onprem-none-banner.png",
    ]

    # Remove all banners that doesn't have both PLATFORM and ORCH
    for path, item in zip([DOCS_PATH], [BANNERS]):
        [
            os.remove(os.path.join(path, x))
            for x in item
            if not (PLATFORM in x and ORCH in x)
        ]

    # Remove runai yaml files if ORCH != runai
    RUNAI_YAML_PATH = os.path.join(DOCS_PATH, "runai")
    if ORCH != "runai":
        shutil.rmtree(RUNAI_YAML_PATH)

        # Update the main mkdocs.yml file to remove the Run:ai section
        update_mkdocs_yml(
            os.path.join(
                "aisg-context", "guide-site", "mkdocs.yml"
            )
        )


if __name__ == "__main__":
    populate_problem("{{cookiecutter.problem_template}}")
    remove_redundant_files()
