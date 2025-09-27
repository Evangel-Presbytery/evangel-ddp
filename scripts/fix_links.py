#!/usr/bin/env python3
import os
import re

# -------------------------
# Configuration
# -------------------------
output_dir = "_book"  # adjust if your output folder differs

# Match anchors like <span id="p38.10"></span> or <h2 id="foo">
anchor_pattern = re.compile(r'id="([a-zA-Z0-9\\.\\-]+)"')

# Match internal links like <a href="#p38.10">...</a>
link_pattern = re.compile(r'<a\\s+href="#([a-zA-Z0-9\\.\\-]+)"')

# -------------------------
# Step 1: Collect all anchors per HTML file
# -------------------------
def collect_anchors(root_dir):
    file_anchors = {}      # filename -> set of anchors
    anchor_to_file = {}    # anchor -> filename
    for root, _, files in os.walk(root_dir):
        for file in files:
            if not file.endswith(".html"):
                continue
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                anchors = set(anchor_pattern.findall(content))
                if anchors:
                    file_anchors[file] = anchors
                    for a in anchors:
                        anchor_to_file[a] = file
    print(f"Collected {len(anchor_to_file)} anchors across {len(file_anchors)} files.")
    return file_anchors, anchor_to_file

# -------------------------
# Step 2: Fix cross-file links & warn on missing anchors
# -------------------------
def fix_links(root_dir, file_anchors, anchor_to_file):
    for root, _, files in os.walk(root_dir):
        for file in files:
            if not file.endswith(".html"):
                continue
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            def replacer(match):
                anchor = match.group(1)
                # If anchor is in this same file, leave unchanged
                if file in file_anchors and anchor in file_anchors[file]:
                    return match.group(0)
                # If anchor exists in another file, rewrite link
                target_file = anchor_to_file.get(anchor)
                if target_file:
                    return f'<a href="./{target_file}#{anchor}"'
                # Otherwise: warn and leave unchanged
                print(f"WARNING: Missing anchor '{anchor}' referenced in {file}")
                return match.group(0)

            updated_content = link_pattern.sub(replacer, content)

            if updated_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)

# -------------------------
# Main
# -------------------------
def main():
    print(f"Scanning HTML files in {output_dir}...")
    file_anchors, anchor_to_file = collect_anchors(output_dir)
    fix_links(output_dir, file_anchors, anchor_to_file)
    print("Finished fixing cross-file anchor links.")

if __name__ == "__main__":
    main()
