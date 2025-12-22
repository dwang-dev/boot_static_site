import unittest

from htmlnode import LeafNode

props = {
  "href": "https://www.google.com",
  "target": "_blank",
}

class TestLeafNode(unittest.TestCase):
  def test_props_to_html(self):
    node = LeafNode("p", "Hello world", props=props)
    self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
  
  def test_no_value_raises_err(self):
    with self.assertRaises(ValueError):
      node = LeafNode("p", "")

  def test_to_html_p(self):
    node = LeafNode("p", "Hello world", props)
    self.assertEqual(node.to_html(), f"<p href=\"https://www.google.com\" target=\"_blank\">Hello world</p>")

  def test_to_html_div(self):
    node = LeafNode("div", "Hello world", props)
    self.assertEqual(node.to_html(), f"<div href=\"https://www.google.com\" target=\"_blank\">Hello world</div>")

  def test_to_html_a(self):
    node = LeafNode("a", "Hello world", props)
    self.assertEqual(node.to_html(), f"<a href=\"https://www.google.com\" target=\"_blank\">Hello world</a>")
    
if __name__ == "__main__":
  unittest.main() 