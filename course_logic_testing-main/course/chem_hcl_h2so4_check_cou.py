#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/12/03 16:54
# @Author  : wupenghui
# @File    : chem_acid_base_neutralization_reaction_cou.py
import random
from . comm import *
from . comm . course_base import ConfigModel
from logger import logger
import copy
if 82 - 82: Iii1i
class CHEM_hcl_h2so4_check ( ConfigModel ) :
 if 12 - 12: i111IiI1Iii1I / OoOo
 def __init__ ( self ) :
  super ( CHEM_hcl_h2so4_check , self ) . __init__ ( )
  if 12 - 12: OOo0O0oOo0O . ooo0oOoooOOO0 * Ii1I111 + i1iiIII111
  self . flg1_1 = False
  self . flg1_2 = False
  self . flg2_1 = False
  if 29 - 29: iI + o00Oo - OOoOoo000O00 * Oo0Oo - ii1I1iII1I1I . i1I1IiIIiIi1
  self . background = None
  if 93 - 93: iI111iiIi11i % Oo % Ooo0o
  if 11 - 11: i1I1 - O000o / O0OO0OooooOo * ii % i111IiI1Iii1I * iI
  if 9 - 9: Oo0Oo
 def hand_sth ( self , hands , sth ) :
  if hands . shape [ 0 ] != 0 and sth . shape [ 0 ] != 0 :
   for i1Ii1i in hands :
    oOooo0OOO = i1Ii1i [ : 4 ]
    if iou ( oOooo0OOO , sth [ 0 ] [ : 4 ] ) > 0 :
     return True
  return False
  if 53 - 53: i111IiI1Iii1I * OOo0O0oOo0O * i1I1IiIIiIi1 . Oo0Oo
 def container_red_liquid ( self , beaker , red_liquid ) :
  if red_liquid . shape [ 0 ] == 0 or beaker . shape [ 0 ] == 0 :
   return False
  else :
   if iou ( beaker [ 0 ] [ : 4 ] , red_liquid [ 0 ] [ : 4 ] ) > 0.75 * box_area ( red_liquid [ 0 ] [ : 4 ] ) :
    return True
    if 14 - 14: i1iiIII111 / O000o
 def glass_column_beaker ( self , glass_column , beaker ) :
  if glass_column . shape [ 0 ] != 0 and beaker . shape [ 0 ] != 0 :
   glass_column [ 0 ] [ 1 ] = glass_column [ 0 ] [ 1 ] + ( glass_column [ 0 ] [ 3 ] - glass_column [ 0 ] [ 1 ] ) / 2
   if iou ( glass_column [ 0 ] [ : 4 ] , beaker [ 0 ] [ : 4 ] ) > 0 :
    return True
  else :
   return False
   if 58 - 58: Ii1I111 - o00Oo
 def dropper_above_sth ( self , dropper , beaker ) :
  if dropper . shape [ 0 ] != 0 and beaker . shape [ 0 ] != 0 :
   beaker [ 0 ] [ 1 ] = 0
   if iou ( beaker [ 0 ] [ : 4 ] , dropper [ 0 ] [ : 4 ] ) > 0.6 * box_area ( dropper [ 0 ] [ : 4 ] ) :
    return True
  else :
   return False
   if 60 - 60: Oo . O000o
 def stir_check ( self , bbox , glass_column , beaker ) :
  if glass_column . shape [ 0 ] != 0 and beaker . shape [ 0 ] != 0 :
   i1iiiiIIIiIi = glass_column [ 0 ] [ : 4 ]
   II = beaker [ 0 ] [ : 4 ]
   if iou ( i1iiiiIIIiIi , II ) > 0 :
    OO0000 = min ( i1iiiiIIIiIi [ 0 ] , II [ 0 ] )
    oOoo0 = min ( i1iiiiIIIiIi [ 1 ] , II [ 1 ] )
    Iio0 = max ( i1iiiiIIIiIi [ 2 ] , II [ 2 ] )
    i1i = max ( i1iiiiIIIiIi [ 3 ] , II [ 3 ] )
    I1i = [ OO0000 , oOoo0 , Iio0 , i1i ]
    I1i = torch . Tensor ( I1i )
    for i1111IIi in bbox :
     if iou ( i1111IIi , I1i ) > 0 :
      return True
   return False
  return False
  if 86 - 86: iI + i1I1IiIIiIi1 + OOoOoo000O00 / Oo0Oo - Iii1i . Oo
 def beaker_test_tube ( self , hands , test_tube , beaker ) :
  ii1IiIiiII = False
  I1I111i11I = False
  if hands . shape [ 0 ] == 2 and test_tube . shape [ 0 ] != 0 and beaker . shape [ 0 ] != 0 :
   for i1Ii1i in hands :
    oOooo0OOO = i1Ii1i [ : 4 ]
    if iou ( oOooo0OOO , test_tube [ 0 ] [ : 4 ] ) > 0 :
     ii1IiIiiII = True
    if iou ( oOooo0OOO , beaker [ 0 ] [ : 4 ] ) > 0 :
     I1I111i11I = True
   if ii1IiIiiII and I1I111i11I :
    if iou ( beaker [ 0 ] [ : 4 ] , test_tube [ 0 ] [ : 4 ] ) > 0 :
     return True
  else :
   return False
   if 85 - 85: ooo0oOoooOOO0
 def score_process ( self , top_true , front_true , side_true ) :
  if 34 - 34: OOo0O0oOo0O
  if top_true or front_true or side_true :
   if front_true :
    I1i1Ii , Ooo0OO , ii1Ii1I , oo0 , i11iIii , OO , iiI1I11iiiiI , iII11iIi1iIiI , iIIiii1iI , OOO , OooOoo0OO0OO0 , IiIi1Ii1111 , Ii1I1I1i , OOOO0O0ooO0O , I1iIIiI1 , OO0o0O0o0 , I111Iii1Ii , iiIiII11i11II , o00o = self . preds_front
    if 97 - 97: iI111iiIi11i
    if 29 - 29: i1I1 * Oo
    if 7 - 7: OOo0O0oOo0O / ooo0oOoooOOO0 - i1I1 - ii % Oo0Oo
    if 97 - 97: i1I1 % O000o - Ii1I111 - Ooo0o
   if top_true :
    O0O0O , Ii1IiIII1 , iiI1 , iII , OooOO00o , OOO00000oO , IIiII11I , I11i , o0O , IiII , oOOOOOOoO , ii1i1ii , i1 , iI1i , IIIi1111iiIi1 , I1II1ii111i , I1i1iI1I1Ii1 , oOoOO0O0 , I111 = self . preds_top
    if 35 - 35: Ooo0o % iI111iiIi11i - O0OO0OooooOo * Oo0Oo + iI
    if 12 - 12: iI - O0OO0OooooOo - ii
    if 86 - 86: Iii1i + Oo0Oo - Ooo0o / i1iiIII111
    if 46 - 46: o00Oo + o00Oo % O000o
   if side_true :
    ii1 , Oo0O00OOoo , o0oO00OO , O0OO0OOOOoo0o , o00ooo0OO0000 , oOoOo , o0oOoo0O0o0Oo , IIIIiiIIi , Ii111iii1 , oo0O0 , III1II11i , iiI1iiii1iii , O0OOooO0O0Oo0 , I11iIi1i1iIi , iI11 , OO0 , O00OOo , II1Iiii111i1I , i11IIi1I1 = self . preds_side
    if 63 - 63: Ooo0o
    if 45 - 45: Oo0Oo + OOo0O0oOo0O * Oo0Oo / iI111iiIi11i
    if 89 - 89: i1I1IiIIiIi1 + i111IiI1Iii1I % OoOo - Oo0Oo
    if 33 - 33: i1I1IiIIiIi1 . Iii1i % O000o
    if 60 - 60: i1iiIII111 . ii1I1iII1I1I % Ooo0o % Oo
    if 98 - 98: i1iiIII111
   if not self . scorePoint1 :
    if self . hand_sth ( i11iIii , I1i1Ii ) and self . dropper_above_sth ( Ooo0OO , i11iIii ) :
     oO0Ooo = 0.1
     self . assignScore ( index = 1 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = oO0Ooo ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "1.jpg" ,
 preds = self . preds_front
 )
     if 81 - 81: Ii1I111 / O000o + O000o . OoOo - iI
   if not self . scorePoint1 and self . scorePoint2 :
    if II1Iiii111i1I . shape [ 0 ] != 0 or oOoOO0O0 . shape [ 0 ] != 0 and iiIiII11i11II . shape [ 0 ] != 0 :
     self . flg2_1 = True
    if self . flg2_1 :
     if o00o . shape [ 0 ] != 0 or i11IIi1I1 . shape [ 0 ] != 0 or I111 . shape [ 0 ] != 0 :
      oO0Ooo = 0.1
      self . assignScore ( index = 2 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = oO0Ooo ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "2.jpg" ,
 preds = self . preds_front
 )
      if 15 - 15: ooo0oOoooOOO0 . OOoOoo000O00 - o00Oo % iI111iiIi11i
      if 62 - 62: Oo / ooo0oOoooOOO0 % i1iiIII111 - ii
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
