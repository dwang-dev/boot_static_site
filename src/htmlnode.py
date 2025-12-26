class HTMLNode():
  def __init__(self, tag:str=None, value:str=None, children:list=[], props:dict[str, str]=None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props
  
  def to_html(self) -> None:
    raise NotImplementedError("TODO")
  
  def props_to_html(self) -> str:
    if self.props == None:
      return ""
    s = ""
    for prop, val in self.props.items():
      s += f" {prop}=\"{val}\""
    return s

  def __repr__(self) -> str:
    return f'''
    <{self.tag} {self.props_to_html()}>
      {self.value}
    <\{self.tag}>
    '''

class LeafNode(HTMLNode):
  def __init__(self, tag:str, value:str, props:dict[str, str]=None):
    if value == None:
      raise ValueError("Leaf nodes must have a value")
    super().__init__(tag, value, props=props)

  def to_html(self) -> str:
    if self.tag == None:
      return f"{self.value}"
    else:
      return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
  def __repr__(self) -> str:
    return self.to_html()

class ParentNode(HTMLNode):
  def __init__(self, tag:str, children:list[HTMLNode]=[], props:dict[str, str]=None):
    super().__init__(tag, children=children, props=props)
  
  def to_html(self) -> str:
    if self.tag == None:
      raise ValueError("No tag in parent element")
    if self.children == None:
      raise ValueError("Missing children")      
    s = f"<{self.tag}{self.props_to_html()}>"
    for child in self.children:
      s += child.to_html()
    s += f"</{self.tag}>"
    return s
  
  def __repr__(self) -> str:
    return self.to_html()