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
    Supports heading levels 1 to 6, unordered lists, and ordered lists.
    """
    try:
        with open(markdown_file, 'r') as md_file:
            html_content = ""
            in_ul_list = False  # Track if we're inside an unordered list
            in_ol_list = False  # Track if we're inside an ordered list

            for line in md_file:
                # Heading match for levels 1 to 6
                heading_match = re.match(r"^(#{1,6}) (.+)", line)
                # Unordered list match
                ul_list_item_match = re.match(r"^- (.+)", line)
                # Ordered list match
                ol_list_item_match = re.match(r"^\* (.+)", line)

                if heading_match:
                    if in_ul_list:
                        html_content += "</ul>\n"
                        in_ul_list = False
                    if in_ol_list:
                        html_content += "</ol>\n"
                        in_ol_list = False
                    heading_level = len(heading_match.group(1))
                    heading_text = heading_match.group(2)
                    html_content += f"<h{heading_level}>{heading_text}</h{heading_level}>\n"

                elif ul_list_item_match:
                    if in_ol_list:
                        html_content += "</ol>\n"
                        in_ol_list = False
                    if not in_ul_list:
                        html_content += "<ul>\n"
                        in_ul_list = True
                    list_item_text = ul_list_item_match.group(1)
                    html_content += f"    <li>{list_item_text}</li>\n"

                elif ol_list_item_match:
                    if in_ul_list:
                        html_content += "</ul>\n"
                        in_ul_list = False
                    if not in_ol_list:
                        html_content += "<ol>\n"
                        in_ol_list = True
                    list_item_text = ol_list_item_match.group(1)
                    html_content += f"    <li>{list_item_text}</li>\n"

                else:
                    if in_ul_list:
                        html_content += "</ul>\n"
                        in_ul_list = False
                    if in_ol_list:
                        html_content += "</ol>\n"
                        in_ol_list = False
                    html_content += f"<p>{line.strip()}</p>\n"
            
            if in_ul_list:
                html_content += "</ul>\n"
            if in_ol_list:
                html_content += "</ol>\n"

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
