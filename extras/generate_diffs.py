# Run it in the root folder: python extras/generate_diffs.py
import argparse
import difflib
import os


def create_patch(alt_path: str, base_path: str) -> None:
    # Read the source file and the equivalent working file
    try:
        with open(alt_path, "r") as alt_file:
            alt_lines = alt_file.readlines()

        with open(base_path, "r") as base_file:
            base_lines = base_file.readlines()

        # Ensure the last line of each file ends with a newline
        if alt_lines and not alt_lines[-1].endswith("\n"):
            alt_lines[-1] += "\n"

        if base_lines and not base_lines[-1].endswith("\n"):
            base_lines[-1] += "\n"
            
        # Check if this is a template file that might contain Jinja2 syntax
        is_template_file = alt_path.endswith(('.yml', '.yaml', '.j2', '.html', '.md', '.jinja2'))
        
        # Additional check for files that might contain Jinja2 syntax based on content
        if not is_template_file:
            for line in alt_lines + base_lines:
                if '{%' in line or '{{' in line:
                    is_template_file = True
                    print(f"Detected Jinja2 syntax in {alt_path}, treating as template file")
                    break
        
        # For template files, we need to be careful with the diff context
        context_lines = 4 if is_template_file else 2

        # Use difflib to create a unified diff
        diff = difflib.unified_diff(
            base_lines, alt_lines, fromfile=base_path, tofile=alt_path, n=context_lines
        )

        # Create diff file path
        diff_path = alt_path + ".diff"

        # Write the diff to the diff file
        diff_content = list(diff)
        if diff_content:
            with open(diff_path, "w") as diff_file:
                diff_file.writelines(diff_content)
            print(f"Created diff: {diff_path}")
        else:
            print(f"No differences found between {alt_path} and {base_path}")
    except FileNotFoundError:
        print(f"File not found: {alt_path} or {base_path}")
    except Exception as e:
        print(f"Patch failed for {alt_path}, {base_path}: {e}")


def generate_diffs():
    base_dir = "{{cookiecutter.repo_name}}"
    problem_templates_dir = os.path.join(base_dir, "problem-templates")

    for problem_domain in os.listdir(problem_templates_dir):
        alt_dir = os.path.join(problem_templates_dir, problem_domain)

        for root, dirs, files in os.walk(alt_dir):
            for file_name in files:
                if not file_name.endswith(".diff"):
                    alt_file_path = os.path.join(root, file_name)
                    base_file_path = alt_file_path.replace(alt_dir, base_dir)

                    if os.path.exists(base_file_path):
                        create_patch(alt_file_path, base_file_path)

                        # Remove the original file in alt_dir
                        os.remove(alt_file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create patches or generate diffs.")
    subparsers = parser.add_subparsers()

    create_parser = subparsers.add_parser("create", help="Create a diff file")
    create_parser.add_argument("alt_file", type=str, help="Path to the alternate file")

    args = parser.parse_args()

    if hasattr(args, "alt_file"):
        # Assumes that alt_file is at */**
        # Preferably problem_templates/<type>
        base_file = os.path.join((parts := args.alt_file.split(os.sep))[0], *parts[3:])
        create_patch(args.alt_file, base_file)
    else:
        generate_diffs()
