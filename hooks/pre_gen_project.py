import re
import sys
import os
import shutil


COOKIE_INPUTS = {
    "project_name": {
        "user_input": "{{cookiecutter.project_name}}",
        "regex": r"^[a-zA-Z_]+(?:_? [a-zA-Z0-9]+)*$"},
    "description": {
        "user_input": "{{cookiecutter.description}}"},
    "repo_name": {
        "user_input": "{{cookiecutter.repo_name}}",
        "regex": r"^[a-z][a-z0-9-]+$"},
    "src_package_name": {
        "user_input": "{{cookiecutter.src_package_name}}",
        "regex": r"^[a-z](?:_?[a-z0-9]+)*$"},
    "src_package_name_short": {
        "user_input": "{{cookiecutter.src_package_name_short}}",
        "regex": r"^[a-z](?:_?[a-z0-9]+)*$"},
    "platform": {
        "user_input": "{{cookiecutter.platform}}",
        "avail": ["onprem", "gcp"]},
    "orchestrator": {
        "user_input": "{{cookiecutter.orchestrator}}",
        "avail": ["runai"]},
    "registry_project_path": {
        "user_input": "{{cookiecutter.registry_project_path}}",
        "regex": r"^(https?:\/\/)?([a-zA-Z0-9.-]+(:[a-zA-Z0-9.-]+)?@)?([a-zA-Z0-9.-]+)(:[0-9]+)?\/([a-zA-Z0-9._-]+\/)*([a-zA-Z0-9._-]+)(:[a-zA-Z0-9._-]+)?$"},
    "problem_template": {
        "user_input": "{{cookiecutter.problem_template}}",
        "avail": ["base", "cv", "hdb", "unified"]}, # hdb, unified - hidden options, only invoked through cookiecutter.json
    "author_name": {
        "user_input": "{{cookiecutter.author_name}}",
        "regex": r"^[a-zA-Z](?:_?[a-zA-Z0-9]+)*$"}
}

ERROR_MSG_LIST = []


def check_input_length(
    cookie_input_key: str, 
    cookie_input_val: str
) -> None:

    global ERROR_MSG_LIST

    input_val = cookie_input_val["user_input"].strip()
    if len(input_val) not in range(1, 73):
        ERROR_MSG_LIST.append("ERROR: %s - '%s' is not of valid length (1 to 72)."
            % (cookie_input_key, cookie_input_val["user_input"]))


def check_input_regex(
    cookie_input_key: str, 
    cookie_input_val: str
) -> None:

    global ERROR_MSG_LIST

    if not re.match(cookie_input_val["regex"], cookie_input_val["user_input"]):
        match cookie_input_key:
            case "project_name":
                ERROR_MSG_LIST.append("ERROR: %s - '%s' is not a valid project name. Please use only alphanumeric characters."
                    % (cookie_input_key, cookie_input_val["user_input"]))
            case "repo_name":
                ERROR_MSG_LIST.append("ERROR: %s - '%s' is not a valid repository name. Only alphanumeric characters and hyphens are permitted."
                    % (cookie_input_key, cookie_input_val["user_input"]))
            case "src_package_name" | "src_package_name_short":
                ERROR_MSG_LIST.append("ERROR: %s - '%s' is not a valid Python package name."
                    % (cookie_input_key, cookie_input_val["user_input"]))
            case "registry_project_path":
                ERROR_MSG_LIST.append("ERROR: %s - '%s' is not a valid container registry path."
                    % (cookie_input_key, cookie_input_val["user_input"]))
            case "author_name":
                ERROR_MSG_LIST.append("ERROR: %s - '%s' is not a valid name."
                    % (cookie_input_key, cookie_input_val["user_input"]))


def check_not_implemented(
    cookie_input_key: str, 
    cookie_input_val: str
) -> None:
    
    global ERROR_MSG_LIST

    if cookie_input_val["user_input"] not in cookie_input_val["avail"]:
        ERROR_MSG_LIST.append("ERROR: %s - '%s' has not been implemented."
            % (cookie_input_key, cookie_input_val["user_input"]))


def check_cookiecutter_inputs() -> None:

    global COOKIE_INPUTS
    global ERROR_MSG_LIST

    for cookie_input_key, cookie_input_val in COOKIE_INPUTS.items():
        if cookie_input_key != 'registry_project_path':
            check_input_length(cookie_input_key, cookie_input_val)
        if "regex" in cookie_input_val:
            check_input_regex(cookie_input_key, cookie_input_val)
        if "avail" in cookie_input_val:
            check_not_implemented(cookie_input_key, cookie_input_val)

    if len(ERROR_MSG_LIST) > 0:
        for error_msg in ERROR_MSG_LIST:
            print(error_msg)
        sys.exit(1)


def delete_other_problem_templates() -> None:
    """
    Delete all problem template folders except the one specified by the user.
    This keeps the repository clean by removing unused template code.
    """
    problem_template = COOKIE_INPUTS['problem_template']['user_input']
    problem_templates_dir = "problem-templates"
    
    # If selected template is 'base', delete the entire problem-templates folder
    if problem_template == "base":
        if os.path.exists(problem_templates_dir):
            print(f"Removing entire problem-templates directory for base template")
            shutil.rmtree(problem_templates_dir)
        return
        
    # Get all directories in the problem-templates folder
    if os.path.exists(problem_templates_dir):
        for template_dir in os.listdir(problem_templates_dir):
            dir_path = os.path.join(problem_templates_dir, template_dir)
            # Check if it's a directory and not the selected template
            if os.path.isdir(dir_path) and template_dir != problem_template:
                print(f"Removing unused problem template: {template_dir}")
                shutil.rmtree(dir_path)

if __name__ == "__main__":
    check_cookiecutter_inputs()
    delete_other_problem_templates()
