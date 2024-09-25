import os
import shutil
from unidiff import PatchSet


def apply_patch(patch: PatchSet, src_dir: str) -> None:

    for patched_file in patch:
        source_file_path = os.path.join(src_dir, patched_file.source_file)
        target_file_path = os.path.join(src_dir, patched_file.target_file)

        if not os.path.exists(target_file_path):
            os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
            with open(target_file_path, 'w') as f:
                pass  # Create an empty file if it does not exist
        
        modified_lines = []
        
        with open(source_file_path, 'r') as f:
            original_lines = f.readlines()

        line_index = 0
        for hunk in patched_file:
            # Apply each hunk
            while line_index < hunk.source_start - 1:
                modified_lines.append(original_lines[line_index])
                line_index += 1
                
            for line in hunk:
                if line.is_removed or line.is_context:
                    # Skip original lines (those that are removed)
                    line_index += 1
                if line.is_added or line.is_context:
                    # Add new lines (those that are added)
                    modified_lines.append(line.value)
        
        # Append any remaining lines after the last hunk
        while line_index < len(original_lines):
            modified_lines.append(original_lines[line_index])
            line_index += 1
        
        # Write the patched content back into the file
        with open(target_file_path, 'w') as f:
            f.writelines(modified_lines)


def generate_template_scripts() -> None:
    
    working_dir = os.path.join(os.getcwd(), "{{cookiecutter.repo_name}}")
    problem_templates_dir = os.path.join(working_dir, "problem-templates")
    for problem_domain in os.listdir(problem_templates_dir):
        src_dir = os.path.join(working_dir, "problem-templates", problem_domain)
        
        if not os.path.isdir(src_dir):
            continue
        
        for root, dirs, files in os.walk(src_dir):
            for file_name in files:
                if file_name.endswith('.diff'):
                    diff_file_path = os.path.join(root, file_name)

                    with open(diff_file_path, 'r') as diff_file:
                        patch_set = PatchSet(diff_file.read())
                
                    apply_patch(patch_set, os.getcwd())
                
                    # Remove the diff file after applying
                    os.remove(diff_file_path)


if __name__ == "__main__":
    generate_template_scripts()