#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/10/25 15:04
# @Author  : Wupenghui
# @File    : phy_plane_mirror_imaging_cou.py
if 82 - 82: Iii1i
import random
from . comm import *
from . comm . course_base import ConfigModel
from logger import logger
import copy
if 87 - 87: Ii % i1i1i1111I . Oo / OooOoo * I1Ii1I1 - I1I
if 81 - 81: i1 + ooOOO / oOo0O00 * i1iiIII111 * IiIIii11Ii
class PHY_plane_mirror_imaging ( ConfigModel ) :
 if 55 - 55: o0Oo - ii1I1iII1I1I . i1I1IiIIiIi1 % oo0O000ooO * iIIiiIIiii1
 def __init__ ( self ) :
  super ( PHY_plane_mirror_imaging , self ) . __init__ ( )
  self . score1_lock = False
  self . score2_lock = False
  self . score3_lock = False
  self . score4_lock = False
  self . score5_lock = False
  self . score6_lock = False
  self . score7_lock = False
  self . score8_lock = False
  self . score9_lock = False
  self . score10_lock = False
  if 11 - 11: ooo0O0oO00
  self . flag1 = False
  self . flag2 = False
  self . flag3 = False
  self . flag3_1 = False
  self . flag3_2 = False
  self . flag4 = False
  self . flag4_1 = False
  self . flag4_2 = False
  self . flag5 = False
  self . flag5_1 = False
  self . flag5_2 = False
  self . flag6 = False
  self . flag6_1 = False
  self . flag6_2 = False
  self . flag7 = False
  self . flag7_1 = False
  self . flag7_2 = False
  self . flag8 = False
  self . flag8_1 = False
  self . flag8_2 = False
  self . flag9 = False
  self . flag10 = False
  self . flag11 = False
  self . flag12 = False
  self . flag13 = False
  self . flag14 = False
  if 55 - 55: I11II1Ii % iIi
  self . culture_dish_top_box = None
  self . corn_beaker_top_box = None
  self . tube_count = 0
  if 76 - 76: I11II1Ii / Iii1i / Ii . i1i1i1111I / Ii
  self . scoreTime1 = time . time ( )
  self . scoreTime2 = time . time ( )
  self . scoreTime3 = time . time ( )
  self . scoreTime4 = time . time ( )
  self . scoreTime5 = time . time ( )
  self . scoreTime6 = time . time ( )
  self . scoreTime7 = time . time ( )
  self . scoreTime8 = time . time ( )
  self . lastTime = time . time ( )
  self . scorePoint6_time1 = None
  self . scorePoint10_time = 0
  self . count_score = 0
  self . score8_count = 0
  if 43 - 43: iIIiiIIiii1
 def glass_plate_candle_paper_tool ( self , glass_plate_side , candle_side , paper_side ) :
  IIi1i111IiII = glass_plate_side [ 0 ] [ : 4 ]
  i1I = candle_side [ 0 ] [ : 4 ]
  OO0o000o = candle_side [ 1 ] [ : 4 ]
  IIiiii1IiIiII = paper_side [ 0 ] [ : 4 ]
  if 32 - 32: i1I1IiIIiIi1
  if ( i1I [ 0 ] < IIi1i111IiII [ 0 ] or OO0o000o [ 0 ] < IIi1i111IiII [ 1 ] ) and ( i1I [ 0 ] > IIi1i111IiII [ 0 ] or OO0o000o [ 0 ] > IIi1i111IiII [ 0 ] ) :
   if iou ( IIiiii1IiIiII , i1I ) > 0 and iou ( IIiiii1IiIiII , OO0o000o ) > 0 :
    return True
  return False
  if 71 - 71: Ii
 def candle_glass_plate_tool ( self , candle_front , glass_plate_front ) :
  iiIII = candle_front [ 0 ] [ : 4 ]
  IioOOOO000 = candle_front [ 1 ] [ : 4 ]
  oOoo0 = glass_plate_front [ 0 ] [ : 4 ]
  if 95 - 95: i1iiIII111 . Ii . oo0O000ooO % iIIiiIIiii1 % I1Ii1I1
  if iou ( iiIII , oOoo0 ) == box_area ( iiIII ) or iou ( IioOOOO000 , oOoo0 ) == box_area ( IioOOOO000 ) :
   if iou ( iiIII , oOoo0 ) >= 0.8 * box_area ( iiIII ) or iou ( IioOOOO000 , oOoo0 ) >= 0.8 * box_area ( IioOOOO000 ) :
    return True
  return False
  if 8 - 8: I1Ii1I1 . iIi . i1 . Oo - I11II1Ii
 def measure_real_virtual ( self , paper_front , ruler_front , pen_front , hand_front ) :
  iiI1111IIi1 = False
  oOo00O = False
  if paper_front . shape [ 0 ] != 0 and ruler_front . shape [ 0 ] != 0 and pen_front . shape [ 0 ] != 0 and hand_front . shape [ 0 ] != 0 :
   if iou ( paper_front [ 0 ] [ : 4 ] , ruler_front [ 0 ] [ : 4 ] ) > 0.9 * box_area ( ruler_front [ 0 ] [ : 4 ] ) and iou ( pen_front [ 0 ] [ : 4 ] , ruler_front [ 0 ] [ : 4 ] ) > 0 :
    if 59 - 59: Iii1i . iIi - I11II1Ii
    for ii1IiIiiII in hand_front :
     I1I111i11I = ii1IiIiiII [ : 4 ]
     if iou ( I1I111i11I , pen_front [ 0 ] [ : 4 ] ) > 0 :
      iiI1111IIi1 = True
     elif iou ( I1I111i11I , ruler_front [ 0 ] [ : 4 ] ) > 0 :
      oOo00O = True
  if iiI1111IIi1 and oOo00O :
   return True
  return False
  if 85 - 85: OooOoo
 def judge_glass_plate_paper_candles ( self , glass_plate_side , candle_side , paper_side ) :
  if glass_plate_side . shape [ 0 ] != 0 and paper_side . shape [ 0 ] != 0 and candle_side . shape [ 0 ] == 2 :
   if iou ( glass_plate_side [ 0 ] [ : 4 ] , paper_side [ 0 ] [ : 4 ] ) > 0.45 * box_area ( glass_plate_side [ 0 ] [ : 4 ] ) :
    if 34 - 34: Oo
    if self . glass_plate_candle_paper_tool ( glass_plate_side , candle_side , paper_side ) is True :
     return True
  return False
  if 96 - 96: ooOOO / iIi + i1iiIII111 / ooOOO / iIIiiIIiii1
 def score1_tool ( self , glass_plate_side , paper_side ) :
  if self . score1_lock is True :
   return True
  if glass_plate_side . shape [ 0 ] != 0 and paper_side . shape [ 0 ] != 0 :
   if iou ( glass_plate_side [ 0 ] [ : 4 ] , paper_side [ 0 ] [ : 4 ] ) > 0.35 * box_area ( glass_plate_side [ 0 ] [ : 4 ] ) :
    if 63 - 63: i1i1i1111I . ii1I1iII1I1I * ooOOO
    return True
  return False
  if 6 - 6: i1iiIII111
 def score4_tool ( self , glass_plate_side , paper_side , candle_side , glass_plate_front , candle_front , paper_front ) :
  I1I1 = self . judge_glass_plate_paper_candles ( glass_plate_side , candle_side , paper_side )
  if I1I1 and candle_front . shape [ 0 ] != 0 and glass_plate_front . shape [ 0 ] != 0 and paper_front . shape [ 0 ] != 0 :
   if candle_front . shape [ 0 ] == 2 :
    if 91 - 91: Iii1i % i1i1i1111I . OooOoo * ooo0O0oO00
    if self . candle_glass_plate_tool ( candle_front , glass_plate_front ) :
     return True
   if candle_front . shape [ 0 ] == 1 :
    return True
    if 5 - 5: ooo0O0oO00 % ii1I1iII1I1I / OooOoo
 def score6_tool ( self , paper_front , ruler_front , pen_front , hand_front ) :
  if self . score6_lock is True :
   return True
  if paper_front . shape [ 0 ] != 0 and ruler_front . shape [ 0 ] != 0 and pen_front . shape [ 0 ] != 0 and hand_front . shape [ 0 ] != 0 :
   if self . measure_real_virtual ( paper_front , ruler_front , pen_front , hand_front ) :
    return True
  return False
  if 6 - 6: Ii + I1I + i1
 def score_process ( self , top_true , front_true , side_true ) :
  if 86 - 86: IiIIii11Ii
  if top_true or front_true or side_true :
   if top_true :
    oooOo , I11iIi1i , oooOOOooo , IIiII11 , OooOoo0OO0OO0 , IiIi1Ii1111 , Ii1I1I1i = self . preds_top
   if side_true :
    OOOO0O0ooO0O , I1iIIiI1 , OO0o0O0o0 , I111Iii1Ii , ii , IiII11i11II , o00o = self . preds_side
   if front_true :
    Ii11I , iIiO000O0Oo0 , Oo0O0O , Ii1IiIII1 , iiI1 , iII , OooOO00o = self . preds_front
    if 98 - 98: oo0O000ooO - IiIIii11Ii . o0Oo + ooo0O0oO00 - ooo0O0oO00
    if 78 - 78: i1 - ooOOO
    if 56 - 56: o0Oo . o0Oo + I1Ii1I1 * i1I1IiIIiIi1
    if 17 - 17: Iii1i % I11II1Ii - Iii1i % ii1I1iII1I1I . OooOoo
    if 60 - 60: ooOOO . o0Oo
    if 42 - 42: i1iiIII111 - i1iiIII111
    if 98 - 98: ii1I1iII1I1I + i1i1i1111I + Iii1i - ooo0O0oO00
    if 7 - 7: i1i1i1111I / Ii * Iii1i
    if 32 - 32: iIi . OooOoo
    if 31 - 31: Oo - I11II1Ii
    if 28 - 28: ooOOO * I1Ii1I1 + iIi % Oo
    if 100 - 100: Oo + I11II1Ii
    if 4 - 4: o0Oo % I1I - i1i1i1111I
    if 76 - 76: i1 * oOo0O00 . iIi * I11II1Ii . IiIIii11Ii . ooo0O0oO00
    if 55 - 55: i1i1i1111I + i1iiIII111 % ii1I1iII1I1I . Oo - IiIIii11Ii - i1I1IiIIiIi1
    if 91 - 91: I1Ii1I1 - iIIiiIIiii1
    if 84 - 84: ooo0O0oO00 % i1I1IiIIiIi1 - ii1I1iII1I1I
    if 94 - 94: i1iiIII111 + i1i1i1111I / i1I1IiIIiIi1 + i1I1IiIIiIi1 / I11II1Ii
    if 79 - 79: i1iiIII111 - oo0O000ooO . I1Ii1I1 + I1I - ooOOO + i1iiIII111
    if 36 - 36: ooOOO * Iii1i % I1I % i1 . ii1I1iII1I1I
    if 63 - 63: oo0O000ooO / oo0O000ooO * Iii1i - oOo0O00 . i1
    if 52 - 52: oOo0O00 / I11II1Ii * oo0O000ooO + iIIiiIIiii1 % ii1I1iII1I1I + ooo0O0oO00
    if 43 - 43: i1I1IiIIiIi1 * oOo0O00 + ooOOO
    if 30 - 30: I1I
    if 41 - 41: ooo0O0oO00
    if 98 - 98: I1I / oo0O000ooO / I11II1Ii + iIi % Oo + I1I
    if 38 - 38: I1Ii1I1 + oOo0O00
    if 2 - 2: OooOoo % Ii + ooo0O0oO00 . OooOoo + oo0O000ooO * Oo
    if 2 - 2: oo0O000ooO + i1I1IiIIiIi1 - I1Ii1I1 + ooOOO . oo0O000ooO
    if 15 - 15: o0Oo
    if 63 - 63: I11II1Ii
    if 81 - 81: OooOoo . I11II1Ii / i1i1i1111I + Oo / ii1I1iII1I1I % iIi
    if 77 - 77: iIIiiIIiii1 / i1I1IiIIiIi1 - oOo0O00 - ii1I1iII1I1I % oOo0O00
    if 73 - 73: iIi . Oo * I1I / i1i1i1111I + I1Ii1I1
    if 31 - 31: i1i1i1111I % I1Ii1I1
    if 1 - 1: iIi - oOo0O00 - i1 . oOo0O00
    if 91 - 91: i1I1IiIIiIi1 * i1 . ooOOO
    if 81 - 81: I1I * Oo - i1 % OooOoo * ooOOO
    if 19 - 19: Ii
    if 22 - 22: I11II1Ii % i1I1IiIIiIi1 + Oo
    if 60 - 60: o0Oo + iIIiiIIiii1 + oo0O000ooO % i1i1i1111I - Ii % ii1I1iII1I1I
    if 95 - 95: ooOOO % i1i1i1111I . i1
    if 87 - 87: Iii1i % ooOOO * Ii % oo0O000ooO / iIIiiIIiii1
    if 84 - 84: I1Ii1I1 + ii1I1iII1I1I % oo0O000ooO * i1i1i1111I
    if 61 - 61: i1iiIII111 - Oo + I1Ii1I1
    if 43 - 43: oo0O000ooO * o0Oo + Ii % i1I1IiIIiIi1
    if 12 - 12: i1iiIII111 + o0Oo . iIIiiIIiii1
    if 1 - 1: i1I1IiIIiIi1 % Ii - iIIiiIIiii1 / iIi + i1I1IiIIiIi1 - Ii
    if 27 - 27: OooOoo % i1I1IiIIiIi1 + oo0O000ooO
    if 16 - 16: iIi
    if 31 - 31: oOo0O00 / Iii1i % ii1I1iII1I1I % i1 . i1I1IiIIiIi1 . Oo
    if 83 - 83: oOo0O00 - iIIiiIIiii1
    if 91 - 91: oo0O000ooO - i1 - i1I1IiIIiIi1
    if 71 - 71: I1I - iIi
    if 66 - 66: i1i1i1111I / ii1I1iII1I1I + iIIiiIIiii1 + Iii1i + oOo0O00 + I11II1Ii
    if 75 - 75: OooOoo - ooo0O0oO00 - IiIIii11Ii - ooo0O0oO00 + o0Oo % i1I1IiIIiIi1
    if 42 - 42: i1 * I11II1Ii
    if 50 - 50: Ii - i1iiIII111
    if 96 - 96: o0Oo * OooOoo - Ii - OooOoo
    if 65 - 65: Oo + Oo - i1I1IiIIiIi1 % OooOoo . ii1I1iII1I1I
    if 84 - 84: oo0O000ooO . ooOOO
    if 44 - 44: o0Oo * i1i1i1111I * ooo0O0oO00 + i1iiIII111 - oo0O000ooO
    if 70 - 70: iIi
    if 9 - 9: oOo0O00 * i1
    if 96 - 96: ii1I1iII1I1I
    if not self . scorePoint1 :
     if 13 - 13: Oo * I1Ii1I1 - oOo0O00 * Ii . Ii + oOo0O00
     if 46 - 46: OooOoo - iIIiiIIiii1 / ii1I1iII1I1I
     if 73 - 73: I1Ii1I1 / i1i1i1111I / o0Oo % i1 % I11II1Ii - OooOoo
     if 30 - 30: ooOOO * ooOOO - Iii1i * i1I1IiIIiIi1
     if 37 - 37: I1Ii1I1 % i1I1IiIIiIi1 . I11II1Ii + ii1I1iII1I1I + ooOOO * i1I1IiIIiIi1
     if 39 - 39: oo0O000ooO - Oo
     if 31 - 31: IiIIii11Ii % oOo0O00 % oOo0O00 * Iii1i
     if 85 - 85: Iii1i + Ii % oo0O000ooO % oOo0O00
     if 100 - 100: IiIIii11Ii % i1
     if 82 - 82: ooOOO % OooOoo
     if 81 - 81: Ii
     if 40 - 40: I11II1Ii . OooOoo + oOo0O00 . i1iiIII111
     if 96 - 96: I1I / ooo0O0oO00 / iIIiiIIiii1 + iIIiiIIiii1
     if 35 - 35: oo0O000ooO + oOo0O00
     if 96 - 96: i1I1IiIIiIi1 . OooOoo . i1
     if 87 - 87: o0Oo * IiIIii11Ii % o0Oo . ooOOO . Oo % i1I1IiIIiIi1
     if 48 - 48: ooOOO * o0Oo % IiIIii11Ii * i1 . Iii1i - iIi
     if 72 - 72: i1 % i1i1i1111I * i1I1IiIIiIi1
     if 90 - 90: ii1I1iII1I1I * OooOoo . Ii
     if 5 - 5: Oo - i1 . ooo0O0oO00
     if 18 - 18: IiIIii11Ii - ooo0O0oO00 * I11II1Ii - OooOoo
     if 54 - 54: oo0O000ooO . ii1I1iII1I1I % Ii + IiIIii11Ii * i1I1IiIIiIi1 / i1I1IiIIiIi1
     if 31 - 31: IiIIii11Ii . IiIIii11Ii % Ii
     if 51 - 51: Oo / i1i1i1111I - I1I
     if 83 - 83: Iii1i % i1iiIII111 . OooOoo / I1I % ooo0O0oO00 . I1I
     if 76 - 76: i1iiIII111 / OooOoo
     if 77 - 77: ooOOO
     if 19 - 19: ooOOO % I1Ii1I1
     if OO0o0O0o0 . shape [ 0 ] != 0 and I111Iii1Ii . shape [ 0 ] != 0 :
      if iou ( OO0o0O0o0 [ 0 ] [ : 4 ] , I111Iii1Ii [ 0 ] [ : 4 ] ) > 0.35 * box_area ( OO0o0O0o0 [ 0 ] [ : 4 ] ) :
       if 15 - 15: OooOoo . IiIIii11Ii . I11II1Ii / Iii1i + ooOOO / Ii
       self . score1_lock = True
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
       if 58 - 58: iIi / iIIiiIIiii1 . i1I1IiIIiIi1 + Iii1i * Ii
       if 62 - 62: Oo - i1I1IiIIiIi1 - i1i1i1111I . i1iiIII111
       if 78 - 78: OooOoo . ooOOO
    if not self . scorePoint2 and self . score1_tool ( OO0o0O0o0 , I111Iii1Ii ) :
     if OOOO0O0ooO0O . shape [ 0 ] != 0 and I111Iii1Ii . shape [ 0 ] != 0 and IiII11i11II . shape [ 0 ] != 0 :
      for ii1IiIiiII in OOOO0O0ooO0O :
       I1I111i11I = ii1IiIiiII [ : 4 ]
       if iou ( I1I111i11I , IiII11i11II [ 0 ] [ : 4 ] ) > 0 :
        if iou ( IiII11i11II [ 0 ] [ : 4 ] , I111Iii1Ii [ 0 ] [ : 4 ] ) > 0 :
         self . score2_lock = True
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
         if 80 - 80: ooo0O0oO00 % i1iiIII111 * iIi - oOo0O00 % iIIiiIIiii1 - iIi
         if 56 - 56: Oo
         if 84 - 84: I1I % i1I1IiIIiIi1 - ii1I1iII1I1I / i1I1IiIIiIi1 + ii1I1iII1I1I - Oo
    if not self . scorePoint3 and self . score1_tool ( OO0o0O0o0 , I111Iii1Ii ) :
     if OO0o0O0o0 . shape [ 0 ] != 0 and I1iIIiI1 . shape [ 0 ] != 0 and I111Iii1Ii . shape [ 0 ] != 0 :
      for O0OOo0O in I1iIIiI1 :
       iiI = O0OOo0O [ : 4 ]
       if iiI [ 0 ] > OO0o0O0o0 [ 0 ] [ : 4 ] [ 0 ] :
        if iou ( iiI , I111Iii1Ii [ 0 ] [ : 4 ] ) > 0.4 * box_area ( iiI ) :
         self . score3_lock = True
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
         if 13 - 13: IiIIii11Ii * ooo0O0oO00 / I11II1Ii . ooo0O0oO00 % Oo + ii1I1iII1I1I
         if 46 - 46: Ii - iIi + IiIIii11Ii + I11II1Ii . I1I % OooOoo
         if 85 - 85: Oo / ooo0O0oO00 + Oo + ooOOO
    if not self . scorePoint4 :
     I1I1 = self . judge_glass_plate_paper_candles ( OO0o0O0o0 , I1iIIiI1 , I111Iii1Ii )
     if I1I1 and iIiO000O0Oo0 . shape [ 0 ] != 0 and Oo0O0O . shape [ 0 ] != 0 and Ii1IiIII1 . shape [ 0 ] != 0 :
      if iIiO000O0Oo0 . shape [ 0 ] == 2 :
       if 74 - 74: ooo0O0oO00 - iIi
       if self . candle_glass_plate_tool ( iIiO000O0Oo0 , Oo0O0O ) :
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
      if iIiO000O0Oo0 . shape [ 0 ] == 1 :
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
       if 79 - 79: ooo0O0oO00 * iIi . ooOOO * I1Ii1I1 . oOo0O00 + i1iiIII111
       if 45 - 45: I1Ii1I1
       if 19 - 19: o0Oo * OooOoo . Iii1i * iIIiiIIiii1 . I1I
    if not self . scorePoint5 :
     if self . judge_glass_plate_paper_candles ( OO0o0O0o0 , I1iIIiI1 , I111Iii1Ii ) is True and not self . flag5 :
      if 49 - 49: i1iiIII111 - IiIIii11Ii / i1iiIII111 + I11II1Ii
      self . flag5 = True
     if not self . flag5_1 and IiII11i11II . shape [ 0 ] != 0 and OOOO0O0ooO0O . shape [ 0 ] != 0 and OO0o0O0o0 . shape [ 0 ] != 0 and I1iIIiI1 . shape [ 0 ] != 0 :
      if 77 - 77: Ii
      for ii1IiIiiII in OOOO0O0ooO0O :
       I1I111i11I = ii1IiIiiII [ : 4 ]
       if 20 - 20: Ii % i1i1i1111I
       if 35 - 35: ii1I1iII1I1I * iIi - ii1I1iII1I1I - ooOOO
       if 28 - 28: IiIIii11Ii . Oo - I11II1Ii + iIIiiIIiii1 - oOo0O00
       for O0OOo0O in I1iIIiI1 :
        iiI = O0OOo0O [ : 4 ]
        if iou ( iiI , I1I111i11I ) > 0 and I1I111i11I [ 0 ] < OO0o0O0o0 [ 0 ] [ : 4 ] [ 0 ] :
         self . flag5_1 = True
     if not self . flag5_2 and IiII11i11II . shape [ 0 ] != 0 and OOOO0O0ooO0O . shape [ 0 ] != 0 and OO0o0O0o0 . shape [ 0 ] != 0 and I1iIIiI1 . shape [ 0 ] != 0 :
      if 6 - 6: iIi - Ii
      for ii1IiIiiII in OOOO0O0ooO0O :
       I1I111i11I = ii1IiIiiII [ : 4 ]
       if 1 - 1: I1I + OooOoo
       if 98 - 98: i1iiIII111 + Iii1i . oo0O000ooO
       if 96 - 96: OooOoo / ooo0O0oO00 - i1 * iIIiiIIiii1
       for O0OOo0O in I1iIIiI1 :
        iiI = O0OOo0O [ : 4 ]
        if iou ( iiI , I1I111i11I ) > 0 and I1I111i11I [ 0 ] > OO0o0O0o0 [ 0 ] [ : 4 ] [ 0 ] :
         self . flag5_2 = True
     if self . flag5_2 is True and self . flag5_1 is True :
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
      if 72 - 72: i1i1i1111I + Ii - Iii1i - i1i1i1111I - I11II1Ii + ii1I1iII1I1I
      if 74 - 74: ii1I1iII1I1I * Oo + Iii1i - i1iiIII111
      if 22 - 22: IiIIii11Ii - ii1I1iII1I1I . i1 . I11II1Ii - o0Oo
    if not self . scorePoint6 :
     if self . score6_tool ( Ii1IiIII1 , iiI1 , iII , Ii11I ) :
      self . score6_lock = True
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
      if 68 - 68: o0Oo
      if 40 - 40: i1 + I1Ii1I1 + iIIiiIIiii1 . Oo * iIIiiIIiii1 % I1I
      if 100 - 100: OooOoo + Oo / OooOoo
    if not self . scorePoint7 and self . score6_tool ( Ii1IiIII1 , iiI1 , iII , Ii11I ) :
     if self . judge_glass_plate_paper_candles ( OO0o0O0o0 , I1iIIiI1 , I111Iii1Ii ) :
      self . flag7_1 = True
     if self . judge_glass_plate_paper_candles ( OO0o0O0o0 , I1iIIiI1 , I111Iii1Ii ) and self . measure_real_virtual ( I111Iii1Ii , ii , IiII11i11II , OOOO0O0ooO0O ) :
      if 33 - 33: iIi / OooOoo
      self . flag7_2 = True
     if self . flag7_1 and self . flag7_2 :
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
      if 98 - 98: I1Ii1I1 . oo0O000ooO * I11II1Ii - i1I1IiIIiIi1 % I11II1Ii * iIi
      if 42 - 42: OooOoo + i1i1i1111I - i1I1IiIIiIi1 - oOo0O00 * I11II1Ii + Ii
      if 46 - 46: oOo0O00 . i1I1IiIIiIi1 - Ii . oOo0O00 + i1i1i1111I
    if not self . scorePoint8 :
     if self . score8_count == 3 :
      self . scorePoint8 = True
      Ii1iIII11i = 0.1
      self . assignScore ( index = 8 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = Ii1iIII11i ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "8.jpg" ,
 preds = self . preds_front
 )
     else :
      if self . judge_glass_plate_paper_candles ( OO0o0O0o0 , I1iIIiI1 , I111Iii1Ii ) is True and not self . flag8_1 :
       if 83 - 83: iIi
       self . flag8_1 = True
      if self . flag8_1 is True and not self . flag8_2 :
       if OOOO0O0ooO0O . shape [ 0 ] != 0 and I1iIIiI1 . shape [ 0 ] != 0 and OO0o0O0o0 . shape [ 0 ] != 0 :
        for ii1IiIiiII in OOOO0O0ooO0O :
         I1I111i11I = ii1IiIiiII [ : 4 ]
         for O0OOo0O in I1iIIiI1 :
          iiI = O0OOo0O [ : 4 ]
          if iou ( I1I111i11I , iiI ) > 0.35 * box_area ( iiI ) and iiI [ 0 ] < OO0o0O0o0 [ 0 ] [ : 4 ] [ 0 ] :
           self . flag8_2 = True
      if self . flag8_1 and self . flag8_2 :
       self . score8_count += 1
       self . flag8_1 = False
       self . flag8_2 = False
       if 77 - 77: i1I1IiIIiIi1 - ooo0O0oO00 % Ii * I11II1Ii - I1I
       if 42 - 42: iIIiiIIiii1 - Ii / Oo - i1i1i1111I + iIIiiIIiii1
       if 83 - 83: i1 . i1I1IiIIiIi1
       if 57 - 57: iIi % IiIIii11Ii / oOo0O00 + ii1I1iII1I1I - i1iiIII111
    if not self . scorePoint9 and self . count_score > 3 :
     if Ii1I1I1i . shape [ 0 ] != 0 :
      Ii1iIII11i = 0.1
      self . assignScore ( index = 9 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = Ii1iIII11i ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "9.jpg" ,
 preds = self . preds_front
 )
      if 87 - 87: i1iiIII111 . i1iiIII111 . ooo0O0oO00 . o0Oo * oOo0O00
      if 33 - 33: iIi * i1iiIII111 / I11II1Ii . OooOoo * oOo0O00 + o0Oo
      if 17 - 17: i1i1i1111I * ooo0O0oO00 + i1iiIII111 - iIIiiIIiii1 / i1i1i1111I
    if not self . scorePoint10 :
     if self . scorePoint9 is True :
      self . scorePoint10_time += 1
     if self . scorePoint10_time > 1000 :
      Ii1iIII11i = 0.1
      self . assignScore ( index = 10 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = Ii1iIII11i ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "10.jpg" ,
 preds = self . preds_front
 )
      if 83 - 83: iIIiiIIiii1 - Iii1i + oOo0O00 + I1I / oo0O000ooO + I1I
      if 29 - 29: i1i1i1111I / oOo0O00
      if 13 - 13: iIIiiIIiii1 % i1iiIII111 . OooOoo % o0Oo % OooOoo
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
