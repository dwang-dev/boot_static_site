import unittest
from inline import *


class InlineTests(unittest.TestCase):
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

  def test_text_to_textnode_no_options(self):
    nodes = text_to_textnodes("This is completely normal text")
    self.assertListEqual([
      TextNode("This is completely normal text", TextType.TEXT)
    ], nodes)
