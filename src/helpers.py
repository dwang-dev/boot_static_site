from textnode import TextNode, TextType
from htmlnode import LeafNode, HTMLNode, ParentNode
import re
from enum import Enum
import shutil
import os

class BlockType(Enum):
  PARAGRAPH = 1
  HEADING = 2
  CODE = 3
  QUOTE = 4
  UNORDERED_LIST = 5
  ORDERED_LIST = 6

def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
  match text_node.text_type:
    case TextType.TEXT:
      return LeafNode(None, text_node.text)
    case TextType.BOLD:
      return LeafNode("b", text_node.text)
    case TextType.ITALIC:
      return LeafNode("i", text_node.text)
    case TextType.CODE:
      return LeafNode("code", text_node.text)
    case TextType.LINK:
      return LeafNode("a", text_node.text, {"href": f"{text_node.url}"})
    case TextType.IMAGE:
      return LeafNode("img", "", {"src": f"{text_node.url}", "alt": "alt text"})
    case _:
      raise Exception("Invalid text type")

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
  new_nodes: list[TextNode] = []
  for node in old_nodes:
    if node.text_type != TextType.TEXT:
      new_nodes.append(node)
      continue
    splits = node.text.split(delimiter)
    # Check if delimiter count is even (pairs)
    if len(splits) % 2 == 0:
      raise Exception("Invalid markdown syntax. Must have closing delimiter.")
    # Process all splits in pairs
    for i in range(len(splits)):
      if i % 2 == 0:  # Plain text
        if splits[i]:  # Only add non-empty text
          new_nodes.append(TextNode(splits[i], TextType.TEXT))
      else:  # Delimited text
        new_nodes.append(TextNode(splits[i], text_type))
  return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
  return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
  return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
          
def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
  new_nodes = []
  for old_node in old_nodes:
    md_imgs = extract_markdown_images(old_node.text)
    if len(md_imgs) == 0:
      new_nodes.append(old_node)
      continue
    unprocessed_text = old_node.text
    for alt_text, link in md_imgs:
      # List of size 2. 1st elem is text before markdown. 2nd is text after markdown
      # (remaining unprocessed text).
      parts = unprocessed_text.split(f"![{alt_text}]({link})")
      if parts[0] != "":
        new_nodes.append(TextNode(parts[0], TextType.TEXT))
      new_nodes.append(TextNode(alt_text, TextType.IMAGE, link))
      unprocessed_text = parts[1]
    if unprocessed_text != "":
      new_nodes.append(TextNode(unprocessed_text, TextType.TEXT))
  return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
  new_nodes = []
  for old_node in old_nodes:
    md_links = extract_markdown_links(old_node.text)
    if len(md_links) == 0:
      new_nodes.append(old_node)
      continue
    unprocessed_text = old_node.text
    for link_text, link in md_links:
      # List of size 2. 1st elem is text before markdown. 2nd is text after markdown
      # (remaining unprocessed text).
      parts = unprocessed_text.split(f"[{link_text}]({link})")
      if parts[0] != "":
        new_nodes.append(TextNode(parts[0], TextType.TEXT))
      new_nodes.append(TextNode(link_text, TextType.LINK, link))
      unprocessed_text = parts[1]
    if unprocessed_text != "": # Handle remaining text in string.
      new_nodes.append(TextNode(unprocessed_text, TextType.TEXT))
  return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
  og_textnode = TextNode(text, TextType.TEXT)
  nodes = split_nodes_delimiter([og_textnode], "`", TextType.CODE)
  nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
  nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
  nodes = split_nodes_link(nodes)
  nodes = split_nodes_image(nodes)
  return nodes

def markdown_to_blocks(markdown: str) -> list[str]:
  blocks: list[str] = markdown.split("\n\n")
  for i in range(len(blocks)):
    blocks[i] = blocks[i].strip(" \n")
  return [b for b in blocks if b != ""]

