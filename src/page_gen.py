import os
import shutil
import re
from block import markdown_to_html_node

def copy_directory_contents_recursive(source: str, dest: str) -> None:
  """
  Recursively copies all files and subdirectories from one directory to another.

	Arguments:
    - source: Source directory to copy files from.
    - dest: Destination directory to copies files to. 
  
  Returns: 
    - None
  """
  os.makedirs(dest, exist_ok=True)
  for c in os.listdir(source):
    src_path = os.path.join(source, c)
    dest_path = os.path.join(dest, c)
    print(f" * {src_path} -> {dest_path}")
    if os.path.isfile(src_path):
      shutil.copy2(src_path, dest_path)
    else:
      copy_directory_contents_recursive(src_path, dest_path)

def extract_title(markdown:str) -> str:
  """
  Extracts the title (first Header 1 item) from a markdown document.

  Arguments:
    - markdown: String representation of markdown document.

  Returns:
    - str: Markdown document title.
  """
  lines = markdown.split('\n')
  for line in lines:
    match = re.search(r"^#{1} (.*)$", line)
    if match:
      return match.group(1).strip()
  return None

def generate_page(from_path:str, template_path:str, dest_path:str, basepath:str) -> None:
  """
  Dynamically generates a HTML file from a markdown file.

  Arguments:
    - from_path: Path of source markdown file.
    - template_path: Path of a template HTML file to generate HTML file.
    - dest_path: New path of HTML file to create.
    - basepath: Basepath of the HTML site.
  
  Returns:
    - None.
  """
  print(f"Generate page from {from_path} to {dest_path} using {template_path}.")
  with open(template_path, "r") as file:
    template_contents:str = file.read()
  with open(from_path, "r") as file:
    md:str = file.read()
  html_content:str = markdown_to_html_node(md).to_html()
  title:str = extract_title(md)
  html_file_content:str = template_contents.replace("{{ Title }}", title)
  html_file_content = html_file_content.replace("{{ Content }}", html_content)
  html_file_content = html_file_content.replace("href=\"/", f"href=\"{basepath}")
  html_file_content = html_file_content.replace("src=\"/", f"src=\"{basepath}")
  with open(dest_path, "w") as file:
    file.write(html_file_content)

def generate_page_recursive(from_path:str, template_path:str, dest_path:str, basepath:str) -> None:
  for dir_content in os.listdir(from_path):
    dir_content_path = os.path.join(from_path, dir_content)
    if os.path.isfile(dir_content_path):
      match = re.search(pattern=r"^(.*)\.md$", string=dir_content)
      new_dest_path = os.path.join(dest_path, f"{match.group(1)}.html")
      generate_page(dir_content_path, template_path, new_dest_path, basepath)
    else:
      new_dest_path = os.path.join(dest_path, dir_content)
      os.makedirs(new_dest_path, exist_ok=True)
      generate_page_recursive(dir_content_path, template_path, new_dest_path, basepath)
