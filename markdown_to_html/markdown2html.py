#!/usr/bin/python3
"""
markdown2html.py - A script to convert Markdown to HTML.
"""

import sys
import os
import re
import hashlib

def convert_markdown_to_html(markdown_file, html_file):
    """
    Converts Markdown content to HTML and writes it to the output file.
    Supports heading levels 1 to 6, unordered lists, ordered lists, paragraphs, bold/emphasis, MD5 conversion, and character removal.
    """
    try:
        with open(markdown_file, 'r') as md_file:
            html_content = ""
            in_ul_list = False  # Track if we're inside an unordered list
            in_ol_list = False  # Track if we're inside an ordered list
            paragraph_lines = []  # Stores lines of text for a paragraph block

            for line in md_file:
                line = line.rstrip()

                # Heading match for levels 1 to 6
                heading_match = re.match(r"^(#{1,6}) (.+)", line)
                # Unordered list match
                ul_list_item_match = re.match(r"^- (.+)", line)
                # Ordered list match
                ol_list_item_match = re.match(r"^\* (.+)", line)

                # Bold and Emphasis matches
                bold_match = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
                emphasis_match = re.sub(r"__(.+?)__", r"<em>\1</em>", bold_match)

                # Handle MD5 for [[...]]
                md5_match = re.sub(r"\[\[(.*?)\]\]", lambda m: hashlib.md5(m.group(1).encode()).hexdigest(), emphasis_match)
                
                # Handle character removal for ((...))
                char_remove_match = re.sub(r"\(\((.*?)\)\)", lambda m: m.group(1).replace('c', '').replace('C', ''), md5_match)

                if heading_match:
                    # Close any open lists or paragraph blocks before starting a new heading
                    if in_ul_list:
                        html_content += "</ul>\n"
                        in_ul_list = False
                    if in_ol_list:
                        html_content += "</ol>\n"
                        in_ol_list = False
                    if paragraph_lines:
                        html_content += "<p>\n" + "<br/>\n".join(paragraph_lines) + "\n</p>\n"
                        paragraph_lines = []

                    # Process heading
                    heading_level = len(heading_match.group(1))
                    heading_text = heading_match.group(2)
                    html_content += f"<h{heading_level}>{heading_text}</h{heading_level}>\n"

                elif ul_list_item_match:
                    # Close paragraph blocks or ordered lists before starting an unordered list
                    if in_ol_list:
                        html_content += "</ol>\n"
                        in_ol_list = False
                    if paragraph_lines:
                        html_content += "<p>\n" + "<br/>\n".join(paragraph_lines) + "\n</p>\n"
                        paragraph_lines = []
                    if not in_ul_list:
                        html_content += "<ul>\n"
                        in_ul_list = True

                    # Process unordered list item
                    list_item_text = ul_list_item_match.group(1)
                    html_content += f"    <li>{char_remove_match}</li>\n"

                elif ol_list_item_match:
                    # Close paragraph blocks or unordered lists before starting an ordered list
                    if in_ul_list:
                        html_content += "</ul>\n"
                        in_ul_list = False
                    if paragraph_lines:
                        html_content += "<p>\n" + "<br/>\n".join(paragraph_lines) + "\n</p>\n"
                        paragraph_lines = []
                    if not in_ol_list:
                        html_content += "<ol>\n"
                        in_ol_list = True

                    # Process ordered list item
                    list_item_text = ol_list_item_match.group(1)
                    html_content += f"    <li>{char_remove_match}</li>\n"

                elif line == "":
                    # End of paragraph block; close and output it
                    if paragraph_lines:
                        html_content += "<p>\n" + "<br/>\n".join(paragraph_lines) + "\n</p>\n"
                        paragraph_lines = []
                else:
                    # Collect lines for a paragraph
                    if in_ul_list:
                        html_content += "</ul>\n"
                        in_ul_list = False
                    if in_ol_list:
                        html_content += "</ol>\n"
                        in_ol_list = False
                    paragraph_lines.append(char_remove_match)

            # Close any remaining open tags at the end of the document
            if in_ul_list:
                html_content += "</ul>\n"
            if in_ol_list:
                html_content += "</ol>\n"
            if paragraph_lines:
                html_content += "<p>\n" + "<br/>\n".join(paragraph_lines) + "\n</p>\n"

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
