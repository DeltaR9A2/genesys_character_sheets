from LibSheet import *

def make_info_box(title):
    info = BorderBox(title)
    inner = info.add_child(FlexGrid([1],[1,1,1,1]))
    
    inner.add_child(WriteIn("Name"))
    inner.add_child(WriteIn("Alias"))
    inner.add_child(WriteIn("Concept"))
    inner.add_child(WriteIn("Player"))
    
    return info

def add_identity(parent, margin=(0.25,0.0,0.25,0.0)):
  ident = parent.add_child(Margin(margin)).add_child(FlexGrid([1],[1,1,1,1]))

  row = ident.add_child(FlexGrid([6,6,2],[1]))
  row.add_child(WriteIn("Name"))
  row.add_child(WriteIn("Vocation"))
  row.add_child(WriteIn("Rating"))
  ident.add_child(WriteIn("Licenses"))
  row = ident.add_child(FlexGrid([6,6,2],[1]))
  row.add_child(WriteIn("Lifestyle"))
  row.add_child(WriteIn("Location"))
  row.add_child(WriteIn("Months"))
  ident.add_child(WriteIn("Notes"))

def add_commlink(parent, margin=(0.0,0.25,0.0,0.25)):
  cl = parent.add_child(Margin(margin)).add_child(FlexGrid([1],[1,1,1,11]))

  cl.add_child(WriteIn("Model"))
  cl.add_child(WriteIn("OS"))
  row = cl.add_child(FlexGrid([1,1,1,1],[1]))
  row.add_child(WriteIn("Rsp"))
  row.add_child(WriteIn("Sig"))
  row.add_child(WriteIn("Sys"))
  row.add_child(WriteIn("FW"))
  cl.add_child(Table(
    columns = (1,),
    headings = ("Programs",),
    anchors = ("start",),
    data = ()
  ))

def add_ranged_weapon(parent, margin=0.0):
  weapon = parent.add_child(Margin(margin)).add_child(FlexGrid([1],[1,1,1,1,1]))

  weapon.add_child(WriteIn("Weapon"))
  row = weapon.add_child(FlexGrid([4,4,4,5,7],[1]))
  row.add_child(WriteIn("DP"))
  row.add_child(WriteIn("DV"))
  row.add_child(WriteIn("AP"))
  row.add_child(WriteIn("RC"))
  row.add_child(WriteIn("Ammo"))
  row = weapon.add_child(FlexGrid([5,7],[1]))
  row.add_child(WriteIn("Mode"))
  row.add_child(WriteIn("Range"))
  weapon.add_child(WriteIn("Notes"))
  weapon.add_child(Rect(styles["border"]))

def add_melee_weapon(parent, margin=0.0):
  weapon = parent.add_child(Margin(margin)).add_child(FlexGrid([1],[1,1,1,1]))

  weapon.add_child(WriteIn("Weapon"))
  row = weapon.add_child(FlexGrid([2,2,2,3],[1]))
  row.add_child(WriteIn("DP"))
  row.add_child(WriteIn("DV"))
  row.add_child(WriteIn("AP"))
  row.add_child(WriteIn("Reach"))
  weapon.add_child(WriteIn("Notes"))
  weapon.add_child(Rect(styles["border"]))

def add_armor_set(parent, margin=(0.25,0.0,0.25,0.0)):
  armor = parent.add_child(Margin(margin))

  armor.add_child(Table(
    columns = (10,3,3,12),
    headings = ("Armor","B","I","Notes"),
    anchors = ("start","middle","middle","middle"),
    data = (
      (None, None, None, None),
      (None, None, None, None),
      (None, None, None, None),
      (None, None, None, None),
      (None, None, None, None),
      ("Combined", None, None, None),
      ("Plus Body", None, None, None),
    )
  ))

class ThreeColumnPage(Page):
  def __init__(self, title, margin=10, holes=None):
    super(ThreeColumnPage, self).__init__(margin=margin, holes=holes)
    
    columns = self.add_child(FlexGrid([33,33,33],[1]))

    col = columns.add_child(FlexGrid([1],[10,90]))

    col.add_child(make_info_box(title))
    
    self.l_col = col.add_child(Margin(0))
    self.m_col = columns.add_child(Margin(0))
    self.r_col = columns.add_child(Margin(0))
    
class TwoColumnRightPage(Page):
  def __init__(self, title, margin=10, holes=None):
    super(TwoColumnRightPage, self).__init__(margin=margin, holes=holes)
    
    columns = self.add_child(FlexGrid([33,66],[1]))

    col = columns.add_child(FlexGrid([1],[10,90]))

    col.add_child(make_info_box(title))
    
    self.l_col = col.add_child(Margin(0))
    self.r_col = columns.add_child(Margin(0))
    
class OneColumnPage(Page):
  def __init__(self, title, margin=10, holes=None):
    super(OneColumnPage, self).__init__(margin=margin, holes=holes)
    
    rows = self.add_child(FlexGrid([1],[10,90]))

    top = rows.add_child(FlexGrid([33,66],[1]))
    top.add_child(make_info_box(title))
    
    self.upper = top.add_child(Margin(0))
    self.lower = rows.add_child(Margin(0))
    

