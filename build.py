import os
import glob
import re
import yaml
import markdown
from jinja2 import Environment, FileSystemLoader
from markdown.preprocessors import Preprocessor
from markdown.inlinepatterns import InlineProcessor

# --- 1. Configuration ---
MD_FILES_DIR = '.'
TEMPLATE_DIR = 'templates'
OUTPUT_DIR = 'site'
EXCLUDE_FILES = ['README.md', 'GEMINI.md', 'CLAUDE.md', 'PERSONA.md']

# --- 2. Custom Markdown Extension for Wikilinks ---

WIKILINK_RE = r'\[\[([_a-zA-Z0-9-éàè ]+)(?:\|([^\]]+))?\]\]'

class WikilinkInlineProcessor(InlineProcessor):
    """
    Process wikilinks like [[page|text]] into <a href="page.html">text</a>.
    """
    def handleMatch(self, m, data):
        href = m.group(1).strip()
        text = m.group(2)
        if text is None:
            text = href

        # Convert markdown filename to html filename
        html_href = f"{href}.html"

        el = markdown.util.etree.Element('a')
        el.set('href', html_href)
        el.text = text
        return el, m.start(0), m.end(0)

class WikilinkExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.inlinePatterns.register(WikilinkInlineProcessor(WIKILINK_RE, md), 'wikilink', 175)

# --- 2b. Preprocessor for Obsidian callouts and .md links ---

class ObsidianPreprocessor(Preprocessor):
    """
    Convert Obsidian-specific syntax:
    - Callouts: > [!NOTE] -> Bootstrap alerts
    - .md links: [text](file.md) -> [text](file.html)
    """
    CALLOUT_TYPES = {
        'NOTE': ('info', 'bi-info-circle'),
        'TIP': ('success', 'bi-lightbulb'),
        'IMPORTANT': ('primary', 'bi-exclamation-circle'),
        'WARNING': ('warning', 'bi-exclamation-triangle'),
        'CAUTION': ('warning', 'bi-exclamation-triangle'),
        'DANGER': ('danger', 'bi-x-octagon'),
        'ABSTRACT': ('secondary', 'bi-file-text'),
        'SUMMARY': ('secondary', 'bi-file-text'),
        'INFO': ('info', 'bi-info-circle'),
        'TODO': ('info', 'bi-check-square'),
        'SUCCESS': ('success', 'bi-check-circle'),
        'QUESTION': ('warning', 'bi-question-circle'),
        'FAILURE': ('danger', 'bi-x-circle'),
        'BUG': ('danger', 'bi-bug'),
        'EXAMPLE': ('light', 'bi-code'),
        'QUOTE': ('light', 'bi-quote'),
    }

    def run(self, lines):
        new_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]

            # Check for callout start: > [!TYPE]
            callout_match = re.match(r'^>\s*\[!(\w+)\]\s*(.*)?$', line)
            if callout_match:
                callout_type = callout_match.group(1).upper()
                title = callout_match.group(2) or callout_type.capitalize()

                style, icon = self.CALLOUT_TYPES.get(callout_type, ('info', 'bi-info-circle'))

                # Collect callout content
                callout_content = []
                i += 1
                while i < len(lines) and lines[i].startswith('>'):
                    content_line = re.sub(r'^>\s?', '', lines[i])
                    callout_content.append(content_line)
                    i += 1

                # Generate Bootstrap alert HTML
                content_html = '<br>'.join(callout_content) if callout_content else ''
                new_lines.append(f'<div class="alert alert-{style}" role="alert">')
                new_lines.append(f'<i class="bi {icon} me-2"></i><strong>{title}</strong>')
                if content_html:
                    new_lines.append(f'<p class="mb-0 mt-2">{content_html}</p>')
                new_lines.append('</div>')
                new_lines.append('')
                continue

            # Convert .md links to .html links
            line = re.sub(r'\[([^\]]+)\]\(([^)]+)\.md(#[^)]*)?\)', r'[\1](\2.html\3)', line)

            new_lines.append(line)
            i += 1

        return new_lines

class ObsidianExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(ObsidianPreprocessor(md), 'obsidian', 30)

# --- 3. Main Build Script ---

def main():
    print("Starting build process...")

    # Create output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}")

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template('base.html')
    print("Loaded base template.")

    # Find all Markdown files, excluding specified ones
    all_md_files = glob.glob(os.path.join(MD_FILES_DIR, '*.md'))
    md_files_to_process = [f for f in all_md_files if os.path.basename(f) not in EXCLUDE_FILES]
    
    print(f"Found {len(md_files_to_process)} markdown files to process...")

    # Process each Markdown file
    for md_file in md_files_to_process:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content_raw = f.read()

            # Separate frontmatter from content
            parts = content_raw.split('---')
            if len(parts) >= 3:
                frontmatter_raw = parts[1]
                md_content = '---'.join(parts[2:])
                
                frontmatter = yaml.safe_load(frontmatter_raw)
                title = frontmatter.get('title', 'No Title')
            else:
                # Handle files with no frontmatter
                md_content = content_raw
                title = os.path.splitext(os.path.basename(md_file))[0]
                frontmatter = {}

            # Convert Markdown content to HTML
            md = markdown.Markdown(extensions=[
                'fenced_code',
                'tables',
                'attr_list',
                WikilinkExtension(),
                ObsidianExtension()
            ])
            html_content = md.convert(md_content)

            # Render the template
            final_html = template.render(title=title, content=html_content)

            # Write the final HTML file
            base_filename = os.path.splitext(os.path.basename(md_file))[0]
            output_path = os.path.join(OUTPUT_DIR, f"{base_filename}.html")
            
            with open(output_path, 'w', encoding='utf-8') as f_out:
                f_out.write(final_html)
            
            print(f"  -> Successfully generated {output_path}")

        except Exception as e:
            print(f"  -> ERROR processing {md_file}: {e}")

    print("Build process finished.")

if __name__ == '__main__':
    main()
