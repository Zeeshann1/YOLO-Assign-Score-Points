#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/11/30 10:04
# @Author  : wupenghui
# @File    : chem_properties_of_acids_cou.py
import random
from . comm import *
from . comm . course_base import ConfigModel
from logger import logger
import copy
if 82 - 82: Iii1i
class CHEM_properties_of_acids ( ConfigModel ) :
 if 12 - 12: i111IiI1Iii1I / OoOo
 def __init__ ( self ) :
  super ( CHEM_properties_of_acids , self ) . __init__ ( )
  if 12 - 12: OOo0O0oOo0O . ooo0oOoooOOO0 * Ii1I111 + i1iiIII111
  self . flg1_1 = False
  self . flg1_2 = False
  self . flg1_3 = False
  self . flg2 = False
  self . flg2_1 = False
  self . flg2_2 = False
  self . flg2_3 = False
  self . flg2_4 = False
  self . flg3_1 = False
  self . flg3_2 = False
  self . flg3_3 = False
  self . flg3_4 = False
  self . flg4_1 = False
  self . flg4_2 = False
  self . flg4_3 = False
  self . flg4_4 = False
  self . flg5_1 = False
  self . flg5_2 = False
  self . flg5_3 = False
  self . flg5_4 = False
  self . flg5_5 = False
  if 29 - 29: iI + o00Oo - OOoOoo000O00 * Oo0Oo - ii1I1iII1I1I . i1I1IiIIiIi1
  self . flg6_1 = False
  if 93 - 93: iI111iiIi11i % Oo % Ooo0o
  self . flg7_1 = False
  if 11 - 11: i1I1 - O000o / O0OO0OooooOo * ii % i111IiI1Iii1I * iI
  self . diff_flag = True
  self . background = None
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
   if iou ( beaker [ 0 ] [ : 4 ] , dropper [ 0 ] [ : 4 ] ) > 0.5 * box_area ( dropper [ 0 ] [ : 4 ] ) :
    return True
  else :
   return False
   if 60 - 60: Oo . O000o
 def dropper_HCHO ( self , dropper , HCHO_liquid_column ) :
  if dropper . shape [ 0 ] != 0 and HCHO_liquid_column . shape [ 0 ] != 0 :
   if iou ( dropper [ 0 ] [ : 4 ] , HCHO_liquid_column [ 0 ] [ : 4 ] ) > 0.75 * box_area ( HCHO_liquid_column [ 0 ] [ : 4 ] ) :
    return True
  else :
   return False
   if 13 - 13: O000o
 def stir_check ( self , bbox , glass_column , beaker ) :
  if glass_column . shape [ 0 ] != 0 and beaker . shape [ 0 ] != 0 :
   iiIII = glass_column [ 0 ] [ : 4 ]
   IioOOOO000 = beaker [ 0 ] [ : 4 ]
   if iou ( iiIII , IioOOOO000 ) > 0 :
    oOoo0 = min ( iiIII [ 0 ] , IioOOOO000 [ 0 ] )
    Iio0 = min ( iiIII [ 1 ] , IioOOOO000 [ 1 ] )
    i1i = max ( iiIII [ 2 ] , IioOOOO000 [ 2 ] )
    I1i = max ( iiIII [ 3 ] , IioOOOO000 [ 3 ] )
    i1111IIi = [ oOoo0 , Iio0 , i1i , I1i ]
    i1111IIi = torch . Tensor ( i1111IIi )
    for oOo00O in bbox :
     if iou ( oOo00O , i1111IIi ) > 0 :
      return True
   return False
  return False
  if 59 - 59: Iii1i . ii - O0OO0OooooOo
 def tweezers_clip_sth ( self , tweezers , sths , hands ) :
  ii1IiIiiII = False
  if tweezers . shape [ 0 ] != 0 and sths . shape [ 0 ] != 0 and hands . shape [ 0 ] != 0 :
   for i1Ii1i in hands :
    oOooo0OOO = i1Ii1i [ : 4 ]
    for I1I111i11I in sths :
     iii11i = I1I111i11I [ : 4 ]
     if iou ( iii11i , oOooo0OOO ) > 0 :
      Oo0Oo00O0OO = oOooo0OOO
      iIIiiIi1Ii1I = iii11i
      ii1IiIiiII = True
   if ii1IiIiiII :
    if 71 - 71: O000o - OOo0O0oOo0O . ooo0oOoooOOO0 . i111IiI1Iii1I % O0OO0OooooOo + O000o
    if 19 - 19: i111IiI1Iii1I / ii1I1iII1I1I + ii1I1iII1I1I . i1iiIII111
    if self . hand_sth ( hands , sths ) and ( 3 * ( iIIiiIi1Ii1I [ 2 ] - iIIiiIi1Ii1I [ 0 ] ) < ( iIIiiIi1Ii1I [ 3 ] - iIIiiIi1Ii1I [ 1 ] ) ) :
     return True
  else :
   return False
   if 88 - 88: OOo0O0oOo0O * ii1I1iII1I1I
 def tweezers_sth ( self , tweezers , bottle ) :
  if tweezers . shape [ 0 ] != 0 and bottle . shape [ 0 ] != 0 :
   oooOo = tweezers [ 0 ] [ : 4 ]
   I11iIi1i = bottle [ 0 ] [ : 4 ]
   if iou ( oooOo , I11iIi1i ) > 0.3 * box_area ( I11iIi1i ) :
    return True
  else :
   return False
   if 49 - 49: Ooo0o
 def medicinal_ladle_sth ( self , medicinal_ladle , sth ) :
  if medicinal_ladle . shape [ 0 ] != 0 and sth . shape [ 0 ] != 0 :
   if iou ( medicinal_ladle [ 0 ] [ : 4 ] , sth [ 0 ] [ : 4 ] ) > 0 :
    return True
  else :
   return False
   if 29 - 29: ii1I1iII1I1I - OOoOoo000O00
 def shake_check ( self , bbox , hands , test_tube ) :
  if hands . shape [ 0 ] != 0 and test_tube . shape [ 0 ] != 0 :
   for i1Ii1i in hands :
    oOooo0OOO = i1Ii1i [ : 4 ]
    i1 = test_tube [ 0 ] [ : 4 ]
    if iou ( i1 , oOooo0OOO ) > 0 :
     oOoo0 = min ( i1 [ 0 ] , oOooo0OOO [ 0 ] )
     Iio0 = min ( i1 [ 1 ] , oOooo0OOO [ 1 ] )
     i1i = max ( i1 [ 2 ] , oOooo0OOO [ 2 ] )
     I1i = max ( i1 [ 3 ] , oOooo0OOO [ 3 ] )
     IIiII11 = [ oOoo0 , Iio0 , i1i , I1i ]
     IIiII11 = torch . Tensor ( IIiII11 ) . cuda ( )
     for OooOoo0OO0OO0 in bbox :
      if iou ( OooOoo0OO0OO0 , IIiII11 ) > 0 :
       return True
  return False
  if 66 - 66: i1I1IiIIiIi1
 def heating_test_tube ( self , burn_alcohol_lamp , test_tube ) :
  if burn_alcohol_lamp . shape [ 0 ] != 0 and test_tube . shape [ 0 ] != 0 :
   if iou ( burn_alcohol_lamp [ 0 ] [ : 4 ] , test_tube [ 0 ] [ : 4 ] ) > 0 :
    return True
  else :
   return False
   if 74 - 74: i111IiI1Iii1I + iI111iiIi11i
 def red_liquid_test_tube ( self , red_liquid_column , test_tube ) :
  if red_liquid_column . shape [ 0 ] != 0 and test_tube . shape [ 0 ] != 0 :
   if iou ( red_liquid_column [ 0 ] [ : 4 ] , test_tube [ 0 ] [ : 4 ] ) > 0.65 * box_area ( red_liquid_column [ 0 ] [ : 4 ] ) :
    return True
  else :
   return False
   if 1 - 1: i1iiIII111 % iI111iiIi11i + Oo0Oo . Oo0Oo % OOo0O0oOo0O
 def beaker_test_tube ( self , hands , test_tube , beaker ) :
  OOOO0O0ooO0O = False
  I1iIIiI1 = False
  if hands . shape [ 0 ] == 2 and test_tube . shape [ 0 ] != 0 and beaker . shape [ 0 ] != 0 :
   for i1Ii1i in hands :
    oOooo0OOO = i1Ii1i [ : 4 ]
    if iou ( oOooo0OOO , test_tube [ 0 ] [ : 4 ] ) > 0 :
     OOOO0O0ooO0O = True
    if iou ( oOooo0OOO , beaker [ 0 ] [ : 4 ] ) > 0 :
     I1iIIiI1 = True
   if OOOO0O0ooO0O and I1iIIiI1 :
    if iou ( beaker [ 0 ] [ : 4 ] , test_tube [ 0 ] [ : 4 ] ) > 0 :
     return True
  else :
   return False
   if 78 - 78: Oo + Oo - i1iiIII111 * Ooo0o % Ii1I111 * OoOo
 def score_process ( self , top_true , front_true , side_true ) :
  if 37 - 37: ii * OoOo + OOoOoo000O00 / i1iiIII111 / ooo0oOoooOOO0
  if top_true or front_true or side_true :
   if front_true :
    iI1iI , o0OOOoo00ooOo , I1 , iiI1111II , O0OO , oO0O0oOOo0Oo , O0ooooO , iII , OooOO00o , OO , O00000oO , IIiII11I , I11i , o0O , IiII = self . preds_front
    if 42 - 42: Oo0Oo - Oo0Oo
    if 98 - 98: iI111iiIi11i + OoOo + Iii1i - O000o
    if 7 - 7: OoOo / i111IiI1Iii1I * Iii1i
   if top_true :
    i1iI1i , IIIi1111iiIi1 , I1II1ii111i , I1i1iI1I1Ii1 , oOoOO0O0 , I111 , OO00OOooO , o000OOoOO , IIIII , oooo0OO0o0 , OooOoO0oO , O0OO00OO0O , Ooo0oO , ii1II , oOoOo = self . preds_top
    if 39 - 39: O000o
    if 17 - 17: i111IiI1Iii1I . OOoOoo000O00 % ooo0oOoooOOO0
    if 82 - 82: Iii1i . OOoOoo000O00 % Ooo0o - Oo
   if side_true :
    if 44 - 44: o00Oo . Ooo0o
    iIi111ii , Iii , oOOOO0OO00 , i1iI1 , ii1ii , I11IIiiI1 , O0o , oo0o0oOo , iI11 , OO0 , O00OOo , II1Iiii111i1I , i11IIi1I1 , oOOOO0ooO , O0O0oO = self . preds_side
    if 12 - 12: Oo0Oo + i1I1IiIIiIi1 . i1I1
    if 1 - 1: Oo % i111IiI1Iii1I - i1I1 / ii + Oo - i111IiI1Iii1I
    if 27 - 27: ooo0oOoooOOO0 % Oo + Ooo0o
    if 16 - 16: ii
   if self . diff_flag :
    i1i1Ii = copy . deepcopy ( self . frame_front )
    ii1iI1I11 , OOoO0oOo0 , iII1Ii = i1i1Ii . shape
    i1i1Ii = cv2 . resize ( i1i1Ii , ( 640 , 360 ) )
    self . bbox = [ ]
    O00OoO0OOO0 = cv2 . getStructuringElement ( cv2 . MORPH_ELLIPSE , ( 9 , 4 ) )
    Oo0o0Oo = np . ones ( ( 5 , 5 ) , np . uint8 )
    o0O0OO0 = cv2 . cvtColor ( i1i1Ii , cv2 . COLOR_BGR2GRAY )
    o0O0OO0 = cv2 . GaussianBlur ( o0O0OO0 , ( 9 , 9 ) , 0 )
    if 84 - 84: i111IiI1Iii1I - ooo0oOoooOOO0
    if self . background is None :
     self . background = o0O0OO0
    oo0Oo0oO0 = cv2 . absdiff ( self . background , o0O0OO0 )
    if 20 - 20: Ooo0o
    oo0Oo0oO0 = cv2 . threshold ( oo0Oo0oO0 , 25 , 255 , cv2 . THRESH_BINARY ) [ 1 ]
    oo0Oo0oO0 = cv2 . dilate ( oo0Oo0oO0 , O00OoO0OOO0 , iterations = 2 )
    if 34 - 34: i1I1IiIIiIi1 % OoOo * Oo0Oo
    O0O0o0oo00Oo , I11 = cv2 . findContours ( oo0Oo0oO0 . copy ( ) , cv2 . RETR_EXTERNAL , cv2 . CHAIN_APPROX_SIMPLE )
    for I1Ii in O0O0o0oo00Oo :
     if 6 - 6: OOoOoo000O00 . ii1I1iII1I1I + iI111iiIi11i
     if cv2 . contourArea ( I1Ii ) < 160 :
      continue
     [ iI11iiii1I , IiiI1III1iI , oOO , OOOOoOOooO0O0 ] = cv2 . boundingRect ( I1Ii )
     [ O0 , O0Ii1Ii1 , I111i1i11iII , IiiII1Iiii1I1 ] = [ ( iI11iiii1I / 640 ) * OOoO0oOo0 , ( IiiI1III1iI / 360 ) * ii1iI1I11 , oOO * ( float ( OOoO0oOo0 / 640 ) ) ,
 OOOOoOOooO0O0 * ( float ( ii1iI1I11 / 360 ) ) ]
     if 65 - 65: o00Oo / OOoOoo000O00 - Oo0Oo
     [ oOoo0 , Iio0 , i1i , I1i ] = [ O0 , O0Ii1Ii1 , O0 + I111i1i11iII , O0Ii1Ii1 + IiiII1Iiii1I1 ]
     if torch . cuda . is_available ( ) :
      IiiOOo = torch . Tensor ( [ oOoo0 , Iio0 , i1i , I1i ] ) . cuda ( )
     else :
      IiiOOo = torch . Tensor ( [ oOoo0 , Iio0 , i1i , I1i ] )
     self . bbox . append ( IiiOOo )
   if 34 - 34: Oo . o00Oo + i1I1IiIIiIi1 % ii1I1iII1I1I * OOo0O0oOo0O
   if 87 - 87: Iii1i - ii
   if not self . scorePoint1 :
    if 72 - 72: iI % OoOo * Oo
    if 90 - 90: iI111iiIi11i * ooo0oOoooOOO0 . i111IiI1Iii1I
    if 5 - 5: OOo0O0oOo0O - iI . O000o
    if 18 - 18: ii1I1iII1I1I - O000o * O0OO0OooooOo - ooo0oOoooOOO0
    if 54 - 54: Ooo0o . iI111iiIi11i % i111IiI1Iii1I + ii1I1iII1I1I * Oo / Oo
    if 31 - 31: ii1I1iII1I1I . ii1I1iII1I1I % i111IiI1Iii1I
    if 51 - 51: OOo0O0oOo0O / OoOo - i1iiIII111
    if 83 - 83: Iii1i % Oo0Oo . ooo0oOoooOOO0 / i1iiIII111 % O000o . i1iiIII111
    if 76 - 76: Oo0Oo / ooo0oOoooOOO0
    if self . dropper_above_sth ( iiI1111II , O0OO ) and self . hand_sth ( iI1iI , o0OOOoo00ooOo ) :
     self . flg1_1 = True
    if self . flg1_1 :
     if self . dropper_above_sth ( iiI1111II , o0OOOoo00ooOo ) and self . hand_sth ( iI1iI , o0OOOoo00ooOo ) :
      self . flg1_2 = True
    if self . flg1_2 :
     if 77 - 77: o00Oo
     if 19 - 19: o00Oo % Ii1I111
     if self . dropper_above_sth ( iiI1111II , o0OOOoo00ooOo ) and self . hand_sth ( iI1iI , o0OOOoo00ooOo ) and oO0O0oOOo0Oo . shape [ 0 ] != 0 :
      self . flg1_3 = True
      if 15 - 15: ooo0oOoooOOO0 . ii1I1iII1I1I . O0OO0OooooOo / Iii1i + o00Oo / i111IiI1Iii1I
      Ii1iIII11i = 0.1
      self . assignScore ( index = 1 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = Ii1iIII11i ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "1.jpg" ,
 preds = self . preds_front
 )
      if 58 - 58: ii / i1I1 . Oo + Iii1i * i111IiI1Iii1I
      if 62 - 62: OOo0O0oOo0O - Oo - OoOo . Oo0Oo
      if 78 - 78: ooo0oOoooOOO0 . o00Oo
      if 80 - 80: O000o % Oo0Oo * ii - OOoOoo000O00 % i1I1 - ii
      if 56 - 56: OOo0O0oOo0O
   if not self . scorePoint2 :
    if self . tweezers_sth ( OooOO00o , OO ) :
     self . flg2 = True
    if self . flg2 and self . hand_sth ( iI1iI , o0OOOoo00ooOo ) :
     self . flg2_1 = True
    if self . flg2_1 :
     if self . tweezers_clip_sth ( OooOO00o , o0OOOoo00ooOo , iI1iI ) :
      self . flg2_2 = True
    if self . flg2_2 :
     if self . dropper_above_sth ( iiI1111II , O0OO ) and self . hand_sth ( iI1iI , o0OOOoo00ooOo ) :
      self . flg2_3 = True
    if self . flg2_3 :
     if self . dropper_above_sth ( iiI1111II , o0OOOoo00ooOo ) and self . hand_sth ( iI1iI , o0OOOoo00ooOo ) :
      self . flg2_4 = True
    if self . flg2_4 :
     Ii1iIII11i = 0.1
     self . assignScore ( index = 2 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = Ii1iIII11i ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "2.jpg" ,
 preds = self . preds_front
 )
     if 84 - 84: i1iiIII111 % Oo - iI111iiIi11i / Oo + iI111iiIi11i - OOo0O0oOo0O
     if 41 - 41: o00Oo + ooo0oOoooOOO0 + Ooo0o * OoOo
   if not self . scorePoint3 :
    if self . hand_sth ( iI1iI , o0OOOoo00ooOo ) and iII . shape [ 0 ] != 0 :
     self . flg3_1 = True
    if self . flg3_1 :
     if self . tweezers_clip_sth ( OooOO00o , o0OOOoo00ooOo , iI1iI ) :
      self . flg3_2 = True
    if self . flg3_2 :
     if self . dropper_above_sth ( iiI1111II , O0OO ) and self . hand_sth ( iI1iI , o0OOOoo00ooOo ) :
      self . flg3_3 = True
    if self . flg3_3 :
     if self . dropper_above_sth ( iiI1111II , o0OOOoo00ooOo ) and self . hand_sth ( iI1iI , o0OOOoo00ooOo ) :
      self . flg3_4 = True
    if self . flg3_4 :
     if self . heating_test_tube ( I11i , o0OOOoo00ooOo ) :
      Ii1iIII11i = 0.1
      self . assignScore ( index = 3 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = Ii1iIII11i ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "3.jpg" ,
 preds = self . preds_front
 )
      if 12 - 12: OoOo
      if 56 - 56: ii1I1iII1I1I
   if not self . scorePoint4 :
    if self . hand_sth ( iI1iI , o0OOOoo00ooOo ) and O00000oO . shape [ 0 ] != 0 :
     self . flg4_1 = True
    if self . flg4_1 :
     if self . medicinal_ladle_sth ( IIiII11I , o0OOOoo00ooOo ) :
      self . flg4_2 = True
    if self . flg4_2 :
     if self . dropper_above_sth ( iiI1111II , O0OO ) and self . hand_sth ( iI1iI ,
 o0OOOoo00ooOo ) :
      self . flg4_3 = True
    if self . flg4_3 :
     if self . dropper_above_sth ( iiI1111II , o0OOOoo00ooOo ) and self . hand_sth ( iI1iI , o0OOOoo00ooOo ) :
      self . flg4_4 = True
    if self . flg4_4 :
     if self . heating_test_tube ( I11i , o0OOOoo00ooOo ) :
      Ii1iIII11i = 0.1
      self . assignScore ( index = 4 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = Ii1iIII11i ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "4.jpg" ,
 preds = self . preds_front
 )
      if 17 - 17: O0OO0OooooOo . O000o % OOo0O0oOo0O + ii1I1iII1I1I - iI111iiIi11i
      if 93 - 93: OOoOoo000O00
   if not self . scorePoint5 :
    if self . hand_sth ( iI1iI , o0OOOoo00ooOo ) and self . hand_sth ( iI1iI , O0OO ) :
     self . flg5_1 = True
    if self . flg5_1 :
     if self . hand_sth ( iI1iI , o0OOOoo00ooOo ) and self . dropper_above_sth ( iiI1111II , o0OOOoo00ooOo ) :
      self . flg5_2 = True
    if self . flg5_2 and self . red_liquid_test_tube ( I1 , o0OOOoo00ooOo ) :
     self . flg5_3 = True
    if self . flg5_3 and self . dropper_above_sth ( iiI1111II , o0OOOoo00ooOo ) and self . hand_sth ( iI1iI , o0OOOoo00ooOo ) :
     self . flg5_4 = True
    if self . flg5_4 and self . shake_check ( self . bbox , iI1iI , o0OOOoo00ooOo ) :
     self . flg5_5 = True
    if self . flg5_5 and I1 . shape [ 0 ] == 0 :
     Ii1iIII11i = 0.1
     self . assignScore ( index = 5 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = Ii1iIII11i ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "5.jpg" ,
 preds = self . preds_front
 )
     if 77 - 77: OOo0O0oOo0O + i1I1 % i1iiIII111
     if 20 - 20: iI - ii1I1iII1I1I . ii1I1iII1I1I % o00Oo . iI % iI111iiIi11i
   if not self . scorePoint6 :
    if self . hand_sth ( iI1iI , o0OOOoo00ooOo ) and self . hand_sth ( iI1iI , O0OO ) :
     self . flg6_1 = True
    if self . flg6_1 and self . hand_sth ( iI1iI , o0OOOoo00ooOo ) and self . dropper_above_sth ( iiI1111II , o0OOOoo00ooOo ) :
     if 72 - 72: O000o % ii . o00Oo * Ii1I111 . o00Oo
     Ii1iIII11i = 0.1
     self . assignScore ( index = 6 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = Ii1iIII11i ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "6.jpg" ,
 preds = self . preds_front
 )
     if 90 - 90: ii1I1iII1I1I + Ii1I111 . ooo0oOoooOOO0
     if 73 - 73: OoOo - Iii1i / i1I1 . i1I1IiIIiIi1 / Oo - Oo0Oo
   if not self . scorePoint7 :
    I1I11i = [ self . scorePoint1 , self . scorePoint2 , self . scorePoint3 , self . scorePoint4 , self . scorePoint5 ,
 self . scorePoint6 ]
    I1I11i = np . array ( I1I11i )
    i1i1 = np . sum ( I1I11i != 0 )
    if i1i1 >= 3 :
     if o0O . shape [ 0 ] != 0 or oOOOO0ooO . shape [ 0 ] != 0 :
      self . flg7_1 = True
    if self . flg7_1 :
     if IiII . shape [ 0 ] != 0 or O0O0oO . shape [ 0 ] != 0 or oOoOo . shape [ 0 ] != 0 :
      Ii1iIII11i = 0.1
      self . assignScore ( index = 7 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = Ii1iIII11i ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "7.jpg" ,
 preds = self . preds_front
 )
      if 11 - 11: iI111iiIi11i - ii - Oo
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
