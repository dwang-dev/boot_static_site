from textnode import TextNode, TextType
from htmlnode import LeafNode
import helpers

type = helpers.block_to_blocktype("- Item1\n- Item2\n- Item")
print(type)