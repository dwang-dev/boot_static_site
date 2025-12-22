import unittest

from htmlnode import ParentNode, LeafNode

props = {
  "href": "https://www.google.com",
  "target": "_blank",
}

class TestParentNode(unittest.TestCase):
  def test_parent_node_no_children(self):
    node = ParentNode("div", [], props)
    node.to_html()
    self.assertEqual(node.to_html(), "<div href=\"https://www.google.com\" target=\"_blank\"></div>")

  def test_parent_node_with_children(self):
    node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
)


if __name__ == "__main__":
  unittest.main() 