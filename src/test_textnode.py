import unittest

from textnode import TextNode, TextType
from block import text_node_to_html_node

class TestTextNode(unittest.TestCase):
  ###############################################
  ############### Text Node tests ###############
  ###############################################
  # Equality checks
  def test_eq_no_url(self):
      node = TextNode("This is a text node", TextType.BOLD)
      node2 = TextNode("This is a text node", TextType.BOLD)
      assert(node == node2)

  def test_eq_with_url(self):
      node = TextNode("This is a text node", TextType.BOLD, "Helloworld.com")
      node2 = TextNode("This is a text node", TextType.BOLD, "Helloworld.com")
      assert(node == node2)

  # Inequality checks.
  def test_text_neq(self):
      node = TextNode("This is a text nod", TextType.BOLD)
      node2 = TextNode("This is a text node", TextType.BOLD)
      assert(node != node2)

  def test_type_neq(self):
      node = TextNode("This is a text node", TextType.TEXT)
      node2 = TextNode("This is a text node", TextType.BOLD)
      assert(node != node2)

  def test_url_neq(self):
      node = TextNode("This is a text node", TextType.BOLD, "Heyworld.net")
      node2 = TextNode("This is a text node", TextType.BOLD, "Helloworld.com")
      assert(node != node2)

  # Invalid type check
  def test_invalid_type(self):
      with self.assertRaises(Exception):
        TextNode("This is a text node", "Invalid type")

  ###############################################################
  ############### Textnode to HTMLnode Tests ####################
  ###############################################################

  def test_textnode_to_htmlnode_text(self):
    node = TextNode("Hello world", TextType.TEXT)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, None)
    self.assertEqual(html_node.value, "Hello world")

  def test_textnode_to_htmlnode_bold(self):
    node = TextNode("Hello world", TextType.BOLD)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "b")
    self.assertEqual(html_node.value, "Hello world")

  def test_textnode_to_htmlnode_italic(self):
    node = TextNode("Hello world", TextType.ITALIC)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "i")
    self.assertEqual(html_node.value, "Hello world")

  def test_textnode_to_htmlnode_code(self):
    node = TextNode("Hello world", TextType.CODE, "dummylink.com")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "code")
    self.assertEqual(html_node.value, "Hello world")

  def test_textnode_to_htmlnode_link(self):
    node = TextNode("Hello world", TextType.LINK, "dummylink.com")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "a")
    self.assertEqual(html_node.value, "Hello world")
    self.assertEqual(html_node.props, {"href": f"dummylink.com"})

  def test_textnode_to_htmlnode_image(self):
    node = TextNode("Hello world", TextType.IMAGE, "dummylink.com")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "img")
    self.assertEqual(html_node.value, "")
    self.assertEqual(html_node.props, {"src": f"dummylink.com", "alt": "alt text"})

if __name__ == "__main__":
  unittest.main()