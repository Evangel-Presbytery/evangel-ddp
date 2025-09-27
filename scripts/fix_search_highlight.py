#!/usr/bin/env python3
import os

# -------------------------
# Configuration
# -------------------------
output_dir = "_book"  # adjust if your output folder differs

# -------------------------
# Main
# -------------------------
def main():
    print("Applying search highlight fix...")
    search_js_path = os.path.join(output_dir, "site_libs", "quarto-search", "quarto-search.js")

    if os.path.exists(search_js_path):
        with open(search_js_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Comment out the event listeners that clear the highlighting
        content = content.replace(
            'window.addEventListener("quarto-hrChanged", resetFn);',
            '// window.addEventListener("quarto-hrChanged", resetFn);'
        )
        content = content.replace(
            'window.addEventListener("quarto-sectionChanged", resetFn);',
            '// window.addEventListener("quarto-sectionChanged", resetFn);'
        )

        with open(search_js_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print("Search highlight fix applied.")
    else:
        print(f"WARNING: {search_js_path} not found. Search highlight fix not applied.")

if __name__ == "__main__":
    main()
