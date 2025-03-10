import argparse
import os

from unidiff import PatchSet


def apply_patch(patch: PatchSet, src_dir: str) -> None:
    for patched_file in patch:
        source_file_path = os.path.join(src_dir, patched_file.source_file)
        target_file_path = os.path.join(src_dir, patched_file.target_file)

        if not os.path.exists(target_file_path):
            os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
            with open(target_file_path, "w") as f:
                pass  # Create an empty file if it does not exist

        try:
            with open(source_file_path, "r") as f:
                original_lines = f.readlines()

            modified_lines = []
            line_index = 0
            
            for hunk in patched_file:
                # Apply each hunk
                while line_index < hunk.source_start - 1:
                    modified_lines.append(original_lines[line_index])
                    line_index += 1

                # Extract context lines for matching
                context_lines = []
                for line in hunk:
                    if line.is_context or line.is_removed:
                        context_lines.append(line.value.rstrip('\n'))
                
                # Check if we need to search for a better match
                current_line = line_index
                if current_line < len(original_lines):
                    original_line = original_lines[current_line].rstrip('\n')
                    expected_line = next((l.value.rstrip('\n') for l in hunk if l.is_context or l.is_removed), None)
                    
                    if expected_line and original_line != expected_line:
                        print(f"WARNING: Line mismatch in {source_file_path} at line {current_line + 1}")
                        print(f"  Expected: '{expected_line}'")
                        print(f"  Found:    '{original_line}'")
                        print("Attempting to find the correct location...")
                        
                        # Try to find a better match by looking ahead in the file
                        match_found = False
                        search_range = min(100, len(original_lines) - current_line)  # Look ahead up to 100 lines
                        
                        for offset in range(search_range):
                            search_index = current_line + offset
                            
                            # Check if we have enough lines left to match the context
                            if search_index + len(context_lines) <= len(original_lines):
                                # Check if the context matches at this position
                                match = True
                                for i, ctx_line in enumerate(context_lines):
                                    if original_lines[search_index + i].rstrip('\n') != ctx_line:
                                        match = False
                                        break
                                
                                if match:
                                    print(f"Found matching context at line {search_index + 1}")
                                    # Add lines up to the new match position
                                    while line_index < search_index:
                                        modified_lines.append(original_lines[line_index])
                                        line_index += 1
                                    match_found = True
                                    break
                        
                        if not match_found:
                            print(f"ERROR: Could not find matching context in {source_file_path}")
                            print("Aborting patch for this file.")
                            raise ValueError("Patch context not found")
                
                # Apply the hunk at the current position
                for line in hunk:
                    if line.is_removed or line.is_context:
                        # Skip original lines (those that are removed)
                        if line_index < len(original_lines):
                            line_index += 1
                    
                    if line.is_added or line.is_context:
                        # Add new lines (those that are added)
                        modified_lines.append(line.value)

            # Append any remaining lines after the last hunk
            while line_index < len(original_lines):
                modified_lines.append(original_lines[line_index])
                line_index += 1

            # Write the patched content back into the file
            with open(target_file_path, "w") as f:
                f.writelines(modified_lines)
                
            print(f"Successfully applied patch to {target_file_path}")
                
        except Exception as e:
            print(f"Failed to apply patch to {target_file_path}: {str(e)}")
            print("Skipping this file and continuing with the next one.")


def generate_template_scripts() -> None:
    base_dir = os.path.join(os.getcwd(), "{{cookiecutter.repo_name}}")
    problem_templates_dir = os.path.join(base_dir, "problem-templates")
    for problem_domain in os.listdir(problem_templates_dir):
        src_dir = os.path.join(problem_templates_dir, problem_domain)

        if not os.path.isdir(src_dir):
            continue

        for root, dirs, files in os.walk(src_dir):
            for file_name in files:
                if file_name.endswith(".diff"):
                    diff_file_path = os.path.join(root, file_name)

                    try:
                        with open(diff_file_path, "r") as diff_file:
                            patch_set = PatchSet(diff_file.read())
                        apply_patch(patch_set, os.getcwd())

                        # Remove the diff file after applying
                        os.remove(diff_file_path)
                    except Exception as e:
                        print(f"Patch failed for {root}/{file_name}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Apply patches or generate template scripts."
    )
    subparsers = parser.add_subparsers()

    apply_parser = subparsers.add_parser("apply", help="Apply a diff file")
    apply_parser.add_argument("diff_file", help="Path to the diff file")

    args = parser.parse_args()

    if hasattr(args, "diff_file"):
        with open(args.diff_file, "r") as diff_file:
            patch_set = PatchSet(diff_file.read())
        apply_patch(patch_set, os.getcwd())
    else:
        generate_template_scripts()
