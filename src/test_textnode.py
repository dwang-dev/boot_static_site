import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
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
        node = TextNode("This is a text node", TextType.PLAIN)
        node2 = TextNode("This is a text node", TextType.BOLD)
        assert(node != node2)

    def test_url_neq(self):
        node = TextNode("This is a text node", TextType.BOLD, "Heyworld.net")
        node2 = TextNode("This is a text node", TextType.BOLD, "Helloworld.com")
        assert(node != node2)

    # Invalid type hceck
    def test_invalid_type(self):
        with self.assertRaises(Exception):
          node = TextNode("This is a text node", "Invalid type")
        


if __name__ == "__main__":
    unittest.main()