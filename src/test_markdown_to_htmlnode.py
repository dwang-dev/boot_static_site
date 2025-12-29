import unittest
from helpers import markdown_to_html_node

class MarkdownToHTMLNODE(unittest.TestCase):
    def test_paragraph_no_inline(self):
        md = "Text 1\n\nText 2"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>Text 1</p><p>Text 2</p></div>")
        
    def test_paragraphs_with_inline(self):
        md = """
This is **bolded** paragraph\ntext in a p\ntag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph\ntext in a p\ntag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    
    def test_heading_no_inline(self):
        md = "# h1\n\n## h2\n\n### h3\n\n#### h4\n\n##### h5\n\n###### h6"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>h1</h1><h2>h2</h2><h3>h3</h3><h4>h4</h4><h5>h5</h5><h6>h6</h6></div>")

    def test_heading7_is_paragraph(self):
        md = "####### Text"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>####### Text</p></div>")

    def test_headings_with_inline(self):
        md = "# **Bold Text**\n\n## _Italic Text_ `Code Text`"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1><b>Bold Text</b></h1><h2><i>Italic Text</i> <code>Code Text</code></h2></div>")

    def test_code_no_inline(self):
        md = "```Code Block 1```\n\n```Code Block 2```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><pre><code>Code Block 1</code></pre><pre><code>Code Block 2</code></pre></div>")

    def test_code_with_inline(self):
        md = "```**Code Block 1**```\n\n```_Code_ `Block` 2```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><pre><code>**Code Block 1**</code></pre><pre><code>_Code_ `Block` 2</code></pre></div>")

    def test_quote_no_inline(self):
        md = "> Quote 1\n\n> Quote 2"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>Quote 1</blockquote><blockquote>Quote 2</blockquote></div>")

    def test_quote_with_inline(self):
        md = "> **Bold**\n\n> _Italic_ `Code`"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote><b>Bold</b></blockquote><blockquote><i>Italic</i> <code>Code</code></blockquote></div>")

    def test_ul_no_inline(self):
        md = "- Li 1\n- Li 2\n\n- Li 3\n- Li 4"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>Li 1</li><li>Li 2</li></ul><ul><li>Li 3</li><li>Li 4</li></ul></div>")
    
    def test_ul_with_inline(self):
        md = "- **Bold Li**\n- _Italic Li_\n\n- `Code Li`\n- Normal Li"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li><b>Bold Li</b></li><li><i>Italic Li</i></li></ul><ul><li><code>Code Li</code></li><li>Normal Li</li></ul></div>")

    def test_ol_no_inline(self):
        md = "1. Li 1\n2. Li 2\n\n3. Li 3\n4. Li 4"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>Li 1</li><li>Li 2</li></ol><ol><li>Li 3</li><li>Li 4</li></ol></div>")

    def test_ol_with_inline(self):
        md = "1. **Bold**\n2. _Italic_\n\n3. `Code`\n4. [img](imgurl)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><ol><li><b>Bold</b></li><li><i>Italic</i></li></ol><ol><li><code>Code</code></li><li><a href=\"imgurl\"></a></li></ol></div>"

    def test_paragraph_example(self):
        md = """
This is **bolded** paragraph text in a p tag here\n\nThis is another paragraph with _italic_ text and `code` here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock_example(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>\nThis is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
