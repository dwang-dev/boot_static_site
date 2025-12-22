class HTMLNode():
  def __init__(self, tag=None, value=None, children=[], props=None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props
  
  def to_html(self):
    raise NotImplementedError("TODO")
  
  def props_to_html(self):
    if self.props == None:
      return ""
    s = ""
    for prop, val in self.props.items():
      s += f" {prop}=\"{val}\""
    return s

  def __repr__(self):
    return f'''
    <{self.tag} {self.props_to_html()}>
      {self.value}
    <\{self.tag}>
    '''

class LeafNode(HTMLNode):
  def __init__(self, tag, value, props=None):
    if value == None:
      raise ValueError("Leaf nodes must have a value")
    super().__init__(tag, value, props=props)

  def to_html(self):
    if self.tag == None:
      return f"{self.value}"
    else:
      return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
  def __init__(self, tag, children, props=None):
    super().__init__(tag, children=children, props=props)
  
  def to_html(self):
    if self.tag == None:
      raise ValueError("No tag in parent element")
    if self.children == None:
      raise ValueError("Missing children")      
    s = f"<{self.tag}{self.props_to_html()}>"
    for child in self.children:
      s += child.to_html()
    s += f"</{self.tag}>"
    return s