#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/10/28 16:28
# @Author  : Wupenghui
# @File    : chem_filter_cou.py
if 82 - 82: Iii1i
import random
from . comm import *
from . comm . course_base import ConfigModel
import platform
from ctypes import *
import ctypes
import copy
if 87 - 87: Ii % i1i1i1111I . Oo / OooOoo * I1Ii1I1 - I1I
if 81 - 81: i1 + ooOOO / oOo0O00 * i1iiIII111 * IiIIii11Ii
from logger import logger
if 84 - 84: ooo000 - Ooo0Ooo + iI1iII1I1I1i . IIiIIiIi11I1
iI111iiIi11i = platform . platform ( )
class CHEM_filter_cou ( ConfigModel ) :
 if 11 - 11: i1I1 - O000o / O0OO0OooooOo * ii % Ii * i1
 def __init__ ( self ) :
  super ( CHEM_filter_cou , self ) . __init__ ( )
  if 9 - 9: i1iiIII111
  if 10 - 10: ooOOO / IIiIIiIi11I1 * O000o / O0OO0OooooOo / O0OO0OooooOo
  if 61 - 61: Ooo0Ooo - I1I
  if 13 - 13: Ooo0Ooo
  if 46 - 46: iI1iII1I1I1i - Ii * Oo * Ii
  if 52 - 52: Oo + I1I / O000o / OooOoo - I1Ii1I1 - ooOOO
  if 60 - 60: iI1iII1I1I1i . O000o
  if 13 - 13: O000o
  if 2 - 2: i1
  if 22 - 22: IIiIIiIi11I1 - ooo000 / I1Ii1I1 . ooo000
  if 1 - 1: iI1iII1I1I1i + Ooo0Ooo + O000o * IIiIIiIi11I1
  self . retort_stand_direction = False
  self . flag1 = False
  self . flag2 = False
  self . flag2_1 = False
  self . flag3 = False
  self . flag3_1 = False
  self . flag4 = False
  self . flag5_and_6 = False
  self . flag7 = False
  self . flag7_1 = False
  self . flag7_2 = False
  self . flag8 = False
  self . culture_dish_top_box = None
  self . corn_beaker_top_box = None
  if 20 - 20: I1I + Ii
  self . retort_stand_bbox_collect = [ ]
  self . beaker_bbox_collect = [ ]
  self . funnel_bbox_collect = [ ]
  self . flag_check_beaker_shape = False
  self . build_mistake = False
  if 75 - 75: Ii % i1iiIII111 * Ii . IIiIIiIi11I1 % i1I1 % I1Ii1I1
  if 8 - 8: I1Ii1I1 . ii . i1 . Oo - O0OO0OooooOo
  self . folded_filter_paper_secs = 0.
  self . folded_filter_paper_secs_pre = 0.
  self . filer_paper_fixed_secs = 0.
  self . filer_paper_fixed_secs_pre = 0.
  self . observe_liquid_cleaned_secs = 0.
  self . observe_liquid_cleaned_secs_pre = 0.
  if 32 - 32: Ii % i1i1i1111I % O0OO0OooooOo - i1I1 % i1iiIII111
  self . build_up_false_secs = 0.
  self . build_up_false_secs_pre = 0.
  if 34 - 34: i1iiIII111 * i1
  self . build_up_side_false_secs = 0.
  self . build_up_side_false_secs_pre = 0.
  if 34 - 34: oOo0O00 / i1iiIII111 - Iii1i . iI1iII1I1I1i
  self . status_cache_list = [ ]
  self . status_list = [ ]
  self . status_template = [ 0 , 1 ]
  self . status_error_template = [ 2 , 1 ]
  self . get_status = None
  self . build_up_error_img = None
  self . build_up_error_pred = None
  self . check_beaker_shape_flag = False
  if 80 - 80: i1i1i1111I . I1I % ooOOO % IiIIii11Ii / i1i1i1111I
 def hand_sth ( self , hands , sth ) :
  if hands . shape [ 0 ] != 0 and sth . shape [ 0 ] != 0 :
   for IiI11I in hands :
    IiiIii11iII1 = IiI11I [ : 4 ]
    if iou ( IiiIii11iII1 , sth [ 0 ] [ : 4 ] ) > 0 :
     return True
  return False
  if 27 - 27: I1I + ooOOO * IIiIIiIi11I1 % Ii + Ooo0Ooo . ooOOO
 def judge_folded_paper ( self , folded_filter_paper , funnel_front , funnel_mouth ) :
  if folded_filter_paper . shape [ 0 ] != 0 and funnel_front . shape [ 0 ] != 0 and funnel_mouth . shape [ 0 ] != 0 :
   if iou ( folded_filter_paper [ 0 ] [ : 4 ] , funnel_front [ 0 ] [ : 4 ] ) >= 0.85 * box_area ( folded_filter_paper [ 0 ] [ : 4 ] ) :
    if 6 - 6: i1iiIII111
    self . folded_filter_paper_secs , self . folded_filter_paper_secs_pre , I1I1 = self . duration ( self . folded_filter_paper_secs , 1 ,
 self . folded_filter_paper_secs_pre , 1 )
    if 91 - 91: Iii1i % i1i1i1111I . OooOoo * O000o
    if I1I1 :
     self . folded_filter_paper_secs = 0.
     self . folded_filter_paper_secs_pre = 0.
     return True
     if 5 - 5: O000o % Ooo0Ooo / OooOoo
  return False
  if 6 - 6: Ii + I1I + i1
 def check_beaker_shape ( self , funnel_bbox_collect , beaker_bbox_collect ) :
  if 86 - 86: IiIIii11Ii
  if 100 - 100: ii - OooOoo * I1Ii1I1 / Ooo0Ooo / Iii1i
  I11iIi1i = torch . mean ( torch . stack ( beaker_bbox_collect ) )
  oooOOOooo = torch . mean ( torch . stack ( funnel_bbox_collect ) )
  IIiII11 = ( I11iIi1i / oooOOOooo )
  if IIiII11 >= 0.9 :
   return True
  else :
   return False
   if 52 - 52: i1iiIII111 % Oo . I1Ii1I1 + ooOOO % Oo . ii
 def collect_beaker_funnel_bbox ( self , beakers , funnels , retort_stands ) :
  if beakers . shape [ 0 ] != 0 and funnels . shape [ 0 ] != 0 and retort_stands . shape [ 0 ] != 0 :
   OOO00oO0oOo0O = funnels [ 0 ] [ : 4 ]
   iIi1I1I = retort_stands [ 0 ] [ : 4 ]
   for II1III1I1i in beakers :
    II11i11II1iI = II1III1I1i [ : 4 ]
    if iou ( II11i11II1iI , iIi1I1I ) > 0.8 * box_area ( II11i11II1iI ) :
     self . beaker_bbox_collect . append ( II11i11II1iI [ 2 ] - II11i11II1iI [ 0 ] )
     self . funnel_bbox_collect . append ( OOO00oO0oOo0O [ 2 ] - OOO00oO0oOo0O [ 0 ] )
     if ( len ( self . beaker_bbox_collect ) >= 10 and len ( self . funnel_bbox_collect ) >= 10 ) :
      if self . check_beaker_shape ( self . funnel_bbox_collect , self . beaker_bbox_collect ) :
       self . funnel_bbox_collect . clear ( )
       self . beaker_bbox_collect . clear ( )
       self . check_beaker_shape_flag = True
       return True
      else :
       self . funnel_bbox_collect . clear ( )
       self . beaker_bbox_collect . clear ( )
       self . check_beaker_shape_flag = True
       return False
  else :
   return False
   if 37 - 37: O0OO0OooooOo - ii
 def sth_above_sth ( self , sth1 , sth2 ) :
  OO0o0O0o0 = copy . deepcopy ( sth2 )
  if sth1 . shape [ 0 ] != 0 and OO0o0O0o0 . shape [ 0 ] != 0 :
   OO0o0O0o0 [ 1 ] = 0
   if iou ( OO0o0O0o0 [ : 4 ] , sth1 [ 0 ] [ : 4 ] ) > 0.75 * box_area ( sth1 [ 0 ] [ : 4 ] ) :
    return True
  else :
   return False
   if 11 - 11: ii % i1i1i1111I + i1
 def score3_stage1_true ( self , retort_stand , beakers , siderosphere , funnel , funnel_mouth , folded_filter_paper ) :
  if siderosphere . shape [ 0 ] != 0 and retort_stand . shape [ 0 ] != 0 and beakers . shape [ 0 ] != 0 :
   for II1III1I1i in beakers :
    II11i11II1iI = II1III1I1i [ : 4 ]
    if 87 - 87: I1I / Iii1i / Ii
    if iou ( II11i11II1iI , retort_stand [ 0 ] [ : 4 ] ) > 0.4 * box_area ( II11i11II1iI ) and II11i11II1iI [ 3 ] < retort_stand [ 0 ] [ : 4 ] [ 3 ] :
     if 32 - 32: i1i1i1111I % Ooo0Ooo - O0OO0OooooOo * I1I
     if adjoin ( II11i11II1iI , siderosphere [ 0 ] [ : 4 ] ) is True :
      if funnel . shape [ 0 ] != 0 and funnel_mouth . shape [ 0 ] != 0 :
       if 92 - 92: IIiIIiIi11I1 - i1 - Iii1i / Ooo0Ooo . I1Ii1I1 / i1I1
       if 60 - 60: O000o
       if 32 - 32: iI1iII1I1I1i
       I111II111I1I = copy . deepcopy ( funnel )
       IIi1I1I1i = ( I111II111I1I [ 0 ] [ 3 ] - I111II111I1I [ 0 ] [ 1 ] ) / 2
       I111II111I1I [ 0 ] [ 3 ] = I111II111I1I [ 0 ] [ 1 ] + IIi1I1I1i
       if ( not self . sth_above_sth ( funnel , II1III1I1i ) and iou ( I111II111I1I [ 0 ] [ : 4 ] , siderosphere [ 0 ] [ : 4 ] ) == 0 ) :
        return True
      else :
       return True
  else :
   return False
   if 36 - 36: oOo0O00 . ooOOO / i1iiIII111 + O000o
 def score3_stage1_false ( self , retort_stand , beakers , siderosphere , funnel , funnel_mouth , folded_filter_paper ) :
  if siderosphere . shape [ 0 ] != 0 and retort_stand . shape [ 0 ] != 0 and funnel . shape [ 0 ] != 0 and funnel_mouth . shape [ 0 ] != 0 :
   if 11 - 11: i1 / ooo000
   OOO00oO0oOo0O = funnel [ 0 ] [ : 4 ]
   iII = funnel_mouth [ 0 ] [ : 4 ]
   if iou ( OOO00oO0oOo0O , retort_stand [ 0 ] [ : 4 ] ) > 0.35 * box_area ( OOO00oO0oOo0O ) and iou ( OOO00oO0oOo0O , siderosphere [ 0 ] [ : 4 ] ) > 0 and ( iII [ 1 ] - OOO00oO0oOo0O [ 1 ] ) > ( OOO00oO0oOo0O [ 3 ] - iII [ 3 ] ) :
    if 43 - 43: Ooo0Ooo - I1I . ooo000 - Iii1i % O0OO0OooooOo
    if 49 - 49: IiIIii11Ii . ooo000 + O000o - O000o
    for II1III1I1i in beakers :
     II11i11II1iI = II1III1I1i [ : 4 ]
     if iou ( II11i11II1iI , retort_stand [ 0 ] [ : 4 ] ) >= 0.35 * box_area ( II11i11II1iI ) :
      return False
    return True
  else :
   return False
   if 78 - 78: i1 - ooOOO
 def score3_stage2_true_front ( self , retort_stand , beakers , siderosphere , funnel , funnel_mouth , folded_filter_paper ) :
  if siderosphere . shape [ 0 ] != 0 and retort_stand . shape [ 0 ] != 0 and beakers . shape [ 0 ] != 0 and funnel . shape [ 0 ] != 0 and funnel_mouth . shape [ 0 ] != 0 and folded_filter_paper . shape [ 0 ] != 0 :
   if 56 - 56: ooo000 . ooo000 + I1Ii1I1 * iI1iII1I1I1i
   OOO00oO0oOo0O = funnel [ 0 ] [ : 4 ]
   iII = funnel_mouth [ 0 ] [ : 4 ]
   for II1III1I1i in beakers :
    II11i11II1iI = II1III1I1i [ : 4 ]
    if iou ( II11i11II1iI , retort_stand [ 0 ] [ : 4 ] ) > 0.5 * box_area ( II11i11II1iI ) and iou ( OOO00oO0oOo0O , retort_stand [ 0 ] [ : 4 ] ) > 0 and iou ( OOO00oO0oOo0O , siderosphere [ 0 ] [ : 4 ] ) > 0 and iou ( II11i11II1iI , iII ) > 0 and ( iII [ 1 ] - OOO00oO0oOo0O [ 1 ] ) > ( OOO00oO0oOo0O [ 3 ] - iII [ 3 ] ) and II11i11II1iI [ 3 ] < retort_stand [ 0 ] [ : 4 ] [ 3 ] :
     if 17 - 17: Iii1i % O0OO0OooooOo - Iii1i % Ooo0Ooo . OooOoo
     if 60 - 60: ooOOO . ooo000
     if 42 - 42: i1iiIII111 - i1iiIII111
     if 98 - 98: Ooo0Ooo + i1i1i1111I + Iii1i - O000o
     return True
  else :
   return False
   if 7 - 7: i1i1i1111I / Ii * Iii1i
 def score3_stage2_true_side ( self , retort_stand , beakers , siderosphere , funnel , funnel_mouth , folded_filter_paper ) :
  if siderosphere . shape [ 0 ] != 0 and retort_stand . shape [ 0 ] != 0 and beakers . shape [ 0 ] != 0 and funnel . shape [ 0 ] != 0 and funnel_mouth . shape [ 0 ] != 0 and folded_filter_paper . shape [ 0 ] != 0 :
   if 32 - 32: ii . OooOoo
   OOO00oO0oOo0O = funnel [ 0 ] [ : 4 ]
   iII = funnel_mouth [ 0 ] [ : 4 ]
   for II1III1I1i in beakers :
    II11i11II1iI = II1III1I1i [ : 4 ]
    if iou ( II11i11II1iI , retort_stand [ 0 ] [ : 4 ] ) > 0.5 * box_area ( II11i11II1iI ) and iou ( OOO00oO0oOo0O , retort_stand [ 0 ] [ : 4 ] ) > 0 and iou ( OOO00oO0oOo0O , siderosphere [ 0 ] [ : 4 ] ) > 0 and iou ( II11i11II1iI , iII ) > 0 and ( iII [ 1 ] - OOO00oO0oOo0O [ 1 ] ) > ( OOO00oO0oOo0O [ 3 ] - iII [ 3 ] ) and II11i11II1iI [ 3 ] < retort_stand [ 0 ] [ : 4 ] [ 3 ] :
     if 31 - 31: Oo - O0OO0OooooOo
     if 28 - 28: ooOOO * I1Ii1I1 + ii % Oo
     if 100 - 100: Oo + O0OO0OooooOo
     if 4 - 4: ooo000 % I1I - i1i1i1111I
     return True
  else :
   return False
   if 76 - 76: i1 * oOo0O00 . ii * O0OO0OooooOo . IiIIii11Ii . O000o
 def status_list_judge ( self , siderosphere_top , siderosphere_front , retort_stand_front , beaker_front ,
 funnel_front , funnel_mouth_front , folded_filter_paper_front , retort_stand_side ,
 beaker_side , siderosphere_side , funnel_side , funnel_mouth_side , folded_filter_paper_side ) :
  O00 = True
  if siderosphere_top . shape [ 0 ] != 0 and O00 :
   oOoOO0O0 = siderosphere_top [ 0 ] [ 2 ] - siderosphere_top [ 0 ] [ 0 ]
   IIi1I1I1i = siderosphere_top [ 0 ] [ 3 ] - siderosphere_top [ 0 ] [ 1 ]
   O00 = False
  elif siderosphere_front . shape [ 0 ] != 0 and O00 :
   oOoOO0O0 = siderosphere_front [ 0 ] [ 2 ] - siderosphere_front [ 0 ] [ 0 ]
   IIi1I1I1i = siderosphere_front [ 0 ] [ 3 ] - siderosphere_front [ 0 ] [ 1 ]
   O00 = False
  if not O00 :
   if 20 - 20: i1I1 / ooOOO * O000o % IIiIIiIi11I1
   if 60 - 60: O0OO0OooooOo * i1iiIII111 + i1i1i1111I / ooOOO
   if 58 - 58: O0OO0OooooOo - ii
   if 86 - 86: Iii1i + i1iiIII111 - IIiIIiIi11I1 / I1I
   if oOoOO0O0 > IIi1I1I1i :
    if self . score3_stage1_true ( retort_stand_front , beaker_front ,
 siderosphere_front , funnel_front ,
 funnel_mouth_front , folded_filter_paper_front ) :
     self . status_cache_list . append ( 0 )
    elif self . score3_stage1_false ( retort_stand_front , beaker_front ,
 siderosphere_front , funnel_front ,
 funnel_mouth_front , folded_filter_paper_front ) :
     self . status_cache_list . append ( 2 )
     self . build_up_error_img = self . frame_front
     self . build_up_error_pred = self . preds_front
    elif self . score3_stage2_true_front ( retort_stand_front , beaker_front ,
 siderosphere_front , funnel_front ,
 funnel_mouth_front , folded_filter_paper_front ) :
     self . status_cache_list . append ( 1 )
   else :
    if self . score3_stage1_true ( retort_stand_side , beaker_side ,
 siderosphere_side , funnel_side ,
 funnel_mouth_side , folded_filter_paper_side ) :
     self . status_cache_list . append ( 0 )
    elif self . score3_stage1_false ( retort_stand_side , beaker_side ,
 siderosphere_side , funnel_side ,
 funnel_mouth_side , folded_filter_paper_side ) :
     self . status_cache_list . append ( 2 )
     self . build_up_error_img = self . frame_side
     self . build_up_error_pred = self . preds_side
    elif self . score3_stage2_true_side ( retort_stand_side , beaker_side ,
 siderosphere_side , funnel_side ,
 funnel_mouth_side , folded_filter_paper_side ) :
     self . status_cache_list . append ( 1 )
     if 46 - 46: ooOOO + ooOOO % O000o
  if len ( self . status_cache_list ) >= 10 :
   self . get_status = max ( set ( self . status_cache_list ) , key = self . status_cache_list . count )
   if 2 - 2: i1i1i1111I / Ooo0Ooo / O000o - IIiIIiIi11I1 / IIiIIiIi11I1
   if len ( self . status_list ) != 0 :
    if self . get_status == self . status_list [ - 1 ] :
     pass
    else :
     if len ( self . status_list ) == 2 :
      self . status_list . pop ( 0 )
      self . status_list . append ( self . get_status )
     else :
      self . status_list . append ( self . get_status )
   else :
    self . status_list . append ( self . get_status )
    if 58 - 58: i1i1i1111I
   self . status_cache_list . clear ( )
   if 38 - 38: i1 - oOo0O00
 def score3_tool1 ( self , beakers , retort_stand , siderophere , funnel ) :
  O0OO00OO0O = False
  for II1III1I1i in beakers :
   II11i11II1iI = II1III1I1i [ : 4 ]
   if iou ( II11i11II1iI , retort_stand [ 0 ] [ : 4 ] ) > 0 :
    if adjoin ( II11i11II1iI , siderophere [ 0 ] [ : 4 ] ) is True :
     if funnel . shape [ 0 ] != 0 :
      if iou ( II11i11II1iI , funnel [ 0 ] [ : 4 ] ) == 0 and iou ( siderophere [ 0 ] [ : 4 ] , funnel [ 0 ] [ : 4 ] ) == 0 :
       O0OO00OO0O = True
     else :
      O0OO00OO0O = True
  return O0OO00OO0O
  if 35 - 35: i1 + I1I . i1iiIII111
  if 16 - 16: I1Ii1I1 % I1I / IIiIIiIi11I1 * O0OO0OooooOo + ii % oOo0O00
  if 13 - 13: i1 + IiIIii11Ii
  if 23 - 23: O000o . ooOOO / Ii
  if 7 - 7: OooOoo + IIiIIiIi11I1 * Iii1i . oOo0O00 % IIiIIiIi11I1
  if 62 - 62: I1Ii1I1 + ooOOO . Oo - i1i1i1111I
  if 52 - 52: O0OO0OooooOo . Ii * OooOoo / O0OO0OooooOo
  if 39 - 39: i1
  if 16 - 16: ii - ii % i1I1 / iI1iII1I1I1i - iI1iII1I1I1i
  if 39 - 39: oOo0O00 - ii % ii . Oo * I1I
 def score3_tool2_front ( self , siderosphere_box , funnel_box , funnel_mouth_box , beakers , retort_stand ) :
  if 81 - 81: i1i1i1111I + I1Ii1I1
  if 31 - 31: i1i1i1111I % I1Ii1I1
  if 1 - 1: ii - oOo0O00 - i1 . oOo0O00
  if 91 - 91: iI1iII1I1I1i * i1 . ooOOO
  if 81 - 81: I1I * Oo - i1 % OooOoo * ooOOO
  if 19 - 19: Ii
  funnel_box [ 3 ] = 0.5 * ( funnel_box [ 1 ] + funnel_box [ 3 ] )
  if 22 - 22: O0OO0OooooOo % iI1iII1I1I1i + Oo
  if iou ( siderosphere_box , funnel_box ) > 0 :
   for II1III1I1i in beakers :
    II11i11II1iI = II1III1I1i [ : 4 ]
    if iou ( II11i11II1iI , retort_stand [ 0 ] [ : 4 ] ) > 0.25 * box_area ( II11i11II1iI ) :
     if iou ( II11i11II1iI , funnel_mouth_box ) > 0 :
      return True
  return False
  if 60 - 60: ooo000 + i1I1 + IIiIIiIi11I1 % i1i1i1111I - Ii % Ooo0Ooo
 def score3_tool2_side ( self , siderosphere_box , funnel_box , funnel_mouth_box , beakers , retort_stand ) :
  if 95 - 95: ooOOO % i1i1i1111I . i1
  if 87 - 87: Iii1i % ooOOO * Ii % IIiIIiIi11I1 / i1I1
  funnel_box [ 3 ] = 0.5 * ( funnel_box [ 1 ] + funnel_box [ 3 ] )
  if 84 - 84: I1Ii1I1 + Ooo0Ooo % IIiIIiIi11I1 * i1i1i1111I
  if iou ( siderosphere_box , funnel_box ) > 0 :
   return True
   if 61 - 61: i1iiIII111 - Oo + I1Ii1I1
   if 43 - 43: IIiIIiIi11I1 * ooo000 + Ii % iI1iII1I1I1i
   if 12 - 12: i1iiIII111 + ooo000 . i1I1
   if 1 - 1: iI1iII1I1I1i % Ii - i1I1 / ii + iI1iII1I1I1i - Ii
  return False
  if 27 - 27: OooOoo % iI1iII1I1I1i + IIiIIiIi11I1
 def clean_desk_tools ( self , score1 , score2 , score3 , score4 , score5 , score6 , score7 ) :
  i1i1iI1i1Iii = [ score1 , score2 , score3 , score4 , score5 , score6 , score7 ]
  i1i1iI1i1Iii = np . array ( i1i1iI1i1Iii )
  I1i = np . sum ( i1i1iI1i1Iii != 0 )
  if I1i >= 3 :
   return True
  return False
  if 64 - 64: i1I1 + ooOOO * IIiIIiIi11I1 - i1 - O000o - OooOoo
 def funnel_hand_tool ( self , hands , siderosphere ) :
  if hands . shape [ 0 ] != 0 :
   for IiI11I in hands :
    IiiIii11iII1 = IiI11I [ : 4 ]
    if iou ( IiiIii11iII1 , siderosphere [ 0 ] [ : 4 ] ) > 0 :
     return False
   return True
  else :
   return True
   if 50 - 50: i1I1 % OooOoo
 def judge_grip ( self , hand_front , beaker_box , glass_rod_box ) :
  II1IiI1I = 0
  if hand_front . shape [ 0 ] == 2 :
   for IiI11I in hand_front :
    IiiIii11iII1 = IiI11I [ : 4 ]
    if iou ( IiiIii11iII1 , beaker_box ) > 0 or iou ( IiiIii11iII1 , glass_rod_box ) > 0 :
     II1IiI1I += 1
  else :
   return False
  if II1IiI1I == 2 :
   return True
   if 76 - 76: IIiIIiIi11I1 * iI1iII1I1I1i / IIiIIiIi11I1 % i1iiIII111 + O000o
   if 98 - 98: iI1iII1I1I1i - I1I + i1 * ooo000 % i1
   if 100 - 100: i1iiIII111 . IIiIIiIi11I1 * ooo000 * ooo000
 def folded_filter_paper ( self , folded_filter_paper_front , funnel_front , funnel_mouth_front ) :
  if self . judge_folded_paper ( folded_filter_paper_front , funnel_front , funnel_mouth_front ) :
   return True
  return False
  if 85 - 85: IIiIIiIi11I1 / OooOoo . O0OO0OooooOo % Oo + Oo - i1I1
  if 59 - 59: OooOoo
 def filter_paper_fixed_funnel ( self , funnel_side , wash_bottle_side , folded_filter_paper_side , hand_side , funnel_front ,
 wash_bottle_front , folded_filter_paper_front , hand_front , funnel_top , wash_bottle_top ,
 folded_filter_paper_top , hand_top , glass_rod_side , glass_rod_front , glass_rod_top ) :
  if 53 - 53: i1i1i1111I / ooOOO - ii + ooo000 * i1i1i1111I * i1iiIII111
  if funnel_side . shape [ 0 ] != 0 and wash_bottle_side . shape [ 0 ] != 0 and hand_side . shape [ 0 ] != 0 :
   if iou ( funnel_side [ 0 ] [ : 4 ] , wash_bottle_side [ 0 ] [ : 4 ] ) > 0 and self . hand_sth ( hand_side , wash_bottle_side ) :
    self . flag2 = True
    self . filer_paper_fixed_secs_pre = self . secs
  elif funnel_front . shape [ 0 ] != 0 and wash_bottle_front . shape [ 0 ] != 0 and hand_front . shape [ 0 ] != 0 :
   if iou ( funnel_front [ 0 ] [ : 4 ] , wash_bottle_front [ 0 ] [ : 4 ] ) > 0 and self . hand_sth ( hand_front , wash_bottle_front ) :
    self . flag2 = True
    self . filer_paper_fixed_secs_pre = self . secs
  elif funnel_top . shape [ 0 ] != 0 and wash_bottle_top . shape [ 0 ] != 0 and hand_top . shape [ 0 ] != 0 :
   if iou ( funnel_top [ 0 ] [ : 4 ] , wash_bottle_top [ 0 ] [ : 4 ] ) > 0 and self . hand_sth ( hand_top , wash_bottle_top ) :
    self . flag2 = True
    self . filer_paper_fixed_secs_pre = self . secs
    if 87 - 87: i1iiIII111 - IIiIIiIi11I1 * Ii % i1i1i1111I % i1
  if self . flag2 is True :
   if glass_rod_side . shape [ 0 ] != 0 and funnel_side . shape [ 0 ] != 0 and self . flag2 :
    if iou ( glass_rod_side [ 0 ] [ : 4 ] , funnel_side [ 0 ] [ : 4 ] ) > 0 :
     if 81 - 81: i1 + i1i1i1111I * Oo - Oo * I1Ii1I1 - oOo0O00
     self . filer_paper_fixed_secs = self . secs
     if ( self . filer_paper_fixed_secs - self . filer_paper_fixed_secs_pre ) < 10 :
      self . filer_paper_fixed_secs = 0.
      self . filer_paper_fixed_secs_pre = 0.
      self . flag2 = False
      return True
   if glass_rod_front . shape [ 0 ] != 0 and funnel_front . shape [ 0 ] != 0 and self . flag2 :
    if iou ( glass_rod_front [ 0 ] [ : 4 ] , funnel_front [ 0 ] [ : 4 ] ) > 0 :
     self . filer_paper_fixed_secs = self . secs
     if ( self . filer_paper_fixed_secs - self . filer_paper_fixed_secs_pre ) < 10 :
      self . filer_paper_fixed_secs = 0.
      self . filer_paper_fixed_secs_pre = 0.
      self . flag2 = False
      return True
      if 4 - 4: i1iiIII111
   if glass_rod_top . shape [ 0 ] != 0 and funnel_top . shape [ 0 ] != 0 and self . flag2 :
    if iou ( glass_rod_top [ 0 ] [ : 4 ] , funnel_top [ 0 ] [ : 4 ] ) > 0 :
     self . filer_paper_fixed_secs = self . secs
     if ( self . filer_paper_fixed_secs - self . filer_paper_fixed_secs_pre ) < 10 :
      self . filer_paper_fixed_secs = 0.
      self . filer_paper_fixed_secs_pre = 0.
      self . flag2 = False
      return True
      if 8 - 8: IiIIii11Ii + OooOoo - i1
  return False
  if 68 - 68: I1Ii1I1 % I1Ii1I1 / ii . ooo000
  if 80 - 80: IIiIIiIi11I1 / OooOoo % iI1iII1I1I1i / ooOOO * ooOOO - Iii1i
 def bottom_up_build_equipment ( self , siderosphere_top , siderosphere_front , retort_stand_front , beaker_front ,
 funnel_front , funnel_mouth_front , folded_filter_paper_front , retort_stand_side ,
 beaker_side , siderosphere_side , funnel_side , funnel_mouth_side , folded_filter_paper_side ) :
  O00 = True
  if siderosphere_top . shape [ 0 ] != 0 and O00 :
   oOoOO0O0 = siderosphere_top [ 0 ] [ 2 ] - siderosphere_top [ 0 ] [ 0 ]
   IIi1I1I1i = siderosphere_top [ 0 ] [ 3 ] - siderosphere_top [ 0 ] [ 1 ]
   O00 = False
  elif siderosphere_front . shape [ 0 ] != 0 and O00 :
   oOoOO0O0 = siderosphere_front [ 0 ] [ 2 ] - siderosphere_front [ 0 ] [ 0 ]
   IIi1I1I1i = siderosphere_front [ 0 ] [ 3 ] - siderosphere_front [ 0 ] [ 1 ]
   O00 = False
   if 60 - 60: O000o * i1i1i1111I / iI1iII1I1I1i
  if not O00 :
   if oOoOO0O0 > IIi1I1I1i :
    if self . score3_stage1_false ( retort_stand_front , beaker_front , siderosphere_front , funnel_front ,
 funnel_mouth_front , folded_filter_paper_front ) :
     if 45 - 45: Ooo0Ooo + ooOOO * oOo0O00 - ooo000 / IIiIIiIi11I1
     self . build_up_false_secs , self . build_up_false_secs_pre , I1I1 = self . duration ( self . build_up_false_secs , 0.5 ,
 self . build_up_false_secs_pre , 0.5 )
     if I1I1 :
      self . build_up_false_secs = 0.
      self . build_up_false_secs_pre = 0.
      self . build_mistake = True
      if 14 - 14: O0OO0OooooOo - IiIIii11Ii
    if not self . flag3 and self . score3_stage1_true ( retort_stand_front , beaker_front ,
 siderosphere_front , funnel_front ,
 funnel_mouth_front , folded_filter_paper_front ) :
     self . flag3 = True
     if 74 - 74: oOo0O00 * ooo000 . ooOOO
    if self . flag3 is True :
     if self . score3_stage2_true_front ( retort_stand_front , beaker_front , siderosphere_front ,
 funnel_front , funnel_mouth_front ,
 folded_filter_paper_front ) and not self . build_mistake :
      self . flag3 = False
      return True
   elif oOoOO0O0 <= IIi1I1I1i :
    if self . score3_stage1_false ( retort_stand_side , beaker_side , siderosphere_side , funnel_side ,
 funnel_mouth_side , folded_filter_paper_side ) :
     if 2 - 2: Ii * IIiIIiIi11I1 % i1 + IiIIii11Ii % i1
     self . build_up_side_false_secs , self . build_up_side_false_secs_pre , I1I1 = self . duration ( self . build_up_side_false_secs , 0.5 ,
 self . build_up_side_false_secs_pre , 0.5 )
     if I1I1 :
      self . build_up_side_false_secs = 0.
      self . build_up_side_false_secs_pre = 0.
      self . build_mistake = True
    if not self . flag3 and self . score3_stage1_true ( retort_stand_side , beaker_side ,
 siderosphere_side , funnel_side ,
 funnel_mouth_side , folded_filter_paper_side ) :
     self . flag3 = True
    if self . flag3 is True :
     if self . score3_stage2_true_side ( retort_stand_side , beaker_side , siderosphere_side ,
 funnel_side , funnel_mouth_side ,
 folded_filter_paper_side ) and not self . build_mistake :
      self . flag3 = False
      return True
      if 82 - 82: ooOOO % OooOoo
  return False
  if 81 - 81: Ii
  if 40 - 40: O0OO0OooooOo . OooOoo + oOo0O00 . i1iiIII111
 def funnel_closed_beaker ( self , siderosphere_top , siderosphere_front , retort_stand_front , beaker_front , funnel_front ,
 funnel_mouth_front , folded_filter_paper_front , hand_front , retort_stand_side , beaker_side ,
 siderosphere_side , funnel_side , funnel_mouth_side , folded_filter_paper_side , hand_side ) :
  oo0O0 = True
  if siderosphere_top . shape [ 0 ] != 0 and oo0O0 :
   oOoOO0O0 = siderosphere_top [ 0 ] [ 2 ] - siderosphere_top [ 0 ] [ 0 ]
   IIi1I1I1i = siderosphere_top [ 0 ] [ 3 ] - siderosphere_top [ 0 ] [ 1 ]
   oo0O0 = False
  elif siderosphere_front . shape [ 0 ] != 0 and oo0O0 :
   oOoOO0O0 = siderosphere_front [ 0 ] [ 2 ] - siderosphere_front [ 0 ] [ 0 ]
   IIi1I1I1i = siderosphere_front [ 0 ] [ 3 ] - siderosphere_front [ 0 ] [ 1 ]
   oo0O0 = False
   if 65 - 65: ooOOO / oOo0O00 - i1iiIII111
  if not oo0O0 :
   if oOoOO0O0 > IIi1I1I1i :
    if self . score3_stage2_true_front ( retort_stand_front , beaker_front , siderosphere_front ,
 funnel_front , funnel_mouth_front , folded_filter_paper_front ) :
     self . flag4 = True
     if 15 - 15: OooOoo . ooo000 / IiIIii11Ii % i1i1i1111I
    if self . flag4 is True :
     if hand_front . shape [ 0 ] != 0 and retort_stand_front . shape [ 0 ] != 0 and beaker_front . shape [ 0 ] != 0 :
      if 51 - 51: ooOOO
      for IiI11I in hand_front :
       IiiIii11iII1 = IiI11I [ : 4 ]
       for II1III1I1i in beaker_front :
        II11i11II1iI = II1III1I1i [ : 4 ]
        if iou ( retort_stand_front [ 0 ] [ : 4 ] , II11i11II1iI ) > 0 and II11i11II1iI [ 3 ] < retort_stand_front [ 0 ] [ : 4 ] [ 3 ] :
         if 69 - 69: iI1iII1I1I1i
         if iou ( IiiIii11iII1 , II11i11II1iI ) > 0 :
          self . flag4 = False
          return True
          if 48 - 48: ooOOO * ooo000 % IiIIii11Ii * i1 . Iii1i - ii
   elif oOoOO0O0 <= IIi1I1I1i :
    if self . score3_stage2_true_side ( retort_stand_side , beaker_side , siderosphere_side ,
 funnel_side , funnel_mouth_side , folded_filter_paper_side ) :
     self . flag4 = True
     if 72 - 72: i1 % i1i1i1111I * iI1iII1I1I1i
    if self . flag4 is True :
     if hand_side . shape [ 0 ] != 0 and retort_stand_side . shape [ 0 ] != 0 and beaker_side . shape [ 0 ] != 0 :
      if 90 - 90: Ooo0Ooo * OooOoo . Ii
      for IiI11I in hand_side :
       IiiIii11iII1 = IiI11I [ : 4 ]
       for II1III1I1i in beaker_side :
        II11i11II1iI = II1III1I1i [ : 4 ]
        if iou ( retort_stand_side [ 0 ] [ : 4 ] , II11i11II1iI ) > 0 and II11i11II1iI [ 3 ] < retort_stand_side [ 0 ] [ : 4 ] [ 3 ] :
         if 5 - 5: Oo - i1 . O000o
         if iou ( IiiIii11iII1 , II11i11II1iI ) > 0 :
          self . flag4 = False
          return True
          if 18 - 18: IiIIii11Ii - O000o * O0OO0OooooOo - OooOoo
  return False
  if 54 - 54: IIiIIiIi11I1 . Ooo0Ooo % Ii + IiIIii11Ii * iI1iII1I1I1i / iI1iII1I1I1i
 def score_process ( self , top_true , front_true , side_true ) :
  if 31 - 31: IiIIii11Ii . IiIIii11Ii % Ii
  if top_true or front_true or side_true :
   if top_true :
    OoOo0 , iI , iii1i1iiIi1 , Ii1I , iiiiIi1IiiIi , Ii1iIII11i , oo000OO0ooO , OoO0OooO0ooo , O00OO00O , i111iIIiIIII , oOO0OOo , ooo , o0Oo0o000O0oO , OoO0OOo00oo0O , i1IiI1i = self . preds_top
    if 55 - 55: ii % O000o * ii . ooOOO * Iii1i
    if 24 - 24: oOo0O00 * IiIIii11Ii + Iii1i
   if side_true :
    i1Iii11ii11 , IIIiII1I , ii1i , I1II1IIIi , IiI111I1 , oO0oo , IiIII , i1IiiI11i , o0oOoOoO , O0OOoOoOo0O0O , IiI , oO0OoOoo , iI11iii , Ii1i1 , iII11I11111I = self . preds_side
    if 81 - 81: iI1iII1I1I1i / IIiIIiIi11I1 . iI1iII1I1I1i
    if 81 - 81: O0OO0OooooOo + IiIIii11Ii . i1I1
   if front_true :
    IIiiIIi1i , O00oO00oO0O , iiI1i11ii , I111iIIII , O0o00OoOo00O , O00oOo00oOO00 , o0oO0O0Oo00 , IIiIIiiIIi , iiIi , Ii1Iiii11i1 , oO00oO0O , ooOOoO00OO , O0Ooo0oOo0 , Oo00oOooOO , IiIooO0OoOo = self . preds_front
    if 48 - 48: i1iiIII111 . Oo
    if 92 - 92: OooOoo + Ii / IIiIIiIi11I1 + OooOoo * IIiIIiIi11I1 * iI1iII1I1I1i
    if 79 - 79: i1i1i1111I
   if not self . scorePoint1 :
    if self . folded_filter_paper ( O00oO00oO0O , O0o00OoOo00O , O00oOo00oOO00 ) :
     Ii111 = 0.1
     self . assignScore ( index = 1 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = Ii111 ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "1.jpg" ,
 preds = self . preds_front
 )
     if 68 - 68: oOo0O00 . oOo0O00 / Ii . i1
     if 54 - 54: iI1iII1I1I1i % Oo . ii - Iii1i % i1I1 * O0OO0OooooOo
   if not self . scorePoint2 :
    if 31 - 31: oOo0O00 / Iii1i - IiIIii11Ii % O0OO0OooooOo / I1Ii1I1 - i1i1i1111I
    if 68 - 68: i1I1 . i1I1 % i1I1
    if 71 - 71: ooo000
    if 61 - 61: ooo000
    if 48 - 48: Iii1i * i1i1i1111I + IiIIii11Ii
    if 31 - 31: Oo * i1iiIII111 % Ii / O000o + I1Ii1I1 + iI1iII1I1I1i
    if 90 - 90: I1Ii1I1 * i1i1i1111I / iI1iII1I1I1i * Ii
    if 38 - 38: I1I . Ii
    if 41 - 41: ooo000 % IIiIIiIi11I1 % ooOOO
    if 5 - 5: oOo0O00 / Ii + i1iiIII111 * Oo + Ooo0Ooo + ooo000
    if 96 - 96: i1iiIII111 - IIiIIiIi11I1 / IIiIIiIi11I1 * IiIIii11Ii
    if 67 - 67: Ooo0Ooo . Ooo0Ooo . ii
    if 24 - 24: i1iiIII111 + i1i1i1111I . oOo0O00 + iI1iII1I1I1i + ii
    if 92 - 92: iI1iII1I1I1i / iI1iII1I1I1i + IiIIii11Ii . ii
    if 56 - 56: Ii * ooo000 . IiIIii11Ii
    if 66 - 66: I1Ii1I1 * OooOoo . iI1iII1I1I1i % OooOoo . i1 . IiIIii11Ii
    if 47 - 47: Ii % OooOoo % iI1iII1I1I1i * IiIIii11Ii
    if 48 - 48: O0OO0OooooOo . i1I1 / ooo000 + i1iiIII111
    if 84 - 84: Oo / I1Ii1I1 . IIiIIiIi11I1
    if 67 - 67: Oo % ooOOO + iI1iII1I1I1i * I1I
    if 79 - 79: IIiIIiIi11I1 * Oo / OooOoo
    if 10 - 10: iI1iII1I1I1i / i1iiIII111 . IiIIii11Ii * i1i1i1111I
    if 71 - 71: oOo0O00 + I1Ii1I1 / i1I1 + Oo / I1I
    if 18 - 18: Iii1i - IiIIii11Ii
    if 71 - 71: iI1iII1I1I1i + OooOoo % i1i1i1111I % oOo0O00 . ooo000
    if 92 - 92: i1I1 - Ooo0Ooo - i1i1i1111I % i1iiIII111 / i1i1i1111I * iI1iII1I1I1i
    if 60 - 60: IiIIii11Ii % O000o / O0OO0OooooOo * OooOoo / i1I1 - Ii
    if 16 - 16: oOo0O00 / I1Ii1I1 / i1 + i1I1 + oOo0O00
    if 11 - 11: O000o / OooOoo + oOo0O00
    if 79 - 79: i1I1 . I1Ii1I1 * O0OO0OooooOo % I1Ii1I1 / ii
    if 93 - 93: O0OO0OooooOo + Iii1i . Ii . O0OO0OooooOo * ooOOO
    if 84 - 84: Ooo0Ooo % ii
    if 82 - 82: IIiIIiIi11I1
    if 81 - 81: oOo0O00 + i1 - ooo000 * iI1iII1I1I1i + i1i1i1111I
    if 89 - 89: I1Ii1I1
    if 57 - 57: iI1iII1I1I1i - i1iiIII111 / OooOoo % i1iiIII111
    if 92 - 92: IiIIii11Ii * OooOoo - IiIIii11Ii
    if 66 - 66: i1iiIII111 . iI1iII1I1I1i / ooOOO . i1 - OooOoo
    if 13 - 13: oOo0O00
    if 50 - 50: i1 - i1iiIII111 / i1iiIII111 % I1Ii1I1 / IIiIIiIi11I1
    if 66 - 66: oOo0O00 - Iii1i - ooo000 . i1I1
    if 59 - 59: O0OO0OooooOo / IiIIii11Ii
    if 7 - 7: oOo0O00
    if 64 - 64: IIiIIiIi11I1 * O000o + Oo . OooOoo - ooOOO
    if 94 - 94: IiIIii11Ii - ooo000 . Ii
    if 73 - 73: IiIIii11Ii / oOo0O00 % ooo000 . iI1iII1I1I1i % O000o
    if 36 - 36: ii * OooOoo . ooo000 . i1iiIII111 + O000o
    if 47 - 47: ii / i1I1
    if 52 - 52: Ii . OooOoo . i1iiIII111 * i1I1 - iI1iII1I1I1i
    if 20 - 20: OooOoo % ii + I1Ii1I1 + ii - oOo0O00
    if 76 - 76: i1I1 % IIiIIiIi11I1 % O0OO0OooooOo
    if 39 - 39: IiIIii11Ii . Oo + O0OO0OooooOo - oOo0O00
    if 93 - 93: Iii1i * IIiIIiIi11I1 % O0OO0OooooOo + i1 % Ii * O0OO0OooooOo
    if 62 - 62: ii % ooo000
    if 19 - 19: Ii / Oo % Iii1i / i1iiIII111 - OooOoo - Ooo0Ooo
    if 89 - 89: i1I1 - ii
    if 61 - 61: Ii * OooOoo * I1I % i1iiIII111 % IIiIIiIi11I1 * i1I1
    if 49 - 49: iI1iII1I1I1i / i1iiIII111 % O000o
    if 46 - 46: ooOOO * IIiIIiIi11I1 % i1 / O000o + i1 + oOo0O00
    if 99 - 99: I1I * IIiIIiIi11I1 * i1iiIII111
    if 62 - 62: ooOOO % Oo + O0OO0OooooOo
    if 87 - 87: ooo000 - OooOoo + Ii + i1i1i1111I + IiIIii11Ii
    if 57 - 57: IIiIIiIi11I1 + I1I / ooOOO % ooOOO % Oo / ii
    if 95 - 95: i1 / i1I1 . i1 / Oo . Ooo0Ooo
    if 43 - 43: Oo - OooOoo * O000o . Ooo0Ooo / IIiIIiIi11I1 * IIiIIiIi11I1
    if 84 - 84: i1iiIII111 + oOo0O00
    if 83 - 83: i1i1i1111I
    if 84 - 84: O000o / Ii * Ooo0Ooo / Ii / ooo000
    if 64 - 64: oOo0O00 * Ii
    if self . filter_paper_fixed_funnel ( IiI111I1 , o0oOoOoO , IIIiII1I , i1Iii11ii11 ,
 O0o00OoOo00O , iiIi , O00oO00oO0O , IIiiIIi1i ,
 iiiiIi1IiiIi , O00OO00O , iI , OoOo0 ,
 I1II1IIIi , I111iIIII , Ii1I ) :
     Ii111 = 0.1
     self . assignScore ( index = 2 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = Ii111 ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "2.jpg" ,
 preds = self . preds_front
 )
   self . status_list_judge ( OoO0OooO0ooo , IIiIIiiIIi , o0oO0O0Oo00 , iiI1i11ii ,
 O0o00OoOo00O , O00oOo00oOO00 , O00oO00oO0O , IiIII ,
 ii1i , i1IiiI11i , IiI111I1 , oO0oo , IIIiII1I )
   if not self . check_beaker_shape_flag and IiIooO0OoOo . shape [ 0 ] != 0 :
    if 1 in self . status_list :
     if self . collect_beaker_funnel_bbox ( iiI1i11ii , O0o00OoOo00O , o0oO0O0Oo00 ) :
      pass
     else :
      Ii111 = 0.1
      self . assignError ( index = 3 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = Ii111 ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "3.jpg" ,
 preds = self . preds_front
 )
   if not self . scorePoint3 :
    if 2 - 2: ii % i1iiIII111 . oOo0O00
    if 59 - 59: i1I1 % OooOoo - iI1iII1I1I1i % I1I + i1iiIII111 . I1Ii1I1
    if 94 - 94: ooOOO * I1Ii1I1 * i1iiIII111 . oOo0O00
    if 73 - 73: I1Ii1I1 / ooo000 % i1I1 - i1i1i1111I + Oo - I1Ii1I1
    if 18 - 18: i1 + ooOOO . i1 - iI1iII1I1I1i
    if 97 - 97: oOo0O00 + O0OO0OooooOo % Iii1i
    if 34 - 34: i1 + Oo . oOo0O00 - ooo000 / i1I1 * oOo0O00
    if 89 - 89: oOo0O00
    if 48 - 48: i1 / IIiIIiIi11I1 / iI1iII1I1I1i / ii * IiIIii11Ii
    if 54 - 54: IIiIIiIi11I1 % I1I % ii / i1I1 . i1I1 - IiIIii11Ii
    if 10 - 10: Ii . i1I1 % O0OO0OooooOo / OooOoo % I1Ii1I1
    if 42 - 42: Oo - I1I * O0OO0OooooOo * i1i1i1111I - i1I1
    if 58 - 58: iI1iII1I1I1i
    if 17 - 17: iI1iII1I1I1i - Ii % iI1iII1I1I1i % oOo0O00 * Iii1i
    if 51 - 51: I1I . i1i1i1111I % Ii
    if 55 - 55: i1i1i1111I * Ii % i1i1i1111I
    if 61 - 61: oOo0O00
    if 53 - 53: Ooo0Ooo / IiIIii11Ii
    if 49 - 49: ooo000 - O000o . IiIIii11Ii / Oo
    if 23 - 23: i1I1 - i1 / Iii1i . iI1iII1I1I1i + O000o
    if 55 - 55: i1 - iI1iII1I1I1i / OooOoo + I1I + Oo
    if 5 - 5: ii - i1 . i1i1i1111I / ii . iI1iII1I1I1i . ii
    if 87 - 87: i1 . Ii * iI1iII1I1I1i - O000o / Ii / OooOoo
    if 65 - 65: O0OO0OooooOo / O0OO0OooooOo + ii
    if 99 - 99: i1 + OooOoo + i1I1 * Ooo0Ooo / ooOOO + Ii
    if 72 - 72: I1Ii1I1 * Ooo0Ooo * IIiIIiIi11I1 % IiIIii11Ii . ooo000
    if 68 - 68: Ooo0Ooo * OooOoo - oOo0O00
    if 49 - 49: IIiIIiIi11I1 % i1
    if 29 - 29: OooOoo * Ii - O000o
    if 53 - 53: i1I1 % ooo000 / ooOOO / I1I
    if 43 - 43: iI1iII1I1I1i . i1i1i1111I + I1I % ooOOO . ii - ii
    if 6 - 6: I1I
    if 98 - 98: O000o * IIiIIiIi11I1 / i1iiIII111 / Iii1i + I1I
    if 25 - 25: IIiIIiIi11I1 . ii / I1I * i1 - i1iiIII111 % oOo0O00
    if 49 - 49: IiIIii11Ii % ooOOO + i1I1 + IIiIIiIi11I1
    if 60 - 60: IIiIIiIi11I1
    if 98 - 98: IiIIii11Ii / Ooo0Ooo + Ii
    if 73 - 73: OooOoo * Iii1i
    if 34 - 34: O0OO0OooooOo % Ooo0Ooo * OooOoo + i1iiIII111 / i1
    if 49 - 49: IIiIIiIi11I1 / i1iiIII111 % IIiIIiIi11I1 + IIiIIiIi11I1 * iI1iII1I1I1i
    if 22 - 22: I1Ii1I1 + O000o / I1Ii1I1 - Ii % Ii % i1i1i1111I
    if 86 - 86: Iii1i
    if 53 - 53: i1 * i1i1i1111I
    if 91 - 91: I1I . i1I1
    if 59 - 59: ii . ii * IIiIIiIi11I1
    if 85 - 85: Iii1i . O000o % Iii1i - Iii1i
    if 68 - 68: O000o + Iii1i + Ooo0Ooo % Oo / i1I1 . OooOoo
    if 31 - 31: i1I1 % ooOOO
    if 46 - 46: i1i1i1111I - ooo000 + iI1iII1I1I1i
    if 73 - 73: i1 * oOo0O00
    if 88 - 88: Ii
    if 12 - 12: ooo000 - IIiIIiIi11I1 % Iii1i . I1Ii1I1
    if 11 - 11: i1iiIII111 - Oo % Ii % i1
    if 28 - 28: IIiIIiIi11I1 % Ii + ooOOO . O0OO0OooooOo % Ii * I1Ii1I1
    if 41 - 41: I1I
    if 76 - 76: ooo000 * i1i1i1111I
    if 39 - 39: i1 % O0OO0OooooOo
    if 50 - 50: i1iiIII111 % OooOoo - i1i1i1111I * IiIIii11Ii % Oo . Ooo0Ooo
    if 30 - 30: i1iiIII111
    if 78 - 78: ooo000 % Iii1i + ooOOO * IIiIIiIi11I1 - i1
    if 46 - 46: Ooo0Ooo - O0OO0OooooOo / ooo000 * ii . oOo0O00
    if 32 - 32: i1i1i1111I . OooOoo + OooOoo - ooo000 * IiIIii11Ii + Oo
    if 12 - 12: oOo0O00
    if 57 - 57: Oo + i1i1i1111I / I1Ii1I1
    if 56 - 56: O000o % Ooo0Ooo % Iii1i . i1i1i1111I
    if 46 - 46: ii . i1iiIII111 % Iii1i - Ooo0Ooo + ooo000
    if 100 - 100: O000o
    if 32 - 32: I1Ii1I1 % ooo000 * OooOoo / oOo0O00 + ooOOO
    if 64 - 64: I1Ii1I1 . Ooo0Ooo
    if 36 - 36: IIiIIiIi11I1 + IiIIii11Ii . i1 + IIiIIiIi11I1
    if 77 - 77: iI1iII1I1I1i / OooOoo . Iii1i + i1iiIII111 - ii
    if 49 - 49: i1iiIII111 - ii - OooOoo
    if self . status_list == self . status_template :
     Ii111 = 0.1
     self . assignScore ( index = 3 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = Ii111 ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "3.jpg" ,
 preds = self . preds_front
 )
    if self . status_list == self . status_error_template :
     Ii111 = 0.1
     self . assignError ( index = 1 ,
 img = self . build_up_error_img ,
 object = self . objects_front ,
 conf = Ii111 ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "1.jpg" ,
 preds = self . build_up_error_pred
 )
   if not self . scorePoint4 :
    if 39 - 39: I1I % i1iiIII111 - I1Ii1I1
    if 51 - 51: IIiIIiIi11I1 + i1 % i1iiIII111
    if 49 - 49: IiIIii11Ii - O0OO0OooooOo . I1I
    if 76 - 76: O000o / iI1iII1I1I1i . I1I * oOo0O00 - i1i1i1111I
    if 53 - 53: OooOoo - oOo0O00 * ooOOO / OooOoo * Ooo0Ooo * ooo000
    if 10 - 10: IIiIIiIi11I1 % ooo000 % i1I1 % Ooo0Ooo
    if 70 - 70: IiIIii11Ii
    if 90 - 90: i1i1i1111I % i1 . IiIIii11Ii * ii / Ii
    if 73 - 73: ooo000 * Ooo0Ooo + Iii1i . ooOOO . i1I1 / i1I1
    if 72 - 72: O0OO0OooooOo * iI1iII1I1I1i / ooo000 + O0OO0OooooOo - i1I1
    if 20 - 20: IIiIIiIi11I1 . oOo0O00 . Ooo0Ooo
    if 11 - 11: OooOoo
    if 45 - 45: iI1iII1I1I1i + i1I1 / IIiIIiIi11I1
    if 45 - 45: iI1iII1I1I1i . iI1iII1I1I1i * i1i1i1111I + oOo0O00
    if 6 - 6: Iii1i . Oo + I1Ii1I1 * i1 * I1Ii1I1 % O000o
    if 21 - 21: Ooo0Ooo % i1 - ooo000
    if 81 - 81: Ooo0Ooo / ooo000
    if 4 - 4: I1I % O0OO0OooooOo - ooo000 - I1I . ooOOO / i1i1i1111I
    if 74 - 74: O000o
    if 24 - 24: I1I + Oo - ooOOO
    if 86 - 86: i1iiIII111 % ooo000 % ooo000 % O0OO0OooooOo
    if 15 - 15: iI1iII1I1I1i + I1Ii1I1 % oOo0O00
    if 79 - 79: OooOoo . Oo + oOo0O00 / I1Ii1I1 . IiIIii11Ii
    if 89 - 89: ooo000 % Ooo0Ooo
    if 77 - 77: ooo000 % Ooo0Ooo
    if 24 - 24: O000o * I1Ii1I1 * I1Ii1I1 % IIiIIiIi11I1
    if 37 - 37: i1iiIII111 / iI1iII1I1I1i
    if 80 - 80: IiIIii11Ii
    if 2 - 2: I1I / O000o - IIiIIiIi11I1 % Ooo0Ooo
    if 88 - 88: iI1iII1I1I1i - I1Ii1I1 - O0OO0OooooOo . Iii1i
    if 98 - 98: Ii + ooOOO
    if 29 - 29: I1Ii1I1 + O0OO0OooooOo - IIiIIiIi11I1 * i1I1 % Oo
    if 74 - 74: ooOOO
    if 100 - 100: O000o + iI1iII1I1I1i . I1I % Oo - i1
    if 39 - 39: iI1iII1I1I1i
    if 34 - 34: iI1iII1I1I1i . i1 . I1I
    if 95 - 95: IiIIii11Ii * ii * Ooo0Ooo * ii / OooOoo
    if 27 - 27: O0OO0OooooOo . IiIIii11Ii
    if 69 - 69: O000o % i1iiIII111 / oOo0O00
    if 38 - 38: i1I1 + Oo * Ooo0Ooo / ooOOO . OooOoo
    if 90 - 90: OooOoo / i1iiIII111
    if 32 - 32: IIiIIiIi11I1 - O0OO0OooooOo / ooOOO * Ooo0Ooo * iI1iII1I1I1i - i1i1i1111I
    if 82 - 82: ooo000
    if 66 - 66: IiIIii11Ii + IIiIIiIi11I1 - O0OO0OooooOo + i1i1i1111I . iI1iII1I1I1i * IiIIii11Ii
    if 9 - 9: I1I - I1I - ooOOO - oOo0O00 + i1iiIII111
    if 71 - 71: O0OO0OooooOo / i1iiIII111 - Ii * Oo . iI1iII1I1I1i
    if 3 - 3: I1Ii1I1
    if 57 - 57: Ooo0Ooo . OooOoo / oOo0O00 * I1Ii1I1
    if 36 - 36: IiIIii11Ii
    if 33 - 33: IiIIii11Ii
    if 86 - 86: Ii / oOo0O00 - i1 * i1i1i1111I - Oo * Iii1i
    if 28 - 28: OooOoo . i1 % iI1iII1I1I1i % Iii1i
    if 2 - 2: Oo + OooOoo - i1i1i1111I - ooo000 / Oo . Oo
    if 41 - 41: OooOoo + OooOoo - OooOoo
    if 9 - 9: Iii1i % I1Ii1I1 % IiIIii11Ii - I1I * OooOoo
    if 53 - 53: iI1iII1I1I1i * i1i1i1111I / OooOoo . O0OO0OooooOo . ooo000
    if 45 - 45: OooOoo + ooOOO / i1i1i1111I * i1
    if 71 - 71: ii % Iii1i + oOo0O00 * i1I1 / ii
    if 66 - 66: ooo000 * oOo0O00
    if 83 - 83: i1
    if 64 - 64: i1 . ii - i1I1 . Iii1i
    if 47 - 47: ooo000 / Ooo0Ooo % IiIIii11Ii
    if 70 - 70: IIiIIiIi11I1 / Iii1i . i1i1i1111I % ooOOO . Ii / Ii
    if 51 - 51: i1I1 + Ooo0Ooo - ooo000 * O000o . O000o
    if self . funnel_closed_beaker ( OoO0OooO0ooo , IIiIIiiIIi , o0oO0O0Oo00 , iiI1i11ii ,
 O0o00OoOo00O , O00oOo00oOO00 , O00oO00oO0O , IIiiIIi1i ,
 IiIII , ii1i , i1IiiI11i , IiI111I1 ,
 oO0oo , IIIiII1I , i1Iii11ii11 ) :
     Ii111 = 0.1
     self . assignScore ( index = 4 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = Ii111 ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "4.jpg" ,
 preds = self . preds_front
 )
     if 79 - 79: i1i1i1111I + oOo0O00
   if ( not self . scorePoint5 or not self . scorePoint6 ) and (
 self . scorePoint3 is True or self . scorePoint4 is True ) :
    if I111iIIII . shape [ 0 ] != 0 and iiI1i11ii . shape [ 0 ] != 0 and O0o00OoOo00O . shape [ 0 ] != 0 and IIiIIiiIIi . shape [ 0 ] != 0 :
     if 11 - 11: OooOoo / i1iiIII111 % O0OO0OooooOo - i1i1i1111I * oOo0O00
     for II1III1I1i in iiI1i11ii :
      II11i11II1iI = II1III1I1i [ : 4 ]
      if II11i11II1iI [ 1 ] < IIiIIiiIIi [ 0 ] [ 1 ] :
       if iou ( II11i11II1iI , I111iIIII [ 0 ] [ : 4 ] ) > 0.15 * box_area ( II11i11II1iI ) and self . judge_grip ( IIiiIIi1i , II11i11II1iI , I111iIIII [ 0 ] [ : 4 ] ) :
        if 90 - 90: i1 * i1 . Ooo0Ooo . Oo
        self . scorePoint5 = True
        self . scorePoint6 = True
        self . scorePoint8 = False
        Ii111 = 0.1
        self . assignScore ( index = 5 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = Ii111 ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "5.jpg" ,
 preds = self . preds_front
 )
        Ii111 = 0.1
        self . assignScore ( index = 6 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = Ii111 ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "6.jpg" ,
 preds = self . preds_front
 )
        continue
        if 59 - 59: Ii % I1Ii1I1 + Iii1i . OooOoo * Iii1i
   if not self . scorePoint7 and self . scorePoint5 and self . scorePoint6 :
    if Ii1Iiii11i1 . shape [ 0 ] != 0 :
     self . observe_liquid_cleaned_secs , self . observe_liquid_cleaned_secs_pre , I1I1 = self . duration (
 self . observe_liquid_cleaned_secs , 40 ,
 self . observe_liquid_cleaned_secs_pre , 1 )
     if I1I1 :
      self . observe_liquid_cleaned_secs = 0.
      self . observe_liquid_cleaned_secs_pre = 0.
      self . scorePoint7 = True
      self . scorePoint8 = False
     Ii111 = 0.1
     self . assignScore ( index = 7 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = Ii111 ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "7.jpg" ,
 preds = self . preds_front
 )
     if 21 - 21: i1I1 + ooOOO % IiIIii11Ii / OooOoo
    if O0OOoOoOo0O0O . shape [ 0 ] != 0 :
     self . observe_liquid_cleaned_secs , self . observe_liquid_cleaned_secs_pre , I1I1 = self . duration (
 self . observe_liquid_cleaned_secs , 40 ,
 self . observe_liquid_cleaned_secs_pre , 1 )
     if 96 - 96: Oo * i1iiIII111 . Ooo0Ooo
     if I1I1 :
      self . observe_liquid_cleaned_secs = 0.
      self . observe_liquid_cleaned_secs_pre = 0.
      self . scorePoint7 = True
      self . scorePoint8 = False
     Ii111 = 0.1
     self . assignScore ( index = 7 ,
 img = self . frame_side ,
 object = self . objects_side ,
 conf = Ii111 ,
 time_frame = self . time_side ,
 num_frame = self . num_frame_side ,
 name_save = "7.jpg" ,
 preds = self . preds_side
 )
     if 35 - 35: ooOOO . O0OO0OooooOo * i1i1i1111I * iI1iII1I1I1i - i1I1
   if not self . scorePoint8 and self . clean_desk_tools ( self . scorePoint1 , self . scorePoint2 ,
 self . scorePoint3 , self . scorePoint4 ,
 self . scorePoint5 , self . scorePoint6 ,
 self . scorePoint7 ) :
    if o0Oo0o000O0oO . shape [ 0 ] != 0 :
     self . flag8 = True
    if self . flag8 is True and OoO0OOo00oo0O . shape [ 0 ] != 0 :
     self . flag8 = False
     Ii111 = 0.1
     self . assignScore ( index = 8 ,
 img = self . frame_top ,
 object = self . objects_top ,
 conf = Ii111 ,
 time_frame = self . time_top ,
 num_frame = self . num_frame_top ,
 name_save = "8.jpg" ,
 preds = self . preds_top
 )
     if 47 - 47: IIiIIiIi11I1
     if 73 - 73: I1Ii1I1 + ooOOO
     if 99 - 99: O0OO0OooooOo
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
