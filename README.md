# DocLocal
A demo GUI that integrating GitHub documents to local.

# Features
TODO: add figure

# Installation
```pip install PyQt5 markdown requests```

# Usage
```python GUI.py```

# Update&TODO
TODO:
1. Git module is needed for parsing and generating subdirectories.  
2. Other website's documentation and wikis need to be added (which document formats are supported for parsing?).  
3. A list of commonly used websites and a cheatsheet need to be added.  
4. Display using GitHub icon/other icons as required.  
5. Support for DIY tag.   

230613 update:
Parse for supporting Google/DuckDuckgo/Bing search
Support for .rst and .md files.   
Use original filenames instead of readme1234. Add renaming function for duplicate names.  
Address Issue: Chinese names cannot be displayed. Use quote to address it.  
Address Issue: Unable to update the second link.  
Automatically switch to the web search tab after clicking.  
Automatically open the Markdown file after successful GitHub download and update the left directory bar.  
Cancel the main code directory on the left and only keep the subdirectories.  
Some websites are timing out, e.g. https://github.com/facebookresearch/segment-anything.  
Display a loading progress bar during the loading process.  

230612 achieved:
Direct download in the box.   
Browser loading.   
Integrated page for Markdown/Web Search.   
