import random
from . comm import *
from . comm . course_base import ConfigModel
import copy
if 82 - 82: Iii1i
class CHEM_evaporation_crystallization ( ConfigModel ) :
 if 12 - 12: i111IiI1Iii1I / OoOo
 def __init__ ( self ) :
  super ( CHEM_evaporation_crystallization , self ) . __init__ ( )
  if 12 - 12: OOo0O0oOo0O . ooo0oOoooOOO0 * Ii1I111 + i1iiIII111
  self . retort_stand_direction = False
  if 29 - 29: iI + o00Oo - OOoOoo000O00 * Oo0Oo - ii1I1iII1I1I . i1I1IiIIiIi1
  self . flag1 = False
  self . flag1_1 = False
  self . flag2 = False
  self . flag2_1 = False
  self . flag3 = False
  self . flag3_1 = False
  self . flag4 = False
  self . flag5 = False
  self . flag5_and_6 = False
  self . flag6 = False
  self . flag6_1 = False
  self . flag7 = False
  self . flag7_1 = False
  self . flag7_2 = False
  self . flag8 = False
  if 93 - 93: iI111iiIi11i % Oo % Ooo0o
  self . transfer_liquid_flag = False
  self . culture_dish_top_box = None
  self . corn_beaker_top_box = None
  if 11 - 11: i1I1 - O000o / O0OO0OooooOo * ii % i111IiI1Iii1I * iI
  self . diff_flag = False
  self . background = None
  self . bbox = [ ]
  self . retort_stand_bbox_collect = [ ]
  self . beaker_bbox_collect = [ ]
  self . flag_check_beaker_shape = False
  self . beaker_retort_stand_front_count = 0
  self . beaker_retort_stand_side_count = 0
  self . paper_funnel_count_front = 0
  self . paper_funnel_count_side = 0
  self . flame_out_secs = 0.
  self . flame_out_secs_pre = 0.
  self . stir_secs = 0.
  self . stir_secs_pre = 0.
  self . ignition_secs = 0.
  self . ignition_secs_pre = 0.
  if 9 - 9: Oo0Oo
  self . ignition_stir_secs = 0.
  self . ignition_stir_secs_pre = 0.
  if 10 - 10: o00Oo / Ooo0o * O000o / O0OO0OooooOo / O0OO0OooooOo
  self . flame_stop_secs = 0.
  self . flame_stop_secs_pre = 0.
  if 61 - 61: iI111iiIi11i - i1iiIII111
  self . cool_down_secs = 0.
  self . cool_down_secs_pre = 0.
  if 13 - 13: iI111iiIi11i
  self . clean_desk_secs = 0.
  self . clean_desk_secs_pre = 0.
  if 46 - 46: Oo - i111IiI1Iii1I * OOo0O0oOo0O * i111IiI1Iii1I
  if 52 - 52: OOo0O0oOo0O + i1iiIII111 / O000o / ooo0oOoooOOO0 - Ii1I111 - o00Oo
  # 自下向上搭建第一步，铁架台上只有酒精灯没有蒸发皿
 def state1_tools ( self , retort_stand_front , alcohol_lamp_front , evaporating_dish_front ) :
  if retort_stand_front . shape [ 0 ] != 0 and alcohol_lamp_front . shape [ 0 ] != 0 :
   if iou ( retort_stand_front [ 0 ] [ : 4 ] , alcohol_lamp_front [ 0 ] [ : 4 ] ) > 0.65 * box_area ( alcohol_lamp_front [ 0 ] [ : 4 ] ) :
    if evaporating_dish_front . shape [ 0 ] == 0 :
     return True
    else :
     oO0 = copy . deepcopy ( alcohol_lamp_front )
     oO0 [ 0 ] [ 1 ] = 0
     if iou ( oO0 [ 0 ] [ : 4 ] , evaporating_dish_front [ 0 ] [ : 4 ] ) == 0 :
      return True
  else :
   return False
   if 13 - 13: O000o
   if 2 - 2: iI
 def state2_tools ( self , retort_stand_front , alcohol_lamp_front , evaporating_dish_front ) :
  if retort_stand_front . shape [ 0 ] != 0 and alcohol_lamp_front . shape [ 0 ] != 0 and evaporating_dish_front . shape [ 0 ] != 0 :
   if iou ( retort_stand_front [ 0 ] [ : 4 ] , alcohol_lamp_front [ 0 ] [ : 4 ] ) > 0.65 * box_area ( alcohol_lamp_front [ 0 ] [ : 4 ] ) and iou ( retort_stand_front [ 0 ] [ : 4 ] , evaporating_dish_front [ 0 ] [ : 4 ] ) > 0.65 * box_area ( evaporating_dish_front [ 0 ] [ : 4 ] ) and self . sth_above_sth ( evaporating_dish_front , alcohol_lamp_front ) :
    if 22 - 22: Ooo0o - i1I1IiIIiIi1 / Ii1I111 . i1I1IiIIiIi1
    if 1 - 1: Oo + iI111iiIi11i + O000o * Ooo0o
    return True
  else :
   return False
   if 20 - 20: i1iiIII111 + i111IiI1Iii1I
 def hand_sth ( self , hands , sth ) :
  if hands . shape [ 0 ] != 0 and sth . shape [ 0 ] != 0 :
   for Iio0 in hands :
    i1i = Iio0 [ : 4 ]
    if iou ( i1i , sth [ 0 ] [ : 4 ] ) > 0 :
     return True
  return False
  if 87 - 87: OOo0O0oOo0O - O0OO0OooooOo
 def sth_above_sth ( self , sth1 , sth2 ) :
  if sth1 . shape [ 0 ] != 0 and sth2 . shape [ 0 ] != 0 :
   iiI1111IIi1 = copy . deepcopy ( sth2 )
   iiI1111IIi1 [ 0 ] [ 1 ] = 0
   if iou ( iiI1111IIi1 [ 0 ] [ : 4 ] , sth1 [ 0 ] [ : 4 ] ) > 0.20 * box_area ( sth1 [ 0 ] [ : 4 ] ) :
    return True
  else :
   return False
   if 92 - 92: o00Oo / ooo0oOoooOOO0 - OOoOoo000O00
 def faulty2_tools ( self , flame , retort_stand ) :
  if flame . shape [ 0 ] != 0 and retort_stand . shape [ 0 ] != 0 :
   if iou ( flame [ 0 ] [ : 4 ] , retort_stand [ 0 ] [ : 4 ] ) == 0 :
    return True
  else :
   return True
   if 59 - 59: Iii1i . ii - O0OO0OooooOo
   if 13 - 13: O000o
 def stir_check ( self , bbox , glass_column , beaker ) :
  if glass_column . shape [ 0 ] != 0 and beaker . shape [ 0 ] != 0 :
   IIii = glass_column [ 0 ] [ : 4 ]
   OO00 = beaker [ 0 ] [ : 4 ]
   if iou ( IIii , OO00 ) > 0 :
    o0O0ooOoo00o = min ( IIii [ 0 ] , OO00 [ 0 ] )
    Oo0Oo00O0OO = min ( IIii [ 1 ] , OO00 [ 1 ] )
    iIIiiIi1Ii1I = max ( IIii [ 2 ] , OO00 [ 2 ] )
    oo0 = max ( IIii [ 3 ] , OO00 [ 3 ] )
    i11iIii = [ o0O0ooOoo00o , Oo0Oo00O0OO , iIIiiIi1Ii1I , oo0 ]
    i11iIii = torch . Tensor ( i11iIii ) . cuda ( )
    for OO in bbox :
     if iou ( OO , i11iIii ) > 0 :
      return True
   return False
  return False
  if 27 - 27: OOo0O0oOo0O / O000o + ii - ooo0oOoooOOO0 * Ii1I111 / Ii1I111
 def hand_without_sth ( self , hands , sths ) :
  if hands . shape [ 0 ] == 0 :
   return True
  for o0OO in sths :
   if o0OO . shape [ 0 ] == 0 :
    continue
   for I1iI in o0OO :
    IiIII = I1iI [ : 4 ]
    for Iio0 in hands :
     i1i = Iio0 [ : 4 ]
     if iou ( i1i , IiIII ) > 0 :
      return False
  return True
  if 30 - 30: i1iiIII111 . i1I1IiIIiIi1
  if 43 - 43: o00Oo . i1I1 + i1I1IiIIiIi1
  if 87 - 87: Iii1i + o00Oo . O0OO0OooooOo / i111IiI1Iii1I + OOo0O0oOo0O
 def bottom_up_put_up_quipment ( self , retort_stand_front , alcohol_lamp_front , evaporating_dish_front ) :
  if self . state1_tools ( retort_stand_front , alcohol_lamp_front , evaporating_dish_front ) :
   self . flag1_1 = True
  if self . flag1_1 and self . state2_tools ( retort_stand_front , alcohol_lamp_front , evaporating_dish_front ) :
   return True
  return False
  if 77 - 77: Oo0Oo + ii - OOo0O0oOo0O % i1I1IiIIiIi1
  if 74 - 74: i111IiI1Iii1I + iI111iiIi11i
 def transfer_liquid_orderly ( self , retort_stand_front , alcohol_lamp_front , evaporating_dish_front ,
 hand_glass_rod_beaker_front ) :
  if self . state2_tools ( retort_stand_front , alcohol_lamp_front , evaporating_dish_front ) :
   if self . sth_above_sth ( hand_glass_rod_beaker_front , evaporating_dish_front ) :
    return True
  return False
  if 1 - 1: i1iiIII111 % iI111iiIi11i + Oo0Oo . Oo0Oo % OOo0O0oOo0O
  if 93 - 93: OOoOoo000O00 % iI111iiIi11i * Oo0Oo
 def alcohol_lamp_external_flame_heating ( self , retort_stand_front , alcohol_lamp_front , evaporating_dish_front ,
 flame_front ) :
  if self . state2_tools ( retort_stand_front , alcohol_lamp_front , evaporating_dish_front ) and flame_front . shape [ 0 ] != 0 :
   if 52 - 52: O000o + i1iiIII111 / i1I1IiIIiIi1 - Ii1I111 * O0OO0OooooOo % OOoOoo000O00
   if iou ( flame_front [ 0 ] [ : 4 ] , retort_stand_front [ 0 ] [ : 4 ] ) == box_area ( flame_front [ 0 ] [ : 4 ] ) and ( alcohol_lamp_front [ 0 ] [ 0 ] < flame_front [ 0 ] [ 0 ] < alcohol_lamp_front [ 0 ] [ 2 ] ) :
    if 52 - 52: OOoOoo000O00 . i1iiIII111 + O0OO0OooooOo - Oo0Oo % Oo
    self . ignition_secs , self . ignition_secs_pre , Oo0O0o0oO000 = self . duration ( self . ignition_secs , 8 ,
 self . ignition_secs_pre , 1 )
    if Oo0O0o0oO000 :
     self . ignition_secs = 0.
     self . ignition_secs_pre = 0.
     return True
  return False
  if 80 - 80: iI . OOoOoo000O00 * iI
  if 26 - 26: i111IiI1Iii1I . iI
  if 61 - 61: Oo . O0OO0OooooOo - i1I1IiIIiIi1 / i1I1IiIIiIi1 - iI
  if 19 - 19: Iii1i * iI111iiIi11i . Ii1I111 / i1I1 * i111IiI1Iii1I - O000o
 def glass_rod_stir ( self , retort_stand_front , alcohol_lamp_front , evaporating_dish_front , glass_rod_front , flame_front ) :
  if 32 - 32: Oo
  if self . state2_tools ( retort_stand_front , alcohol_lamp_front , evaporating_dish_front ) and flame_front . shape [ 0 ] != 0 :
   if 18 - 18: i1I1 * ii % Oo + ii
   if iou ( flame_front [ 0 ] [ : 4 ] , retort_stand_front [ 0 ] [ : 4 ] ) == box_area ( flame_front [ 0 ] [ : 4 ] ) and ( alcohol_lamp_front [ 0 ] [ 0 ] < flame_front [ 0 ] [ 0 ] < alcohol_lamp_front [ 0 ] [ 2 ] ) :
    if 93 - 93: O000o - Ii1I111 - Ooo0o * o00Oo - iI
    self . ignition_stir_secs , self . ignition_stir_secs_pre , Oo0O0o0oO000 = self . duration ( self . ignition_stir_secs , 3 ,
 self . ignition_stir_secs_pre , 1 )
    if Oo0O0o0oO000 :
     self . ignition_stir_secs = 0.
     self . ignition_stir_secs_pre = 0.
     self . flag3_1 = True
     self . diff_flag = True
     if 82 - 82: Ooo0o % iI * o00Oo
  if self . flag3_1 and self . stir_check ( self . bbox , glass_rod_front , evaporating_dish_front ) :
   self . stir_secs , self . stir_secs_pre , Oo0O0o0oO000 = self . duration ( self . stir_secs , 5 ,
 self . stir_secs_pre , 1 )
   if Oo0O0o0oO000 :
    self . stir_secs = 0.
    self . stir_secs_pre = 0.
    return True
  return False
  if 57 - 57: OOoOoo000O00
  if 31 - 31: Oo0Oo + OoOo % ooo0oOoooOOO0
 def waste_heat_evaporated_dryness ( self , retort_stand_front , alcohol_lamp_front , evaporating_dish_front , flame_front , siderosphere_front ) :
  if self . state2_tools ( retort_stand_front , alcohol_lamp_front , evaporating_dish_front ) and flame_front . shape [ 0 ] != 0 :
   if 20 - 20: ooo0oOoooOOO0 - i1iiIII111
   if iou ( flame_front [ 0 ] [ : 4 ] , retort_stand_front [ 0 ] [ : 4 ] ) == box_area ( flame_front [ 0 ] [ : 4 ] ) and ( alcohol_lamp_front [ 0 ] [ 0 ] < flame_front [ 0 ] [ 0 ] < alcohol_lamp_front [ 0 ] [ 2 ] ) :
    if 9 - 9: Oo0Oo - Oo % i111IiI1Iii1I - i1iiIII111
    self . flame_stop_secs , self . flame_stop_secs_pre , Oo0O0o0oO000 = self . duration ( self . flame_stop_secs , 3 ,
 self . flame_stop_secs_pre , 1 )
    if Oo0O0o0oO000 :
     self . flame_stop_secs = 0.
     self . flame_stop_secs_pre = 0.
     self . flag5 = True
     if 54 - 54: Iii1i % i1I1IiIIiIi1 % Iii1i - ii1I1iII1I1I
  if self . flag5 :
   if evaporating_dish_front . shape [ 0 ] != 0 and siderosphere_front . shape [ 0 ] != 0 and retort_stand_front . shape [ 0 ] != 0 :
    if iou ( evaporating_dish_front [ 0 ] [ : 4 ] , siderosphere_front [ 0 ] [ : 4 ] ) > 0 :
     if flame_front . shape [ 0 ] == 0 :
      self . flame_out_secs , self . flame_out_secs_pre , Oo0O0o0oO000 = self . duration ( self . flame_out_secs , 0.5 ,
 self . flame_out_secs_pre , 0.5 )
      if Oo0O0o0oO000 :
       self . flame_out_secs = 0.
       self . flame_out_secs_pre = 0.
       return True
       if 39 - 39: O000o - O000o * iI % Ooo0o
  return False
  if 29 - 29: Ooo0o - i1I1IiIIiIi1 . Oo0Oo
  if 86 - 86: Ii1I111 - ooo0oOoooOOO0 - O000o % i1I1IiIIiIi1 . O0OO0OooooOo % Iii1i
 def evaporating_to_asbestos_net ( self , asbestos_network_front , evaporating_dish_front , asbestos_network_top ,
 evaporating_dish_top , retort_stand_front , alcohol_lamp_front , flame_front ) :
  if self . state2_tools ( retort_stand_front , alcohol_lamp_front , evaporating_dish_front ) and flame_front . shape [ 0 ] != 0 :
   if 11 - 11: ooo0oOoooOOO0 - Ii1I111 - o00Oo . Oo0Oo - Oo / Oo0Oo
   if iou ( flame_front [ 0 ] [ : 4 ] , retort_stand_front [ 0 ] [ : 4 ] ) == box_area ( flame_front [ 0 ] [ : 4 ] ) and ( alcohol_lamp_front [ 0 ] [ 0 ] < flame_front [ 0 ] [ 0 ] < alcohol_lamp_front [ 0 ] [ 2 ] ) :
    if 44 - 44: iI111iiIi11i + OoOo + Iii1i - O000o
    self . flag6 = True
    if 7 - 7: OoOo / i111IiI1Iii1I * Iii1i
  if self . flag6 and asbestos_network_front . shape [ 0 ] != 0 and evaporating_dish_front . shape [ 0 ] != 0 :
   if iou ( asbestos_network_front [ 0 ] [ : 4 ] , evaporating_dish_front [ 0 ] [ : 4 ] ) > 0.35 * box_area (
 evaporating_dish_front [ 0 ] [ : 4 ] ) and self . sth_above_sth ( evaporating_dish_front ,
 asbestos_network_front ) :
    return True
  if self . flag6 and asbestos_network_top . shape [ 0 ] != 0 and evaporating_dish_top . shape [ 0 ] != 0 :
   if iou ( asbestos_network_top [ 0 ] [ : 4 ] , evaporating_dish_top [ 0 ] [ : 4 ] ) > 0.35 * box_area ( evaporating_dish_top [ 0 ] [ : 4 ] ) :
    self . cool_down_secs , self . cool_down_secs_pre , Oo0O0o0oO000 = self . duration ( self . cool_down_secs , 1 ,
 self . cool_down_secs_pre , 0.5 )
    if Oo0O0o0oO000 :
     self . cool_down_secs = 0.
     self . cool_down_secs_pre = 0.
     return True
  return False
  if 32 - 32: ii . ooo0oOoooOOO0
 def score_process ( self , top_true , front_true , side_true ) :
  if 31 - 31: OOo0O0oOo0O - O0OO0OooooOo
  if top_true or front_true or side_true :
   if top_true :
    IIIi1111iiIi1 , I1II1ii111i , I1i1iI1I1Ii1 , oOoOO0O0 , I111 , OO00OOooO , o000OOoOO , IIIII , oooo0OO0o0 , OooOoO0oO , O0OO00OO0O , Ooo0oO , ii1II , oOoOo = self . preds_top
    if 39 - 39: O000o
    if 17 - 17: i111IiI1Iii1I . OOoOoo000O00 % ooo0oOoooOOO0
    if 82 - 82: Iii1i . OOoOoo000O00 % Ooo0o - Oo
    oO = [ I1II1ii111i , I1i1iI1I1Ii1 , oOoOO0O0 , I111 , OO00OOooO ,
 o000OOoOO , IIIII , Ooo0oO ]
    if 62 - 62: OoOo
   if side_true :
    O00 , i1Ii , iI111i1III , O00o00 , iiI1iiii1iii , O0OOooO0O0Oo0 , I11iIi1i1iIi , iI11 , OO0 , O00OOo , II1Iiii111i1I , i11IIi1I1 , oOOOO0ooO , O0O0oO = self . preds_side
    if 12 - 12: Oo0Oo + i1I1IiIIiIi1 . i1I1
    if 1 - 1: Oo % i111IiI1Iii1I - i1I1 / ii + Oo - i111IiI1Iii1I
   if front_true :
    IiII1Iii11 , i1i1Ii , ii1iI1I11 , OOoO0oOo0 , iII1Ii , O00OoO0OOO0 , Oo0o0Oo , o0O0OO0 , Iioo0Oo0oO0 , iII11I1iI , O0O0o0oo00Oo , I11 , I1Ii , II = self . preds_front
    if 46 - 46: ooo0oOoooOOO0 - i1I1 / iI111iiIi11i
    if 73 - 73: Ii1I111 / OoOo / i1I1IiIIiIi1 % iI % O0OO0OooooOo - ooo0oOoooOOO0
    if 30 - 30: o00Oo * o00Oo - Iii1i * Oo
    oOO = [ i1i1Ii , ii1iI1I11 , OOoO0oOo0 , iII1Ii ,
 O00OoO0OOO0 , Oo0o0Oo , o0O0OO0 , I11 ]
    if 76 - 76: iI111iiIi11i * o00Oo * Oo
   if self . diff_flag :
    oOooO0O0 = copy . deepcopy ( self . frame_front )
    O0 , O0Ii1Ii1 , I111i1i11iII = oOooO0O0 . shape
    if 5 - 5: ooo0oOoooOOO0 + OOoOoo000O00 . iI111iiIi11i + i1iiIII111 / ooo0oOoooOOO0
    oOooO0O0 = cv2 . resize ( oOooO0O0 , ( 640 , 360 ) )
    self . bbox = [ ]
    OOOO = cv2 . getStructuringElement ( cv2 . MORPH_ELLIPSE , ( 9 , 4 ) )
    oooo000O0 = cv2 . cvtColor ( oOooO0O0 , cv2 . COLOR_BGR2GRAY )
    oooo000O0 = cv2 . GaussianBlur ( oooo000O0 , ( 9 , 9 ) , 0 )
    if 47 - 47: i1I1IiIIiIi1
    if self . background is None :
     self . background = oooo000O0
    IiII111I1I = cv2 . absdiff ( self . background , oooo000O0 )
    IiII111I1I = cv2 . threshold ( IiII111I1I , 25 , 255 , cv2 . THRESH_BINARY ) [ 1 ]
    IiII111I1I = cv2 . dilate ( IiII111I1I , OOOO , iterations = 2 )
    if 82 - 82: iI . Iii1i - ii
    oo0O0O0Ooooo , Ooo = cv2 . findContours ( IiII111I1I . copy ( ) , cv2 . RETR_EXTERNAL , cv2 . CHAIN_APPROX_SIMPLE )
    for II1111I11 in oo0O0O0Ooooo :
     if cv2 . contourArea ( II1111I11 ) < 160 :
      continue
     [ IiI1IIi1IiII , I1I , oOooOo0o , iii1ii1 ] = cv2 . boundingRect ( II1111I11 )
     [ iIi1i , o0Oo , iiIi , oOoo ] = [ ( IiI1IIi1IiII / 640 ) * O0Ii1Ii1 , ( I1I / 360 ) * O0 , oOooOo0o * ( float ( O0Ii1Ii1 / 640 ) ) ,
 iii1ii1 * ( float ( O0 / 360 ) ) ]
     [ o0O0ooOoo00o , Oo0Oo00O0OO , iIIiiIi1Ii1I , oo0 ] = [ iIi1i , o0Oo , iIi1i + iiIi , o0Oo + oOoo ]
     ooOOO00oO0o0o = torch . Tensor ( [ o0O0ooOoo00o , Oo0Oo00O0OO , iIIiiIi1Ii1I , oo0 ] ) . cuda ( )
     self . bbox . append ( ooOOO00oO0o0o )
     if 94 - 94: OOoOoo000O00 % Iii1i - Ooo0o . iI111iiIi11i - OOo0O0oOo0O * Ooo0o
     if 92 - 92: OoOo . ii + OoOo / ooo0oOoooOOO0
   if not self . scorePoint1 :
    if self . bottom_up_put_up_quipment ( i1i1Ii , iII1Ii , OOoO0oOo0 ) :
     O00OO00O = 0.1
     self . assignScore ( index = 1 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = O00OO00O ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "1.jpg" ,
 preds = self . preds_front
 )
     if 13 - 13: O000o . i1iiIII111 * Oo - iI111iiIi11i / Oo + i1I1IiIIiIi1
     if 54 - 54: Oo0Oo . Oo0Oo - o00Oo * ooo0oOoooOOO0 + Ooo0o * OoOo
   if not self . scorePoint2 :
    if self . transfer_liquid_orderly ( i1i1Ii , iII1Ii , OOoO0oOo0 ,
 I1Ii ) :
     O00OO00O = 0.1
     self . assignScore ( index = 2 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = O00OO00O ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "2.jpg" ,
 preds = self . preds_front
 )
     if 12 - 12: OoOo
     if 56 - 56: ii1I1iII1I1I
   if not self . scorePoint3 :
    if self . alcohol_lamp_external_flame_heating ( i1i1Ii , iII1Ii , OOoO0oOo0 ,
 Iioo0Oo0oO0 ) :
     O00OO00O = 0.1
     self . assignScore ( index = 3 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = O00OO00O ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "3.jpg" ,
 preds = self . preds_front
 )
     if 17 - 17: O0OO0OooooOo . O000o % OOo0O0oOo0O + ii1I1iII1I1I - iI111iiIi11i
     if 93 - 93: OOoOoo000O00
   if not self . scorePoint4 :
    if self . glass_rod_stir ( i1i1Ii , iII1Ii , OOoO0oOo0 , O00OoO0OOO0 ,
 Iioo0Oo0oO0 ) :
     self . diff_flag = False
     O00OO00O = 0.1
     self . assignScore ( index = 4 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = O00OO00O ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "4.jpg" ,
 preds = self . preds_front
 )
     if 77 - 77: OOo0O0oOo0O + i1I1 % i1iiIII111
     if 20 - 20: iI - ii1I1iII1I1I . ii1I1iII1I1I % o00Oo . iI % iI111iiIi11i
   if not self . scorePoint5 :
    if self . waste_heat_evaporated_dryness ( i1i1Ii , iII1Ii , OOoO0oOo0 ,
 Iioo0Oo0oO0 , ii1iI1I11 ) :
     O00OO00O = 0.1
     self . assignScore ( index = 5 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = O00OO00O ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "5.jpg" ,
 preds = self . preds_front
 )
     if 72 - 72: O000o % ii . o00Oo * Ii1I111 . o00Oo
   if not self . scorePoint6 :
    if self . evaporating_to_asbestos_net ( Oo0o0Oo , OOoO0oOo0 , o000OOoOO ,
 oOoOO0O0 , i1i1Ii , iII1Ii , Iioo0Oo0oO0 ) :
     O00OO00O = 0.1
     self . assignScore ( index = 6 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = O00OO00O ,
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
     if iII11I1iI . shape [ 0 ] != 0 or O00OOo . shape [ 0 ] != 0 or OooOoO0oO . shape [ 0 ] != 0 :
      self . clean_desk_secs , self . clean_desk_secs_pre , Oo0O0o0oO000 = self . duration ( self . clean_desk_secs , 0.5 ,
 self . clean_desk_secs_pre , 0.3 )
      if Oo0O0o0oO000 :
       self . flag6_1 = True
       self . clean_desk_secs = 0.
       self . clean_desk_secs_pre = 0.
    if self . flag6_1 :
     if O0O0o0oo00Oo . shape [ 0 ] != 0 or II1Iiii111i1I . shape [ 0 ] != 0 or O0OO00OO0O . shape [ 0 ] != 0 :
      O00OO00O = 0.1
      self . assignScore ( index = 7 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = O00OO00O ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "7.jpg" ,
 preds = self . preds_front
 )
     if self . hand_without_sth ( IIIi1111iiIi1 , oO ) and self . hand_without_sth ( IiII1Iii11 , oOO ) and not self . state2_tools ( i1i1Ii , iII1Ii , OOoO0oOo0 ) :
      if 11 - 11: iI111iiIi11i - ii - Oo
      O00OO00O = 0.1
      self . assignScore ( index = 7 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = O00OO00O ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "7.jpg" ,
 preds = self . preds_front
 )
      if 54 - 54: i1I1 / ii1I1iII1I1I . iI111iiIi11i
      if 15 - 15: O0OO0OooooOo * i1I1 - OOoOoo000O00
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
