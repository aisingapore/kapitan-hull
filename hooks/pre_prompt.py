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
                        
                        # First try to find a perfect match for the first few context lines
                        context_prefix = context_lines[:min(3, len(context_lines))]
                        if context_prefix:
                            for offset in range(search_range):
                                search_index = current_line + offset
                                
                                # Check if we have enough lines left to match the context prefix
                                if search_index + len(context_prefix) <= len(original_lines):
                                    # Check if the context prefix matches at this position
                                    prefix_match = True
                                    for i, ctx_line in enumerate(context_prefix):
                                        if original_lines[search_index + i].rstrip('\n') != ctx_line:
                                            prefix_match = False
                                            break
                                    
                                    if prefix_match:
                                        print(f"Found matching context prefix at line {search_index + 1}")
                                        # Add lines up to the new match position
                                        while line_index < search_index:
                                            modified_lines.append(original_lines[line_index])
                                            line_index += 1
                                        match_found = True
                                        break
                        
                        # If no prefix match, try to match the full context
                        if not match_found:
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
                            # Try to find a partial match (at least 50% of context lines)
                            min_match_lines = max(1, len(context_lines) // 2)
                            best_match_score = 0
                            best_match_index = -1
                            
                            for offset in range(search_range):
                                search_index = current_line + offset
                                match_score = 0
                                
                                # Check how many context lines match at this position
                                for i, ctx_line in enumerate(context_lines):
                                    if search_index + i < len(original_lines) and original_lines[search_index + i].rstrip('\n') == ctx_line:
                                        match_score += 1
                                
                                if match_score > best_match_score:
                                    best_match_score = match_score
                                    best_match_index = search_index
                            
                            if best_match_score >= min_match_lines:
                                print(f"Found partial match ({best_match_score}/{len(context_lines)} lines) at line {best_match_index + 1}")
                                # Add lines up to the best match position
                                while line_index < best_match_index:
                                    modified_lines.append(original_lines[line_index])
                                    line_index += 1
                                match_found = True
                        
                        if not match_found:
                            print(f"WARNING: Could not find matching context in {source_file_path}")
                            print(f"Context lines: {context_lines[:3]}")
                            print("Continuing with best effort...")
                            # Instead of raising an error, we'll continue at the current position
                
                # Apply the hunk at the current position
                removed_count = 0
                for line in hunk:
                    if line.is_removed or line.is_context:
                        # Skip original lines (those that are removed)
                        if line_index < len(original_lines):
                            if line.is_removed:
                                removed_count += 1
                            line_index += 1
                    
                    if line.is_added or line.is_context:
                        # Add new lines (those that are added)
                        modified_lines.append(line.value)
                
                # If we didn't remove any lines but should have, try to advance the line_index
                # This handles cases where the context matched but the lines to remove didn't
                if removed_count == 0 and any(line.is_removed for line in hunk):
                    # Just advance by the number of lines that should have been removed
                    expected_removed = sum(1 for line in hunk if line.is_removed)
                    if line_index + expected_removed <= len(original_lines):
                        print(f"WARNING: Lines to remove don't match expected content in {source_file_path}")
                        print(f"Expected: {[l.value.rstrip('\\n') for l in hunk if l.is_removed]}")
                        print(f"Found: {[original_lines[line_index+i].rstrip('\\n') for i in range(expected_removed) if line_index+i < len(original_lines)]}")
                        print("Proceeding with caution...")
                        line_index += expected_removed

            # Append any remaining lines after the last hunk
            while line_index < len(original_lines):
                modified_lines.append(original_lines[line_index])
                line_index += 1

            # Check if this is a template file that might contain Jinja2 syntax
            is_template_file = target_file_path.endswith(('.yml', '.yaml', '.j2', '.html', '.md', '.jinja2'))
            
            # Additional check for files that might contain Jinja2 syntax based on content
            if not is_template_file and any('{%' in line or '{{' in line for line in modified_lines):
                is_template_file = True
                print(f"Detected Jinja2 syntax in {target_file_path}, treating as template file")
            
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
    
    # Check if problem_templates_dir exists
    if not os.path.exists(problem_templates_dir):
        print(f"Problem templates directory not found: {problem_templates_dir}")
        return
    
    for problem_domain in os.listdir(problem_templates_dir):
        src_dir = os.path.join(problem_templates_dir, problem_domain)

        if not os.path.isdir(src_dir):
            continue

        print(f"Processing problem domain: {problem_domain}")
        patch_count = 0
        success_count = 0
        
        for root, dirs, files in os.walk(src_dir):
            for file_name in files:
                if file_name.endswith(".diff"):
                    diff_file_path = os.path.join(root, file_name)
                    patch_count += 1

                    try:
                        with open(diff_file_path, "r") as diff_file:
                            patch_content = diff_file.read()
                            if not patch_content.strip():
                                print(f"Empty diff file: {diff_file_path}")
                                os.remove(diff_file_path)
                                continue
                                
                            patch_set = PatchSet(patch_content)
                        
                        apply_patch(patch_set, os.getcwd())
                        success_count += 1

                        # Remove the diff file after applying
                        os.remove(diff_file_path)
                    except Exception as e:
                        print(f"Patch failed for {diff_file_path}: {e}")
        
        print(f"Applied {success_count}/{patch_count} patches for {problem_domain}")


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
