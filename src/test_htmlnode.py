import unittest

from htmlnode import HTMLNode

props = {
  "href": "https://www.google.com",
  "target": "_blank",
}

class TestHTMLNode(unittest.TestCase):
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


if __name__ == "__main__":
  unittest.main() 