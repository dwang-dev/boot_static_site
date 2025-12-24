import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from helpers import (text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, 
                     extract_markdown_links, split_nodes_image, split_nodes_link,
                     text_to_textnodes, markdown_to_blocks
                     )

props = {
  "href": "https://www.google.com",
  "target": "_blank",
}

class TestNode(unittest.TestCase):
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
        node = TextNode("This is a text node", "Invalid type")

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

  ################################################################
  ############### split_nodes_delimiter() Tests #################
  ################################################################

  def test_split_nodes_delimiter_code(self):
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    self.assertEqual(len(new_nodes), 3)
    self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
    self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
    self.assertEqual(new_nodes[2], TextNode(" word", TextType.TEXT))

  def test_split_nodes_delimiter_bold(self):
    node = TextNode("This is text with a **bold** word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    self.assertEqual(len(new_nodes), 3)
    self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
    self.assertEqual(new_nodes[1], TextNode("bold", TextType.BOLD))
    self.assertEqual(new_nodes[2], TextNode(" word", TextType.TEXT))

  def test_split_nodes_delimiter_italic(self):
    node = TextNode("This is text with a _italic_ word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
    self.assertEqual(len(new_nodes), 3)
    self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
    self.assertEqual(new_nodes[1], TextNode("italic", TextType.ITALIC))
    self.assertEqual(new_nodes[2], TextNode(" word", TextType.TEXT))

  def test_split_nodes_delimiter_multiple_nodes(self):
    node1 = TextNode("First `code block` word", TextType.TEXT)
    node2 = TextNode("Second `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
    self.assertEqual(len(new_nodes), 6)
    self.assertEqual(new_nodes[0], TextNode("First ", TextType.TEXT))
    self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
    self.assertEqual(new_nodes[2], TextNode(" word", TextType.TEXT))
    self.assertEqual(new_nodes[3], TextNode("Second ", TextType.TEXT))
    self.assertEqual(new_nodes[4], TextNode("code block", TextType.CODE))
    self.assertEqual(new_nodes[5], TextNode(" word", TextType.TEXT))

  def test_split_nodes_delimiter_no_text_lhs(self):
    node = TextNode("`code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    self.assertEqual(len(new_nodes), 2)
    self.assertEqual(new_nodes[0], TextNode("code block", TextType.CODE))
    self.assertEqual(new_nodes[1], TextNode(" word", TextType.TEXT))

  def test_split_nodes_delimiter_no_text_rhs(self):
    node = TextNode("word `code block`", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    self.assertEqual(len(new_nodes), 2)
    self.assertEqual(new_nodes[0], TextNode("word ", TextType.TEXT))
    self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))

  def test_split_nodes_delimiter_multiple_delimiters(self):
    node = TextNode("First `code block` word. Second `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    self.assertEqual(len(new_nodes), 5)
    self.assertEqual(new_nodes[0], TextNode("First ", TextType.TEXT))
    self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
    self.assertEqual(new_nodes[2], TextNode(" word. Second ", TextType.TEXT))
    self.assertEqual(new_nodes[3], TextNode("code block", TextType.CODE))
    self.assertEqual(new_nodes[4], TextNode(" word", TextType.TEXT))

  def test_split_nodes_delimiter_no_text_lhs_rhs(self):
    node = TextNode("`code block`", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    self.assertEqual(len(new_nodes), 1)
    self.assertEqual(new_nodes[0], TextNode("code block", TextType.CODE))

  def test_split_nodes_delimiter_throws_missing_delimiter(self):
    node = TextNode("This is text with a `code block word", TextType.TEXT)
    with self.assertRaises(Exception):
      new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

  def test_split_nodes_delimiter_throws_too_many_delimiters(self):
    node = TextNode("This is text `with a `code block` word", TextType.TEXT)
    with self.assertRaises(Exception):
      new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

  def test_split_nodes_appends_when_not_text_type(self):
    node = TextNode("This is text with a `code block` word", TextType.CODE)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    self.assertEqual(len(new_nodes), 1)
    self.assertEqual(new_nodes[0], TextNode("This is text with a `code block` word", TextType.CODE))

  ################################################################
  ############### extract_markdown_images() Tests ################
  ################################################################

  def test_extract_md_imgs(self):
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    md_imgs = extract_markdown_images(text)
    self.assertEqual(len(md_imgs), 2)
    self.assertEqual(md_imgs[0], ("rick roll", "https://i.imgur.com/aKaOqIh.gif"))
    self.assertEqual(md_imgs[1], ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"))
  
  def test_extract_md_imgs_no_brackets(self):
    text = "This is text with a !rick roll(https://i.imgur.com/aKaOqIh.gif)"
    md_imgs = extract_markdown_images(text)
    self.assertEqual(len(md_imgs), 0)

  def test_extract_md_imgs_no_opening_brackets(self):
    text = "This is text with a !rick roll](https://i.imgur.com/aKaOqIh.gif)"
    md_imgs = extract_markdown_images(text)
    self.assertEqual(len(md_imgs), 0)

  def test_extract_md_imgs_no_closing_brackets(self):
    text = "This is text with a ![rick roll(https://i.imgur.com/aKaOqIh.gif)"
    md_imgs = extract_markdown_images(text)
    self.assertEqual(len(md_imgs), 0)

  def test_extract_md_imgs_no_parenthesis(self):
    text = "This is text with a ![rick roll]https://i.imgur.com/aKaOqIh.gif"
    md_imgs = extract_markdown_images(text)
    self.assertEqual(len(md_imgs), 0)

  def test_extract_md_imgs_no_opening_parenthesis(self):
    text = "This is text with a ![rick roll]https://i.imgur.com/aKaOqIh.gif)"
    md_imgs = extract_markdown_images(text)
    self.assertEqual(len(md_imgs), 0)

  def test_extract_md_imgs_no_closing_parenthesis(self):
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif"
    md_imgs = extract_markdown_images(text)
    self.assertEqual(len(md_imgs), 0)
  

  def test_extract_md_imgs_l_bracket_in_alt_text(self):
    text = "This is text with a ![rick [roll](https://i.imgur.com/aKaOqIh.gif)"
    md_imgs = extract_markdown_images(text)
    self.assertEqual(len(md_imgs), 0)

  def test_extract_md_imgs_r_bracket_in_alt_text(self):
    text = "This is text with a ![rick ]roll](https://i.imgur.com/aKaOqIh.gif)"
    md_imgs = extract_markdown_images(text)
    self.assertEqual(len(md_imgs), 0)

  def test_extract_md_imgs_l_parenthesis_in_link(self):
    text = "This is text with a ![rick roll](https://i.im(gur.com/aKaOqIh.gif)"
    md_imgs = extract_markdown_images(text)
    self.assertEqual(len(md_imgs), 0)

  # TODO: Fix edge case with right parenthesis in link.
  # def test_extract_md_imgs_r_parenthesis_in_link(self):
  #   text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
  #   md_imgs = extract_markdown_images(text)
  #   self.assertEqual(len(md_imgs), 0)

  def test_extract_md_imgs_no_exclamation(self):
    text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif)"
    md_imgs = extract_markdown_images(text)
    self.assertEqual(len(md_imgs), 0)

  ################################################################
  ############### extract_markdown_links() Tests ################
  ################################################################

  def test_extract_md_links(self):
    text = "[rick roll](https://i.imgur.com/aKaOqIh.gif)[obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    md_imgs = extract_markdown_links(text)
    self.assertEqual(len(md_imgs), 2)
    self.assertEqual(md_imgs[0], ("rick roll", "https://i.imgur.com/aKaOqIh.gif"))
    self.assertEqual(md_imgs[1], ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"))

  def test_extract_md_links_no_brackets(self):
    text = "rick roll(https://i.imgur.com/aKaOqIh.gif)"
    md_imgs = extract_markdown_links(text)
    self.assertEqual(len(md_imgs), 0)

  def test_extract_md_links_no_opening_brackets(self):
    text = "rick roll](https://i.imgur.com/aKaOqIh.gif)"
    md_imgs = extract_markdown_links(text)
    self.assertEqual(len(md_imgs), 0)

  def test_extract_md_links_no_closing_brackets(self):
    text = "[rick roll(https://i.imgur.com/aKaOqIh.gif)"
    md_imgs = extract_markdown_links(text)
    self.assertEqual(len(md_imgs), 0)

  def test_extract_md_links_no_parenthesis(self):
    text = "[rick roll]https://i.imgur.com/aKaOqIh.gif"
    md_imgs = extract_markdown_links(text)
    self.assertEqual(len(md_imgs), 0)

  def test_extract_md_links_no_opening_parenthesis(self):
    text = "[rick roll]https://i.imgur.com/aKaOqIh.gif)"
    md_imgs = extract_markdown_links(text)
    self.assertEqual(len(md_imgs), 0)

  def test_extract_md_links_no_closing_parenthesis(self):
    text = "[rick roll](https://i.imgur.com/aKaOqIh.gif"
    md_imgs = extract_markdown_links(text)
    self.assertEqual(len(md_imgs), 0)
  
  # TODO fix with left bracket in text.
  # def test_extract_md_links_l_bracket_in_alt_text(self):
  #   text = "[rick [roll](https://i.imgur.com/aKaOqIh.gif)"
  #   md_imgs = extract_markdown_links(text)
  #   self.assertEqual(len(md_imgs), 0)

  def test_extract_md_links_r_bracket_in_alt_text(self):
    text = "[rick ]roll](https://i.imgur.com/aKaOqIh.gif)"
    md_imgs = extract_markdown_links(text)
    self.assertEqual(len(md_imgs), 0)

  def test_extract_md_links_l_parenthesis_in_link(self):
    text = "[rick roll](https://i.im(gur.com/aKaOqIh.gif)"
    md_imgs = extract_markdown_links(text)
    self.assertEqual(len(md_imgs), 0)

  ################################################################
  ############### split_nodes_image() Tests ######################
  ################################################################

  def test_split_images_single_img(self):
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png). Cool image right?",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(". Cool image right?", TextType.TEXT),
        ],
        new_nodes,
    )

  def test_split_images_multiple_imgs(self):
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )
      
  def test_split_images_no_img(self):
    node = TextNode(
        "This is text with no image. Cool non-image right?",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual([node], new_nodes)

  def test_split_images_no_valid_img(self):
    node = TextNode(
        "This is text with an image(https://i.imgur.com/zjjcJKZ.png). Cool image right?",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual([node], new_nodes)
    
  ################################################################
  ############### split_nodes_link() Tests #######################
  ################################################################

  def test_split_links_single_link(self):
    node = TextNode(
        "This is a link [Link Text](https://i.imgur.com/zjjcJKZ.png). Cool link right?",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
        [
            TextNode("This is a link ", TextType.TEXT),
            TextNode("Link Text", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(". Cool link right?", TextType.TEXT),
        ],
        new_nodes,
    )

  def test_split_links_multiple_links(self):
    node = TextNode(
        "This is a link [Link Text](https://i.imgur.com/zjjcJKZ.png) and another [Link2 Text](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
        [
            TextNode("This is a link ", TextType.TEXT),
            TextNode("Link Text", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("Link2 Text", TextType.LINK, "https://i.imgur.com/3elNhQu.png")
        ],
        new_nodes,
    )

  def test_split_link_no_link(self):
    node = TextNode(
        "This is text with no image. Cool non-image right?",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual([node], new_nodes)

  def test_split_images_no_valid_link(self):
    node = TextNode(
        "This is text with an image(https://i.imgur.com/zjjcJKZ.png). Cool image right?",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual([node], new_nodes)

  ################################################################
  ############### text_to_textnode Tests #########################
  ################################################################

  def test_text_to_textnode_only_bold(self):
    text = "This is **text** with an"
    nodes = text_to_textnodes(text)
    self.assertListEqual([
      TextNode("This is ", TextType.TEXT),
      TextNode("text", TextType.BOLD),
      TextNode(" with an", TextType.TEXT),
    ], nodes)

  def test_text_to_textnode_only_italic(self):
    text = "This is _text_ with an"
    nodes = text_to_textnodes(text)
    self.assertListEqual([
      TextNode("This is ", TextType.TEXT),
      TextNode("text", TextType.ITALIC),
      TextNode(" with an", TextType.TEXT),
    ], nodes)

  def test_text_to_textnode_only_code(self):
    text = "This is `text` with an"
    nodes = text_to_textnodes(text)
    self.assertListEqual([
      TextNode("This is ", TextType.TEXT),
      TextNode("text", TextType.CODE),
      TextNode(" with an", TextType.TEXT),
    ], nodes)
    
  def test_text_to_textnode_only_img(self):
    text = "This is ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) with an"
    nodes = text_to_textnodes(text)
    self.assertListEqual([
      TextNode("This is ", TextType.TEXT),
      TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
      TextNode(" with an", TextType.TEXT),
    ], nodes)

  def test_text_to_textnode_only_link(self):
    text = "This is [obi wan link](https://i.imgur.com/fJRm4Vk.jpeg) with an"
    nodes = text_to_textnodes(text)
    self.assertListEqual([
      TextNode("This is ", TextType.TEXT),
      TextNode("obi wan link", TextType.LINK, "https://i.imgur.com/fJRm4Vk.jpeg"),
      TextNode(" with an", TextType.TEXT),
    ], nodes)

  def test_text_to_textnode_multiple_bold(self):
    text = "This is **text** with an **text2**"
    nodes = text_to_textnodes(text)
    self.assertListEqual([
      TextNode("This is ", TextType.TEXT),
      TextNode("text", TextType.BOLD),
      TextNode(" with an ", TextType.TEXT),
      TextNode("text2", TextType.BOLD),
    ], nodes)

  def test_text_to_textnode_multiple_bold_one_italic(self):
    text = "This is **text** with an **text2** _italictext_"
    nodes = text_to_textnodes(text)
    self.assertListEqual([
      TextNode("This is ", TextType.TEXT),
      TextNode("text", TextType.BOLD),
      TextNode(" with an ", TextType.TEXT),
      TextNode("text2", TextType.BOLD),
      TextNode(" ", TextType.TEXT),
      TextNode("italictext", TextType.ITALIC),
    ], nodes)

  def test_text_to_textnode_all_options(self):
    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    nodes = text_to_textnodes(text)
    self.assertListEqual([
      TextNode("This is ", TextType.TEXT),
      TextNode("text", TextType.BOLD),
      TextNode(" with an ", TextType.TEXT),
      TextNode("italic", TextType.ITALIC),
      TextNode(" word and a ", TextType.TEXT),
      TextNode("code block", TextType.CODE),
      TextNode(" and an ", TextType.TEXT),
      TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
      TextNode(" and a ", TextType.TEXT),
      TextNode("link", TextType.LINK, "https://boot.dev"),
    ], nodes)

  ##########################################################################
  ############### markdown_to_blocks tests #################################
  ##########################################################################

  def test_markdown_to_blocks(self):
    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
  """
    blocks = markdown_to_blocks(md)
    self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )

  def test_markdown_to_blocks_strips_whitespace(self):
    md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

      - This is a list
- with items
  """
    blocks = markdown_to_blocks(md)
    self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )

  def test_markdown_to_blocks_single_block(self):
    md = """
This is **bolded** paragraph
  """
    blocks = markdown_to_blocks(md)
    self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
        ],
    )

  def test_markdown_to_blocks_no_blocks(self):
    md = ""
    blocks = markdown_to_blocks(md)
    self.assertEqual(blocks, [])

if __name__ == "__main__":
  unittest.main()