#!/usr/bin/python3
"""
markdown2html.py - A script to convert Markdown to HTML.
"""

import sys
import os

def convert_markdown_to_html(markdown_file, html_file):
    """
    Converts Markdown content to simple HTML and writes it to the output file.
    For simplicity, this script only handles basic text conversion.
    """
    try:
        with open(markdown_file, 'r') as md_file:
            content = md_file.read()
            
            # Simple conversion logic (can be enhanced to handle Markdown syntax properly)
            html_content = "<html><body><p>" + content.replace('\n', '<br>\n') + "</p></body></html>"
            
            with open(html_file, 'w') as output_file:
                output_file.write(html_content)

    except Exception as e:
        sys.stderr.write(f"Error: {str(e)}\n")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    if not os.path.exists(markdown_file):
        sys.stderr.write(f"Missing {markdown_file}\n")
        sys.exit(1)

    convert_markdown_to_html(markdown_file, html_file)
    sys.exit(0)
