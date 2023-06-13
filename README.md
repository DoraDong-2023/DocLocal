# DocLocal
A demo GUI that integrating GitHub documents to local.

# Features
TODO: add figure

# Installation
`pip install -r requirements.txt`

# Usage
`python GUI.py`

# Update&TODO
TODO:
Automatically switch between web search and Markdown reader.
Automatically determine input and decide whether to download or perform a Google search, etc.
https://github.com/facebookresearch/segment-anything does not allow requests and throws an error.
The loading process cannot be displayed until it finishes, and only the final result is shown.
Unable to automatically update the path display.
Need to add equation analysis.
Add a tag.
Need to add documentation from other websites or wikis (what document parsing is supported).
Need to add a list of commonly used websites and cheatsheets.
Need to display using Github icons/other icons.

230613 update:
Support for .rst and .md files
Use original filenames instead of readme1234. Add renaming function for duplicate names.
Address Issue: Chinese names cannot be displayed. Use quote to address it.
Address Issue: Unable to update the second link.

230612 achieved:
Direct download in the box
Browser loading
Integrated page for Markdown/Web Search
