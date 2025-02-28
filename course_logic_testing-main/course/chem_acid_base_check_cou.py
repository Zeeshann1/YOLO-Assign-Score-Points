#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/9/17 15:04
# @Author  : Wupenghui
# @File    : chem_filter_cou.py
if 82 - 82: Iii1i
import time
import random
if 87 - 87: Ii % i1i1i1111I . Oo / OooOoo * I1Ii1I1 - I1I
import cv2
import numpy as np
import torch
if 81 - 81: i1 + ooOOO / oOo0O00 * i1iiIII111 * IiIIii11Ii
import random
from . comm import *
from . comm . course_base import ConfigModel
from logger import logger
import copy
if 84 - 84: ooo000 - Ooo0Ooo + iI1iII1I1I1i . IIiIIiIi11I1
if 98 - 98: I11iiIi11i1I % oOO
class CHEM_acid_base_check ( ConfigModel ) :
 if 63 - 63: iI1iI11Ii111
 def __init__ ( self ) :
  super ( CHEM_acid_base_check , self ) . __init__ ( )
  self . d_time = 0.
  if 26 - 26: O0OooooOo + oOO % iI1iI11Ii111 / Iii1i / Ii . i1
  self . flag1 = False
  self . flag1_1 = False
  self . flag1_2 = False
  self . flag1_3 = True
  self . flag2 = True
  self . flag2_1 = False
  self . flag2_2 = False
  self . flag3 = False
  self . flag3_1 = False
  self . flag3_1_1 = False
  self . flag3_1_2 = False
  self . flag3_2 = False
  self . flag5 = True
  self . flag5_1 = False
  self . flag5_2 = False
  self . flag5_1_1 = False
  self . flag5_1_2 = False
  self . flag7 = False
  self . flag8 = False
  self . flag8_1 = False
  self . flag8_2 = False
  self . flag9 = False
  self . flag9_1 = False
  self . flag9_2 = False
  if 9 - 9: i1iiIII111
  self . culture_dish_top_box = None
  self . corn_beaker_top_box = None
  self . tube_count = 0
  if 10 - 10: ooOOO / IIiIIiIi11I1 * oOO / iI1iI11Ii111 / iI1iI11Ii111
  self . diff_flag = True
  if 61 - 61: Ooo0Ooo - I1I
  self . background = None
  self . bbox = [ ]
  if 13 - 13: Ooo0Ooo
  self . scoreTime1 = time . time ( )
  self . scoreTime2 = time . time ( )
  self . scoreTime3 = time . time ( )
  self . scoreTime4 = time . time ( )
  self . scoreTime5 = time . time ( )
  self . scoreTime6 = time . time ( )
  self . scoreTime7 = time . time ( )
  self . scoreTime8 = time . time ( )
  self . lastTime = time . time ( )
  self . scorePoint3_time1 = None
  self . scorePoint4_time1 = None
  self . scorePoint4_time2 = None
  self . scorePoint6_time1 = None
  self . scorePoint6_time2 = None
  self . count_score = 0
  if 46 - 46: iI1iII1I1I1i - Ii * Oo * Ii
  self . count = 10000
  if 52 - 52: Oo + I1I / oOO / OooOoo - I1Ii1I1 - ooOOO
 def cork_upend_judge_flg ( self , front , top , side , mode = "cork" ) :
  if mode == "wooden_cork" :
   if top . shape [ 0 ] != 0 :
    return True
   else :
    if front . shape [ 0 ] == 0 and side . shape [ 0 ] == 0 :
     return False
    elif front . shape [ 0 ] != 0 or side . shape [ 0 ] != 0 :
     return True
  elif mode == "cork" :
   if front . shape [ 0 ] != 0 or side . shape [ 0 ] != 0 :
    return True
   elif front . shape [ 0 ] == 0 and side . shape [ 0 ] == 0 :
    return False
    if 60 - 60: iI1iII1I1I1i . oOO
    if 13 - 13: oOO
 def test_tube_dropper_loca_judge ( self , box1 , box2 , mode = "single" ) :
  if 2 - 2: i1
  if 22 - 22: IIiIIiIi11I1 - ooo000 / I1Ii1I1 . ooo000
  if 1 - 1: iI1iII1I1I1i + Ooo0Ooo + oOO * IIiIIiIi11I1
  if 20 - 20: I1I + Ii
  if 75 - 75: Ii % i1iiIII111 * Ii . IIiIIiIi11I1 % I11iiIi11i1I % I1Ii1I1
  if 8 - 8: I1Ii1I1 . O0OooooOo . i1 . Oo - iI1iI11Ii111
  if 32 - 32: Ii % i1i1i1111I % iI1iI11Ii111 - I11iiIi11i1I % i1iiIII111
  if 34 - 34: i1iiIII111 * i1
  if 34 - 34: oOo0O00 / i1iiIII111 - Iii1i . iI1iII1I1I1i
  if 80 - 80: i1i1i1111I . I1I % ooOOO % IiIIii11Ii / i1i1i1111I
  if 32 - 32: I1Ii1I1 + oOO - oOo0O00
  if 79 - 79: Iii1i % oOO * Oo + ooOOO / Oo . oOO
  if 20 - 20: O0OooooOo + i1iiIII111 / I1I
  if 88 - 88: I11iiIi11i1I + ooOOO - i1i1i1111I . Ooo0Ooo * Ii + Iii1i
  if 43 - 43: ooOOO * I1Ii1I1
  if 95 - 95: Ooo0Ooo % Iii1i % i1i1i1111I . OooOoo
  if 70 - 70: IiIIii11Ii
  if 75 - 75: Ooo0Ooo / Ii / IiIIii11Ii + IiIIii11Ii . I1I
  i1I11ii = False
  iii1II11 = box1 [ 2 ] - box1 [ 0 ]
  I1iI = box2 [ 3 ] - box2 [ 1 ]
  if I1iI > 1.5 * iii1II11 :
   i1I11ii = True
   return i1I11ii
   if 5 - 5: I1I / IiIIii11Ii - i1 + i1
 def find_hand_tube ( self , hand_front , test_tube_front ) :
  for iIIiII11 in hand_front :
   OooOoo0OO0OO0 = iIIiII11 [ : 4 ]
   for IiIi1Ii1111 in test_tube_front :
    Ii1I1I1i = IiIi1Ii1111 [ : 4 ]
    if iou ( OooOoo0OO0OO0 , Ii1I1I1i ) > 0 :
     OOOO0O0ooO0O = min ( OooOoo0OO0OO0 [ 0 ] , Ii1I1I1i [ 0 ] )
     I1iIIiI1 = min ( OooOoo0OO0OO0 [ 1 ] , Ii1I1I1i [ 1 ] )
     OO0o0O0o0 = max ( OooOoo0OO0OO0 [ 2 ] , Ii1I1I1i [ 2 ] )
     I111Iii1Ii = max ( OooOoo0OO0OO0 [ 3 ] , Ii1I1I1i [ 3 ] )
     ii = [ OOOO0O0ooO0O , I1iIIiI1 , OO0o0O0o0 , I111Iii1Ii ]
     ii = torch . Tensor ( ii )
     if 32 - 32: i1i1i1111I % Ooo0Ooo - iI1iI11Ii111 * I1I
     if 92 - 92: IIiIIiIi11I1 - i1 - Iii1i / Ooo0Ooo . I1Ii1I1 / I11iiIi11i1I
     return ii
     if 60 - 60: oOO
 def check_shake_tube_NMS ( self , bbox , real_box ) :
  for iiI1111II in bbox :
   if iou ( iiI1111II , real_box ) > 0 :
    return True
   return False
   if 79 - 79: Ooo0Ooo % iI1iII1I1I1i % IIiIIiIi11I1 / ooOOO - ooOOO / I11iiIi11i1I
 def score9_tools ( self ) :
  pass
  if 63 - 63: ooOOO / i1i1i1111I - oOo0O00 * ooOOO / i1iiIII111 + oOO
 def score11_tools ( self ) :
  pass
  if 11 - 11: i1 / ooo000
 def clean_desk_tools ( self , score1 , score2 , score3 , score4 , score5 , score6 , score7 , score8 , score9 , score10 ) :
  iII = [ score1 , score2 , score3 , score4 , score5 , score6 , score7 , score8 , score9 , score10 ]
  iII = np . array ( iII )
  OooOO00o = np . sum ( iII != 0 )
  if OooOO00o >= 6 :
   return True
  return False
  if 98 - 98: IIiIIiIi11I1 - IiIIii11Ii . ooo000 + oOO - oOO
  if 78 - 78: i1 - ooOOO
 def score_process ( self , top_true , front_true , side_true ) :
  if top_true or front_true or side_true :
   if top_true :
    OO , OoOo00oO000oo , oooOOOoOO , OOOoOo , I1i1i , ii1ii , Ii1iI1IIi111 , ii1iI1 , Ooo000oo0O00o , II1Ii11IiI , oO0O0oOo , OO00OOooO , o000OOoOO , IIIII , oooo0OO0o0 , OooOoO0oO , O0OO00OO0O , Ooo0oO , ii1II = self . preds_top
    if 93 - 93: O0OooooOo % Oo + oOo0O00 / IiIIii11Ii / I1Ii1I1
    if 39 - 39: oOO
    if 17 - 17: Ii . oOo0O00 % OooOoo
    if 82 - 82: Iii1i . oOo0O00 % IIiIIiIi11I1 - iI1iII1I1I1i
   if side_true :
    oO , oOOii1I , i1I , III1II11i , iiI1iiii1iii , O0OOooO0O0Oo0 , I11iIi1i1iIi , iI11 , OO0 , O00OOo , II1Iiii111i1I , i11IIi1I1 , oOOOO0ooO , O0O0oO , IIiI1i , OoOOooO0oOO0Oo , iiI1i1IiiiIi1 , II11IIIIiI1iI , iIIOO = self . preds_side
    if 93 - 93: iI1iI11Ii111 % IIiIIiIi11I1 * OooOoo
    if 58 - 58: IiIIii11Ii - oOO + ooo000 % i1iiIII111 - I1I
    if 90 - 90: ooo000 % i1
    if 100 - 100: i1iiIII111 . IIiIIiIi11I1 * ooo000 * ooo000
   if front_true :
    Iioo0Oo0oO0 , iII11I1iI , O0O0o0oo00Oo , I11 , I1Ii , II , Ooo0O00o , i1IIiiI1III1iI , oOOOOOOoOOooO0O0 , O0 , O0Ii1Ii1 , I111i1i11iII , IiiII1Iiii1I1 , oOO0Oo , oo00 , OOo , oO000O0O0 , ooOo00O0o0o0 , OOooooOOooo0 = self . preds_front
    if 18 - 18: IiIIii11Ii - oOO * iI1iI11Ii111 - OooOoo
    if 54 - 54: IIiIIiIi11I1 . Ooo0Ooo % Ii + IiIIii11Ii * iI1iII1I1I1i / iI1iII1I1I1i
    if 31 - 31: IiIIii11Ii . IiIIii11Ii % Ii
    if 51 - 51: Oo / i1i1i1111I - I1I
    if 83 - 83: Iii1i % i1iiIII111 . OooOoo / I1I % oOO . I1I
    if 76 - 76: i1iiIII111 / OooOoo
    if 77 - 77: ooOOO
    if 19 - 19: ooOOO % I1Ii1I1
    if 15 - 15: OooOoo . IiIIii11Ii . iI1iI11Ii111 / Iii1i + ooOOO / Ii
    if 17 - 17: I11iiIi11i1I - i1i1i1111I . iI1iII1I1I1i - I11iiIi11i1I + Oo % iI1iII1I1I1i
    if 65 - 65: Ii % I11iiIi11i1I
    if 39 - 39: Iii1i * IIiIIiIi11I1 . Ooo0Ooo - Oo
    if 63 - 63: i1i1i1111I - i1iiIII111 . OooOoo % OooOoo . O0OooooOo + iI1iI11Ii111
    if 71 - 71: ooo000 + I11iiIi11i1I % iI1iII1I1I1i + O0OooooOo % Oo - Oo
    if 84 - 84: I1I % iI1iII1I1I1i - Ooo0Ooo / iI1iII1I1I1i + Ooo0Ooo - Oo
    if 41 - 41: ooOOO + OooOoo + IIiIIiIi11I1 * i1i1i1111I
    if 12 - 12: i1i1i1111I
    if 56 - 56: IiIIii11Ii
    if 17 - 17: iI1iI11Ii111 . oOO % Oo + IiIIii11Ii - Ooo0Ooo
    if 93 - 93: oOo0O00
    if 77 - 77: Oo + I11iiIi11i1I % I1I
    if 20 - 20: i1 - IiIIii11Ii . IiIIii11Ii % ooOOO . i1 % Ooo0Ooo
    if 72 - 72: oOO % O0OooooOo . ooOOO * I1Ii1I1 . ooOOO
    if 90 - 90: IiIIii11Ii + I1Ii1I1 . OooOoo
    if 73 - 73: i1i1i1111I - Iii1i / I11iiIi11i1I . ooo000 / iI1iII1I1I1i - i1iiIII111
    if 21 - 21: i1iiIII111 + O0OooooOo % i1i1i1111I
    if 7 - 7: O0OooooOo / Ii
    if 87 - 87: ooOOO
    if 57 - 57: IIiIIiIi11I1 - iI1iII1I1I1i % ooOOO - I11iiIi11i1I / IiIIii11Ii . Ooo0Ooo
    if 15 - 15: iI1iI11Ii111 * I11iiIi11i1I - oOo0O00
    if 6 - 6: O0OooooOo - Ii
    if 1 - 1: I1I + OooOoo
    if 98 - 98: i1iiIII111 + Iii1i . IIiIIiIi11I1
    if 96 - 96: OooOoo / oOO - i1 * I11iiIi11i1I
    if 72 - 72: i1i1i1111I + Ii - Iii1i - i1i1i1111I - iI1iI11Ii111 + Ooo0Ooo
    if 74 - 74: Ooo0Ooo * Oo + Iii1i - i1iiIII111
    if 22 - 22: IiIIii11Ii - Ooo0Ooo . i1 . iI1iI11Ii111 - ooo000
    if 68 - 68: ooo000
    if 40 - 40: i1 + I1Ii1I1 + I11iiIi11i1I . Oo * I11iiIi11i1I % I1I
    if 100 - 100: OooOoo + Oo / OooOoo
    if 33 - 33: O0OooooOo / OooOoo
    if 98 - 98: I1Ii1I1 . IIiIIiIi11I1 * iI1iI11Ii111 - iI1iII1I1I1i % iI1iI11Ii111 * O0OooooOo
    if 42 - 42: OooOoo + i1i1i1111I - iI1iII1I1I1i - oOo0O00 * iI1iI11Ii111 + Ii
    if 46 - 46: oOo0O00 . iI1iII1I1I1i - Ii . oOo0O00 + i1i1i1111I
    if 83 - 83: O0OooooOo
    if 77 - 77: iI1iII1I1I1i - oOO % Ii * iI1iI11Ii111 - I1I
    if 42 - 42: I11iiIi11i1I - Ii / Oo - i1i1i1111I + I11iiIi11i1I
    if 83 - 83: i1 . iI1iII1I1I1i
    if 57 - 57: O0OooooOo % IiIIii11Ii / oOo0O00 + Ooo0Ooo - i1iiIII111
    if 87 - 87: i1iiIII111 . i1iiIII111 . oOO . ooo000 * oOo0O00
    if 33 - 33: O0OooooOo * i1iiIII111 / iI1iI11Ii111 . OooOoo * oOo0O00 + ooo000
    if 17 - 17: i1i1i1111I * oOO + i1iiIII111 - I11iiIi11i1I / i1i1i1111I
    if 83 - 83: I11iiIi11i1I - Iii1i + oOo0O00 + I1I / IIiIIiIi11I1 + I1I
    if 29 - 29: i1i1i1111I / oOo0O00
    if 13 - 13: I11iiIi11i1I % i1iiIII111 . OooOoo % ooo000 % OooOoo
    if 21 - 21: O0OooooOo * I1Ii1I1
    if 93 - 93: Ooo0Ooo . i1 + O0OooooOo - oOo0O00
    if 97 - 97: i1 - i1 % IIiIIiIi11I1 + IiIIii11Ii / iI1iI11Ii111 * iI1iII1I1I1i
    if 60 - 60: I11iiIi11i1I - Ooo0Ooo % I1Ii1I1
    if 26 - 26: ooOOO / IIiIIiIi11I1 . oOO + I11iiIi11i1I . Oo
    if 37 - 37: I1Ii1I1
    if 35 - 35: OooOoo % i1i1i1111I - iI1iII1I1I1i / IiIIii11Ii
    if 4 - 4: ooo000 . IiIIii11Ii % ooo000 / i1i1i1111I
    if 48 - 48: i1iiIII111 . Oo
    if 92 - 92: OooOoo + Ii / IIiIIiIi11I1 + OooOoo * IIiIIiIi11I1 * iI1iII1I1I1i
    if 79 - 79: i1i1i1111I
    if 3 - 3: OooOoo / O0OooooOo % I11iiIi11i1I
    if 55 - 55: oOo0O00
    if 31 - 31: Ii . Ooo0Ooo / O0OooooOo
    if 59 - 59: Oo
    if 64 - 64: Iii1i % I11iiIi11i1I * i1 % OooOoo * oOo0O00
    if 55 - 55: O0OooooOo
    if 46 - 46: Ooo0Ooo % I1Ii1I1
    if 86 - 86: I11iiIi11i1I . i1i1i1111I + oOO % I11iiIi11i1I % Iii1i % ooo000
    if 61 - 61: ooo000
    if 48 - 48: Iii1i * i1i1i1111I + IiIIii11Ii
    if 31 - 31: Oo * i1iiIII111 % Ii / oOO + I1Ii1I1 + iI1iII1I1I1i
    if 90 - 90: I1Ii1I1 * i1i1i1111I / iI1iII1I1I1i * Ii
    if 38 - 38: I1I . Ii
    if 41 - 41: ooo000 % IIiIIiIi11I1 % ooOOO
    if 5 - 5: oOo0O00 / Ii + i1iiIII111 * Oo + Ooo0Ooo + ooo000
    if 96 - 96: i1iiIII111 - IIiIIiIi11I1 / IIiIIiIi11I1 * IiIIii11Ii
    if 67 - 67: Ooo0Ooo . Ooo0Ooo . O0OooooOo
    if 24 - 24: i1iiIII111 + i1i1i1111I . oOo0O00 + iI1iII1I1I1i + O0OooooOo
    if 92 - 92: iI1iII1I1I1i / iI1iII1I1I1i + IiIIii11Ii . O0OooooOo
    if 56 - 56: Ii * ooo000 . IiIIii11Ii
    if 66 - 66: I1Ii1I1 * OooOoo . iI1iII1I1I1i % OooOoo . i1 . IiIIii11Ii
    if 47 - 47: Ii % OooOoo % iI1iII1I1I1i * IiIIii11Ii
    if 48 - 48: iI1iI11Ii111 . I11iiIi11i1I / ooo000 + i1iiIII111
    if 84 - 84: Oo / I1Ii1I1 . IIiIIiIi11I1
    if 67 - 67: Oo % ooOOO + iI1iII1I1I1i * I1I
    if 79 - 79: IIiIIiIi11I1 * Oo / OooOoo
    if 10 - 10: iI1iII1I1I1i / i1iiIII111 . IiIIii11Ii * i1i1i1111I
    if 71 - 71: oOo0O00 + I1Ii1I1 / I11iiIi11i1I + Oo / I1I
    if 18 - 18: Iii1i - IiIIii11Ii
    if 71 - 71: iI1iII1I1I1i + OooOoo % i1i1i1111I % oOo0O00 . ooo000
    if 92 - 92: I11iiIi11i1I - Ooo0Ooo - i1i1i1111I % i1iiIII111 / i1i1i1111I * iI1iII1I1I1i
    if 60 - 60: IiIIii11Ii % oOO / iI1iI11Ii111 * OooOoo / I11iiIi11i1I - Ii
    if 16 - 16: oOo0O00 / I1Ii1I1 / i1 + I11iiIi11i1I + oOo0O00
    if 11 - 11: oOO / OooOoo + oOo0O00
    if 79 - 79: I11iiIi11i1I . I1Ii1I1 * iI1iI11Ii111 % I1Ii1I1 / O0OooooOo
    if 93 - 93: iI1iI11Ii111 + Iii1i . Ii . iI1iI11Ii111 * ooOOO
    if 84 - 84: Ooo0Ooo % O0OooooOo
    if 82 - 82: IIiIIiIi11I1
    if 81 - 81: oOo0O00 + i1 - ooo000 * iI1iII1I1I1i + i1i1i1111I
    if 89 - 89: I1Ii1I1
    if 57 - 57: iI1iII1I1I1i - i1iiIII111 / OooOoo % i1iiIII111
    if 92 - 92: IiIIii11Ii * OooOoo - IiIIii11Ii
    if 66 - 66: i1iiIII111 . iI1iII1I1I1i / ooOOO . i1 - OooOoo
    if 13 - 13: oOo0O00
    if 50 - 50: i1 - i1iiIII111 / i1iiIII111 % I1Ii1I1 / IIiIIiIi11I1
    if 66 - 66: oOo0O00 - Iii1i - ooo000 . I11iiIi11i1I
    if 59 - 59: iI1iI11Ii111 / IiIIii11Ii
    if 7 - 7: oOo0O00
    if 64 - 64: IIiIIiIi11I1 * oOO + Oo . OooOoo - ooOOO
    if 94 - 94: IiIIii11Ii - ooo000 . Ii
    if 73 - 73: IiIIii11Ii / oOo0O00 % ooo000 . iI1iII1I1I1i % oOO
    if 36 - 36: O0OooooOo * OooOoo . ooo000 . i1iiIII111 + oOO
    if 47 - 47: O0OooooOo / I11iiIi11i1I
    if 52 - 52: Ii . OooOoo . i1iiIII111 * I11iiIi11i1I - iI1iII1I1I1i
    if 20 - 20: OooOoo % O0OooooOo + I1Ii1I1 + O0OooooOo - oOo0O00
    if 76 - 76: I11iiIi11i1I % IIiIIiIi11I1 % iI1iI11Ii111
    if 39 - 39: IiIIii11Ii . Oo + iI1iI11Ii111 - oOo0O00
    if 93 - 93: Iii1i * IIiIIiIi11I1 % iI1iI11Ii111 + i1 % Ii * iI1iI11Ii111
    if 62 - 62: O0OooooOo % ooo000
    if 19 - 19: Ii / Oo % Iii1i / i1iiIII111 - OooOoo - Ooo0Ooo
    if 89 - 89: I11iiIi11i1I - O0OooooOo
    if 61 - 61: Ii * OooOoo * I1I % i1iiIII111 % IIiIIiIi11I1 * I11iiIi11i1I
    if 49 - 49: iI1iII1I1I1i / i1iiIII111 % oOO
    if 46 - 46: ooOOO * IIiIIiIi11I1 % i1 / oOO + i1 + oOo0O00
    if 99 - 99: I1I * IIiIIiIi11I1 * i1iiIII111
    if 62 - 62: ooOOO % Oo + iI1iI11Ii111
    if 87 - 87: ooo000 - OooOoo + Ii + i1i1i1111I + IiIIii11Ii
    if 57 - 57: IIiIIiIi11I1 + I1I / ooOOO % ooOOO % Oo / O0OooooOo
    if 95 - 95: i1 / I11iiIi11i1I . i1 / Oo . Ooo0Ooo
    if 43 - 43: Oo - OooOoo * oOO . Ooo0Ooo / IIiIIiIi11I1 * IIiIIiIi11I1
    if 84 - 84: i1iiIII111 + oOo0O00
    if 83 - 83: i1i1i1111I
    if 84 - 84: oOO / Ii * Ooo0Ooo / Ii / ooo000
    if 64 - 64: oOo0O00 * Ii
    if 2 - 2: O0OooooOo % i1iiIII111 . oOo0O00
    if 59 - 59: I11iiIi11i1I % OooOoo - iI1iII1I1I1i % I1I + i1iiIII111 . I1Ii1I1
    if 94 - 94: ooOOO * I1Ii1I1 * i1iiIII111 . oOo0O00
    if 73 - 73: I1Ii1I1 / ooo000 % I11iiIi11i1I - i1i1i1111I + Oo - I1Ii1I1
    if 18 - 18: i1 + ooOOO . i1 - iI1iII1I1I1i
    if 97 - 97: oOo0O00 + iI1iI11Ii111 % Iii1i
    if 34 - 34: i1 + Oo . oOo0O00 - ooo000 / I11iiIi11i1I * oOo0O00
    if 89 - 89: oOo0O00
    if 48 - 48: i1 / IIiIIiIi11I1 / iI1iII1I1I1i / O0OooooOo * IiIIii11Ii
    if 54 - 54: IIiIIiIi11I1 % I1I % O0OooooOo / I11iiIi11i1I . I11iiIi11i1I - IiIIii11Ii
    if 10 - 10: Ii . I11iiIi11i1I % iI1iI11Ii111 / OooOoo % I1Ii1I1
    if 42 - 42: Oo - I1I * iI1iI11Ii111 * i1i1i1111I - I11iiIi11i1I
    if 58 - 58: iI1iII1I1I1i
    if 17 - 17: iI1iII1I1I1i - Ii % iI1iII1I1I1i % oOo0O00 * Iii1i
    if 51 - 51: I1I . i1i1i1111I % Ii
    if 55 - 55: i1i1i1111I * Ii % i1i1i1111I
    if 61 - 61: oOo0O00
    if 53 - 53: Ooo0Ooo / IiIIii11Ii
    if 49 - 49: ooo000 - oOO . IiIIii11Ii / Oo
    if 23 - 23: I11iiIi11i1I - i1 / Iii1i . iI1iII1I1I1i + oOO
    if 55 - 55: i1 - iI1iII1I1I1i / OooOoo + I1I + Oo
    if 5 - 5: O0OooooOo - i1 . i1i1i1111I / O0OooooOo . iI1iII1I1I1i . O0OooooOo
    if 87 - 87: i1 . Ii * iI1iII1I1I1i - oOO / Ii / OooOoo
    if 65 - 65: iI1iI11Ii111 / iI1iI11Ii111 + O0OooooOo
    if 99 - 99: i1 + OooOoo + I11iiIi11i1I * Ooo0Ooo / ooOOO + Ii
    if 72 - 72: I1Ii1I1 * Ooo0Ooo * IIiIIiIi11I1 % IiIIii11Ii . ooo000
    if 68 - 68: Ooo0Ooo * OooOoo - oOo0O00
    if 49 - 49: IIiIIiIi11I1 % i1
    if 29 - 29: OooOoo * Ii - oOO
    if 53 - 53: I11iiIi11i1I % ooo000 / ooOOO / I1I
    if 43 - 43: iI1iII1I1I1i . i1i1i1111I + I1I % ooOOO . O0OooooOo - O0OooooOo
    if 6 - 6: I1I
    if 98 - 98: oOO * IIiIIiIi11I1 / i1iiIII111 / Iii1i + I1I
    if 25 - 25: IIiIIiIi11I1 . O0OooooOo / I1I * i1 - i1iiIII111 % oOo0O00
    if 49 - 49: IiIIii11Ii % ooOOO + I11iiIi11i1I + IIiIIiIi11I1
    if 60 - 60: IIiIIiIi11I1
    if 98 - 98: IiIIii11Ii / Ooo0Ooo + Ii
    if 73 - 73: OooOoo * Iii1i
    if 34 - 34: iI1iI11Ii111 % Ooo0Ooo * OooOoo + i1iiIII111 / i1
    if 49 - 49: IIiIIiIi11I1 / i1iiIII111 % IIiIIiIi11I1 + IIiIIiIi11I1 * iI1iII1I1I1i
    if 22 - 22: I1Ii1I1 + oOO / I1Ii1I1 - Ii % Ii % i1i1i1111I
    if 86 - 86: Iii1i
    if 53 - 53: i1 * i1i1i1111I
    if 91 - 91: I1I . I11iiIi11i1I
    if 59 - 59: O0OooooOo . O0OooooOo * IIiIIiIi11I1
    if 85 - 85: Iii1i . oOO % Iii1i - Iii1i
    if 68 - 68: oOO + Iii1i + Ooo0Ooo % Oo / I11iiIi11i1I . OooOoo
    if 31 - 31: I11iiIi11i1I % ooOOO
    if 46 - 46: i1i1i1111I - ooo000 + iI1iII1I1I1i
    if 73 - 73: i1 * oOo0O00
    if 88 - 88: Ii
    if 12 - 12: ooo000 - IIiIIiIi11I1 % Iii1i . I1Ii1I1
    if 11 - 11: i1iiIII111 - Oo % Ii % i1
    if 28 - 28: IIiIIiIi11I1 % Ii + ooOOO . iI1iI11Ii111 % Ii * I1Ii1I1
    if 41 - 41: I1I
    if 76 - 76: ooo000 * i1i1i1111I
    if 39 - 39: i1 % iI1iI11Ii111
    if 50 - 50: i1iiIII111 % OooOoo - i1i1i1111I * IiIIii11Ii % Oo . Ooo0Ooo
    if 30 - 30: i1iiIII111
    if 78 - 78: ooo000 % Iii1i + ooOOO * IIiIIiIi11I1 - i1
    if 46 - 46: Ooo0Ooo - iI1iI11Ii111 / ooo000 * O0OooooOo . oOo0O00
    if 32 - 32: i1i1i1111I . OooOoo + OooOoo - ooo000 * IiIIii11Ii + Oo
    if 12 - 12: oOo0O00
    if 57 - 57: Oo + i1i1i1111I / I1Ii1I1
    if 56 - 56: oOO % Ooo0Ooo % Iii1i . i1i1i1111I
    if 46 - 46: O0OooooOo . i1iiIII111 % Iii1i - Ooo0Ooo + ooo000
    if 100 - 100: oOO
    if 32 - 32: I1Ii1I1 % ooo000 * OooOoo / oOo0O00 + ooOOO
    if 64 - 64: I1Ii1I1 . Ooo0Ooo
    if 36 - 36: IIiIIiIi11I1 + IiIIii11Ii . i1 + IIiIIiIi11I1
    if 77 - 77: iI1iII1I1I1i / OooOoo . Iii1i + i1iiIII111 - O0OooooOo
    if 49 - 49: i1iiIII111 - O0OooooOo - OooOoo
    if 39 - 39: I1I % i1iiIII111 - I1Ii1I1
    if 51 - 51: IIiIIiIi11I1 + i1 % i1iiIII111
    if 49 - 49: IiIIii11Ii - iI1iI11Ii111 . I1I
    if 76 - 76: oOO / iI1iII1I1I1i . I1I * oOo0O00 - i1i1i1111I
    if 53 - 53: OooOoo - oOo0O00 * ooOOO / OooOoo * Ooo0Ooo * ooo000
    if 10 - 10: IIiIIiIi11I1 % ooo000 % I11iiIi11i1I % Ooo0Ooo
    if 70 - 70: IiIIii11Ii
    if 90 - 90: i1i1i1111I % i1 . IiIIii11Ii * O0OooooOo / Ii
    if 73 - 73: ooo000 * Ooo0Ooo + Iii1i . ooOOO . I11iiIi11i1I / I11iiIi11i1I
    if 72 - 72: iI1iI11Ii111 * iI1iII1I1I1i / ooo000 + iI1iI11Ii111 - I11iiIi11i1I
    if 20 - 20: IIiIIiIi11I1 . oOo0O00 . Ooo0Ooo
    if 11 - 11: OooOoo
    if 45 - 45: iI1iII1I1I1i + I11iiIi11i1I / IIiIIiIi11I1
    if 45 - 45: iI1iII1I1I1i . iI1iII1I1I1i * i1i1i1111I + oOo0O00
    if 6 - 6: Iii1i . Oo + I1Ii1I1 * i1 * I1Ii1I1 % oOO
    if 21 - 21: Ooo0Ooo % i1 - ooo000
    if 81 - 81: Ooo0Ooo / ooo000
    if 4 - 4: I1I % iI1iI11Ii111 - ooo000 - I1I . ooOOO / i1i1i1111I
    if 74 - 74: oOO
    if 24 - 24: I1I + Oo - ooOOO
    if 86 - 86: i1iiIII111 % ooo000 % ooo000 % iI1iI11Ii111
    if 15 - 15: iI1iII1I1I1i + I1Ii1I1 % oOo0O00
    if 79 - 79: OooOoo . Oo + oOo0O00 / I1Ii1I1 . IiIIii11Ii
    if 89 - 89: ooo000 % Ooo0Ooo
    if 77 - 77: ooo000 % Ooo0Ooo
    if 24 - 24: oOO * I1Ii1I1 * I1Ii1I1 % IIiIIiIi11I1
    if 37 - 37: i1iiIII111 / iI1iII1I1I1i
    if 80 - 80: IiIIii11Ii
    if 2 - 2: I1I / oOO - IIiIIiIi11I1 % Ooo0Ooo
    if 88 - 88: iI1iII1I1I1i - I1Ii1I1 - iI1iI11Ii111 . Iii1i
    if 98 - 98: Ii + ooOOO
    if 29 - 29: I1Ii1I1 + iI1iI11Ii111 - IIiIIiIi11I1 * I11iiIi11i1I % Oo
    if 74 - 74: ooOOO
    if 100 - 100: oOO + iI1iII1I1I1i . I1I % Oo - i1
    if 39 - 39: iI1iII1I1I1i
    if 34 - 34: iI1iII1I1I1i . i1 . I1I
    if 95 - 95: IiIIii11Ii * O0OooooOo * Ooo0Ooo * O0OooooOo / OooOoo
    if 27 - 27: iI1iI11Ii111 . IiIIii11Ii
    if 69 - 69: oOO % i1iiIII111 / oOo0O00
    if 38 - 38: I11iiIi11i1I + Oo * Ooo0Ooo / ooOOO . OooOoo
    if 90 - 90: OooOoo / i1iiIII111
    if 32 - 32: IIiIIiIi11I1 - iI1iI11Ii111 / ooOOO * Ooo0Ooo * iI1iII1I1I1i - i1i1i1111I
    if 82 - 82: ooo000
    if 66 - 66: IiIIii11Ii + IIiIIiIi11I1 - iI1iI11Ii111 + i1i1i1111I . iI1iII1I1I1i * IiIIii11Ii
    if 9 - 9: I1I - I1I - ooOOO - oOo0O00 + i1iiIII111
    if 71 - 71: iI1iI11Ii111 / i1iiIII111 - Ii * Oo . iI1iII1I1I1i
    if 3 - 3: I1Ii1I1
    if 57 - 57: Ooo0Ooo . OooOoo / oOo0O00 * I1Ii1I1
    if 36 - 36: IiIIii11Ii
    if 33 - 33: IiIIii11Ii
    if 86 - 86: Ii / oOo0O00 - i1 * i1i1i1111I - Oo * Iii1i
    if 28 - 28: OooOoo . i1 % iI1iII1I1I1i % Iii1i
    if 2 - 2: Oo + OooOoo - i1i1i1111I - ooo000 / Oo . Oo
    if 41 - 41: OooOoo + OooOoo - OooOoo
    if 9 - 9: Iii1i % I1Ii1I1 % IiIIii11Ii - I1I * OooOoo
    if 53 - 53: iI1iII1I1I1i * i1i1i1111I / OooOoo . iI1iI11Ii111 . ooo000
    if 45 - 45: OooOoo + ooOOO / i1i1i1111I * i1
    if 71 - 71: O0OooooOo % Iii1i + oOo0O00 * I11iiIi11i1I / O0OooooOo
    if 66 - 66: ooo000 * oOo0O00
    if 83 - 83: i1
    if 64 - 64: i1 . O0OooooOo - I11iiIi11i1I . Iii1i
    if 47 - 47: ooo000 / Ooo0Ooo % IiIIii11Ii
    if 70 - 70: IIiIIiIi11I1 / Iii1i . i1i1i1111I % ooOOO . Ii / Ii
    if 51 - 51: I11iiIi11i1I + Ooo0Ooo - ooo000 * oOO . oOO
    if 79 - 79: i1i1i1111I + oOo0O00
    if 11 - 11: OooOoo / i1iiIII111 % iI1iI11Ii111 - i1i1i1111I * oOo0O00
    if 90 - 90: i1 * i1 . Ooo0Ooo . Oo
    if 59 - 59: Ii % I1Ii1I1 + Iii1i . OooOoo * Iii1i
    if 21 - 21: I11iiIi11i1I + ooOOO % IiIIii11Ii / OooOoo
    if 96 - 96: Oo * i1iiIII111 . Ooo0Ooo
    if 35 - 35: ooOOO . iI1iI11Ii111 * i1i1i1111I * iI1iII1I1I1i - I11iiIi11i1I
    if 47 - 47: IIiIIiIi11I1
    if 73 - 73: I1Ii1I1 + ooOOO
    if 99 - 99: iI1iI11Ii111
    if 87 - 87: i1 . I11iiIi11i1I * Ii . i1 . IIiIIiIi11I1 . IiIIii11Ii
    if 50 - 50: Ii / oOO
    if 92 - 92: Ooo0Ooo * i1iiIII111 / Ooo0Ooo / i1iiIII111 * i1i1i1111I + iI1iI11Ii111
    if 48 - 48: I11iiIi11i1I
    if 87 - 87: I1Ii1I1
    if 29 - 29: ooo000 . iI1iII1I1I1i . oOo0O00 + i1i1i1111I + oOO
    if 59 - 59: IiIIii11Ii
    if 26 - 26: oOo0O00 % O0OooooOo * i1
    if 60 - 60: IIiIIiIi11I1 % oOO / i1
    if 20 - 20: Ooo0Ooo
    if 4 - 4: IiIIii11Ii % Iii1i
    if 43 - 43: ooo000
    if 95 - 95: Oo + I11iiIi11i1I / Ooo0Ooo / Ii - ooOOO / i1i1i1111I
    if 6 - 6: Ooo0Ooo % IiIIii11Ii
    if 59 - 59: iI1iI11Ii111 . I11iiIi11i1I . ooo000 / iI1iI11Ii111 . Ii % Ooo0Ooo
    if 85 - 85: oOo0O00 / ooOOO
    if 41 - 41: i1iiIII111 * iI1iII1I1I1i + i1 + i1i1i1111I
    if 26 - 26: Oo % OooOoo
    if 14 - 14: iI1iII1I1I1i - i1iiIII111
    if 53 - 53: oOO
    if 46 - 46: oOo0O00 - iI1iII1I1I1i
    if 34 - 34: i1i1i1111I
    if 21 - 21: O0OooooOo + I1I . OooOoo + i1 . ooo000 + I11iiIi11i1I
    if 7 - 7: ooOOO + Iii1i / iI1iII1I1I1i - oOO % Oo / iI1iII1I1I1i
    if 14 - 14: Iii1i . Ii
    if 100 - 100: I1I / ooo000
    if 48 - 48: i1i1i1111I * iI1iI11Ii111 % i1i1i1111I + i1i1i1111I . iI1iII1I1I1i / OooOoo
    if 12 - 12: Ii . Ii - I1Ii1I1
    if 74 - 74: ooo000 * Iii1i - Ooo0Ooo - I1Ii1I1
    if 46 - 46: ooOOO / ooOOO
    if 58 - 58: O0OooooOo . O0OooooOo
    if 79 - 79: oOo0O00 * IIiIIiIi11I1
    if 53 - 53: Ii - ooOOO . OooOoo - I1I - I11iiIi11i1I
    if 32 - 32: Iii1i % IiIIii11Ii - oOO - IiIIii11Ii - I11iiIi11i1I % i1iiIII111
    if 50 - 50: Iii1i / O0OooooOo + i1
    if 4 - 4: IIiIIiIi11I1 . IiIIii11Ii % iI1iI11Ii111
    if 30 - 30: i1 . i1
    if 35 - 35: Ii * iI1iI11Ii111 / IiIIii11Ii - I1Ii1I1 / i1
    if 76 - 76: IiIIii11Ii * Iii1i % IiIIii11Ii
    if 73 - 73: iI1iI11Ii111 / IIiIIiIi11I1 / oOo0O00 % IIiIIiIi11I1 / Ii
    if 12 - 12: i1
    if 78 - 78: I11iiIi11i1I . IIiIIiIi11I1
    if 1 - 1: I1I % i1iiIII111 / I1Ii1I1
    if 42 - 42: Iii1i
    if 19 - 19: OooOoo * I11iiIi11i1I . i1i1i1111I + ooo000 + iI1iI11Ii111
    if 13 - 13: i1iiIII111 + I1Ii1I1 / Ooo0Ooo
    if 82 - 82: i1iiIII111 * oOO / O0OooooOo * IiIIii11Ii
    if 29 - 29: I1Ii1I1 % oOo0O00 - oOo0O00 * I1Ii1I1 / Iii1i * iI1iI11Ii111
    if 51 - 51: I1Ii1I1 . i1iiIII111 % i1 % iI1iI11Ii111 * Oo
    if 64 - 64: i1i1i1111I + i1
    if 45 - 45: i1i1i1111I / i1iiIII111 * iI1iII1I1I1i
    if 2 - 2: i1 / i1i1i1111I * IiIIii11Ii
    if 33 - 33: Iii1i
    if 7 - 7: Ooo0Ooo - Ooo0Ooo / ooo000 - IiIIii11Ii
    if 70 - 70: IIiIIiIi11I1 . i1 % iI1iII1I1I1i / i1i1i1111I
    if 5 - 5: i1iiIII111 . Oo + i1i1i1111I
    if 44 - 44: I1Ii1I1 - i1i1i1111I
    if 71 - 71: i1iiIII111
    if 77 - 77: Iii1i - I1Ii1I1 - Ooo0Ooo % Ii / Oo
    if 43 - 43: Ooo0Ooo / oOO
    if 93 - 93: ooOOO % oOo0O00 * i1 + Ii . iI1iI11Ii111 - oOO
    if 63 - 63: IiIIii11Ii . Iii1i
    if 55 - 55: oOo0O00
    if 85 - 85: IIiIIiIi11I1 % Oo / I1I . oOo0O00 / IIiIIiIi11I1 . Oo
    if 40 - 40: IIiIIiIi11I1 - ooOOO * oOO . ooo000
    if 24 - 24: IiIIii11Ii - iI1iII1I1I1i / Ii
    if 34 - 34: ooOOO - ooOOO / Ii % OooOoo
    if 97 - 97: Oo * IiIIii11Ii . Ooo0Ooo % i1 % Ii % ooo000
    if 67 - 67: IIiIIiIi11I1 % i1 % oOo0O00 - i1i1i1111I
    if 51 - 51: I11iiIi11i1I . I11iiIi11i1I % O0OooooOo % Oo / I1Ii1I1 - I1Ii1I1
    if 28 - 28: Ii / Ooo0Ooo
    if 11 - 11: I1I - OooOoo * ooOOO % i1i1i1111I + ooo000 . oOO
    if 51 - 51: ooOOO + iI1iII1I1I1i % O0OooooOo . I11iiIi11i1I % Ooo0Ooo
    if 15 - 15: OooOoo / iI1iI11Ii111 % Oo % Oo
    if 73 - 73: oOo0O00
    if 69 - 69: ooOOO - IIiIIiIi11I1 - iI1iI11Ii111
    if 78 - 78: I1Ii1I1 . ooo000 + O0OooooOo / O0OooooOo
    if 88 - 88: Ii - i1iiIII111 - i1 * IIiIIiIi11I1 . IiIIii11Ii + Iii1i
    if 44 - 44: ooOOO + Oo - i1
    if 18 - 18: iI1iII1I1I1i * ooOOO + Ooo0Ooo
    if 78 - 78: I1I . I1I - IIiIIiIi11I1 - IiIIii11Ii % I11iiIi11i1I . I1Ii1I1
    if 9 - 9: I11iiIi11i1I * OooOoo - I11iiIi11i1I
    if 73 - 73: I1Ii1I1
    if 25 - 25: i1 . Ii
    if 59 - 59: IiIIii11Ii
    if 91 - 91: IiIIii11Ii + iI1iII1I1I1i
    if 65 - 65: Oo * Iii1i * IiIIii11Ii / IIiIIiIi11I1
    if 77 - 77: IIiIIiIi11I1 / oOO % IiIIii11Ii + I1Ii1I1
    if 34 - 34: i1i1i1111I * Iii1i + Ii - iI1iI11Ii111 / i1 / i1
    if 87 - 87: Ooo0Ooo + I11iiIi11i1I
    if 3 - 3: IIiIIiIi11I1 . I1Ii1I1 / Iii1i % ooOOO / oOo0O00 % ooOOO
    if 55 - 55: iI1iII1I1I1i + I1I + oOo0O00 - I11iiIi11i1I
    if 80 - 80: Oo % I11iiIi11i1I . IiIIii11Ii * oOO
    if 83 - 83: oOo0O00 % Oo + i1i1i1111I - ooOOO + i1iiIII111
    if 36 - 36: oOo0O00 * OooOoo / I11iiIi11i1I
    if 98 - 98: O0OooooOo . ooo000
    if 85 - 85: OooOoo * Iii1i * IIiIIiIi11I1
    if 38 - 38: ooo000 - Ii - iI1iI11Ii111
    if 91 - 91: i1iiIII111 / i1 * oOO * IIiIIiIi11I1 * IiIIii11Ii
    if 65 - 65: oOO / oOo0O00 / Oo
    if 61 - 61: ooOOO * oOO
    if 98 - 98: i1iiIII111 * i1i1i1111I
    if 29 - 29: oOo0O00 / i1iiIII111 - IiIIii11Ii
    if 34 - 34: iI1iII1I1I1i + IIiIIiIi11I1 . iI1iI11Ii111 . O0OooooOo % i1i1i1111I
    if 61 - 61: Oo % ooo000
    if 68 - 68: Ii - OooOoo / I1I
    if 44 - 44: iI1iII1I1I1i % i1iiIII111 / I1Ii1I1 * i1i1i1111I
    if 63 - 63: I1Ii1I1 * Ii + Iii1i
    if 58 - 58: I1Ii1I1 / I1Ii1I1 % IIiIIiIi11I1
    if 98 - 98: OooOoo
    if 79 - 79: Ooo0Ooo * Ooo0Ooo - ooo000 - Iii1i
    if 5 - 5: IiIIii11Ii / i1iiIII111 . I1I % Iii1i . i1
    if 29 - 29: oOo0O00 + Oo / I11iiIi11i1I - oOo0O00 % i1i1i1111I / Ii
    if 39 - 39: I11iiIi11i1I - I11iiIi11i1I % i1iiIII111
    if 56 - 56: i1iiIII111 / IiIIii11Ii - I1Ii1I1 / Iii1i - i1 / OooOoo
    if 28 - 28: iI1iI11Ii111 . I1Ii1I1 % IiIIii11Ii . Ii * ooOOO - oOO
    if 80 - 80: O0OooooOo
    if 7 - 7: Iii1i . Oo . iI1iII1I1I1i - Oo - ooOOO % IIiIIiIi11I1
    if 90 - 90: Iii1i / oOo0O00
    if 54 - 54: I11iiIi11i1I . O0OooooOo + OooOoo % Oo - O0OooooOo % Oo
    if 37 - 37: Oo
    if 64 - 64: I1I % ooOOO
    if 67 - 67: Ooo0Ooo + oOo0O00
    if 21 - 21: oOO
    if 64 - 64: IIiIIiIi11I1 * i1iiIII111
    if 31 - 31: Iii1i
    if 86 - 86: Oo
    if 74 - 74: OooOoo - I11iiIi11i1I . Oo . i1 + oOo0O00 - ooOOO
    if 60 - 60: Oo
    if 23 - 23: oOo0O00
    if 47 - 47: Ooo0Ooo + Oo * Ii . OooOoo . I1Ii1I1 * i1iiIII111
    if 46 - 46: ooOOO % i1i1i1111I * i1iiIII111 + I1Ii1I1
    if 15 - 15: iI1iII1I1I1i - ooo000 + IIiIIiIi11I1 * Ooo0Ooo
    if 84 - 84: OooOoo . Ii
    if 21 - 21: Ooo0Ooo
    if 76 - 76: iI1iII1I1I1i % O0OooooOo / IiIIii11Ii - O0OooooOo
    if 4 - 4: OooOoo * IIiIIiIi11I1 - Ooo0Ooo . Ii - ooOOO . i1iiIII111
    if 2 - 2: I11iiIi11i1I * iI1iI11Ii111 * iI1iI11Ii111 * i1iiIII111 / I11iiIi11i1I % O0OooooOo
    if 13 - 13: i1 * IiIIii11Ii - ooo000 * OooOoo
    if 72 - 72: Iii1i . I1Ii1I1 * IIiIIiIi11I1 % I1Ii1I1 - i1i1i1111I
    if 97 - 97: i1 + ooOOO + I11iiIi11i1I . i1
    if 71 - 71: ooo000 - i1i1i1111I / iI1iII1I1I1i - iI1iII1I1I1i % IIiIIiIi11I1 . iI1iII1I1I1i
    if 41 - 41: IIiIIiIi11I1
    if 96 - 96: Oo . Ooo0Ooo - oOO . Iii1i % O0OooooOo . O0OooooOo
    if 82 - 82: oOO % iI1iII1I1I1i / i1iiIII111
    if 47 - 47: i1
   if self . diff_flag :
    O00O00O0Oo = copy . deepcopy ( self . frame_front )
    iI , O0O0oooOo0 , o0oooO = O00O00O0Oo . shape
    O00O00O0Oo = cv2 . resize ( O00O00O0Oo , ( 640 , 360 ) )
    self . bbox = [ ]
    I1IiI = cv2 . getStructuringElement ( cv2 . MORPH_ELLIPSE , ( 9 , 4 ) )
    iI111iIi1 = np . ones ( ( 5 , 5 ) , np . uint8 )
    II1i11i1iiI = cv2 . cvtColor ( O00O00O0Oo , cv2 . COLOR_BGR2GRAY )
    II1i11i1iiI = cv2 . GaussianBlur ( II1i11i1iiI , ( 9 , 9 ) , 0 )
    if 85 - 85: i1iiIII111 % ooo000 % O0OooooOo - i1 * ooOOO
    if self . background is None :
     self . background = II1i11i1iiI
    OOooO0 = cv2 . absdiff ( self . background , II1i11i1iiI )
    if 90 - 90: oOo0O00 % oOO * oOO + I1I * I1I / O0OooooOo
    OOooO0 = cv2 . threshold ( OOooO0 , 25 , 255 , cv2 . THRESH_BINARY ) [ 1 ]
    OOooO0 = cv2 . dilate ( OOooO0 , I1IiI , iterations = 2 )
    if 92 - 92: IiIIii11Ii * OooOoo * I1Ii1I1
    o0O0000 , Oo0ooOoo = cv2 . findContours ( OOooO0 . copy ( ) , cv2 . RETR_EXTERNAL , cv2 . CHAIN_APPROX_SIMPLE )
    for iiI1Ii in o0O0000 :
     if 8 - 8: I1I + Ii % iI1iII1I1I1i + O0OooooOo . oOO * i1
     if cv2 . contourArea ( iiI1Ii ) < 160 :
      continue
     [ o0O00oOOO0 , o0 , oOo0000O000 , iIi1ii ] = cv2 . boundingRect ( iiI1Ii )
     [ iiII1Iii , oO0oooO , iii1II11 , I1iI ] = [ ( o0O00oOOO0 / 640 ) * O0O0oooOo0 , ( o0 / 360 ) * iI , oOo0000O000 * ( float ( O0O0oooOo0 / 640 ) ) ,
 iIi1ii * ( float ( iI / 360 ) ) ]
     if 77 - 77: O0OooooOo
     [ OOOO0O0ooO0O , I1iIIiI1 , OO0o0O0o0 , I111Iii1Ii ] = [ iiII1Iii , oO0oooO , iiII1Iii + iii1II11 , oO0oooO + I1iI ]
     if torch . cuda . is_available ( ) :
      O0Oo0O0oo0o = torch . Tensor ( [ OOOO0O0ooO0O , I1iIIiI1 , OO0o0O0o0 , I111Iii1Ii ] ) . cuda ( )
     else :
      O0Oo0O0oo0o = torch . Tensor ( [ OOOO0O0ooO0O , I1iIIiI1 , OO0o0O0o0 , I111Iii1Ii ] )
     self . bbox . append ( O0Oo0O0oo0o )
     if 65 - 65: oOO - oOO
     if 52 - 52: IiIIii11Ii
     if 29 - 29: i1iiIII111 * i1iiIII111
   if not self . scorePoint1 :
    self . flag1_1 = self . cork_upend_judge_flg ( Ooo0O00o , Ii1iI1IIi111 , I11iIi1i1iIi , "cork" )
    self . flag1_2 = self . cork_upend_judge_flg ( i1IIiiI1III1iI , ii1iI1 ,
 iI11 , "wooden_cork" )
    if self . flag1_1 is True and self . flag1_2 is True and self . flag1_3 is True :
     if Iioo0Oo0oO0 . shape [ 0 ] != 0 and O0Ii1Ii1 . shape [ 0 ] != 0 :
      for iIIiII11 in Iioo0Oo0oO0 :
       OooOoo0OO0OO0 = iIIiII11 [ : 4 ]
       for O00O0 in O0Ii1Ii1 :
        iIIi111ii1II = O00O0 [ : 4 ]
        if iou ( iIIi111ii1II , OooOoo0OO0OO0 ) > 0.8 * box_area ( OooOoo0OO0OO0 ) and I111i1i11iII . shape [ 0 ] != 0 :
         if 15 - 15: oOO + oOo0O00 * I11iiIi11i1I . IiIIii11Ii
         for OOIiii11i1ii in I111i1i11iII :
          Ii1 = OOIiii11i1ii [ : 4 ]
          if iou ( iIIi111ii1II , Ii1 ) > 0.9 * box_area ( Ii1 ) :
           self . flag1_3 = False
           continue
    if self . flag1_1 is True and self . flag1_2 is True and self . flag1_3 is True :
     if oO . shape [ 0 ] != 0 and II1Iiii111i1I . shape [ 0 ] != 0 :
      for iIIiII11 in oO :
       OooOoo0OO0OO0 = iIIiII11 [ : 4 ]
       for O00O0 in II1Iiii111i1I :
        iIIi111ii1II = O00O0 [ : 4 ]
        if iou ( iIIi111ii1II , OooOoo0OO0OO0 ) > 0.8 * box_area ( OooOoo0OO0OO0 ) and i11IIi1I1 . shape [ 0 ] != 0 :
         if 90 - 90: i1i1i1111I - OooOoo * iI1iII1I1I1i . i1iiIII111 * i1i1i1111I . i1i1i1111I
         for OOIiii11i1ii in i11IIi1I1 :
          Ii1 = OOIiii11i1ii [ : 4 ]
          if iou ( iIIi111ii1II , Ii1 ) > 0.9 * box_area ( Ii1 ) :
           self . flag1_3 = False
           continue
    if self . flag1_1 is True and self . flag1_2 is True and self . flag1_3 is True :
     i1i1iI = 0.1
     self . assignScore ( index = 1 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = i1i1iI ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "1.jpg" ,
 preds = self . preds_front
 )
     if 53 - 53: ooo000 - i1iiIII111 - ooo000 . Oo
     if 69 - 69: O0OooooOo
     if 9 - 9: Ii % i1i1i1111I * I11iiIi11i1I + oOo0O00 . oOo0O00 * O0OooooOo
   if not self . scorePoint2 :
    if self . flag2 is True and Iioo0Oo0oO0 . shape [ 0 ] == 2 and I11 . shape [ 0 ] != 0 and O0Ii1Ii1 . shape [ 0 ] != 0 :
     if 12 - 12: ooo000 - Iii1i - IIiIIiIi11I1
     for iIIiII11 in Iioo0Oo0oO0 :
      OooOoo0OO0OO0 = iIIiII11 [ : 4 ]
      if iou ( OooOoo0OO0OO0 , I11 [ 0 ] [ : 4 ] ) > 0.35 * box_area ( I11 [ 0 ] [ : 4 ] ) :
       self . flag2_1 = True
      for O00O0 in O0Ii1Ii1 :
       iIIi111ii1II = O00O0 [ : 4 ]
       if iou ( OooOoo0OO0OO0 , iIIi111ii1II ) > 0.8 * box_area ( OooOoo0OO0OO0 ) :
        self . flag2_2 = True
     if self . flag2_1 is True and self . flag2_2 is True :
      for O00O0 in O0Ii1Ii1 :
       iIIi111ii1II = O00O0 [ : 4 ]
       if iou ( iIIi111ii1II , I11 [ 0 ] [ : 4 ] ) > 0 :
        i1i1iI = 0.1
        self . assignScore ( index = 2 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = i1i1iI ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "2.jpg" ,
 preds = self . preds_front
 )
        self . flag2_1 = False
        self . flag2_2 = False
        self . flag2 = False
        continue
        if 21 - 21: OooOoo / ooo000 * oOo0O00 % OooOoo * oOo0O00
    if self . flag2 is True and OO . shape [ 0 ] == 2 and OOOoOo . shape [ 0 ] != 0 and oO0O0oOo . shape [ 0 ] != 0 :
     if 87 - 87: IiIIii11Ii * oOO . OooOoo % Ii . iI1iI11Ii111 . O0OooooOo
     for iIIiII11 in OO :
      OooOoo0OO0OO0 = iIIiII11 [ : 4 ]
      if iou ( OooOoo0OO0OO0 , OOOoOo [ 0 ] [ : 4 ] ) > 0.35 * box_area ( OOOoOo [ 0 ] [ : 4 ] ) :
       self . flag2_1 = True
      for O00O0 in oO0O0oOo :
       iIIi111ii1II = O00O0 [ : 4 ]
       if iou ( OooOoo0OO0OO0 , iIIi111ii1II ) > 0.8 * box_area ( OooOoo0OO0OO0 ) :
        self . flag2_2 = True
     if self . flag2_1 is True and self . flag2_2 is True :
      for O00O0 in oO0O0oOo :
       iIIi111ii1II = O00O0 [ : 4 ]
       if iou ( iIIi111ii1II , OOOoOo [ 0 ] [ : 4 ] ) > 0 :
        i1i1iI = 0.1
        self . assignScore ( index = 2 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = i1i1iI ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "2.jpg" ,
 preds = self . preds_front
 )
        self . flag2_1 = False
        self . flag2_2 = False
        self . flag2 = False
        continue
        if 51 - 51: i1i1i1111I % I1I + IiIIii11Ii * Ooo0Ooo / I11iiIi11i1I
    if self . flag2 is True and oO . shape [ 0 ] == 2 and III1II11i . shape [ 0 ] != 0 and II1Iiii111i1I . shape [ 0 ] != 0 :
     if 19 - 19: i1 / O0OooooOo
     for iIIiII11 in oO :
      OooOoo0OO0OO0 = iIIiII11 [ : 4 ]
      if iou ( OooOoo0OO0OO0 , III1II11i [ 0 ] [ : 4 ] ) > 0.35 * box_area ( III1II11i [ 0 ] [ : 4 ] ) :
       self . flag2_1 = True
      for O00O0 in II1Iiii111i1I :
       iIIi111ii1II = O00O0 [ : 4 ]
       if iou ( OooOoo0OO0OO0 , iIIi111ii1II ) > 0.8 * box_area ( OooOoo0OO0OO0 ) :
        self . flag2_2 = True
     if self . flag2_1 is True and self . flag2_2 is True :
      for O00O0 in II1Iiii111i1I :
       iIIi111ii1II = O00O0 [ : 4 ]
       if iou ( iIIi111ii1II , III1II11i [ 0 ] [ : 4 ] ) > 0 :
        i1i1iI = 0.1
        self . assignScore ( index = 2 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = i1i1iI ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "2.jpg" ,
 preds = self . preds_front
 )
        self . flag2_1 = False
        self . flag2_2 = False
        self . flag2 = False
        continue
        if 33 - 33: I1Ii1I1 . iI1iI11Ii111
        if 7 - 7: oOO - oOo0O00 . i1i1i1111I * Oo + I1I
        if 93 - 93: i1iiIII111 - OooOoo + i1 * oOo0O00 . O0OooooOo
   if not self . scorePoint3 :
    if 9 - 9: IIiIIiIi11I1 + iI1iII1I1I1i
    if 43 - 43: oOo0O00 * iI1iI11Ii111 * iI1iI11Ii111 / IiIIii11Ii % i1iiIII111
    if 55 - 55: i1iiIII111 . i1
    if 29 - 29: Ooo0Ooo * IiIIii11Ii + i1iiIII111 / iI1iII1I1I1i - IiIIii11Ii - oOo0O00
    if 63 - 63: I1Ii1I1 . O0OooooOo * ooOOO . oOO / I1I
    if 34 - 34: i1i1i1111I * i1i1i1111I * I11iiIi11i1I . Iii1i * iI1iI11Ii111 % ooo000
    if 99 - 99: Ii / ooOOO % oOO % OooOoo - IiIIii11Ii
    if 51 - 51: oOo0O00 % OooOoo
    if 60 - 60: i1i1i1111I % IiIIii11Ii - Iii1i % i1 * O0OooooOo
    if 88 - 88: OooOoo % iI1iII1I1I1i
    if 21 - 21: iI1iI11Ii111 % OooOoo
    if 95 - 95: IiIIii11Ii - i1 . i1 - ooOOO . i1 + Ii
    if 86 - 86: IiIIii11Ii % ooo000
    if 61 - 61: Ii . i1iiIII111 * I11iiIi11i1I . ooOOO
    if 95 - 95: oOO % I1Ii1I1 % ooo000
    if 84 - 84: iI1iI11Ii111 + i1i1i1111I * ooOOO % ooo000
    if 29 - 29: IiIIii11Ii - IIiIIiIi11I1 + O0OooooOo - I11iiIi11i1I . OooOoo
    if 57 - 57: i1i1i1111I / I11iiIi11i1I
    if 83 - 83: OooOoo / I1Ii1I1 / IiIIii11Ii
    if 78 - 78: i1 . i1iiIII111 - Oo * IIiIIiIi11I1 - I1I - iI1iI11Ii111
    if 21 - 21: Iii1i - Ii / iI1iI11Ii111 / I1Ii1I1 % I11iiIi11i1I / Ii
    if 74 - 74: I1Ii1I1 . ooOOO
    if 24 - 24: O0OooooOo - Iii1i % oOo0O00 * I1I . iI1iII1I1I1i
    if 78 - 78: I1Ii1I1 - Ooo0Ooo / OooOoo % iI1iI11Ii111
    if 99 - 99: I11iiIi11i1I % ooOOO
    if 22 - 22: i1iiIII111 * O0OooooOo - i1i1i1111I % ooo000 / OooOoo - Oo
    if 3 - 3: I11iiIi11i1I % Ooo0Ooo
    if 20 - 20: I1Ii1I1 . O0OooooOo - Ii % I11iiIi11i1I % Oo
    if 12 - 12: OooOoo * oOO % Ooo0Ooo . I11iiIi11i1I
    if 54 - 54: I11iiIi11i1I . i1 - IIiIIiIi11I1
    if 99 - 99: iI1iI11Ii111 + iI1iI11Ii111 * Ooo0Ooo . OooOoo
    if 33 - 33: i1i1i1111I / O0OooooOo + Ooo0Ooo % ooOOO
    if 25 - 25: Iii1i
    if 74 - 74: I11iiIi11i1I . ooo000 . I1I * i1iiIII111 * Ooo0Ooo
    if 47 - 47: OooOoo
    if self . flag3_1 is False and I1Ii . shape [ 0 ] != 0 and Iioo0Oo0oO0 . shape [ 0 ] != 0 and O0O0o0oo00Oo . shape [ 0 ] != 0 and iII11I1iI . shape [ 0 ] != 0 :
     if 55 - 55: ooOOO % oOO + iI1iI11Ii111 - O0OooooOo + ooo000 + I1I
     for iIIiII11 in Iioo0Oo0oO0 :
      OooOoo0OO0OO0 = iIIiII11 [ : 4 ]
      if iou ( OooOoo0OO0OO0 , I1Ii [ 0 ] [ : 4 ] ) > 0.35 * box_area ( I1Ii [ 0 ] [ : 4 ] ) :
       self . flag3_1_1 = True
       if 53 - 53: IIiIIiIi11I1 % IiIIii11Ii / oOO % ooOOO - oOo0O00
      if iou ( OooOoo0OO0OO0 , iII11I1iI [ 0 ] [ : 4 ] ) > 0.25 * box_area ( iII11I1iI [ 0 ] [ : 4 ] ) :
       self . flag3_1_2 = True
       if 74 - 74: ooo000 * OooOoo * Oo
    if self . flag3_1_1 is True and self . flag3_1_2 is True and I1Ii . shape [ 0 ] != 0 and iII11I1iI . shape [ 0 ] != 0 :
     if 96 - 96: I1Ii1I1 - Oo
     if 28 - 28: i1iiIII111 - O0OooooOo % Ii * ooo000 / Iii1i
     if ( iII11I1iI [ 0 ] [ 3 ] < I1Ii [ 0 ] [ 1 ] ) :
      if self . test_tube_dropper_loca_judge ( I1Ii [ 0 ] , iII11I1iI [ 0 ] , mode = "double" ) is True :
       self . flag3 = True
       if 12 - 12: O0OooooOo - Ooo0Ooo
    if self . flag3 is True and Iioo0Oo0oO0 . shape [ 0 ] != 0 and I1Ii . shape [ 0 ] != 0 :
     if self . check_shake_tube_NMS ( self . bbox , I1Ii [ 0 ] [ : 4 ] ) is True :
      self . scorePoint4_time1 = time . time ( )
      self . flag3_1 = True
      self . flag3_2 = True
      i1i1iI = 0.1
      self . assignScore ( index = 3 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = i1i1iI ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "3.jpg" ,
 preds = self . preds_front
 )
      if 12 - 12: ooOOO
      if 29 - 29: O0OooooOo . ooo000 . ooo000
      if 79 - 79: oOo0O00 % O0OooooOo * I1Ii1I1 . IIiIIiIi11I1 * Iii1i - I1I
    elif self . flag3_1 is False and iiI1iiii1iii . shape [ 0 ] != 0 and oO . shape [ 0 ] != 0 and oOOii1I . shape [ 0 ] != 0 and i1I . shape [ 0 ] != 0 and OO . shape [ 0 ] != 0 and I1i1i . shape [ 0 ] != 0 and OoOo00oO000oo . shape [ 0 ] != 0 and oooOOOoOO . shape [ 0 ] != 0 :
     if 85 - 85: I1I + O0OooooOo . I11iiIi11i1I % i1 * O0OooooOo
     if 22 - 22: IiIIii11Ii . Iii1i / i1i1i1111I / ooo000 + ooo000 + ooo000
     if 76 - 76: Iii1i % i1i1i1111I
     pass
     if 12 - 12: oOO + IiIIii11Ii % ooOOO + O0OooooOo / I1I
     if 59 - 59: Iii1i % I1Ii1I1 + I11iiIi11i1I - Oo
     if 72 - 72: I11iiIi11i1I
   if not self . scorePoint4 and self . scorePoint3 is True :
    self . scorePoint4_time2 = time . time ( )
    if ( self . scorePoint4_time2 - self . scorePoint4_time1 ) > 6.5 :
     i1i1iI = 0.1
     self . assignScore ( index = 4 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = i1i1iI ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "4.jpg" ,
 preds = self . preds_front
 )
     if 38 - 38: I11iiIi11i1I . oOO + iI1iI11Ii111
     if 33 - 33: ooo000 - IIiIIiIi11I1 % i1iiIII111 / iI1iII1I1I1i - Iii1i % IIiIIiIi11I1
     if 15 - 15: ooo000 . i1 * i1
   if not self . scorePoint5 :
    if 41 - 41: I11iiIi11i1I + Iii1i % ooOOO * i1
    if 37 - 37: ooo000
    if 87 - 87: i1i1i1111I + I1Ii1I1 % i1iiIII111 - I1I + ooOOO % I1Ii1I1
    if 96 - 96: IIiIIiIi11I1 / I1I * i1 / I1I + I1I / i1
    if 80 - 80: Oo / i1i1i1111I . IIiIIiIi11I1
    if 79 - 79: oOO
    if 6 - 6: O0OooooOo + IIiIIiIi11I1 + ooOOO % IIiIIiIi11I1
    if 24 - 24: ooo000 + iI1iI11Ii111 / Ii / Ooo0Ooo % IIiIIiIi11I1
    if 70 - 70: I11iiIi11i1I
    if 45 - 45: I1Ii1I1 * Oo - I11iiIi11i1I * iI1iII1I1I1i
    if 41 - 41: Iii1i . I1I * iI1iI11Ii111 - i1iiIII111 . O0OooooOo + ooOOO
    if 24 - 24: i1 + IIiIIiIi11I1 + i1iiIII111 % I1Ii1I1 + IIiIIiIi11I1
    if 55 - 55: IiIIii11Ii - IiIIii11Ii
    if 52 - 52: I1Ii1I1 - OooOoo % iI1iI11Ii111
    if 88 - 88: ooOOO . i1
    if 72 - 72: I1I - OooOoo / Iii1i - I1Ii1I1
    if 54 - 54: I11iiIi11i1I / i1iiIII111 % oOo0O00 - ooOOO
    if 72 - 72: ooo000 . I1Ii1I1 . I1I . IIiIIiIi11I1 + Oo
    if 58 - 58: ooOOO + IiIIii11Ii + oOO % IiIIii11Ii + Ooo0Ooo . Oo
    if 45 - 45: I1I % iI1iI11Ii111 % oOO * oOo0O00 / i1iiIII111 + I11iiIi11i1I
    if 63 - 63: i1i1i1111I - O0OooooOo - iI1iII1I1I1i + OooOoo * i1iiIII111 / Ooo0Ooo
    if 81 - 81: ooo000 % i1i1i1111I . i1iiIII111 / i1iiIII111 / i1iiIII111
    if 84 - 84: ooOOO * ooo000 % ooOOO
    if 57 - 57: iI1iI11Ii111 * iI1iII1I1I1i % Ooo0Ooo
    if 22 - 22: OooOoo . i1
    if 85 - 85: i1i1i1111I * I1Ii1I1 / ooo000
    if 14 - 14: i1i1i1111I
    if 61 - 61: Iii1i . I11iiIi11i1I - Oo . O0OooooOo + OooOoo
    if 11 - 11: oOo0O00 - i1 / oOo0O00 * OooOoo - I11iiIi11i1I / I1Ii1I1
    if 4 - 4: IiIIii11Ii
    if 42 - 42: oOO - oOO + OooOoo - oOO
    if 23 - 23: iI1iII1I1I1i % iI1iI11Ii111 * I11iiIi11i1I - oOO * oOo0O00
    if 45 - 45: i1 % iI1iII1I1I1i . IiIIii11Ii + Ooo0Ooo
    if 34 - 34: Iii1i + Iii1i
    if self . flag5_1 is False and I1Ii . shape [ 0 ] != 0 and Iioo0Oo0oO0 . shape [ 0 ] != 0 and O0O0o0oo00Oo . shape [ 0 ] != 0 and iII11I1iI . shape [ 0 ] != 0 :
     if 67 - 67: oOo0O00 + IIiIIiIi11I1
     for iIIiII11 in Iioo0Oo0oO0 :
      OooOoo0OO0OO0 = iIIiII11 [ : 4 ]
      if iou ( OooOoo0OO0OO0 , I1Ii [ 0 ] [ : 4 ] ) > 0.35 * box_area ( I1Ii [ 0 ] [ : 4 ] ) :
       self . flag5_1_1 = True
      if iou ( OooOoo0OO0OO0 , iII11I1iI [ 0 ] [ : 4 ] ) > 0.25 * box_area ( iII11I1iI [ 0 ] [ : 4 ] ) :
       self . flag5_1_2 = True
       if 69 - 69: IIiIIiIi11I1
     if self . flag5_1_1 is True and self . flag5_1_2 is True and I1Ii . shape [ 0 ] != 0 and iII11I1iI . shape [ 0 ] != 0 :
      if ( iII11I1iI [ 0 ] [ 3 ] < I1Ii [ 0 ] [ 1 ] ) :
       if self . test_tube_dropper_loca_judge ( I1Ii [ 0 ] , iII11I1iI [ 0 ] ,
 mode = "double" ) is True :
        self . flag5 = True
        if 97 - 97: Iii1i + oOo0O00 - i1 % Iii1i
     if self . flag3 is True and Iioo0Oo0oO0 . shape [ 0 ] != 0 and I1Ii . shape [ 0 ] != 0 :
      if self . check_shake_tube_NMS ( self . bbox , I1Ii [ 0 ] [ : 4 ] ) is True :
       self . scorePoint4_time1 = time . time ( )
       self . flag3_1 = True
       self . flag3_2 = True
       i1i1iI = 0.1
       self . assignScore ( index = 3 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = i1i1iI ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "3.jpg" ,
 preds = self . preds_front
 )
       if 71 - 71: Ooo0Ooo / Ooo0Ooo % ooo000
     if self . flag5 is True and Iioo0Oo0oO0 . shape [ 0 ] != 0 and I1Ii . shape [ 0 ] != 0 :
      if self . check_shake_tube_NMS ( self . bbox , I1Ii [ 0 ] [ : 4 ] ) is True :
       self . scorePoint6_time1 = time . time ( )
       self . flag5_1 = True
       self . flag5_2 = True
       i1i1iI = 0.1
       self . assignScore ( index = 5 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = i1i1iI ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "5.jpg" ,
 preds = self . preds_front
 )
       if 32 - 32: ooo000 * ooo000
    elif self . flag5_1 is False and iiI1iiii1iii . shape [ 0 ] != 0 and oO . shape [ 0 ] != 0 and oOOii1I . shape [ 0 ] != 0 and i1I . shape [ 0 ] != 0 and OO . shape [ 0 ] != 0 and I1i1i . shape [ 0 ] != 0 and OoOo00oO000oo . shape [ 0 ] != 0 and oooOOOoOO . shape [ 0 ] != 0 :
     if 29 - 29: Ooo0Ooo . i1 * I11iiIi11i1I
     if 98 - 98: ooOOO * oOO + Ooo0Ooo + i1i1i1111I / I1Ii1I1
     if 18 - 18: iI1iII1I1I1i . iI1iII1I1I1i % ooOOO
     pass
     if 90 - 90: I1I - Iii1i + Ii / Iii1i % I1Ii1I1
     if 14 - 14: OooOoo + iI1iII1I1I1i * Iii1i
     if 30 - 30: OooOoo
   if not self . scorePoint6 and self . scorePoint5 is True :
    self . scorePoint6_time2 = time . time ( )
    if ( self . scorePoint6_time2 - self . scorePoint6_time1 ) > 6.5 :
     i1i1iI = 0.1
     self . assignScore ( index = 6 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = i1i1iI ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "6.jpg" ,
 preds = self . preds_front
 )
     if 2 - 2: i1iiIII111 / oOo0O00 - IiIIii11Ii - iI1iII1I1I1i
     if 90 - 90: i1iiIII111
     if 11 - 11: ooOOO . ooo000
   if not self . scorePoint7 :
    if self . flag7 is False and II . shape [ 0 ] != 0 and O0Ii1Ii1 . shape [ 0 ] != 0 and Iioo0Oo0oO0 . shape [ 0 ] != 0 :
     if 10 - 10: I1Ii1I1 - ooOOO / Iii1i - i1 . ooo000
     for iIIiII11 in Iioo0Oo0oO0 :
      OooOoo0OO0OO0 = iIIiII11 [ : 4 ]
      if iou ( OooOoo0OO0OO0 , II [ 0 ] [ : 4 ] ) > 0 :
       self . flag7 = True
    if self . flag7 is True and II . shape [ 0 ] != 0 and O0Ii1Ii1 . shape [ 0 ] != 0 :
     if iou ( II [ 0 ] [ : 4 ] , O0Ii1Ii1 [ 0 ] [ : 4 ] ) > 0 :
      if 99 - 99: Ii / iI1iII1I1I1i / Oo * I11iiIi11i1I
      if 86 - 86: ooo000 - oOo0O00
      self . scorePoint7 = True
      self . diff_flag = False
      i1i1iI = 0.1
      self . assignScore ( index = 7 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = i1i1iI ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "7.jpg" ,
 preds = self . preds_front
 )
    if self . flag7 is False and ii1ii . shape [ 0 ] != 0 and oO0O0oOo . shape [ 0 ] != 0 and OO . shape [ 0 ] != 0 :
     if 42 - 42: Ii * oOO
     for iIIiII11 in OO :
      OooOoo0OO0OO0 = iIIiII11 [ : 4 ]
      if iou ( OooOoo0OO0OO0 , ii1ii [ 0 ] [ : 4 ] ) > 0 :
       self . flag7 = True
    if self . flag7 is True and ii1ii . shape [ 0 ] != 0 and oO0O0oOo . shape [ 0 ] != 0 :
     if iou ( ii1ii [ 0 ] [ : 4 ] , oO0O0oOo [ 0 ] [ : 4 ] ) > 0 :
      self . diff_flag = False
      i1i1iI = 0.1
      self . assignScore ( index = 7 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = i1i1iI ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "7.jpg" ,
 preds = self . preds_front
 )
    if self . flag7 is False and O0OOooO0O0Oo0 . shape [ 0 ] != 0 and II1Iiii111i1I . shape [ 0 ] != 0 and oO . shape [ 0 ] != 0 :
     if 67 - 67: ooOOO
     for iIIiII11 in oO :
      OooOoo0OO0OO0 = iIIiII11 [ : 4 ]
      if iou ( OooOoo0OO0OO0 , O0OOooO0O0Oo0 [ 0 ] [ : 4 ] ) > 0 :
       self . flag7 = True
    if self . flag7 is True and O0OOooO0O0Oo0 . shape [ 0 ] != 0 and II1Iiii111i1I . shape [ 0 ] != 0 :
     if iou ( O0OOooO0O0Oo0 [ 0 ] [ : 4 ] , II1Iiii111i1I [ 0 ] [ : 4 ] ) > 0 :
      self . diff_flag = False
      i1i1iI = 0.1
      self . assignScore ( index = 7 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = i1i1iI ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "7.jpg" ,
 preds = self . preds_front
 )
      if 62 - 62: I1I + Ii + I1I * i1 . Ooo0Ooo * i1iiIII111
      if 2 - 2: iI1iI11Ii111 + Oo
      if 51 - 51: Ii . iI1iI11Ii111
   if not self . scorePoint8 :
    if not self . flag8_1 and IiiII1Iiii1I1 . shape [ 0 ] != 0 :
     if 89 - 89: O0OooooOo * IiIIii11Ii / i1 . I1Ii1I1
     if 64 - 64: O0OooooOo
     self . flag8_1 = True
    elif not self . flag8_1 and o000OOoOO . shape [ 0 ] != 0 and oooo0OO0o0 . shape [ 0 ] != 0 :
     if 44 - 44: Ii . OooOoo + oOO * OooOoo . i1 - i1iiIII111
     self . flag8_1 = True
    elif not self . flag8_1 and oOOOO0ooO . shape [ 0 ] != 0 and IIiI1i . shape [ 0 ] != 0 :
     if 72 - 72: iI1iII1I1I1i + I1I * ooo000 . OooOoo + Ii + IIiIIiIi11I1
     self . flag8_1 = True
     if 91 - 91: oOo0O00 % IIiIIiIi11I1 % iI1iI11Ii111 / I1Ii1I1
    if self . flag8_1 and not self . flag8_2 and Iioo0Oo0oO0 . shape [ 0 ] != 0 and II . shape [ 0 ] != 0 and O0Ii1Ii1 . shape [ 0 ] != 0 :
     if 70 - 70: iI1iII1I1I1i + O0OooooOo + oOO
     for iIIiII11 in Iioo0Oo0oO0 :
      OooOoo0OO0OO0 = iIIiII11 [ : 4 ]
      if iou ( OooOoo0OO0OO0 , II [ 0 ] [ : 4 ] ) > 0 :
       for O00O0 in O0Ii1Ii1 :
        iIIi111ii1II = O00O0 [ : 4 ]
        if iou ( iIIi111ii1II , II [ 0 ] [ : 4 ] ) > 0 :
         self . flag8_2 = True
    elif self . flag8_1 and not self . flag8_2 and OO . shape [ 0 ] != 0 and ii1ii . shape [ 0 ] != 0 and oO0O0oOo . shape [ 0 ] != 0 :
     if 21 - 21: I11iiIi11i1I
     for iIIiII11 in OO :
      OooOoo0OO0OO0 = iIIiII11 [ : 4 ]
      if iou ( OooOoo0OO0OO0 , ii1ii [ 0 ] [ : 4 ] ) > 0 :
       for O00O0 in oO0O0oOo :
        iIIi111ii1II = O00O0 [ : 4 ]
        if iou ( iIIi111ii1II , ii1ii [ 0 ] [ : 4 ] ) > 0 :
         self . flag8_2 = True
    elif self . flag8_1 and not self . flag8_2 and oO . shape [ 0 ] != 0 and O0OOooO0O0Oo0 . shape [ 0 ] != 0 and II1Iiii111i1I . shape [ 0 ] != 0 :
     if 20 - 20: ooOOO + IiIIii11Ii % Iii1i - I11iiIi11i1I
     for iIIiII11 in oO :
      OooOoo0OO0OO0 = iIIiII11 [ : 4 ]
      if iou ( OooOoo0OO0OO0 , O0OOooO0O0Oo0 [ 0 ] [ : 4 ] ) > 0 :
       for O00O0 in II1Iiii111i1I :
        iIIi111ii1II = O00O0 [ : 4 ]
        if iou ( iIIi111ii1II , O0OOooO0O0Oo0 [ 0 ] [ : 4 ] ) > 0 :
         self . flag8_2 = True
         if 49 - 49: Iii1i / IiIIii11Ii % i1 % i1i1i1111I + oOO * ooo000
    if self . flag8_1 is True and self . flag8_2 is True :
     if II . shape [ 0 ] != 0 and IiiII1Iiii1I1 . shape [ 0 ] != 0 :
      if iou ( II [ 0 ] [ : 4 ] , IiiII1Iiii1I1 [ 0 ] [ : 4 ] ) > 0 :
       i1i1iI = 0.1
       self . assignScore ( index = 8 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = i1i1iI ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "8.jpg" ,
 preds = self . preds_front
 )
     elif ii1ii . shape [ 0 ] != 0 and o000OOoOO . shape [ 0 ] != 0 :
      if iou ( ii1ii [ 0 ] [ : 4 ] , o000OOoOO [ 0 ] [ : 4 ] ) > 0 :
       i1i1iI = 0.1
       self . assignScore ( index = 8 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = i1i1iI ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "8.jpg" ,
 preds = self . preds_front
 )
     elif O0OOooO0O0Oo0 . shape [ 0 ] != 0 and oOOOO0ooO . shape [ 0 ] != 0 :
      if iou ( O0OOooO0O0Oo0 [ 0 ] [ : 4 ] , oOOOO0ooO [ 0 ] [ : 4 ] ) > 0 :
       i1i1iI = 0.1
       self . assignScore ( index = 8 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = i1i1iI ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "8.jpg" ,
 preds = self . preds_front
 )
       if 25 - 25: IIiIIiIi11I1 * OooOoo % oOo0O00 % Ooo0Ooo + i1iiIII111
       if 15 - 15: I11iiIi11i1I
       if 85 - 85: Ii
   if not self . scorePoint9 :
    if IiiII1Iiii1I1 . shape [ 0 ] != 0 and OOo . shape [ 0 ] != 0 and self . flag9 :
     if iou ( IiiII1Iiii1I1 [ 0 ] [ : 4 ] , OOo [ 0 ] [ : 4 ] ) == box_area ( OOo [ 0 ] [ : 4 ] ) :
      if 17 - 17: I1I . Oo
      self . flag9 = False
      i1i1iI = 0.1
      self . assignScore ( index = 9 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = i1i1iI ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "9.jpg" ,
 preds = self . preds_front
 )
    if o000OOoOO . shape [ 0 ] != 0 and OooOoO0oO . shape [ 0 ] != 0 and self . flag9 :
     if iou ( o000OOoOO [ 0 ] [ : 4 ] , OooOoO0oO [ 0 ] [ : 4 ] ) == box_area ( OooOoO0oO [ 0 ] [ : 4 ] ) :
      if 63 - 63: Ii . iI1iI11Ii111
      self . flag9 = False
      i1i1iI = 0.1
      self . assignScore ( index = 9 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = i1i1iI ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "9.jpg" ,
 preds = self . preds_front
 )
    if oOOOO0ooO . shape [ 0 ] != 0 and OoOOooO0oOO0Oo . shape [ 0 ] != 0 and self . flag9 :
     if iou ( oOOOO0ooO [ 0 ] [ : 4 ] , OoOOooO0oOO0Oo [ 0 ] [ : 4 ] ) == box_area ( OoOOooO0oOO0Oo [ 0 ] [ : 4 ] ) :
      if 83 - 83: IIiIIiIi11I1 * O0OooooOo % iI1iI11Ii111 * ooOOO
      self . flag9 = False
      i1i1iI = 0.1
      self . assignScore ( index = 9 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = i1i1iI ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "9.jpg" ,
 preds = self . preds_front
 )
      if 7 - 7: O0OooooOo / i1i1i1111I * Iii1i
      if 27 - 27: i1i1i1111I - Ii - oOO + Ooo0Ooo * Ii + O0OooooOo
      if 35 - 35: i1i1i1111I . i1i1i1111I + I11iiIi11i1I / Oo . i1
      if 69 - 69: I1I / i1 % I1Ii1I1 % oOO
   if not self . scorePoint10 :
    if ( OOo . shape [ 0 ] != 0 or oo00 . shape [ 0 ] != 0 ) and oO000O0O0 . shape [ 0 ] != 0 and Iioo0Oo0oO0 . shape [ 0 ] != 0 :
     if 96 - 96: Oo - iI1iI11Ii111 * iI1iII1I1I1i + Ooo0Ooo * Oo
     for iIIiII11 in Iioo0Oo0oO0 :
      OooOoo0OO0OO0 = iIIiII11 [ : 4 ]
      if iou ( OooOoo0OO0OO0 , oO000O0O0 [ 0 ] [ : 4 ] ) > 0 :
       i1i1iI = 0.1
       self . assignScore ( index = 10 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = i1i1iI ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "10.jpg" ,
 preds = self . preds_front
 )
    elif ( OooOoO0oO . shape [ 0 ] != 0 or oooo0OO0o0 . shape [ 0 ] != 0 ) and O0OO00OO0O . shape [ 0 ] != 0 and OO . shape [ 0 ] != 0 :
     if 22 - 22: ooo000 % I11iiIi11i1I
     for iIIiII11 in OO :
      OooOoo0OO0OO0 = iIIiII11 [ : 4 ]
      if iou ( OooOoo0OO0OO0 , O0OO00OO0O [ 0 ] [ : 4 ] ) > 0 :
       i1i1iI = 0.1
       self . assignScore ( index = 10 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = i1i1iI ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "10.jpg" ,
 preds = self . preds_front
 )
    elif ( OoOOooO0oOO0Oo . shape [ 0 ] != 0 or IIiI1i . shape [ 0 ] != 0 ) and iiI1i1IiiiIi1 . shape [ 0 ] != 0 and oO . shape [ 0 ] != 0 :
     if 44 - 44: oOO / iI1iII1I1I1i % i1iiIII111 + i1iiIII111 % Ooo0Ooo + Ooo0Ooo
     for iIIiII11 in oO :
      OooOoo0OO0OO0 = iIIiII11 [ : 4 ]
      if iou ( OooOoo0OO0OO0 , iiI1i1IiiiIi1 [ 0 ] [ : 4 ] ) > 0 :
       i1i1iI = 0.1
       self . assignScore ( index = 10 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = i1i1iI ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "10.jpg" ,
 preds = self . preds_front
 )
       if 93 - 93: i1 % oOO % I1I
       if 49 - 49: ooOOO * iI1iII1I1I1i + ooo000 - Ii . oOo0O00
       if 77 - 77: I11iiIi11i1I
   if not self . scorePoint11 and self . clean_desk_tools ( self . scorePoint1 , self . scorePoint2 , self . scorePoint3 ,
 self . scorePoint4 , self . scorePoint5 , self . scorePoint6 ,
 self . scorePoint7 , self . scorePoint8 , self . scorePoint9 ,
 self . scorePoint10 ) :
    if Ooo0oO . shape [ 0 ] != 0 :
     if iIIOO . shape [ 0 ] != 0 or OOooooOOooo0 . shape [ 0 ] != 0 and ii1II . shape [ 0 ] != 0 :
      if 18 - 18: oOo0O00 . I1I / i1iiIII111
      i1i1iI = 0.1
      self . assignScore ( index = 11 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = i1i1iI ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "11.jpg" ,
 preds = self . preds_front
 )
      if 3 - 3: oOO + oOO % iI1iI11Ii111 % Oo / iI1iII1I1I1i . IiIIii11Ii
      if 20 - 20: IiIIii11Ii + iI1iI11Ii111
      if 32 - 32: oOo0O00 + i1i1i1111I
   if not self . scorePoint12 and self . scorePoint11 is True :
    i1i1iI = 0.1
    self . assignScore ( index = 12 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = i1i1iI ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "12.jpg" ,
 preds = self . preds_front
 )
    if 74 - 74: I1I % i1i1i1111I * i1iiIII111 * IIiIIiIi11I1
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
