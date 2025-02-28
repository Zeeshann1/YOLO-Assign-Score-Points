#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/12/03 16:54
# @Author  : wupenghui
# @File    : chem_properties_of_base_cou.py
import random
from . comm import *
from . comm . course_base import ConfigModel
from logger import logger
import copy
if 82 - 82: Iii1i
class CHEM_properties_of_base ( ConfigModel ) :
 if 12 - 12: i111IiI1Iii1I / OoOo
 def __init__ ( self ) :
  super ( CHEM_properties_of_base , self ) . __init__ ( )
  self . flg1_1 = False
  self . flg1_2 = False
  self . flg2_1 = False
  self . flg3 = False
  self . flg4 = False
  if 12 - 12: OOo0O0oOo0O . ooo0oOoooOOO0 * Ii1I111 + i1iiIII111
  self . background = None
  if 29 - 29: iI + o00Oo - OOoOoo000O00 * Oo0Oo - ii1I1iII1I1I . i1I1IiIIiIi1
 def hand_sth ( self , hands , sth ) :
  if hands . shape [ 0 ] != 0 and sth . shape [ 0 ] != 0 :
   for oo0O000ooO in hands :
    iIIiiIIiii1 = oo0O000ooO [ : 4 ]
    if iou ( iIIiiIIiii1 , sth [ 0 ] [ : 4 ] ) > 0 :
     return True
  return False
  if 11 - 11: ooo0O0oO00
 def container_red_liquid ( self , beaker , red_liquid ) :
  if red_liquid . shape [ 0 ] == 0 or beaker . shape [ 0 ] == 0 :
   return False
  else :
   if iou ( beaker [ 0 ] [ : 4 ] , red_liquid [ 0 ] [ : 4 ] ) > 0.75 * box_area ( red_liquid [ 0 ] [ : 4 ] ) :
    return True
    if 55 - 55: I11II1Ii % iIi
 def glass_column_beaker ( self , glass_column , beaker ) :
  if glass_column . shape [ 0 ] != 0 and beaker . shape [ 0 ] != 0 :
   glass_column [ 0 ] [ 1 ] = glass_column [ 0 ] [ 1 ] + ( glass_column [ 0 ] [ 3 ] - glass_column [ 0 ] [ 1 ] ) / 2
   if iou ( glass_column [ 0 ] [ : 4 ] , beaker [ 0 ] [ : 4 ] ) > 0 :
    return True
  else :
   return False
   if 76 - 76: i11 / iIi1Ii1i . oOooo0OOO * o00ooO0Ooooo - iIi1Ii1i
 def dropper_above_sth ( self , dropper , beaker ) :
  if dropper . shape [ 0 ] != 0 and beaker . shape [ 0 ] != 0 :
   beaker [ 0 ] [ 1 ] = 0
   if iou ( beaker [ 0 ] [ : 4 ] , dropper [ 0 ] [ : 4 ] ) > 0.6 * box_area ( dropper [ 0 ] [ : 4 ] ) :
    return True
  else :
   return False
   if 58 - 58: Ii1I111 - o00Oo
 def stir_check ( self , bbox , glass_column , beaker ) :
  if glass_column . shape [ 0 ] != 0 and beaker . shape [ 0 ] != 0 :
   oO0 = glass_column [ 0 ] [ : 4 ]
   i1iiiiIIIiIi = beaker [ 0 ] [ : 4 ]
   if iou ( oO0 , i1iiiiIIIiIi ) > 0 :
    II = min ( oO0 [ 0 ] , i1iiiiIIIiIi [ 0 ] )
    OO0000 = min ( oO0 [ 1 ] , i1iiiiIIIiIi [ 1 ] )
    oOoo0 = max ( oO0 [ 2 ] , i1iiiiIIIiIi [ 2 ] )
    Iio0 = max ( oO0 [ 3 ] , i1iiiiIIIiIi [ 3 ] )
    i1i = [ II , OO0000 , oOoo0 , Iio0 ]
    i1i = torch . Tensor ( i1i )
    for I1i in bbox :
     if iou ( I1i , i1i ) > 0 :
      return True
   return False
  return False
  if 75 - 75: o00ooO0Ooooo . ooo0O0oO00 . oOooo0OOO * i11 % Oo0Oo
 def beaker_test_tube ( self , hands , test_tube , beaker ) :
  o0OoOOo00OOO = False
  i11ii1i1I = False
  if hands . shape [ 0 ] == 2 and test_tube . shape [ 0 ] != 0 and beaker . shape [ 0 ] != 0 :
   for oo0O000ooO in hands :
    iIIiiIIiii1 = oo0O000ooO [ : 4 ]
    if iou ( iIIiiIIiii1 , test_tube [ 0 ] [ : 4 ] ) > 0 :
     o0OoOOo00OOO = True
    if iou ( iIIiiIIiii1 , beaker [ 0 ] [ : 4 ] ) > 0 :
     i11ii1i1I = True
   if o0OoOOo00OOO and i11ii1i1I :
    if iou ( beaker [ 0 ] [ : 4 ] , test_tube [ 0 ] [ : 4 ] ) > 0 :
     return True
  else :
   return False
   if 17 - 17: iI . OOoOoo000O00 + Ii1I111
 def score_process ( self , top_true , front_true , side_true ) :
  if 57 - 57: OOoOoo000O00 * i11 % iIi1Ii1i . OOo0O0oOo0O + ooo0oOoooOOO0
  if top_true or front_true or side_true :
   if front_true :
    o00 , I1i1Ii , Ooo0OO , ii1Ii1I , oo0 , i11iIii , OO , iiI1I11iiiiI , iII11iIi1iIiI , iIIiii1iI , OOO , Oo , oOoo0OO0OO0 , IiIi1Ii1111 , Ii1I1I1i , OOOO0O0ooO0O , I1iIIiI1 , OO0o0O0o0 , I111Iii1Ii = self . preds_front
    if 26 - 26: i111IiI1Iii1I . iI
    if 61 - 61: I11II1Ii . oOooo0OOO - i1I1IiIIiIi1 / i1I1IiIIiIi1 - iI
    if 19 - 19: Iii1i * ooo0O0oO00 . Ii1I111 / i11 * i111IiI1Iii1I - iIi1Ii1i
    if 32 - 32: I11II1Ii
   if top_true :
    I111II111I1I , IIi1I1I1i , O0O , II1iiii , oooOOO0OOooOO , IiIIII111 , IIIIi , O0O0oOo00oO0 , iIiIiiIIIiII , OOOoOo , I1i1i , ii1ii , Ii1iI1IIi111 , ii1iI1 , Ooo000oo0O00o , II1Ii11IiI , oO0O0oOo , OO00OOooO , o000OOoOO = self . preds_top
    if 24 - 24: ii1I1iII1I1I / Oo0Oo + o00ooO0Ooooo + o00Oo
    if 72 - 72: i11
    if 25 - 25: iI
    if 93 - 93: iIi1Ii1i - iIi / iIi * I11II1Ii
   if side_true :
    iiI1iI , O0OO00OO0O , Ooo0oO , ii1II , oOoOo , o0oOoo0O0o0Oo , IIIIiiIIi , Ii111iii1 , oo0O0 , III1II11i , iiI1iiii1iii , O0OOooO0O0Oo0 , I11iIi1i1iIi , iI11 , OO0 , O00OOo , II1Iiii111i1I , i11IIi1I1 , oOOOO0ooO = self . preds_side
    if 53 - 53: OOoOoo000O00 - i1I1IiIIiIi1 * i111IiI1Iii1I % OoOo - o00Oo + Oo0Oo
    if 15 - 15: Iii1i % iIi1Ii1i * ooo0O0oO00 - i111IiI1Iii1I
    if 25 - 25: o00ooO0Ooooo + I11II1Ii - i1iiIII111 . iIi1Ii1i + ooo0oOoooOOO0
    if 37 - 37: iIi * Iii1i . o00ooO0Ooooo * iI
    if 91 - 91: iIi1Ii1i + Iii1i
    if 71 - 71: iI . I11II1Ii . ooo0oOoooOOO0 . iIi
   if not self . scorePoint1 :
    if self . hand_sth ( o00 , ii1Ii1I ) and self . hand_sth ( o00 , OOO ) :
     self . flg1_1 = True
    if self . flg1_1 is True :
     if ii1Ii1I . shape [ 0 ] != 0 and OOO . shape [ 0 ] != 0 :
      if iou ( ii1Ii1I [ 0 ] [ : 4 ] , OOO [ 0 ] [ : 4 ] ) :
       OOOoO0oO = 0.1
       self . assignScore ( index = 1 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = OOOoO0oO ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "1.jpg" ,
 preds = self . preds_front
 )
       if 25 - 25: ooo0oOoooOOO0 % o00Oo . Oo0Oo - o00Oo % Iii1i
       if 37 - 37: oOooo0OOO + iIi % I11II1Ii / iIi % Oo0Oo + iIi1Ii1i
   if not self . scorePoint2 :
    if self . hand_sth ( o00 , ii1Ii1I ) and self . hand_sth ( o00 , I1i1Ii ) :
     if self . dropper_above_sth ( I1i1Ii , ii1Ii1I ) :
      OOOoO0oO = 0.1
      self . assignScore ( index = 2 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = OOOoO0oO ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "2.jpg" ,
 preds = self . preds_front
 )
      if 98 - 98: I11II1Ii - i1iiIII111 + iI * i1I1IiIIiIi1 % iI
      if 100 - 100: Oo0Oo . iIi * i1I1IiIIiIi1 * i1I1IiIIiIi1
   if not self . scorePoint3 :
    if self . hand_sth ( o00 , ii1Ii1I ) and self . hand_sth ( o00 , I1i1Ii ) :
     if self . dropper_above_sth ( I1i1Ii , ii1Ii1I ) :
      self . flg3 = True
    if self . flg3 is True :
     if self . hand_sth ( o00 , ii1Ii1I ) and self . hand_sth ( o00 , I1i1Ii ) is False :
      OOOoO0oO = 0.1
      self . assignScore ( index = 3 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = OOOoO0oO ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "3.jpg" ,
 preds = self . preds_front
 )
      if 85 - 85: iIi / ooo0oOoooOOO0 . oOooo0OOO % OOo0O0oOo0O + OOo0O0oOo0O - i11
      if 59 - 59: ooo0oOoooOOO0
   if not self . scorePoint4 :
    oOO = [ self . scorePoint1 , self . scorePoint2 , self . scorePoint3 ]
    oOO = np . array ( oOO )
    OoO00OO00O0o = np . sum ( oOO != 0 )
    if OoO00OO00O0o >= 3 :
     if OO0o0O0o0 . shape [ 0 ] != 0 or i11IIi1I1 . shape [ 0 ] != 0 :
      self . flg4 = True
    if self . flg4 is True :
     OOOoO0oO = 0.1
     self . assignScore ( index = 4 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = OOOoO0oO ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "4.jpg" ,
 preds = self . preds_front
 )
     if 80 - 80: iI
     if 81 - 81: iI + OoOo * OOo0O0oOo0O - OOo0O0oOo0O * Ii1I111 - OOoOoo000O00
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
