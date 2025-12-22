from textnode import TextNode, TextType
from htmlnode import LeafNode

def text_node_to_html_node(text_node):
  match TextType.text_type:
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
      return LeafNode("img", "", {"src": f"text_node.url", "alt": "alt text"})
    case _:
      raise Exception("Invalid text type")
    
    
print("hello world")
node = TextNode("123", "URL", "https://www.boot.dev")
print(node)