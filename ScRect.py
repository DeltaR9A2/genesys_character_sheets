from __future__ import division

import math

class ScRect(object):
  def __init__(self, x=0, y=0, w=1, h=1):
    self.x = x
    self.y = y
    self.w = w
    self.h = h

  @property
  def x(self):
    return self._x
  
  @x.setter
  def x(self, n):
    self._x = round(n, 3)

  @property
  def y(self):
    return self._y
  
  @y.setter
  def y(self, n):
    self._y = round(n, 3)

  @property
  def w(self):
    return self._w
  
  @w.setter
  def w(self, n):
    self._w = round(n, 3)

  @property
  def h(self):
    return self._h
  
  @h.setter
  def h(self, n):
    self._h = round(n, 3)

  def __len__(self):
    return 4
    
  def __getitem__(self, key):
    if key == 0:
      return self.x
    elif key == 1:
      return self.y
    elif key == 2:
      return self.w
    elif key == 3:
      return self.h
    else:
      raise KeyError
    
  def __setitem__(self, key, val):
    if key == 0:
      self.x = val
    elif key == 1:
      self.y = val
    elif key == 2:
      self.w = val
    elif key == 3:
      self.h = val
    else:
      raise KeyError
  
  def __delitem__(self, key):
    raise Exception("Cannot delete the measurements of an ScRect")
  
  def __iter__(self):
    yield self.x
    yield self.y
    yield self.w
    yield self.h
    
  @property
  def l_edge(self):
    return self.x
  
  @l_edge.setter
  def l_edge(self, n):
    self.x = n
  
  @property
  def r_edge(self):
    return self.x + self.w
  
  @r_edge.setter
  def r_edge(self, n):
    self.x = n - self.w
  
  @property
  def t_edge(self):
    return self.y
  
  @t_edge.setter
  def t_edge(self, n):
    self.y = n

  @property
  def b_edge(self):
    return self.y + self.h
  
  @b_edge.setter
  def b_edge(self, n):
    self.y = n - self.h

  @property
  def mid_x(self):
    return self.x + (self.w/2.0)
  
  @mid_x.setter
  def mid_x(self, n):
    self.x = n - (self.w/2.0)
  
  @property
  def mid_y(self):
    return self.y + (self.h/2.0)

  @mid_y.setter
  def mid_y(self, n):
    self.y = n - (self.h/2.0)

  @property
  def center(self):
    return (self.mid_x, self.mid_y)
  
  @center.setter
  def center(self, pair):
    self.mid_x, self.mid_y = pair
  
  @property
  def size(self):
    return (self.w, self.h)
  
  @size.setter
  def size(self, pair):
    self.w, self.h = pair
  
  def move_to(self, other):
    self.center = other.center
    
  def match_to(self, other):
    self.x = other.x
    self.y = other.y
    self.w = other.w
    self.h = other.h
  
  def angle_to(self, other):
    dx = other.x - self.x
    dy = other.y - self.y
    return math.atan2(dy,dx)

  def move_at_angle(self, angle, dist):
    self.x += dist * math.cos(angle)
    self.y += dist * math.sin(angle)
  
  def move_toward(self, other, dist):
    self.move_at_angle(self.angle_to(other), dist)
  
  def collide(self, other):
    if(self.r_edge < other.l_edge or self.l_edge > other.r_edge or
       self.b_edge < other.t_edge or self.t_edge > other.b_edge):
      return False
    else:
      return True
  
  def grow(self, dw, dh):
    center = self.center
    self.w += dw
    self.h += dh
    self.center = center
  
  def copy(self):
    return ScRect(*self)
