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
                # Get the context and removed lines from the hunk for pattern matching
                pattern_lines = []
                for line in hunk:
                    if line.is_context or line.is_removed:
                        pattern_lines.append(line.value.rstrip('\n'))
                
                if not pattern_lines:
                    # If there are no context or removed lines, just add the new lines
                    for line in hunk:
                        if line.is_added:
                            modified_lines.append(line.value)
                    continue
                
                # Try to find the best match for the pattern in the original file
                best_match_index = -1
                best_match_score = 0
                
                # Start searching from the current line_index
                for i in range(line_index, len(original_lines) - len(pattern_lines) + 1):
                    match_score = 0
                    for j, pattern_line in enumerate(pattern_lines):
                        if i + j < len(original_lines) and original_lines[i + j].rstrip('\n') == pattern_line:
                            match_score += 1
                    
                    # If we found a perfect match, use it
                    if match_score == len(pattern_lines):
                        best_match_index = i
                        break
                    
                    # Otherwise, keep track of the best partial match
                    if match_score > best_match_score:
                        best_match_score = match_score
                        best_match_index = i
                
                # If we couldn't find any match, try a more flexible approach
                if best_match_index == -1 or best_match_score < len(pattern_lines) // 2:
                    # Look for the first line of the pattern anywhere in the file
                    if pattern_lines:
                        first_pattern = pattern_lines[0]
                        for i in range(line_index, len(original_lines)):
                            if original_lines[i].rstrip('\n') == first_pattern:
                                best_match_index = i
                                break
                
                # If we still couldn't find a match, just continue from the current position
                if best_match_index == -1:
                    print(f"WARNING: Could not find match for hunk in {source_file_path}")
                    print(f"Context before: {pattern_lines[:2]}")
                    print(f"Lines to remove: {[l.value.rstrip('\\n') for l in hunk if l.is_removed][:2]}")
                    print("Skipping this hunk.")
                    continue
                
                # Add lines up to the match position
                while line_index < best_match_index:
                    modified_lines.append(original_lines[line_index])
                    line_index += 1
                
                # Apply the hunk
                removed_count = 0
                for line in hunk:
                    if line.is_removed:
                        # Skip the line in the original file (remove it)
                        if line_index < len(original_lines):
                            line_index += 1
                            removed_count += 1
                    elif line.is_context:
                        # Keep the context line and move to the next line
                        if line_index < len(original_lines):
                            modified_lines.append(original_lines[line_index])
                            line_index += 1
                    elif line.is_added:
                        # Add the new line
                        modified_lines.append(line.value)
                
                # If we didn't remove any lines but should have, try to advance the line_index
                # This handles cases where the context matched but the lines to remove didn't
                if removed_count == 0 and any(line.is_removed for line in hunk):
                    # Just advance by the number of lines that should have been removed
                    expected_removed = sum(1 for line in hunk if line.is_removed)
                    line_index += expected_removed
                    print(f"WARNING: Lines to remove don't match expected content in {source_file_path}")
                    print(f"Expected: {[l.value.rstrip('\\n') for l in hunk if l.is_removed]}")
                    print(f"Found: {[original_lines[line_index-expected_removed+i].rstrip('\\n') for i in range(expected_removed) if line_index-expected_removed+i < len(original_lines)]}")
                    print("Proceeding with caution...")
            
            # Add any remaining lines
            while line_index < len(original_lines):
                modified_lines.append(original_lines[line_index])
                line_index += 1
            
            # Check if this is a template file that might contain Jinja2 syntax
            is_template_file = target_file_path.endswith(('.yml', '.yaml', '.j2', '.html', '.md'))
            
            # Write the modified content back to the target file
            with open(target_file_path, "w") as f:
                if is_template_file:
                    # For template files, ensure we're preserving Jinja2 syntax
                    f.write(''.join(modified_lines))
                else:
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
