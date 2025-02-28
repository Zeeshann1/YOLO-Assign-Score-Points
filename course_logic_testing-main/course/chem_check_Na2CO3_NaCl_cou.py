#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2022/04/19 11:30
# @Author  : Wupenghui
# @File    : chem_check_Na2CO3_NaCl_cou.py
if 82 - 82: Iii1i
import random
if 87 - 87: Ii % i1i1i1111I . Oo / OooOoo * I1Ii1I1 - I1I
if 81 - 81: i1 + ooOOO / oOo0O00 * i1iiIII111 * IiIIii11Ii
if 84 - 84: ooo000 - Ooo0Ooo + iI1iII1I1I1i . IIiIIiIi11I1
if 98 - 98: I11iiIi11i1I % oOO
from . comm import *
from . comm . course_base import ConfigModel
from logger import logger
import copy
import cv2
if 31 - 31: i1I
class CHEM_check_Na2CO3_NaCl ( ConfigModel ) :
 def __init__ ( self ) :
  super ( CHEM_check_Na2CO3_NaCl , self ) . __init__ ( )
  if 22 - 22: o00o0OO00O % I11iiIi11i1I - iI1iII1I1I1i
  self . flag1_1 = False
  self . flag1_2 = False
  self . flag1_3 = False
  self . flag2 = False
  self . flag2_1 = False
  self . flag3 = False
  self . flag3_1 = False
  self . flag3_2 = False
  self . flag3_3 = False
  self . flag3_4 = False
  self . flag4_1 = False
  self . flag4_2 = False
  self . flag4_3 = False
  self . flag6_1 = False
  self . flag6_2 = False
  self . flag6_3 = False
  self . flag7 = False
  self . flag7_1 = False
  self . flag7_2 = False
  self . flag7_3 = False
  self . flag8 = False
  self . flag9_1 = False
  self . flag9_2 = False
  if 16 - 16: i1i1i1111I / i1iiIII111
  if 3 - 3: i1 % i1 % i1i1i1111I . Ii * i1
  self . reagent_address1 = None
  self . reagent_address2 = None
  self . reagent_address = None
  if 9 - 9: i1iiIII111
  if 10 - 10: ooOOO / IIiIIiIi11I1 * oOO / i1I / i1I
  self . reagent1_used = False
  self . reagent2_used = False
  self . reagent3_used = False
  if 61 - 61: Ooo0Ooo - I1I
  if 13 - 13: Ooo0Ooo
  self . diff_flag = True
  self . reagent_area_init = False
  self . dropper_mistake = False
  self . dropper_mistake_num = 0
  self . test_tube_mistake = False
  self . test_tube_mistake_num = 0
  self . label_paper_mistake = False
  self . label_paper_mistake_num = 0
  self . stopper_mistake = False
  if 46 - 46: iI1iII1I1I1i - Ii * Oo * Ii
  self . dropper_mistake_secs = 0.
  self . dropper_mistake_secs_pre = 0.
  self . dropper_true_secs = 0.
  self . dropper_true_secs_pre = 0.
  self . stopper_positive_secs = 0.
  self . stopper_positive_secs_pre = 0.
  self . observe_label_exist_secs = 0.
  self . observe_label_exist_secs_pre = 0.
  self . observe_label_without_secs = 0.
  self . observe_label_without_secs_pre = 0.
  self . observe_label_secs = 0.
  self . observe_label_secs_pre = 0.
  self . clean_desk_secs = 0.
  self . clean_desk_secs_pre = 0.
  if 52 - 52: Oo + I1I / oOO / OooOoo - I1Ii1I1 - ooOOO
  self . bottle_stopper_opposite_secs = 0.
  self . bottle_stopper_opposite_secs_pre = 0.
  self . bottle_stopper_opposite_dump_secs = 0.
  self . bottle_stopper_opposite_dump_secs_pre = 0.
  if 60 - 60: iI1iII1I1I1i . oOO
  self . dump_end_secs = 0.
  self . dump_end_secs_pre = 0.
  self . hand_without_reagent_secs = 0.
  self . hand_without_reagent_secs_pre = 0.
  if 13 - 13: oOO
  self . bottle_stopper_opposite_secs = 0.
  self . bottle_stopper_opposite_secs_pre = 0.
  self . bottle_stopper_opposite_dump_secs = 0.
  self . bottle_stopper_opposite_dump_secs_pre = 0.
  if 2 - 2: i1
  if 22 - 22: IIiIIiIi11I1 - ooo000 / I1Ii1I1 . ooo000
  self . shake_check1 = False
  self . shake_check2 = False
  self . shake_check3 = False
  if 1 - 1: iI1iII1I1I1i + Ooo0Ooo + oOO * IIiIIiIi11I1
  if 20 - 20: I1I + Ii
  self . score6_img = None
  self . score6_side_img = None
  self . score4_img = None
  self . score3_img = None
  self . score3_preds_front = None
  self . reagent_tube_closed_side_img = None
  self . reagent_tube_closed_side_pred = None
  self . score1_img = None
  self . score1_preds = None
  self . score7_img = None
  self . score7_preds = None
  self . flag6_2_secs = 0.
  self . flag6_2_secs_pre = 0.
  self . score3_5_img = None
  self . score3_5_preds = None
  self . flag3_5_secs = 0.
  self . flag3_5_secs_pre = 0.
  if 75 - 75: Ii % i1iiIII111 * Ii . IIiIIiIi11I1 % I11iiIi11i1I % I1Ii1I1
  self . bbox = [ ]
  self . background = None
  if 8 - 8: I1Ii1I1 . o00o0OO00O . i1 . Oo - i1I
  if 32 - 32: Ii % i1i1i1111I % i1I - I11iiIi11i1I % i1iiIII111
  self . dropper_above_timelist = [ ]
  self . shake_test_tube_timelist = [ ]
  self . dropper_test_tube_time1 = 0.
  self . dropper_test_tube_time2 = 0.
  self . shake_check_secs = 0.
  self . shake_check_secs_pre = 0.
  self . dropper_above_timelist . append ( time . time ( ) )
  self . hand_duster_time = 0.
  self . use_stir_box = None
  self . test_area_cleaned = False
  if 34 - 34: i1iiIII111 * i1
 def hand_sth ( self , hands , sths ) :
  if hands . shape [ 0 ] != 0 and sths . shape [ 0 ] != 0 :
   for O00O in hands :
    OoO = O00O [ : 4 ]
    for ii1IiIiiII in sths :
     I1I111i11I = ii1IiIiiII [ : 4 ]
     if iou ( OoO , I1I111i11I ) > 0 :
      return True
  return False
  if 85 - 85: OooOoo
 def sth_above_sth ( self , sth1 , sth2 ) :
  o00 = copy . deepcopy ( sth2 )
  if sth1 . shape [ 0 ] != 0 and o00 . shape [ 0 ] != 0 :
   o00 [ 0 ] [ 1 ] = 0
   if iou ( o00 [ 0 ] [ : 4 ] , sth1 [ 0 ] [ : 4 ] ) > 0.7 * box_area ( sth1 [ 0 ] [ : 4 ] ) :
    return True
  else :
   return False
   if 20 - 20: o00o0OO00O + i1iiIII111 / I1I
 def sth_above_sth_loose ( self , sth1 , sth2 ) :
  o00 = copy . deepcopy ( sth2 )
  if sth1 . shape [ 0 ] != 0 and o00 . shape [ 0 ] != 0 :
   o00 [ 0 ] [ 1 ] = 0
   if iou ( o00 [ 0 ] [ : 4 ] , sth1 [ 0 ] [ : 4 ] ) > 0.4 * box_area ( sth1 [ 0 ] [ : 4 ] ) :
    return True
  else :
   return False
   if 88 - 88: I11iiIi11i1I + ooOOO - i1i1i1111I . Ooo0Ooo * Ii + Iii1i
 def judge_grip ( self , hand_front , beaker_box , glass_rod_box ) :
  oOo0O00O0ooo = 0
  if hand_front . shape [ 0 ] == 2 :
   for O00O in hand_front :
    OoO = O00O [ : 4 ]
    if iou ( OoO , beaker_box ) > 0 or iou ( OoO , glass_rod_box ) > 0 :
     oOo0O00O0ooo += 1
  else :
   return False
  if oOo0O00O0ooo == 2 :
   return True
   if 89 - 89: Ii % IiIIii11Ii
 def judge_group1 ( self , dropper_bottle_front , reagent_wooden_stopper_front ) :
  if dropper_bottle_front . shape [ 0 ] >= 1 and reagent_wooden_stopper_front . shape [ 0 ] >= 2 :
   return True
  else :
   return False
   if 75 - 75: Ooo0Ooo / Ii / IiIIii11Ii + IiIIii11Ii . I1I
 def judge_group2 ( self , dropper_bottle_front , reagent_wooden_stopper_front ) :
  if dropper_bottle_front . shape [ 0 ] >= 1 and reagent_wooden_stopper_front . shape [ 0 ] >= 2 :
   return True
  else :
   return False
   if 88 - 88: Oo * IiIIii11Ii
   if 100 - 100: o00o0OO00O - OooOoo * I1Ii1I1 / Ooo0Ooo / Iii1i
   if 23 - 23: Ooo0Ooo + i1 * I1Ii1I1 + Oo * Ii - IIiIIiIi11I1
 def hands_take_two_tubes ( self , hands , test_tubes ) :
  if hands . shape [ 0 ] != 0 and test_tubes . shape [ 0 ] >= 2 :
   for O00O in hands :
    OoO = O00O [ : 4 ]
    if iou ( OoO , test_tubes [ 0 ] [ : 4 ] ) > 0 and iou ( OoO , test_tubes [ 1 ] [ : 4 ] ) > 0 :
     return True
  return False
  if 29 - 29: IiIIii11Ii - oOo0O00
 def check_reagent_area ( self , dropper_bottle ) :
  if dropper_bottle . shape [ 0 ] != 2 :
   return False
  else :
   if 30 - 30: I1I . ooo000
   if 43 - 43: ooOOO . I11iiIi11i1I + ooo000
   self . reagent_address1 = dropper_bottle [ 0 ] [ : 4 ]
   self . reagent_address2 = dropper_bottle [ 1 ] [ : 4 ]
   return True
   if 87 - 87: Iii1i + ooOOO . i1I / Ii + Oo
   if 77 - 77: i1iiIII111 + o00o0OO00O - Oo % ooo000
 def test_area_without_sths ( self , test_area , sths ) :
  if test_area . shape [ 0 ] != 0 :
   I1 = test_area [ 0 ] [ : 4 ]
   for ii1IiIiiII in sths :
    I1I111i11I = ii1IiIiiII [ : 4 ]
    if iou ( I1 , I1I111i11I ) != 0 :
     return False
  return True
  if 56 - 56: I11iiIi11i1I
  if 69 - 69: I1I * Ooo0Ooo + i1iiIII111 . i1iiIII111 % Oo * oOo0O00
  if 65 - 65: Ooo0Ooo * ooo000 + oOo0O00
 def CaOH_uesd_check ( self , droppers , reagent_bottle , hands , test_tubes ) :
  if self . CaOH_close_to_test_tube ( hands , test_tubes , reagent_bottle ) and not self . flag1_1 :
   self . flag1_1 = True
   if 71 - 71: Ooo0Ooo / ooo000
  if self . flag1_1 and not self . hand_sth ( hands , reagent_bottle ) :
   self . hand_without_reagent_secs , self . hand_without_reagent_secs_pre , self . flag1_2 = self . duration ( self . hand_without_reagent_secs , 0.2 ,
 self . hand_without_reagent_secs_pre , 0.1 )
   if self . flag1_2 :
    self . hand_without_reagent_secs = 0.
    self . hand_without_reagent_secs_pre = 0.
    self . flag1_2 = False
    self . flag1_3 = True
    if 87 - 87: o00o0OO00O / oOo0O00 % oOO - oOo0O00 . I1I + Ooo0Ooo
    if 75 - 75: i1iiIII111 * iI1iII1I1I1i - I1I - IIiIIiIi11I1 % I1Ii1I1
  if self . flag1_3 :
   if 85 - 85: oOo0O00
   if self . sth_above_sth_loose ( droppers , test_tubes ) :
    self . flag1_3 = False
    self . flag1_1 = False
   elif self . CaOH_close_to_test_tube ( hands , test_tubes , reagent_bottle ) and not self . hand_sth ( hands , droppers ) :
    self . reagent3_used = True
    if 66 - 66: o00o0OO00O * i1i1i1111I + oOo0O00 / I1I / Iii1i / Ii
    self . flag1_3 = False
    if 32 - 32: i1i1i1111I % Ooo0Ooo - i1I * I1I
 def reagent_use_assist ( self , dropper_bottle_top , hands ) :
  if dropper_bottle_top . shape [ 0 ] == 1 :
   self . reagent_address = dropper_bottle_top [ 0 ] [ : 4 ]
   return True
   if 92 - 92: IIiIIiIi11I1 - i1 - Iii1i / Ooo0Ooo . I1Ii1I1 / I11iiIi11i1I
 def reagent_used_check ( self , dropper_bottle_top , test_tubes , hands , droppers ) :
  if 60 - 60: oOO
  if self . hand_sth ( hands , test_tubes ) and self . sth_above_sth_loose ( droppers , test_tubes ) and not self . reagent1_used :
   if self . reagent_use_assist ( dropper_bottle_top , hands ) :
    self . reagent1_used = True
    if 32 - 32: iI1iII1I1I1i
  elif self . score6_img is not None and not self . reagent1_used :
   if self . reagent_use_assist ( dropper_bottle_top , hands ) :
    self . reagent1_used = True
    if 18 - 18: I11iiIi11i1I * o00o0OO00O % iI1iII1I1I1i + o00o0OO00O
  if self . reagent1_used and dropper_bottle_top . shape [ 0 ] == 2 and not self . reagent2_used :
   O0OO = dropper_bottle_top [ 0 ] [ : 4 ]
   oO0O0oOOo0Oo = dropper_bottle_top [ 1 ] [ : 4 ]
   if ( iou ( O0OO , self . reagent_address ) < 0.6 * box_area ( O0OO ) ) and ( iou ( oO0O0oOOo0Oo , self . reagent_address ) < 0.6 * box_area ( oO0O0oOOo0Oo ) ) :
    if 35 - 35: oOO + OooOoo . OooOoo
    self . reagent2_used = True
  elif self . reagent1_used and dropper_bottle_top . shape [ 0 ] == 1 and not self . reagent2_used :
   Ii1iiIII1IIii = dropper_bottle_top [ 0 ] [ : 4 ]
   if iou ( Ii1iiIII1IIii , self . reagent_address ) < 0.6 * box_area ( Ii1iiIII1IIii ) :
    if 54 - 54: Iii1i % ooo000 % Iii1i - IiIIii11Ii
    self . reagent2_used = True
    if 39 - 39: oOO - oOO * i1 % IIiIIiIi11I1
    if 29 - 29: IIiIIiIi11I1 - ooo000 . i1iiIII111
 def dropper_above_test_tube ( self , hands , test_tubes , dropper ) :
  if self . sth_above_sth ( dropper , test_tubes ) and self . hand_sth ( hands , test_tubes ) :
   if 86 - 86: I1Ii1I1 - OooOoo - oOO % ooo000 . i1I % Iii1i
   IIii = copy . deepcopy ( test_tubes )
   if self . hand_sth ( hands , test_tubes ) and dropper . shape [ 0 ] != 0 :
    IIii [ 0 ] [ 1 ] = 0
    if 34 - 34: I1I + i1iiIII111 - ooo000 + ooOOO
    if iou ( IIii [ 0 ] [ : 4 ] , dropper [ 0 ] [ : 4 ] ) < 0.5 * box_area ( dropper [ 0 ] [ : 4 ] ) :
     self . dropper_mistake_secs , self . dropper_mistake_secs_pre , OOo = self . duration ( self . dropper_mistake_secs , 0.3 , self . dropper_mistake_secs_pre , 0.1 )
     if OOo :
      self . dropper_mistake_secs = 0.
      self . dropper_mistake_secs_pre = 0.
      self . dropper_mistake_num += 1
    elif iou ( IIii [ 0 ] [ : 4 ] , dropper [ 0 ] [ : 4 ] ) >= 0.5 * box_area ( dropper [ 0 ] [ : 4 ] ) :
     if 96 - 96: IiIIii11Ii . i1i1i1111I / Ii * i1 . I1I
     if 3 - 3: i1 / IIiIIiIi11I1 / Oo * I1I % iI1iII1I1I1i
     if 90 - 90: I1Ii1I1 + o00o0OO00O % Oo
     if 100 - 100: Oo + i1I
     self . score6_img = self . frame_front
     if 4 - 4: ooo000 % I1I - i1i1i1111I
     if 76 - 76: i1 * oOo0O00 . o00o0OO00O * i1I . IiIIii11Ii . oOO
     if 55 - 55: i1i1i1111I + i1iiIII111 % Ooo0Ooo . Oo - IiIIii11Ii - iI1iII1I1I1i
 def dropper_above_test_tube_side ( self , hands , test_tubes , dropper ) :
  if self . sth_above_sth ( dropper , test_tubes ) and self . hand_sth ( hands , test_tubes ) :
   IIii = copy . deepcopy ( test_tubes )
   if self . hand_sth ( hands , test_tubes ) and dropper . shape [ 0 ] != 0 :
    IIii [ 0 ] [ 1 ] = 0
    if iou ( IIii [ 0 ] [ : 4 ] , dropper [ 0 ] [ : 4 ] ) >= 0.15 * box_area ( dropper [ 0 ] [ : 4 ] ) :
     if 91 - 91: I1Ii1I1 - I11iiIi11i1I
     if 84 - 84: oOO % iI1iII1I1I1i - Ooo0Ooo
     if 94 - 94: i1iiIII111 + i1i1i1111I / iI1iII1I1I1i + iI1iII1I1I1i / i1I
     if 79 - 79: i1iiIII111 - IIiIIiIi11I1 . I1Ii1I1 + I1I - ooOOO + i1iiIII111
     self . score6_side_img = self . frame_side
     if 36 - 36: ooOOO * Iii1i % I1I % i1 . Ooo0Ooo
     if 63 - 63: IIiIIiIi11I1 / IIiIIiIi11I1 * Iii1i - oOo0O00 . i1
 def bottle_stopper_positive_check ( self , hands , bottle_stopper_positives , bottle_stopper_opposites , reagent_bottles ) :
  if self . hand_sth ( hands , reagent_bottles ) :
   if bottle_stopper_positives . shape [ 0 ] != 0 :
    self . stopper_positive_secs , self . stopper_positive_secs_pre , o00OO0 = self . duration ( self . stopper_positive_secs , 0.5 , self . stopper_positive_secs_pre , 0.1 )
    if 68 - 68: oOO - IiIIii11Ii + iI1iII1I1I1i
    if o00OO0 :
     self . stopper_mistake = True
     self . stopper_positive_secs = 0.
     self . stopper_positive_secs_pre = 0.
   if bottle_stopper_opposites . shape [ 0 ] != 0 :
    self . score4_img = self . frame_front
    if 35 - 35: i1 + I1I . i1iiIII111
    if 16 - 16: I1Ii1I1 % I1I / IIiIIiIi11I1 * i1I + o00o0OO00O % oOo0O00
 def bottle_stopper_oppsitive_check ( self , hands , reagent_bottles , test_tubes , bottle_stopper_opposite , bottle_stopper_opposite_top ) :
  if 13 - 13: i1 + IiIIii11Ii
  if bottle_stopper_opposite . shape [ 0 ] != 0 or bottle_stopper_opposite_top . shape [ 0 ] != 0 :
   self . bottle_stopper_opposite_secs , self . bottle_stopper_opposite_secs_pre , o00OO0 = self . duration ( self . bottle_stopper_opposite_secs , 0.2 ,
 self . bottle_stopper_opposite_secs_pre , 0.2 )
   if o00OO0 :
    self . bottle_stopper_opposite_secs = 0.
    self . bottle_stopper_opposite_secs_pre = 0.
    return True
    if 23 - 23: oOO . ooOOO / Ii
    if 7 - 7: OooOoo + IIiIIiIi11I1 * Iii1i . oOo0O00 % IIiIIiIi11I1
 def bottle_stopper_oppsitive_check_dump ( self , hands , reagent_bottles , test_tubes , bottle_stopper_opposite , bottle_stopper_positive , bottle_stopper_opposite_top ) :
  if self . hand_sth ( hands , reagent_bottles ) and self . hand_sth ( hands , test_tubes ) :
   if bottle_stopper_opposite . shape [ 0 ] != 0 or ( bottle_stopper_opposite . shape [ 0 ] == 0 and bottle_stopper_positive . shape [ 0 ] == 0 ) or bottle_stopper_opposite_top . shape [ 0 ] != 0 :
    self . bottle_stopper_opposite_dump_secs , self . bottle_stopper_opposite_dump_secs_pre , o00OO0 = self . duration ( self . bottle_stopper_opposite_dump_secs , 0.2 ,
 self . bottle_stopper_opposite_dump_secs_pre , 0.2 )
    if o00OO0 :
     self . bottle_stopper_opposite_dump_secs = 0.
     self . bottle_stopper_opposite_dump_secs_pre = 0.
     return True
     if 62 - 62: I1Ii1I1 + ooOOO . Oo - i1i1i1111I
     if 52 - 52: i1I . Ii * OooOoo / i1I
 def test_tube_shake_check ( self , bbox , hands , test_tubes ) :
  if self . hand_sth ( hands , test_tubes ) :
   oo0O0 = test_tubes [ 0 ] [ : 4 ]
   if 77 - 77: I11iiIi11i1I / iI1iII1I1I1i - oOo0O00 - Ooo0Ooo % oOo0O00
   if 73 - 73: o00o0OO00O . Oo * I1I / i1i1i1111I + I1Ii1I1
   if 31 - 31: i1i1i1111I % I1Ii1I1
   if 1 - 1: o00o0OO00O - oOo0O00 - i1 . oOo0O00
   if 91 - 91: iI1iII1I1I1i * i1 . ooOOO
   if 81 - 81: I1I * Oo - i1 % OooOoo * ooOOO
   if 19 - 19: Ii
   if 22 - 22: i1I % iI1iII1I1I1i + Oo
   if self . use_stir_box is None :
    for OOO00OOo0oO0O in bbox :
     if iou ( OOO00OOo0oO0O , oo0O0 ) >= 0.85 * box_area ( oo0O0 ) :
      self . use_stir_box = OOO00OOo0oO0O
   else :
    if iou ( self . use_stir_box , oo0O0 ) >= 0.85 * box_area ( oo0O0 ) :
     self . shake_check_secs , self . shake_check_secs_pre , o00OO0 = self . duration ( self . shake_check_secs , 0.85 , self . shake_check_secs_pre , 0.1 )
     if o00OO0 :
      self . shake_check_secs = 0.
      self . shake_check_secs_pre = 0.
      return True
    else :
     self . use_stir_box = None
     if 78 - 78: i1i1i1111I . i1I / i1I
     if 3 - 3: i1I + I1Ii1I1 . I11iiIi11i1I - iI1iII1I1I1i * I1Ii1I1 + i1I
  return False
  if 56 - 56: i1i1i1111I - IiIIii11Ii - i1iiIII111 - Oo + i1iiIII111 / Ooo0Ooo
 def test_tube_shake_check_assit ( self , hands , test_tubes , reagent_bottles , droppers ) :
  if not self . hand_sth ( hands , droppers ) and not self . hand_sth ( hands , reagent_bottles ) and hands . shape [ 0 ] == 2 :
   return True
  elif self . hand_sth ( hands , droppers ) and self . hand_sth ( hands , test_tubes ) and hands . shape [ 0 ] == 2 :
   OO0oOoOOOoO0 = droppers [ 0 ] [ : 4 ]
   for O00O in hands :
    OoO = O00O [ : 4 ]
    for Iii1I1I1 in test_tubes :
     oo0O0 = Iii1I1I1 [ : 4 ]
     if iou ( OoO , oo0O0 ) > 0 :
      if iou ( oo0O0 , OO0oOoOOOoO0 ) == 0 :
       return True
  elif self . hand_sth ( hands , reagent_bottles ) and self . hand_sth ( hands , test_tubes ) and hands . shape [ 0 ] == 2 :
   for O00O in hands :
    OoO = O00O [ : 4 ]
    for oO0oO in reagent_bottles :
     Oo0 = oO0oO [ : 4 ]
     if iou ( OoO , Oo0 ) > 0 :
      i1i1Ii = Oo0
    for Iii1I1I1 in test_tubes :
     oo0O0 = Iii1I1I1 [ : 4 ]
     if iou ( OoO , oo0O0 ) > 0 :
      ii1iI1I11 = oo0O0
      if 35 - 35: IIiIIiIi11I1 - iI1iII1I1I1i / OooOoo % ooo000
   if iou ( i1i1Ii , ii1iI1I11 ) == 0 :
    return True
    if 25 - 25: OooOoo % ooOOO . i1iiIII111 - ooOOO % Iii1i
  return False
  if 37 - 37: i1I + IIiIIiIi11I1 % iI1iII1I1I1i / IIiIIiIi11I1 % i1iiIII111 + oOO
  if 98 - 98: iI1iII1I1I1i - I1I + i1 * ooo000 % i1
 def reagent_bottle_close_to_test_tube ( self , hands , test_tubes , reagent_bottles ) :
  if 100 - 100: i1iiIII111 . IIiIIiIi11I1 * ooo000 * ooo000
  if 85 - 85: IIiIIiIi11I1 / OooOoo . i1I % Oo + Oo - I11iiIi11i1I
  if 59 - 59: OooOoo
  if reagent_bottles . shape [ 0 ] != 0 and test_tubes . shape [ 0 ] != 0 :
   for oO0oO in reagent_bottles :
    Oo0 = oO0oO [ : 4 ]
    oOOOoO00OO00O0o = Oo0 [ 2 ] - Oo0 [ 0 ]
    i1Ii1iIi11iI = Oo0 [ 3 ] - Oo0 [ 1 ]
    if 22 - 22: Iii1i + i1iiIII111 . oOo0O00 . IiIIii11Ii + OooOoo - i1
    for Iii1I1I1 in test_tubes :
     oo0O0 = Iii1I1I1 [ : 4 ]
     if 68 - 68: I1Ii1I1 % I1Ii1I1 / o00o0OO00O . ooo000
     if 80 - 80: IIiIIiIi11I1 / OooOoo % iI1iII1I1I1i / ooOOO * ooOOO - Iii1i
     if 60 - 60: oOO * i1i1i1111I / iI1iII1I1I1i
     if iou ( oo0O0 , Oo0 ) > 0 and ( Oo0 [ 1 ] < oo0O0 [ 1 ] ) and ( oOOOoO00OO00O0o > i1Ii1iIi11iI ) :
      OO0OOOoOOooO = oo0O0 [ 2 ] - oo0O0 [ 0 ]
      OOo0OOo000o00 = oo0O0 [ 3 ] - oo0O0 [ 1 ]
      if ( OOo0OOo000o00 <= ( 7 * OO0OOOoOOooO ) ) :
       return True
  return False
  if 64 - 64: o00o0OO00O / i1 + I1I
 def reagent_bottle_close_to_test_tube_side ( self , hands , reagent_bottles , test_tubes ) :
  if reagent_bottles . shape [ 0 ] != 0 and hands . shape [ 0 ] != 0 :
   for oO0oO in reagent_bottles :
    Oo0 = oO0oO [ : 4 ]
    oOOOoO00OO00O0o = Oo0 [ 2 ] - Oo0 [ 0 ]
    i1Ii1iIi11iI = Oo0 [ 3 ] - Oo0 [ 1 ]
    if 80 - 80: OooOoo * Oo * Ii
    for O00O in hands :
     OoO = O00O [ : 4 ]
     if 40 - 40: i1I . OooOoo + oOo0O00 . i1iiIII111
     if iou ( OoO , Oo0 ) > 0 and ( oOOOoO00OO00O0o * 0.85 > i1Ii1iIi11iI ) :
      return True
  if self . hand_sth ( hands , test_tubes ) and self . hand_sth ( hands , reagent_bottles ) :
   for oO0oO in reagent_bottles :
    Oo0 = oO0oO [ : 4 ]
    oo0O0oOO0Oo = copy . deepcopy ( Oo0 )
    oOOOoO00OO00O0o = Oo0 [ 2 ] - Oo0 [ 0 ]
    i1Ii1iIi11iI = Oo0 [ 3 ] - Oo0 [ 1 ]
    oo0O0oOO0Oo [ 1 ] += ( i1Ii1iIi11iI / 2 )
    if 60 - 60: OooOoo
    for Iii1I1I1 in test_tubes :
     oo0O0 = Iii1I1I1 [ : 4 ]
     for O00O in hands :
      OoO = O00O [ : 4 ]
      if iou ( oo0O0oOO0Oo , oo0O0 ) > 0 and ( oo0O0 [ 2 ] < oo0O0oOO0Oo [ 2 ] ) :
       return True
  return False
  if 97 - 97: ooo000 * oOO
 def CaOH_close_to_test_tube ( self , hands , test_tubes , reagent_bottles ) :
  if 47 - 47: ooo000
  if 2 - 2: Oo % IiIIii11Ii - ooOOO
  if 75 - 75: IiIIii11Ii * i1 . Iii1i - o00o0OO00O
  if reagent_bottles . shape [ 0 ] != 0 and test_tubes . shape [ 0 ] != 0 :
   for oO0oO in reagent_bottles :
    Oo0 = oO0oO [ : 4 ]
    oOOOoO00OO00O0o = Oo0 [ 2 ] - Oo0 [ 0 ]
    i1Ii1iIi11iI = Oo0 [ 3 ] - Oo0 [ 1 ]
    if 72 - 72: i1 % i1i1i1111I * iI1iII1I1I1i
    for Iii1I1I1 in test_tubes :
     oo0O0 = Iii1I1I1 [ : 4 ]
     if 90 - 90: Ooo0Ooo * OooOoo . Ii
     if 5 - 5: Oo - i1 . oOO
     if 18 - 18: IiIIii11Ii - oOO * i1I - OooOoo
     if iou ( oo0O0 , Oo0 ) > 0 and ( Oo0 [ 1 ] < oo0O0 [ 1 ] ) and ( oOOOoO00OO00O0o > i1Ii1iIi11iI ) :
      OO0OOOoOOooO = oo0O0 [ 2 ] - oo0O0 [ 0 ]
      OOo0OOo000o00 = oo0O0 [ 3 ] - oo0O0 [ 1 ]
      if ( OOo0OOo000o00 <= ( 7 * OO0OOOoOOooO ) ) :
       return True
  return False
  if 54 - 54: IIiIIiIi11I1 . Ooo0Ooo % Ii + IiIIii11Ii * iI1iII1I1I1i / iI1iII1I1I1i
  if 31 - 31: IiIIii11Ii . IiIIii11Ii % Ii
 def label_paper_no_towards_palm ( self , hands , label_papers , test_tubes , reagent_bottles ) :
  if self . hand_sth ( hands , test_tubes ) and self . hand_sth ( hands , reagent_bottles ) :
   for oO0oO in reagent_bottles :
    Oo0 = oO0oO [ : 4 ]
    for Iii1I1I1 in test_tubes :
     oo0O0 = Iii1I1I1 [ : 4 ]
     if iou ( oo0O0 , Oo0 ) > 0 :
      if label_papers . shape [ 0 ] == 0 :
       return False
      else :
       for OoOo0 in label_papers :
        iI = OoOo0 [ : 4 ]
        iii1i1iiIi1 = ( Oo0 [ 3 ] - Oo0 [ 1 ] ) / 2
        i1i1Ii = Oo0
        i1i1Ii += iii1i1iiIi1
        if iou ( iI , i1i1Ii ) > 0 :
         self . observe_label_secs , self . observe_label_secs_pre , o00OO0 = self . duration ( self . observe_label_secs , 0.2 , self . observe_label_secs_pre , 0.1 )
         if 1 - 1: OooOoo / ooOOO % I1Ii1I1
         if o00OO0 :
          self . observe_label_secs = 0.
          self . observe_label_secs_pre = 0.
          return True
  return False
  if 15 - 15: OooOoo . IiIIii11Ii . i1I / Iii1i + ooOOO / Ii
  if 17 - 17: I11iiIi11i1I - i1i1i1111I . iI1iII1I1I1i - I11iiIi11i1I + Oo % iI1iII1I1I1i
 def take_solution_to_be_tested_by_pouring ( self ) :
  pass
  if 65 - 65: Ii % I11iiIi11i1I
  if 39 - 39: Iii1i * IIiIIiIi11I1 . Ooo0Ooo - Oo
 def clean_desk_assist ( self , test_area_box , sths ) :
  if sths . shape [ 0 ] == 0 :
   return True
  else :
   for ii1IiIiiII in sths :
    if iou ( test_area_box , ii1IiIiiII [ : 4 ] ) >= 0.15 * box_area ( ii1IiIiiII [ : 4 ] ) :
     return False
  return True
  if 63 - 63: i1i1i1111I - i1iiIII111 . OooOoo % OooOoo . o00o0OO00O + i1I
 def clean_desk_tool ( self , test_area , test_tube , bottle_stopper_positive , bottle_stopper_opposite ,
 dropper , dropper_bottle , reagent_bottle , reagent_wooden_stopper ) :
  O0OO00Oo0o0 = copy . deepcopy ( test_area )
  IiIIIII1i = copy . deepcopy ( O0OO00Oo0o0 [ 0 ] [ : 4 ] )
  O0OOo0O = ( IiIIIII1i [ 2 ] - IiIIIII1i [ 0 ] ) / 5
  iiI = ( IiIIIII1i [ 3 ] - IiIIIII1i [ 1 ] ) / 5
  O0OO00Oo0o0 [ 0 ] [ 0 ] += O0OOo0O
  O0OO00Oo0o0 [ 0 ] [ 2 ] -= O0OOo0O
  O0OO00Oo0o0 [ 0 ] [ 1 ] += ( 2 * iiI )
  I1 = O0OO00Oo0o0 [ 0 ] [ : 4 ]
  if 13 - 13: IiIIii11Ii * oOO / i1I . oOO % Oo + Ooo0Ooo
  if self . clean_desk_assist ( I1 , test_tube ) and self . clean_desk_assist ( I1 , bottle_stopper_opposite ) and self . clean_desk_assist ( I1 , bottle_stopper_positive ) and self . clean_desk_assist ( I1 , dropper ) and self . clean_desk_assist ( I1 , dropper_bottle ) and self . clean_desk_assist ( I1 , reagent_bottle ) and self . clean_desk_assist ( I1 , reagent_wooden_stopper ) :
   if 46 - 46: Ii - o00o0OO00O + IiIIii11Ii + i1I . I1I % OooOoo
   if 85 - 85: Oo / oOO + Oo + ooOOO
   if 74 - 74: oOO - o00o0OO00O
   return True
  return False
  if 79 - 79: oOO * o00o0OO00O . ooOOO * I1Ii1I1 . oOo0O00 + i1iiIII111
 def score_process ( self , top_true , front_true , side_true ) :
  if 45 - 45: I1Ii1I1
  if top_true or front_true or side_true :
   if top_true :
    Ii1 , i1iIIIIiII1I1 , ii1i , I1II1IIIi , IiI111I1 , oO0oo , IiIII , i1IiiI11i , o0oOoOoO , O0OOoOoOo0O0O , IiI , oO0OoOoo = self . preds_top
    if 66 - 66: I11iiIi11i1I . I1I % IiIIii11Ii + OooOoo * Oo / OooOoo
    if 33 - 33: o00o0OO00O / OooOoo
   if side_true :
    iII11I11111I , ooOO0OO0o , oOOooO , oo000OO000oO , II1iiIiI1i1 , i1II1 , IIIII11 , IIi , O000oO , iI111Ii , II1Ii11111 , IIiIIiiIIi = self . preds_side
    if 29 - 29: i1i1i1111I / oOo0O00
    if 13 - 13: I11iiIi11i1I % i1iiIII111 . OooOoo % ooo000 % OooOoo
   if front_true :
    i1i1IiII11iI1 , O0oOO , I1IIII11Iii1 , I1Oo00oOooOO , IiIooO0OoOo , oO , IiiI , oOO0oooOoo000 , ooOooo , OoOiiIIi1Ii1Ii11 , I11 , Ii1III1iI = self . preds_front
    if 9 - 9: Oo / i1iiIII111 % OooOoo
    if 6 - 6: i1iiIII111 % I1Ii1I1 * iI1iII1I1I1i
    if 90 - 90: I1Ii1I1 * i1i1i1111I / iI1iII1I1I1i * Ii
    if 38 - 38: I1I . Ii
   if not self . scorePoint1 :
    if 41 - 41: ooo000 % IIiIIiIi11I1 % ooOOO
    self . score1_img = self . frame_top
    self . score1_preds = self . preds_top
    self . reagent_used_check ( oO0oo , O0oOO , i1i1IiII11iI1 , IiIooO0OoOo )
    if 5 - 5: oOo0O00 / Ii + i1iiIII111 * Oo + Ooo0Ooo + ooo000
    self . CaOH_uesd_check ( IiIooO0OoOo , IiiI , i1i1IiII11iI1 , O0oOO )
    if 96 - 96: i1iiIII111 - IIiIIiIi11I1 / IIiIIiIi11I1 * IiIIii11Ii
    if self . reagent1_used or self . reagent2_used or self . reagent3_used :
     oOoO0o0OOooO0 = 0.1
     self . assignScore ( index = 1 ,
 img = self . frame_top ,
 object = self . objects_top ,
 conf = oOoO0o0OOooO0 ,
 time_frame = self . time_top ,
 num_frame = self . num_frame_top ,
 name_save = "1.jpg" ,
 preds = self . preds_top
 )
     if 38 - 38: o00o0OO00O - Ooo0Ooo * I1Ii1I1
   if not self . scorePoint2 :
    if 89 - 89: iI1iII1I1I1i + IiIIii11Ii . Ooo0Ooo % ooOOO
    i1II111iii11 = [ self . scorePoint3 , self . scorePoint4 , self . scorePoint5 , self . scorePoint6 , self . scorePoint7 ]
    i1II111iii11 = np . array ( i1II111iii11 )
    ooo0 = np . sum ( i1II111iii11 != 0 )
    if ooo0 >= 3 :
     oOoO0o0OOooO0 = 0.1
     self . assignScore ( index = 2 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = oOoO0o0OOooO0 ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "2.jpg" ,
 preds = self . preds_front
 )
     if 47 - 47: i1I - o00o0OO00O . OooOoo
   if not self . scorePoint3 :
    if 87 - 87: IiIIii11Ii + i1i1i1111I - OooOoo % I11iiIi11i1I
    if self . reagent_bottle_close_to_test_tube ( i1i1IiII11iI1 , O0oOO , IiiI ) and not self . flag3 :
     self . flag3 = True
     self . score3_img = self . frame_front
     self . score3_preds_front = self . preds_front
     if 47 - 47: ooOOO + Oo / I1Ii1I1 . IIiIIiIi11I1
    if self . flag3 :
     if self . label_paper_no_towards_palm ( i1i1IiII11iI1 , ooOooo , O0oOO , IiiI ) :
      self . label_paper_mistake = True
      if 67 - 67: Oo % ooOOO + iI1iII1I1I1i * I1I
      if 79 - 79: IIiIIiIi11I1 * Oo / OooOoo
      if 10 - 10: iI1iII1I1I1i / i1iiIII111 . IiIIii11Ii * i1i1i1111I
    if self . flag3 and not self . reagent_bottle_close_to_test_tube ( i1i1IiII11iI1 , O0oOO , IiiI ) :
     if 71 - 71: oOo0O00 + I1Ii1I1 / I11iiIi11i1I + Oo / I1I
     self . dump_end_secs , self . dump_end_secs_pre , self . flag3_1 = self . duration ( self . dump_end_secs , 0.5 , self . dump_end_secs_pre , 0.1 )
     if self . flag3_1 :
      if not self . label_paper_mistake :
       oOoO0o0OOooO0 = 0.1
       self . assignScore ( index = 3 ,
 img = self . score3_img ,
 object = self . objects_front ,
 conf = oOoO0o0OOooO0 ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "3.jpg" ,
 preds = self . score3_preds_front
 )
      else :
       self . flag3 = False
       self . label_paper_mistake = False
      self . dump_end_secs = 0.
      self . dump_end_secs_pre = 0.
      self . flag3_1 = False
      if 18 - 18: Iii1i - IiIIii11Ii
      if 71 - 71: iI1iII1I1I1i + OooOoo % i1i1i1111I % oOo0O00 . ooo000
    if self . hand_sth ( i1i1IiII11iI1 , IiiI ) and self . hand_sth ( i1i1IiII11iI1 , O0oOO ) :
     self . flag3_2 = True
     if 92 - 92: I11iiIi11i1I - Ooo0Ooo - i1i1i1111I % i1iiIII111 / i1i1i1111I * iI1iII1I1I1i
     self . flag3_5_secs_pre = self . time_front
    if self . flag3_2 and self . score3_5_img is None :
     for Iii1I1I1 in O0oOO :
      oo0O0 = Iii1I1I1 [ : 4 ]
      if oo0O0 [ 1 ] <= 50 and ( ( self . time_front - self . flag3_5_secs_pre ) < 2000 ) :
       if 60 - 60: IiIIii11Ii % oOO / i1I * OooOoo / I11iiIi11i1I - Ii
       if 16 - 16: oOo0O00 / I1Ii1I1 / i1 + I11iiIi11i1I + oOo0O00
       if 11 - 11: oOO / OooOoo + oOo0O00
       if 79 - 79: I11iiIi11i1I . I1Ii1I1 * i1I % I1Ii1I1 / o00o0OO00O
       if 93 - 93: i1I + Iii1i . Ii . i1I * ooOOO
       if 84 - 84: Ooo0Ooo % o00o0OO00O
       if 82 - 82: IIiIIiIi11I1
       if 81 - 81: oOo0O00 + i1 - ooo000 * iI1iII1I1I1i + i1i1i1111I
       self . score3_5_img = self . frame_front
       self . score3_5_preds = self . preds_front
       if 89 - 89: I1Ii1I1
       if 57 - 57: iI1iII1I1I1i - i1iiIII111 / OooOoo % i1iiIII111
       if 92 - 92: IiIIii11Ii * OooOoo - IiIIii11Ii
       if 66 - 66: i1iiIII111 . iI1iII1I1I1i / ooOOO . i1 - OooOoo
       if 13 - 13: oOo0O00
       if 50 - 50: i1 - i1iiIII111 / i1iiIII111 % I1Ii1I1 / IIiIIiIi11I1
       if 66 - 66: oOo0O00 - Iii1i - ooo000 . I11iiIi11i1I
       if 59 - 59: i1I / IiIIii11Ii
      else :
       self . flag3_2 = False
       if 7 - 7: oOo0O00
       if 64 - 64: IIiIIiIi11I1 * oOO + Oo . OooOoo - ooOOO
   if not self . scorePoint4 :
    if self . bottle_stopper_oppsitive_check ( i1i1IiII11iI1 , IiiI , O0oOO , I1Oo00oOooOO , I1II1IIIi ) :
     if I1Oo00oOooOO . shape [ 0 ] != 0 :
      oOoO0o0OOooO0 = 0.1
      self . assignScore ( index = 4 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = oOoO0o0OOooO0 ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "4.jpg" ,
 preds = self . preds_front
 )
     else :
      oOoO0o0OOooO0 = 0.1
      self . assignScore ( index = 4 ,
 img = self . frame_top ,
 object = self . objects_top ,
 conf = oOoO0o0OOooO0 ,
 time_frame = self . time_top ,
 num_frame = self . num_frame_top ,
 name_save = "4.jpg" ,
 preds = self . preds_top
 )
      if 94 - 94: IiIIii11Ii - ooo000 . Ii
      if 73 - 73: IiIIii11Ii / oOo0O00 % ooo000 . iI1iII1I1I1i % oOO
   if not self . scorePoint5 :
    if self . reagent_bottle_close_to_test_tube ( i1i1IiII11iI1 , O0oOO , IiiI ) :
     oOoO0o0OOooO0 = 0.1
     self . assignScore ( index = 5 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = oOoO0o0OOooO0 ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "5.jpg" ,
 preds = self . preds_front
 )
    elif self . reagent_bottle_close_to_test_tube_side ( iII11I11111I , IIIII11 , ooOO0OO0o ) :
     self . reagent_tube_closed_side_img = self . frame_side
     self . reagent_tube_closed_side_pred = self . preds_side
     oOoO0o0OOooO0 = 0.1
     self . assignScore ( index = 5 ,
 img = self . frame_side ,
 object = self . objects_side ,
 conf = oOoO0o0OOooO0 ,
 time_frame = self . time_side ,
 num_frame = self . num_frame_side ,
 name_save = "5.jpg" ,
 preds = self . preds_side
 )
     if 36 - 36: o00o0OO00O * OooOoo . ooo000 . i1iiIII111 + oOO
     if 47 - 47: o00o0OO00O / I11iiIi11i1I
   if not self . scorePoint6 :
    self . dropper_above_test_tube ( i1i1IiII11iI1 , O0oOO , IiIooO0OoOo )
    self . dropper_above_test_tube_side ( iII11I11111I , ooOO0OO0o , II1iiIiI1i1 )
    if self . dropper_mistake_num >= 2 :
     self . dropper_mistake = True
     if 52 - 52: Ii . OooOoo . i1iiIII111 * I11iiIi11i1I - iI1iII1I1I1i
    if self . score6_img is not None :
     oOoO0o0OOooO0 = 0.1
     self . assignScore ( index = 6 ,
 img = self . score6_img ,
 object = self . objects_front ,
 conf = oOoO0o0OOooO0 ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "6.jpg" ,
 preds = self . preds_front
 )
    if self . score6_side_img is not None and self . score6_img is None :
     oOoO0o0OOooO0 = 0.1
     self . assignScore ( index = 6 ,
 img = self . score6_side_img ,
 object = self . objects_side ,
 conf = oOoO0o0OOooO0 ,
 time_frame = self . time_side ,
 num_frame = self . num_frame_side ,
 name_save = "6.jpg" ,
 preds = self . preds_side
 )
     if 20 - 20: OooOoo % o00o0OO00O + I1Ii1I1 + o00o0OO00O - oOo0O00
     if 76 - 76: I11iiIi11i1I % IIiIIiIi11I1 % i1I
    if self . hand_sth ( i1i1IiII11iI1 , O0oOO ) and ( self . hand_sth ( i1i1IiII11iI1 , IiIooO0OoOo ) or self . hand_sth ( iII11I11111I , II1iiIiI1i1 ) ) :
     self . flag6_1 = True
     if 39 - 39: IiIIii11Ii . Oo + i1I - oOo0O00
    if self . hand_sth ( i1i1IiII11iI1 , O0oOO ) and self . flag6_1 :
     for Iii1I1I1 in O0oOO :
      oo0O0 = Iii1I1I1 [ : 4 ]
      if oo0O0 [ 1 ] <= 50 and IiIooO0OoOo . shape [ 0 ] == 0 and not self . hand_sth ( i1i1IiII11iI1 , IiiI ) :
       self . flag6_2_secs , self . flag6_2_secs_pre , self . flag6_2 = self . duration ( self . flag6_2_secs , 0.1 , self . flag6_2_secs_pre , 0.1 )
       if 93 - 93: Iii1i * IIiIIiIi11I1 % i1I + i1 % Ii * i1I
       if self . flag6_2 :
        oOoO0o0OOooO0 = 0.1
        self . assignScore ( index = 6 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = oOoO0o0OOooO0 ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "6.jpg" ,
 preds = self . preds_front
 )
        self . flag6_2 = False
        self . flag6_2_secs = 0.
        self . flag6_2_secs_pre = 0.
        if 62 - 62: o00o0OO00O % ooo000
        if 19 - 19: Ii / Oo % Iii1i / i1iiIII111 - OooOoo - Ooo0Ooo
   if not self . scorePoint7 :
    if 89 - 89: I11iiIi11i1I - o00o0OO00O
    if 61 - 61: Ii * OooOoo * I1I % i1iiIII111 % IIiIIiIi11I1 * I11iiIi11i1I
    if 49 - 49: iI1iII1I1I1i / i1iiIII111 % oOO
    if 46 - 46: ooOOO * IIiIIiIi11I1 % i1 / oOO + i1 + oOo0O00
    if 99 - 99: I1I * IIiIIiIi11I1 * i1iiIII111
    if 62 - 62: ooOOO % Oo + i1I
    if 87 - 87: ooo000 - OooOoo + Ii + i1i1i1111I + IiIIii11Ii
    if self . hand_sth ( I11 , O0oOO ) :
     self . score7_img = self . frame_front
     self . score7_preds = self . preds_front
     if 57 - 57: IIiIIiIi11I1 + I1I / ooOOO % ooOOO % Oo / o00o0OO00O
    if self . scorePoint6 :
     oOoO0o0OOooO0 = 0.1
     self . assignScore ( index = 7 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = oOoO0o0OOooO0 ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "7.jpg" ,
 preds = self . preds_front
 )
     if 95 - 95: i1 / I11iiIi11i1I . i1 / Oo . Ooo0Ooo
   if not self . scorePoint9 :
    if IiI . shape [ 0 ] != 0 and ( not self . test_area_without_sths ( oO0OoOoo , IiI ) ) :
     self . clean_desk_secs , self . clean_desk_secs_pre , self . flag9_1 = self . duration ( self . clean_desk_secs , 0.2 , self . clean_desk_secs_pre , 0.1 )
     if self . flag9_1 :
      self . clean_desk_secs = 0.
      self . clean_desk_secs_pre = 0.
      self . flag9_2 = True
      self . hand_duster_time = self . time_top
      if 43 - 43: Oo - OooOoo * oOO . Ooo0Ooo / IIiIIiIi11I1 * IIiIIiIi11I1
    if self . flag9_2 :
     if oO0OoOoo . shape [ 0 ] == 1 and ( self . time_top - self . hand_duster_time ) <= 3000 :
      if self . clean_desk_tool ( oO0OoOoo , i1iIIIIiII1I1 , ii1i , I1II1IIIi ,
 IiI111I1 , oO0oo , IiIII , O0OOoOoOo0O0O ) :
       oOoO0o0OOooO0 = 0.1
       self . assignScore ( index = 9 ,
 img = self . frame_top ,
 object = self . objects_top ,
 conf = oOoO0o0OOooO0 ,
 time_frame = self . time_top ,
 num_frame = self . num_frame_top ,
 name_save = "9.jpg" ,
 preds = self . preds_top
 )
       if 84 - 84: i1iiIII111 + oOo0O00
   if oO0OoOoo . shape [ 0 ] == 1 :
    self . test_area_cleaned = self . clean_desk_tool ( oO0OoOoo , i1iIIIIiII1I1 , ii1i , I1II1IIIi ,
 IiI111I1 , oO0oo , IiIII , O0OOoOoOo0O0O )
    if 83 - 83: i1i1i1111I
    if 84 - 84: oOO / Ii * Ooo0Ooo / Ii / ooo000
 def end ( self ) :
  if 64 - 64: oOo0O00 * Ii
  if 2 - 2: o00o0OO00O % i1iiIII111 . oOo0O00
  if not self . scorePoint9 and self . test_area_cleaned :
   i1II111iii11 = [ self . scorePoint1 , self . scorePoint2 , self . scorePoint3 , self . scorePoint4 , self . scorePoint5 , self . scorePoint6 , self . scorePoint7 ]
   i1II111iii11 = np . array ( i1II111iii11 )
   ooo0 = np . sum ( i1II111iii11 != 0 )
   if ooo0 >= 2 :
    oOoO0o0OOooO0 = 0.1
    self . assignScore ( index = 9 ,
 img = self . frame_top ,
 object = self . objects_top ,
 conf = oOoO0o0OOooO0 ,
 time_frame = self . time_top ,
 num_frame = self . num_frame_top ,
 name_save = "9.jpg" ,
 preds = self . preds_top
 )
    if 59 - 59: I11iiIi11i1I % OooOoo - iI1iII1I1I1i % I1I + i1iiIII111 . I1Ii1I1
  if not self . scorePoint3 and not self . score3_img :
   if self . reagent_tube_closed_side_img is not None :
    oOoO0o0OOooO0 = 0.1
    self . assignScore ( index = 3 ,
 img = self . reagent_tube_closed_side_img ,
 object = self . objects_side ,
 conf = oOoO0o0OOooO0 ,
 time_frame = self . time_side ,
 num_frame = self . num_frame_side ,
 name_save = "3.jpg" ,
 preds = self . reagent_tube_closed_side_pred
 )
    if 94 - 94: ooOOO * I1Ii1I1 * i1iiIII111 . oOo0O00
  if not self . scorePoint7 and self . score7_img is not None :
   oOoO0o0OOooO0 = 0.1
   self . assignScore ( index = 7 ,
 img = self . score7_img ,
 object = self . objects_front ,
 conf = oOoO0o0OOooO0 ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "7.jpg" ,
 preds = self . score7_preds
 )
   if 73 - 73: I1Ii1I1 / ooo000 % I11iiIi11i1I - i1i1i1111I + Oo - I1Ii1I1
  if self . score3_5_img is not None and not self . scorePoint3 and not self . scorePoint5 :
   oOoO0o0OOooO0 = 0.1
   self . assignScore ( index = 3 ,
 img = self . score3_5_img ,
 object = self . objects_front ,
 conf = oOoO0o0OOooO0 ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "3.jpg" ,
 preds = self . score3_5_preds
 )
   if 18 - 18: i1 + ooOOO . i1 - iI1iII1I1I1i
   self . assignScore ( index = 5 ,
 img = self . score3_5_img ,
 object = self . objects_front ,
 conf = oOoO0o0OOooO0 ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "5.jpg" ,
 preds = self . score3_5_preds
 )
   if 97 - 97: oOo0O00 + i1I % Iii1i
  if not self . scorePoint1 and self . score1_img is not None :
   Ooo0oOOoO000O = [ self . scorePoint2 , self . scorePoint3 , self . scorePoint4 , self . scorePoint5 , self . scorePoint6 , self . scorePoint7 ]
   Ooo0oOOoO000O = np . array ( Ooo0oOOoO000O )
   I1iiiIi = np . sum ( Ooo0oOOoO000O != 0 )
   if I1iiiIi >= 1 :
    oOoO0o0OOooO0 = 0.1
    self . assignScore ( index = 1 ,
 img = self . score1_img ,
 object = self . objects_top ,
 conf = oOoO0o0OOooO0 ,
 time_frame = self . time_top ,
 num_frame = self . num_frame_top ,
 name_save = "1.jpg" ,
 preds = self . score1_preds
 )
    if 59 - 59: IiIIii11Ii % oOO - oOO - I1I * o00o0OO00O / i1i1i1111I
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
