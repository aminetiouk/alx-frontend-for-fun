#!/usr/bin/python3
"""
markdown2html.py - A script to convert Markdown to HTML.
"""

import sys
import os
import re

def convert_markdown_to_html(markdown_file, html_file):
    """
    Converts Markdown content to HTML and writes it to the output file.
    Supports heading levels 1 to 6.
    """
    try:
        with open(markdown_file, 'r') as md_file:
            html_content = ""
            
            for line in md_file:
                heading_match = re.match(r"^(#{1,6}) (.+)", line)
                
                if heading_match:
                    heading_level = len(heading_match.group(1))
                    heading_text = heading_match.group(2)
                    html_content += f"<h{heading_level}>{heading_text}</h{heading_level}>\n"
                else:
                    # If not a heading, just wrap line in <p> tags
                    html_content += f"<p>{line.strip()}</p>\n"
            
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
