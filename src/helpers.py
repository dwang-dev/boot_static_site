from textnode import TextNode, TextType
from htmlnode import LeafNode
import re

def text_node_to_html_node(text_node: TextNode):
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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []
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

def extract_markdown_images(text):
  return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
  return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
          
def split_nodes_image(old_nodes):
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

def split_nodes_link(old_nodes):
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

def text_to_textnodes(text):
  og_textnode = TextNode(text, TextType.TEXT)
  nodes = split_nodes_delimiter([og_textnode], "`", TextType.CODE)
  nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
  nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
  nodes = split_nodes_link(nodes)
  nodes = split_nodes_image(nodes)
  return nodes