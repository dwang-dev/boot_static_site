import unittest
from htmlnode import HTMLNode, ParentNode, LeafNode

props = {
  "href": "https://www.google.com",
  "target": "_blank",
}

class TestHTMLNode(unittest.TestCase):
  ###############################################
  ############### HTML Node tests ###############
  ###############################################
  def test_to_html(self):
    node = HTMLNode("p", "Hello world", children=None, props=props)
    with self.assertRaises(Exception):
      node.to_html()

  def test_props_to_html(self):
    node = HTMLNode("p", "Hello world", children=None, props=props)
    self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

  def test_repr(self):
    node = HTMLNode("p", "Hello world", children=None, props=props)
    expected = f'''
    <{node.tag} {node.props_to_html()}>
      {node.value}
    <\{node.tag}>
    '''
    self.assertEqual(node.__repr__(), expected)

  ###############################################
  ############### Leaf Node tests ###############
  ###############################################

  def test_props_to_html(self):
    node = LeafNode("p", "Hello world", props=props)
    self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

  def test_no_value_raises_err(self):
    with self.assertRaises(ValueError):
      node = LeafNode("p", None)

  def test_to_html_p(self):
    node = LeafNode("p", "Hello world", props)
    self.assertEqual(node.to_html(), f"<p href=\"https://www.google.com\" target=\"_blank\">Hello world</p>")

  def test_to_html_div(self):
    node = LeafNode("div", "Hello world", props)
    self.assertEqual(node.to_html(), f"<div href=\"https://www.google.com\" target=\"_blank\">Hello world</div>")

  def test_to_html_a(self):
    node = LeafNode("a", "Hello world", props)
    self.assertEqual(node.to_html(), f"<a href=\"https://www.google.com\" target=\"_blank\">Hello world</a>")

  def test_parent_node_no_children(self):
    node = ParentNode("div", [], props)
    self.assertEqual(node.to_html(), "<div href=\"https://www.google.com\" target=\"_blank\"></div>")

  #################################################
  ############### Parent Node Tests ###############
  #################################################

  def test_parent_node_one_child(self):
    node = ParentNode(
        "div",
        [
            LeafNode("b", "Bold text"),
        ],
    )
    self.assertEqual(node.to_html(), "<div><b>Bold text</b></div>")

  def test_parent_node_one_child_no_tag(self):
    node = ParentNode(
        "div",
        [
            LeafNode(None, "No text"),
        ],
    )
    self.assertEqual(node.to_html(), "<div>No text</div>")

  def test_parent_node_multiple_children(self):
    node = ParentNode(
        "div",
        [
            LeafNode("b", "Bold text"),
            LeafNode("i", "Italic text"),
            LeafNode(None, "No text"),
        ],
    )
    self.assertEqual(node.to_html(), "<div><b>Bold text</b><i>Italic text</i>No text</div>")

  def test_parentnode_one_grandchild(self):
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(parent_node.to_html(),"<div><span><b>grandchild</b></span></div>")

  def test_parentnode_one_grandchild_no_tag(self):
    grandchild_node = LeafNode(None, "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(parent_node.to_html(),"<div><span>grandchild</span></div>")

  def test_parentnode_multiple_grandchildren(self):
    grandchild_node1 = LeafNode("b", "grandchild")
    grandchild_node2 = LeafNode("a", "grandchild2")
    child_node = ParentNode("span", [grandchild_node1, grandchild_node2])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(parent_node.to_html(),"<div><span><b>grandchild</b><a>grandchild2</a></span></div>")