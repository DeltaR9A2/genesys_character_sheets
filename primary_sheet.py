#!/usr/bin/env python3

import sys
from subprocess import call

from common import *

SVG_FILENAME = "Genesys_Charsheet_2019v1_P001_Primary.svg"
PDF_FILENAME = "Genesys_Charsheet_2019v1_P001_Primary.pdf"

def main():
  print("Creating sheet...")
  
  page = ThreeColumnPage("Genesys Character - Primary Sheet", margin=10)

  col = page.l_col.add_child(FlexGrid([1],[16,12,10,5,22,22]))

  information = col.add_child(BorderBox("General Information")).add_child(FlexGrid([5,4],[1,1,1,1,1,1,1]))
  for l,r in INFO_DATA:
    information.add_child(WriteIn(l))
    information.add_child(WriteIn(r))

  col.add_child(BorderBox("Standard Attributes")).add_child(ATTRIBUTE_TABLE)
  col.add_child(BorderBox("Special Attributes")).add_child(SPEC_ATTR_TABLE)

  karma = col.add_child(BorderBox("Karma")).add_child(FlexGrid((1,1),(1,)))
  karma.add_child(WriteIn("Total"))
  karma.add_child(WriteIn("Spent"))

#  col.add_child(BorderBox("Movement")).add_child(MOVEMENT_TABLE)
  col.add_child(BorderBox("Qualities")).add_child(QUALITY_TABLE)
  col.add_child(BorderBox("Notes")).add_child(NOTES_TABLE)

  page.m_col.add_child(BorderBox("Grouped Active Skills")).add_child(GRPD_SKLS_TABLE)

  col = page.r_col.add_child(FlexGrid([1],[60,43]))
  col.add_child(BorderBox("Ungrouped Active Skills")).add_child(UGRP_SKLS_TABLE)
  col.add_child(BorderBox("Knowledge &amp; Language Skills")).add_child(KNOW_SKLS_TABLE)

  page.update()
  
  print("Writing SVG file...")
  with open(SVG_FILENAME, "w") as fh:
    page.draw(fh)
  
  print("Converting to PDF...")
  call(["inkscape","-T","-A",PDF_FILENAME,SVG_FILENAME])

INFO_DATA = (
    ("Gender",      "Age"   ), 
    ("Metatype",    "Height"),
    ("Ethnicity",   "Weight"),
    ("Nationality", "Build" ),
    ("Allegiance",  "Skin"  ),
    ("Street Cred", "Hair"  ),
    ("Notoriety",   "Eyes"  ),
)

ATTRIBUTE_TABLE = Table(
  columns = (8,4,4,8,4,4),
  headings = ("Attribute","Base","Aug","Attribute","Base","Aug"),
  anchors = ("start","middle","middle","start","middle","middle"),
  data = (
    ("Body",      None, None, "Charisma",  None, None),
    ("Agility",   None, None, "Intuition", None, None),
    ("Reaction",  None, None, "Logic",     None, None),
    ("Strength",  None, None, "Willpower", None, None),
  )
)

SPEC_ATTR_TABLE = Table(
  columns = (8,8,8,4,4),
  headings = ("Attribute","Rating","Initiative","DP","IP"),
  anchors = ("start","middle","start","middle","middle"),
  data = (
    ("Edge",      None, "Physical", None, None),
    ("Essence",   None, "Astral",   None, None),
    ("Mag/Res",   None, "Matrix",   None, None),
  )
)

MOVEMENT_TABLE = Table(
  columns = (8,6,6,6,6),
  headings = ("Type","m/pass","m/rnd","km/hr","mi/hr"),
  anchors = ("start","middle","middle","middle","middle"),
  data = (
    ("Walking", None, None, None, None),
    ("Running", None, None, None, None),
  )
)

QUALITY_TABLE = Table(
  columns = (7,1),
  headings = ("Quality","BP"),
  anchors = ("start","middle"),
  data = ()
)


NOTES_TABLE = Table(
  columns = (1,),
  headings = None,
  anchors = ("start",),
  data = ()
)

