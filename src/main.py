from textnode import TextNode, TextType
from htmlnode import LeafNode
import helpers
    
node = TextNode("`code block` word", TextType.TEXT)
new_nodes = helpers.split_nodes_delimiter([node], "`", TextType.CODE)
print(new_nodes)