import os
import glob
import re

tpl_dir = 'store/templates/store/blocks'
files = glob.glob(f"{tpl_dir}/*.html")

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    # If already processed, skip
    if 'data-block-id="{{ block.id }}"' in content:
        continue

    # Add data-block-id and an opacity class if block is inactive
    # Also add a minimum height if empty
    
    # We find the first <div or <section and inject the attributes
    def replacer(match):
        tag = match.group(0)
        # Add attributes
        classes = ""
        if 'class="' in tag:
            # We will append dynamic classes later, for now just add inline style and data-block-id
            return tag.replace('class="', 'data-block-id="{{ block.id }}" {% if request.GET.preview and not block.is_active %}style="opacity: 0.4; outline: 2px dashed red;"{% endif %} class="')
        else:
            # If no class attr, just inject after tag name
            tag_name = tag.split()[0]
            return tag.replace(tag_name, tag_name + ' data-block-id="{{ block.id }}" {% if request.GET.preview and not block.is_active %}style="opacity: 0.4; outline: 2px dashed red;"{% endif %}')
            
    content = re.sub(r'<([a-zA-Z0-9]+)[^>]*>', replacer, content, count=1)
    
    with open(filepath, 'w') as f:
        f.write(content)
        
    print(f"Processed {filepath}")

