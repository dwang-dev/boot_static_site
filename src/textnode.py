from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text: str, text_type: TextType, url:str=None):
        self.text = text
        if not isinstance(text_type, TextType):
            raise Exception("Invalid text type")
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, node) -> bool:
        return self.text == node.text and self.text_type == node.text_type and self.url == node.url
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
def text_node_to_html_node(text_node: TextNode) -> LeafNode:
  """
  Returns a LeafNode object from a TextNode object.
  
  Params:
    - text_node (TextNode): TextNode object.

  Returns:
    - LeafNode: A LeafNode object.
  """
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