def block_to_blocktype(text: str) -> BlockType:
  if re.search(r"^#{0,6} .*$", text, re.DOTALL):
    return BlockType.HEADING
  elif re.search(r"^`{3}.*`{3}$", text, re.DOTALL):
    return BlockType.CODE
  blocktype: BlockType = None
  pattern: str = ""
  lines: list[str] = text.split("\n")
  if re.search(r"^>.*$", lines[0], re.DOTALL):
    blocktype = BlockType.QUOTE
    pattern = r"^>.*$"
  elif re.search(r"^- .*$", lines[0], re.DOTALL):
    blocktype = BlockType.UNORDERED_LIST
    pattern = r"^- .*$"
  elif m := re.search(r"^(\d+)\. .*$", lines[0], re.DOTALL):
    blocktype = BlockType.ORDERED_LIST
    pattern = r"^(\d+)\. .*$"
  else:
    return BlockType.PARAGRAPH
  for l in lines:
    match = re.search(pattern, l, re.DOTALL)
    if not match:
      return BlockType.PARAGRAPH
  return blocktype

def text_to_htmlnode(text:str, tag:str) -> list[HTMLNode]:
  textnodes:list[TextNode] = text_to_textnodes(text)
  htmlnodes:list[HTMLNode] = [text_node_to_html_node(node) for node in textnodes]
  return ParentNode(tag=tag, children=htmlnodes, props=None)

def markdown_to_html_node(markdown:str) -> HTMLNode:
  root = ParentNode("div", children=[])
  blocks = markdown_to_blocks(markdown)
  for block in blocks:
    blocktype: BlockType = block_to_blocktype(block)
    match blocktype:
      case BlockType.PARAGRAPH:
        root.children.append(text_to_htmlnode(text=block, tag="p"))
      case BlockType.HEADING:
        match = re.search(r"^(#{0,6}) (.*)$", block, re.DOTALL)
        root.children.append(text_to_htmlnode(text=match.group(2), tag=f"h{len(match.group(1))}"))
      case BlockType.CODE:
        match = re.search(r"^`{3}(.*)`{3}$", block, re.DOTALL)
        root.children.append(ParentNode("pre", children=[LeafNode("code", value=match.group(1))]))
      case BlockType.QUOTE:
        root.children.append(text_to_htmlnode(text=block[2:], tag="blockquote"))
      case BlockType.UNORDERED_LIST:
        ul_htmlnode = ParentNode(tag="ul", children=[])
        for line in block.split("\n"):
          line_match = re.search(r"^- (.*)$", line, re.DOTALL)
          item_content = line_match.group(1).strip()
          ul_htmlnode.children.append(text_to_htmlnode(text=item_content, tag="li"))
        root.children.append(ul_htmlnode)
      case BlockType.ORDERED_LIST:
        ol_htmlnode:ParentNode = ParentNode(tag="ol", children=[])
        for line in block.split("\n"):
          line_match:re.Match = re.search(r"^(\d+)\. (.*)$", line, re.DOTALL)
          item_content:str = line_match.group(2).strip()
          ol_htmlnode.children.append(text_to_htmlnode(text=item_content, tag="li"))
        root.children.append(ol_htmlnode)
  return root

# def clear_dir(dir_path: str) -> None:
#   for c in os.listdir(dir_path):
#     new_path = os.path.join(dir_path, c)
#     if os.path.isfile(new_path):
#       os.remove(new_path)
#     elif os.path.isdir(new_path):
#       shutil.rmtree(new_path)

def copy_directory_contents_recursive(source: str, dest: str) -> None:
  os.makedirs(dest, exist_ok=True)
  for c in os.listdir(source):
    src_path = os.path.join(source, c)
    dest_path = os.path.join(dest, c)
    if os.path.isfile(src_path):
      shutil.copy2(src_path, dest_path)
    else:
      copy_directory_contents_recursive(src_path, dest_path)

def extract_title(markdown:str) -> str:
  lines = markdown.split('\n')
  for line in lines:
    match = re.search(r"^#{1} (.*)$", line)
    if match:
      return match.group(1).strip()
  return None

def generate_page(from_path:str, template_path:str, dest_path:str, basepath:str) -> None:
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
