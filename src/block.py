from textnode import TextNode, text_node_to_html_node
from htmlnode import LeafNode, HTMLNode, ParentNode
from inline import text_to_textnodes
import re
from enum import Enum

class BlockType(Enum):
  PARAGRAPH = 1
  HEADING = 2
  CODE = 3
  QUOTE = 4
  UNORDERED_LIST = 5
  ORDERED_LIST = 6

def markdown_to_blocks(markdown: str) -> list[str]:
  """
  Returns the blocks of a markdown string.

  Params:
    - markdown (str): Markdown string.

  Returns:
    - list[str]: List of strings. Each string is a block of the markdown.    

  """
  blocks: list[str] = markdown.split("\n\n")
  for i in range(len(blocks)):
    blocks[i] = blocks[i].strip(" \n")
  return [b for b in blocks if b != ""]

def block_to_blocktype(text: str) -> BlockType:
  """
  Returns the blocktype of a markdown block.

  Params:
    - text (str): The markdown block.

  Returns:
    - BlockType: BlockType enum type.
  """
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
  elif re.search(r"^(\d+)\. .*$", lines[0], re.DOTALL):
    blocktype = BlockType.ORDERED_LIST
    pattern = r"^(\d+)\. .*$"
  else:
    return BlockType.PARAGRAPH
  for l in lines:
    match = re.search(pattern, l, re.DOTALL)
    if not match:
      return BlockType.PARAGRAPH
  return blocktype

def text_to_htmlnode(text:str, tag:str) -> ParentNode:
  """
  Given a markdown block and html tag, returns a ParentNode with the specified tag 
  and with children of type HTMLNode.
  
  Params:
    - text (str): Markdown block.
    - tag (str): HTML tag of the ParentNode.

  Returns:
    - ParentNode: ParentNode to be returned.
  """
  textnodes:list[TextNode] = text_to_textnodes(text)
  htmlnodes:list[HTMLNode] = [text_node_to_html_node(node) for node in textnodes]
  return ParentNode(tag=tag, children=htmlnodes, props=None)

def markdown_to_html_node(markdown:str) -> ParentNode:
  """
  Converts the string representation of a markdown doc into a single ParentNode object
  whose children recursively describe the layout of the document.
  
  Params:
    - markdown (str): String representation of a markdown document.
  
  Returns:
    - ParentNode:
  """
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