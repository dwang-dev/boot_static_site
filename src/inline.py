from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
  """
  Given a delimiter and a list of nodes containing text content, splits the list 
  of nodes into more TextNodes. Only nodes of text type 'TextType.TEXT' will be split
  in the list of old nodes. The text content of each node must have each
  delimiter be 'closed' (even number of delimiters). The TextNode in between
  the delimiters will be of type text_type whilst the TextNodes outside
  will be of type TextType.TEXT.
  E.g. "This is text with a `code block` word" ->     
  [
      TextNode("This is text with a ", TextType.TEXT),
      TextNode("code block", TextType.CODE),
      TextNode(" word", TextType.TEXT),
  ]
  Params:
    - old_nodes: List of nodes containing the text content to split.
    - delimiter: Delimiter to split on.
    - text_type: Text type for the node in between the delimiters.
  
  Returns:
    - list[TextNode]
  """
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
  """
  Helper function to extract the markdown images from an inline markdown string.
  """
  return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
  """
  Helper function to extract the markdown links from an inline markdown string.
  """
  return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
          
def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
  """
  Splits a list of nodes potentially containing TextNodes with text_type "IMAGE"
  into more TextNodes of type LINK and TEXT.

  Arguments:
    - old_nodes: List of TextNodes containing the content to split.
  
  Returns:
    - list[TextNode]
  """
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
  """
  Splits a list of nodes potentially containing TextNodes with text_type "LINK"
  into more TextNodes of type LINK and TEXT.

  Arguments:
    - old_nodes: List of TextNodes containing the content to split.
  
  Returns:
    - list[TextNode]
  """
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
  """
  Given inline markdown. Returns a list of TextNodes.

  Params:
    - text (str): The inline text to convert.
  
  Returns:
    - list[TextNode]: A list of TextNodes representing the inline markdown.
  """
  og_textnode = TextNode(text, TextType.TEXT)
  nodes = split_nodes_delimiter([og_textnode], "`", TextType.CODE)
  nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
  nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
  nodes = split_nodes_link(nodes)
  nodes = split_nodes_image(nodes)
  return nodes