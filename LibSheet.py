from ScRect import ScRect

styles = {
  "title":   {"fill":"white", "stroke":"none", "font-family":"Cuprum", "font-weight":"bold", "font-style":"italic", "font-size":3.6},
  "heading": {"fill":"black", "stroke":"none", "font-family":"Cuprum", "font-weight":"bold", "font-size":3.4},
  "label":   {"fill":"black", "stroke":"none", "font-family":"Cuprum", "font-weight":"normal", "font-size":3.4},

  "line": {"fill":"none", "stroke":"black", "stroke-width":"0.05mm"},
  "border": {"fill":"white", "stroke":"black", "stroke-width":"0.05mm"},
  "fill": {"fill":"black", "stroke":"none", "rx":1.0, "ry":1.0},
  "clear":{"fill":"white", "stroke":"none", },
}

class Child(ScRect):
  def __init__(self, name, **attributes):
    super(Child, self).__init__()
    self.name = name
    self.attributes = attributes

  def draw(self, out):
    if self.name is None:
      return
    elif len(self.attributes) < 1:
      out.write("<{} />".format(self.name))
    else:
      out.write("<{} {} />".format(
        self.name, 
        " ".join(
          ["{}='{}'".format(att, val) for att, val in self.attributes.items()]
        )
      ))

  def update(self):
    pass

class Parent(Child):
  def __init__(self, name, **attributes):
    super(Parent, self).__init__(name, **attributes)
    self.children = []

  def add_child(self, child):
    self.children.append(child)
    return child

  def draw(self, out):
    self.draw_head(out)
    self.draw_children(out)
    self.draw_tail(out)

  def draw_head(self, out):
    if self.name is None:
      return
    elif len(self.attributes) < 1:
      out.write("<{}>".format(self.name))
    else:
      out.write("<{} {}>".format(
        self.name, 
        " ".join(
          ["{}='{}'".format(att, val) for att, val in self.attributes.items()]
        )
      ))
  
  def draw_children(self, out):
    for child in self.children:
      child.draw(out)

  def draw_tail(self, out):
    if self.name is None:
      return
    else:
      out.write("</{}>".format(self.name))

  def update(self):
    self.update_self()
    self.update_children()

  def update_self(self):
    pass

  def update_children(self):
    for child in self.children:
      child.update()

#class Page(Parent):
#  def __init__(self):
#    super(Page, self).__init__("svg",
#      width="216mm",
#      height="280mm",
#      viewBox="0 0 216 280",
#    )
#    self.x = 0
#    self.y = 0
#    self.w = 216
#    self.h = 280
#  
#  def update_self(self):
#    subrect = self.copy()
#    
#    for child in self.children:
#      child.match_to(subrect)

class Page(Parent):
  def __init__(self, margin=6, holes=None):
    super(Page, self).__init__("svg",
      width="216mm",
      height="280mm",
      viewBox="0 0 216 280",
    )
    
    if holes is None:
      self.x = margin
      self.y = margin
      self.w = 216 - (margin + margin)
      self.h = 280 - (margin + margin)
    elif holes == "left":
      self.x = margin + 10
      self.y = margin
      self.w = 216 - (margin + margin + 10)
      self.h = 280 - (margin + margin) 
    elif holes == "right":
      self.x = margin
      self.y = margin
      self.w = 216 - (margin + margin + 10)
      self.h = 280 - (margin + margin)
  
  def update_self(self):
    subrect = self.copy()
    
    for child in self.children:
      child.match_to(subrect)

class Margin(Parent):
  def __init__(self, *m):
    super(Margin, self).__init__(None)
    
    # If there is one argument and that argument has a length use it as multiple args
    if len(m) == 1:
      try:
        len(m[0]) # This will raise a TypeError if it has no length
        m = m[0]
      except TypeError:
        pass
    
    if len(m) == 1:
      self.t = m[0]
      self.r = m[0]
      self.b = m[0]
      self.l = m[0]
    elif len(m) == 2:
      self.t = m[1]
      self.r = m[0]
      self.b = m[1]
      self.l = m[0]
    elif len(m) == 4:
      self.t = m[0]
      self.r = m[1]
      self.b = m[2]
      self.l = m[3]
    else:
      raise ValueError("Margin constructor accepts one, two or four arguments.")
  
  def update_self(self):
    subrect = self.copy()

    subrect.x += self.l
    subrect.y += self.t
    subrect.w -= self.l + self.r
    subrect.h -= self.t + self.b
    
    for child in self.children:
      child.match_to(subrect)

class FlexGrid(Parent):
  def __init__(self, h_ratio, v_ratio):
    super(FlexGrid, self).__init__(None)
    
    self.h_ratio = h_ratio
    self.v_ratio = v_ratio
  
  def update_self(self):
    rects = []
    
    h_total = sum(self.h_ratio)
    v_total = sum(self.v_ratio)

    h_sizes = []
    for n in self.h_ratio:
      h_sizes.append(self.w * (n/h_total))
    
    v_sizes = []
    for n in self.v_ratio:
      v_sizes.append(self.h * (n/v_total))
    
    h_stops = [self.x+sum(h_sizes[:n]) for n in range(len(h_sizes))]
    v_stops = [self.y+sum(v_sizes[:n]) for n in range(len(v_sizes))]
    
    for y,h in zip( v_stops, v_sizes):
      for x,w in zip(h_stops, h_sizes):
        rects.append(ScRect(x,y,w,h))

    for child, rect in zip(self.children, rects):
      child.match_to(rect)
  
