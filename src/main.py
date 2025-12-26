from src.textnode import TextNode, TextType
from src.htmlnode import LeafNode
from src.helpers import markdown_to_html_node

md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
node = markdown_to_html_node(md)
html = node.to_html()
print(html)