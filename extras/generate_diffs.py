# Run it in the root folder: python extras/generate_diffs.py
import os
import difflib

def create_patch(src_path, working_path):
    # Read the source file and the equivalent working file
    with open(src_path, 'r') as src_file:
        src_lines = src_file.readlines()
    
    with open(working_path, 'r') as working_file:
        working_lines = working_file.readlines()

    # Use difflib to create a unified diff
    diff = difflib.unified_diff(
        working_lines, src_lines, 
        fromfile=working_path, tofile=src_path, n=0
    )

    # Create diff file path
    diff_path = src_path + '.diff'

    # Write the diff to the diff file
    with open(diff_path, 'w') as diff_file:
        diff_file.writelines(diff)


def generate_diffs():
    working_dir = "{{cookiecutter.repo_name}}"
    problem_templates_dir = os.path.join(working_dir, "problem-templates")

    for problem_domain in os.listdir(problem_templates_dir):
        src_dir = os.path.join(problem_templates_dir, problem_domain)
        
        for root, dirs, files in os.walk(src_dir):
            for file_name in files:
                if not file_name.endswith('.diff'):
                    src_file_path = os.path.join(root, file_name)
                    equivalent_working_file_path = src_file_path.replace(src_dir, working_dir)

                    if os.path.exists(equivalent_working_file_path):
                        create_patch(
                            src_file_path,
                            equivalent_working_file_path
                        )

                        # Remove the original file in src_dir
                        os.remove(src_file_path)

if __name__ == "__main__":
    generate_diffs()