class Rect(Child):
  def __init__(self, style):
    super(Rect, self).__init__("rect", **style)
  
  def update(self):
    self.attributes["x"] = self.x
    self.attributes["y"] = self.y
    self.attributes["width"] = self.w
    self.attributes["height"] = self.h

class Data(ScRect):
  def __init__(self, string):
    super(Data, self).__init__()
    self.string = string
  
  def draw(self, out):
    out.write(self.string)
  
  def update(self):
    pass

class Text(Parent):
  def __init__(self, text, style):
    super(Text, self).__init__("text", **style)
    self.add_child(Data(text))
    self.valign = "middle"
    
  @property
  def halign(self):
    return self.attributes.setdefault("text-anchor","middle")
  
  @halign.setter
  def halign(self, val):
    assert val in ("start","middle","end")
    self.attributes["text-anchor"] = val
  
  @property
  def valign(self):
    return self._valign
  
  @valign.setter
  def valign(self, val):
    assert val in ("top","middle","bottom")
    self._valign = val

    if self._valign == "top":
        self.attributes["dominant-baseline"] = "text-before-edge"
    elif self._valign == "middle":
        self.attributes["dominant-baseline"] = "middle"
    else:
        self.attributes["dominant-baseline"] = "text-after-edge"
    
  @property
  def size(self):
    return self.attributes["font-size"]
  
  @size.setter
  def size(self, val):
    self.attributes["font-size"] = val
    
  def update(self):
    if self.valign == "top":
      self.attributes["y"] = self.t_edge
    if self.valign == "middle":
      self.attributes["y"] = self.mid_y + (self.size * 0.1)
    if self.valign == "bottom":
      self.attributes["y"] = self.b_edge

 
    if self.halign == "start":
      self.attributes["x"] = self.l_edge
    elif self.halign == "middle":
      self.attributes["x"] = self.mid_x
    elif self.halign == "end":
      self.attributes["x"] = self.r_edge

class BorderBox(Parent):
  def __init__(self, title):
    super(BorderBox, self).__init__("g")
    
    temp = self.add_child(Margin(0.5))

    temp.add_child(Rect(styles["fill"]))

    temp = temp.add_child(Margin(0,0.5,0,0.5))
    
    self.title_text = self.add_child(Text(title, styles["title"]))
    self.title_text.halign = "start"
    self.title_text.valign = "middle"

    temp = temp.add_child(Margin(5.0,0,2.0,0))
    
    self.add_child = temp.add_child

  def update_self(self):
    for child in self.children:
      child.match_to(self)
    
    self.title_text.x += 1.5
    self.title_text.y += 1.00
    self.title_text.h = 4.0
    

class Line(Child):
  def __init__(self,x1,y1,x2,y2):
    super(Line, self).__init__("line",**styles["line"])
    
    self.x1 = x1
    self.y1 = y1
    self.x2 = x2
    self.y2 = y2

  @property
  def x1(self):
    return self.attributes["x1"]
  
  @x1.setter
  def x1(self, val):
    self.attributes["x1"] = val

  @property
  def y1(self):
    return self.attributes["y1"]
  
  @y1.setter
  def y1(self, val):
    self.attributes["y1"] = val

  @property
  def x2(self):
    return self.attributes["x2"]
  
  @x2.setter
  def x2(self, val):
    self.attributes["x2"] = val

  @property
  def y2(self):
    return self.attributes["y2"]
  
  @y2.setter
  def y2(self, val):
    self.attributes["y2"] = val

class Table(Parent):
  def __init__(self, columns, headings, anchors, data):
    super(Table, self).__init__("g")
    
    self.columns = columns
    self.headings = headings
    self.anchors = anchors
    self.data = data


  def update_self(self):
    line_height = 4.30	
    line_count = max(1, int(self.h // line_height))
    line_height = self.h / line_count

    rect = self.add_child(Rect(styles["border"]))
    rect.match_to(self)
    rect.h = line_height * line_count
    
    col_total = sum(self.columns)

    h_sizes = []
    for n in self.columns:
      h_sizes.append(self.w * (n/col_total))
    
    h_stops = [self.x+sum(h_sizes[:n]) for n in range(len(h_sizes))]

    for line_num in range(1,line_count):
      self.add_child(
        Line(
          self.l_edge, self.t_edge + (line_num * line_height),
          self.r_edge, self.t_edge + (line_num * line_height)
        )
      )

    for x in h_stops[1:]:
      self.add_child(Line(x, self.t_edge, x, self.b_edge))
    
    if self.headings is not None:
      line_offset = 1
      for x, w, h, a in zip(h_stops, h_sizes, self.headings, self.anchors):
        text = self.add_child(Text(h, styles["heading"]))
        text.x = x+0.5
        text.w = w-1.0
        text.h = line_height
        text.y = self.y
        text.halign = a
    else:
      line_offset = 0

    for line, entry in enumerate(self.data):
      for x, w, d, a in zip(h_stops, h_sizes, entry, self.anchors):
        if d is None:
          continue
        else:
          text = self.add_child(Text(d, styles["label"]))
          text.x = x+0.5
          text.w = w-1.0
          text.h = line_height
          text.y = self.y + ((line+line_offset) * line_height)
          text.halign = a

class WriteIn(Parent):
  def __init__(self, label):
    super(WriteIn, self).__init__(None)
    
    self.rect = self.add_child(Rect(styles["border"]))
    self.label = self.add_child(Text(label, styles["heading"]))
    self.label.halign = "start"
    self.label.valign = "middle"
  
  def update_self(self):
    self.rect.match_to(self)
    self.label.match_to(self)
    self.label.x += 0.5
    self.label.w -= 1.0
       