GRPD_SKLS_TABLE = Table(
  columns = (11,3,3,11),
  headings = ("Skill Name","Att","Rtg","Specialization"),
  anchors = ("start","middle","middle","middle"),
  data = (
    ("Athletics",           "---", None, None),
    ("- Climbing",          "Str", None, None),
    ("- Gymnastics",        "Agi", None, None),
    ("- Running",           "Str", None, None),
    ("- Swimming",          "Str", None, None),
    ("Biotech",             "---", None, None),
    ("- Cybertech*",        "Log", None, None),
    ("- First Aid",         "Log", None, None),
    ("- Medicine*",         "Log", None, None),
    ("Close Combat",        "---", None, None),
    ("- Blades",            "Agi", None, None),
    ("- Clubs",             "Agi", None, None),
    ("- Unarmed",           "Agi", None, None),
    ("Conjuring",           "---", None, None),
    ("- Banishing",         "Mag", None, None),
    ("- Binding",           "Mag", None, None),
    ("- Summoning",         "Mag", None, None),
    ("Cracking",            "---", None, None),
    ("- Cybercombat",       "Log", None, None),
    ("- E-Warfare*",        "Log", None, None),
    ("- Hacking",           "Log", None, None),
    ("Electronics",         "---", None, None),
    ("- Computer",          "Log", None, None),
    ("- Data Search",       "Log", None, None),
    ("- Hardware*",         "Log", None, None),
    ("- Software*",         "Log", None, None),
    ("Firearms",            "---", None, None),
    ("- Automatics",        "Agi", None, None),
    ("- Longarms",          "Agi", None, None),
    ("- Pistols",           "Agi", None, None),
    ("Influence",           "---", None, None),
    ("- Con",               "Cha", None, None),
    ("- Etiquette",         "Cha", None, None),
    ("- Leadership",        "Cha", None, None),
    ("- Negotiation",       "Cha", None, None),
    ("Mechanic",            "---", None, None),
    ("- Aeronautics*",      "Log", None, None),
    ("- Automotive*",       "Log", None, None),
    ("- Industrial*",       "Log", None, None),
    ("- Nautical*",         "Log", None, None),
    ("Outdoors",            "---", None, None),
    ("- Navigation",        "Int", None, None),
    ("- Survival",          "Wil", None, None),
    ("- Tracking",          "Int", None, None),
    ("Sorcery",             "---", None, None),
    ("- Counterspelling",   "Mag", None, None),
    ("- Ritual Casting",    "Mag", None, None),
    ("- Spellcasting",      "Mag", None, None),
    ("Stealth",             "---", None, None),
    ("- Disguise",          "Int", None, None),
    ("- Infiltration",      "Agi", None, None),
    ("- Palming",           "Agi", None, None),
    ("- Shadowing",         "Int", None, None),
    ("Tasking",             "---", None, None),
    ("- Compiling*",        "Res", None, None),
    ("- Decompiling*",      "Res", None, None),
    ("- Registering*",      "Res", None, None),
  )
)

UGRP_SKLS_TABLE = Table(
  columns = (11,3,3,11),
  headings = ("Skill Name","Att","Rtg","Specialization"),
  anchors = ("start","middle","middle","middle"),
  data = (
    ("Arcana",            "Log", None, None),
    ("Archery",           "Agi", None, None),
    ("Armorer",           "Log", None, None),
    ("Artisan",           "Int", None, None),
    ("Assensing*",        "Int", None, None),
    ("Astral Combat*",    "Wil", None, None),
    ("Chemistry",         "Log", None, None),
    ("Demolitions",       "Log", None, None),
    ("Diving",            "Bod", None, None),
    ("Dodge",             "Rea", None, None),
    ("Enchanting",        "Log", None, None),
    ("Escape Artist",     "Agi", None, None),
    ("Forgery",           "Agi", None, None),
    ("Gunnery",           "Agi", None, None),
    ("Heavy Weapons",     "Agi", None, None),
    ("Instruction",       "Cha", None, None),
    ("Intimidation",      "Cha", None, None),
    ("Locksmith",         "Agi", None, None),
    ("Parachuting",       "Bod", None, None),
    ("Perception",        "Int", None, None),
    ("Pilot Aerospace*",  "Rea", None, None),
    ("Pilot Aircraft*",   "Rea", None, None),
    ("Pilot Anthroform*", "Rea", None, None),
    ("Pilot Groundcraft", "Rea", None, None),
    ("Pilot Watercraft",  "Rea", None, None),
    ("Thrown Weapons",    "Agi", None, None),
    (None,                None,  None, None),
    (None,                None,  None, None),
    (None,                None,  None, None),
    (None,                None,  None, None),
    (None,                None,  None, None),
    (None,                None,  None, "*no defaulting"),
  )
)

KNOW_SKLS_TABLE = Table(
  columns = (11,3,3,11),
  headings = ("Skill Name","Att","Rtg","Specialization"),
  anchors = ("start","middle","middle","middle"),
  data = ()
)

if __name__ == "__main__": main()
