from . comm import *
import numpy as np
import platform
from ctypes import *
import cv2
import ctypes
from . comm . course_base import ConfigModel
from logger import logger
from configg . global_config import GLOBAL_all_model_type_name , experimental_site_top as est
from configg . global_config import experimental_site_front as esf
import copy
import ctypes
iIiii1i111i1I = platform . platform ( )
if 5 - 5: i11i1
if 26 - 26: o0Ooo0OOO * IiI / OOo0O0oOo0O . ooo0oOoooOOO0 * Ii1I111 + i1iiIII111
if 29 - 29: iI + o00Oo - OOoOoo000O00 * Oo0Oo - ii1I1iII1I1I . i1I1IiIIiIi1
if 93 - 93: iI111iiIi11i % Oo % Ooo0o
class CHEM_acid_base_neutralization_reaction ( ConfigModel ) :
 def __init__ ( self ) :
  super ( CHEM_acid_base_neutralization_reaction , self ) . __init__ ( )
  if 17 - 17: I1Ii111i1I - OOooooOo00 - i11 / iIi1Ii1i . i11 * i11
  # 辅助库初始化 todo
  if 61 - 61: iI111iiIi11i - i1iiIII111
  if 'Linux' in iIiii1i111i1I :
   self . alg_handle_class = CDLL ( "./aideModel/openvino_inference_sdk/openvino_inference.so" )
   iIIIII1i111i = bytes ( "./aideModel/classModel/acid_base_neutralization_reaction/LFNC_Net.onnx" , "gbk" )
  elif "Windows" in iIiii1i111i1I :
   self . alg_handle_class = CDLL ( "./aideModel/openvino_inference_sdk/openvino_inference.dll" )
   iIIIII1i111i = bytes ( "./aideModel/classModel/acid_base_neutralization_reaction/LFNC_Net.onnx" , "gbk" )
  else :
   assert print ( 'error: unsupport os name->' , iIiii1i111i1I )
   if 8 - 8: Oo0Oo * iI . i1iiIII111 / OOooooOo00
  self . alg_handle_class . alg_init ( iIIIII1i111i , 224 , 224 , 2 , 0 )
  if 58 - 58: Ii1I111 - o00Oo
  if 60 - 60: Oo . OOooooOo00
  if 13 - 13: OOooooOo00
  if 2 - 2: iI
  if 22 - 22: Ooo0o - i1I1IiIIiIi1 / Ii1I111 . i1I1IiIIiIi1
  if 1 - 1: Oo + iI111iiIi11i + OOooooOo00 * Ooo0o
  if 20 - 20: i1iiIII111 + o0Ooo0OOO
  if 75 - 75: o0Ooo0OOO % Oo0Oo * o0Ooo0OOO . Ooo0o % I1Ii111i1I % Ii1I111
  if 8 - 8: Ii1I111 . iIi1Ii1i . iI . OOo0O0oOo0O - i11
  if 32 - 32: o0Ooo0OOO % IiI % i11 - I1Ii111i1I % Oo0Oo
  if 34 - 34: Oo0Oo * iI
  self . d_time = 0.
  self . flg1_1 = False
  self . flg1_2 = False
  self . flg1_3 = False
  self . flg2_1 = False
  self . flg2_2 = False
  self . flg2_3 = False
  self . flg2_4 = False
  self . flg2_5 = False
  if 34 - 34: OOoOoo000O00 / Oo0Oo - i11i1 . Oo
  self . flg3_1 = False
  self . flg3_2 = False
  self . flg3_3 = False
  self . flg4_1 = False
  self . flg4_2 = False
  self . flg4_3 = False
  self . flg4_4 = False
  self . flg4_5 = False
  self . flg5_1 = False
  self . flg5_2 = False
  self . flg6_1 = False
  self . flg8_1 = False
  self . flg9_1 = False
  self . flg9_2 = False
  if 80 - 80: IiI . i1iiIII111 % o00Oo % ii1I1iII1I1I / IiI
  self . diff_flag = False
  self . background = None
  self . observe_secs = 0.
  self . observe_secs_pre = 0.
  self . thermometer_secs = 0.
  self . thermometer_secs_pre = 0.
  self . bbox = [ ]
  if 32 - 32: Ii1I111 + OOooooOo00 - OOoOoo000O00
 def hand_sth ( self , hands , sth ) :
  if hands . shape [ 0 ] != 0 and sth . shape [ 0 ] != 0 :
   for IiiIii11iII1 in hands :
    I11I1 = IiiIii11iII1 [ : 4 ]
    if iou ( I11I1 , sth [ 0 ] [ : 4 ] ) > 0 :
     return True
  return False
  if 63 - 63: IiI . iI111iiIi11i * o00Oo
 def container_red_liquid ( self , beaker , red_liquid ) :
  if red_liquid . shape [ 0 ] == 0 or beaker . shape [ 0 ] == 0 :
   return False
  else :
   if iou ( beaker [ 0 ] [ : 4 ] , red_liquid [ 0 ] [ : 4 ] ) > 0.75 * box_area ( red_liquid [ 0 ] [ : 4 ] ) :
    return True
    if 6 - 6: Oo0Oo
 def glass_column_beaker ( self , hands , glass_columns , beakers ) :
  I1I1 = False
  if hands . shape [ 0 ] != 0 and beakers . shape [ 0 ] != 0 and glass_columns . shape [ 0 ] != 0 :
   for IiiIii11iII1 in hands :
    I11I1 = IiiIii11iII1 [ : 4 ]
    for oo0 in glass_columns :
     i11iIii = oo0 [ : 4 ]
     if iou ( i11iIii , I11I1 ) > 0 :
      OO = I11I1
      iiI1I11iiiiI = i11iIii
      if 2 * ( iiI1I11iiiiI [ 2 ] - iiI1I11iiiiI [ 0 ] ) < ( iiI1I11iiiiI [ 3 ] - iiI1I11iiiiI [ 1 ] ) :
       I1I1 = True
   if I1I1 :
    for iII11iIi1iIiI in beakers :
     iIIiii1iI = iII11iIi1iIiI [ : 4 ]
     if 43 - 43: o00Oo . I1Ii111i1I + i1I1IiIIiIi1
     if 87 - 87: i11i1 + o00Oo . i11 / o0Ooo0OOO + OOo0O0oOo0O
     if iou ( iIIiii1iI , iiI1I11iiiiI ) > 0.1 * box_area ( iiI1I11iiiiI ) :
      I1I1 = False
      return [ True , iiI1I11iiiiI ]
   else :
    return [ False , None ]
  else :
   return [ False , None ]
  return [ False , None ]
  if 77 - 77: Oo0Oo + iIi1Ii1i - OOo0O0oOo0O % i1I1IiIIiIi1
  if 74 - 74: o0Ooo0OOO + iI111iiIi11i
 def dropper_above_sth ( self , dropper , beaker ) :
  iIi1I1I = copy . deepcopy ( beaker )
  if dropper . shape [ 0 ] != 0 and iIi1I1I . shape [ 0 ] != 0 :
   iIi1I1I [ 0 ] [ 1 ] = 0
   if 85 - 85: OOoOoo000O00
   if iou ( iIi1I1I [ 0 ] [ : 4 ] , dropper [ 0 ] [ : 4 ] ) > 0 :
    return True
  else :
   return False
   if 65 - 65: iI111iiIi11i * i1I1IiIIiIi1 + OOoOoo000O00
 def stir_check ( self , bbox , glass_column , beaker ) :
  if glass_column . shape [ 0 ] != 0 and beaker . shape [ 0 ] != 0 :
   i11iIii = glass_column [ 0 ] [ : 4 ]
   iIIiii1iI = beaker [ 0 ] [ : 4 ]
   if iou ( i11iIii , iIIiii1iI ) > 0 :
    i1I11i11 = min ( i11iIii [ 0 ] , iIIiii1iI [ 0 ] )
    OoOOoO000O = min ( i11iIii [ 1 ] , iIIiii1iI [ 1 ] )
    O0o0O0o0o = max ( i11iIii [ 2 ] , iIIiii1iI [ 2 ] )
    Oo0 = max ( i11iIii [ 3 ] , iIIiii1iI [ 3 ] )
    ooooo = [ i1I11i11 , OoOOoO000O , O0o0O0o0o , Oo0 ]
    if torch . cuda . is_available ( ) :
     ooooo = torch . Tensor ( ooooo ) . cuda ( )
    else :
     ooooo = torch . Tensor ( ooooo )
    for oO00o00OO in bbox :
     if iou ( oO00o00OO , ooooo ) > 0 :
      return True
   return False
  return False
  if 52 - 52: i11i1 / OOo0O0oOo0O
 def hand_without_sth ( self , hands , sths ) :
  if hands . shape [ 0 ] == 0 :
   return True
  for o00O in sths :
   if o00O . shape [ 0 ] == 0 :
    continue
   for iIi in o00O :
    O000O0Oo0 = iIi [ : 4 ]
    for IiiIii11iII1 in hands :
     I11I1 = IiiIii11iII1 [ : 4 ]
     if iou ( I11I1 , O000O0Oo0 ) > 0 :
      return False
  return True
  if 61 - 61: iI + o00Oo * Ooo0o % iI
  if 36 - 36: OOoOoo000O00 . o00Oo / Oo0Oo + OOooooOo00
  if 11 - 11: iI / i1I1IiIIiIi1
 def pour_NaOH_into_beaker_teach ( self , hand , beaker , reagent_bottle , dropper ) :
  if hand . shape [ 0 ] != 0 and beaker . shape [ 0 ] != 0 and reagent_bottle . shape [ 0 ] != 0 :
   if 89 - 89: i1iiIII111 * IiI
   self . flg1_1 = True
  if self . flg1_1 and hand . shape [ 0 ] != 0 and dropper . shape [ 0 ] != 0 and beaker . shape [
 0 ] != 0 :
   if self . hand_sth ( hand , dropper ) and adjoin ( beaker [ 0 ] [ : 4 ] , dropper [ 0 ] [ : 4 ] ) :
    self . flg1_1 = False
    return True
  return False
  if 54 - 54: OOooooOo00 + iI111iiIi11i - i1iiIII111 . iI111iiIi11i
  if 50 - 50: i11i1 * i1I1IiIIiIi1 % i11i1 - OOoOoo000O00 + i1I1IiIIiIi1
 def pour_Phenolphthalein_into_NaOH_teach ( self , hand , beaker , reagent_bottle , dropper , red_liquid_column ) :
  if hand . shape [ 0 ] != 0 and beaker . shape [ 0 ] != 0 and reagent_bottle . shape [ 0 ] != 0 :
   if 54 - 54: OOooooOo00 * iI % iI - iI111iiIi11i + Ooo0o
   self . flg2_1 = True
  if self . flg2_1 and hand . shape [ 0 ] != 0 and dropper . shape [ 0 ] != 0 and beaker . shape [
 0 ] != 0 :
   if 4 - 4: i1I1IiIIiIi1 + Ii1I111 * ooo0oOoooOOO0 - iIi1Ii1i
   if self . container_red_liquid ( beaker , red_liquid_column ) :
    self . flg2_1 = False
    return True
  return False
  if 69 - 69: i1I1IiIIiIi1
  if 76 - 76: i11i1 * iI111iiIi11i . Oo / o0Ooo0OOO / o00Oo
 def temperature_measurement_teach ( self , hand , glass_column , thermometer_vacuole , beaker , red_liquid_column ) :
  if 49 - 49: Oo / Oo0Oo + i1I1IiIIiIi1
  if hand . shape [ 0 ] != 0 and glass_column . shape [ 0 ] != 0 and thermometer_vacuole . shape [ 0 ] != 0 and beaker . shape [ 0 ] != 0 :
   if 36 - 36: IiI + i11i1 - OOooooOo00 * o0Ooo0OOO
   if 45 - 45: IiI * o0Ooo0OOO
   if 97 - 97: iI
   if 26 - 26: iIi1Ii1i
   if 20 - 20: Ooo0o / OOo0O0oOo0O
   if 73 - 73: o00Oo - ii1I1iII1I1I
   if 22 - 22: OOo0O0oOo0O % OOoOoo000O00 / i11 . OOoOoo000O00 . i11
   if 87 - 87: i1iiIII111 - i11 . iI * OOo0O0oOo0O
   if 90 - 90: iIi1Ii1i * i11 . o0Ooo0OOO
   if 45 - 45: ii1I1iII1I1I - I1Ii111i1I . Oo0Oo * iI111iiIi11i . Ooo0o
   if 14 - 14: Oo + ooo0oOoooOOO0 * Ii1I111 - I1Ii111i1I
   if 84 - 84: OOooooOo00 % Oo - iI111iiIi11i
   if 94 - 94: Oo0Oo + IiI / Oo + Oo / i11
   if 79 - 79: Oo0Oo - Ooo0o . Ii1I111 + i1iiIII111 - o00Oo + Oo0Oo
   if 36 - 36: o00Oo * i11i1 % i1iiIII111 % iI . iI111iiIi11i
   if 63 - 63: Ooo0o / Ooo0o * i11i1 - OOoOoo000O00 . iI
   for o00OO0 in beaker :
    iIIiii1iI = o00OO0 [ : 4 ]
    if iou ( thermometer_vacuole [ 0 ] [ : 4 ] , iIIiii1iI ) == 0 :
     self . flg3_1 = True
     self . thermometer_secs_pre = self . secs
     if 68 - 68: OOooooOo00 - ii1I1iII1I1I + Oo
  if self . flg3_1 :
   if self . glass_column_beaker ( hand , glass_column , beaker ) [ 0 ] :
    self . thermometer_secs = self . secs
    if ( self . thermometer_secs - self . thermometer_secs_pre ) > 10 :
     return False
    self . observe_secs , self . observe_secs_pre , Ooo0oO = self . duration ( self . observe_secs , 1 ,
 self . observe_secs_pre , 1 )
    if Ooo0oO and self . container_red_liquid ( beaker , red_liquid_column ) :
     if 16 - 16: Ii1I111 % i1iiIII111 / Ooo0o * i11 + iIi1Ii1i % OOoOoo000O00
     if 13 - 13: iI + ii1I1iII1I1I
     if 23 - 23: OOooooOo00 . o00Oo / o0Ooo0OOO
     if 7 - 7: ooo0oOoooOOO0 + Ooo0o * i11i1 . OOoOoo000O00 % Ooo0o
     if 62 - 62: Ii1I111 + o00Oo . OOo0O0oOo0O - IiI
     if 52 - 52: i11 . o0Ooo0OOO * ooo0oOoooOOO0 / i11
     if 39 - 39: iI
     if 16 - 16: iIi1Ii1i - iIi1Ii1i % I1Ii111i1I / Oo - Oo
     if 39 - 39: OOoOoo000O00 - iIi1Ii1i % iIi1Ii1i . OOo0O0oOo0O * i1iiIII111
     if 81 - 81: IiI + Ii1I111
     self . flg3_1 = False
     self . observe_secs = 0.
     self . observe_secs_pre = 0.
     return True
  return False
  if 31 - 31: IiI % Ii1I111
  if 1 - 1: iIi1Ii1i - OOoOoo000O00 - iI . OOoOoo000O00
 def temperature_measurement_class ( self , hand , glass_column , beaker , red_liquid_column , dropper ) :
  if hand . shape [ 0 ] != 0 and glass_column . shape [ 0 ] != 0 and beaker . shape [ 0 ] != 0 :
   if self . glass_column_beaker ( hand , glass_column , beaker ) [ 0 ] :
    ooooo = self . glass_column_beaker ( hand , glass_column , beaker ) [ 1 ]
    ooooo = ooooo . data . cpu ( ) . numpy ( )
    if 91 - 91: Oo * iI . o00Oo
    I1iIiii = self . frame_front [ int ( ooooo [ 1 ] ) : int ( ooooo [ 3 ] ) ,
 int ( ooooo [ 0 ] ) : int ( ooooo [ 2 ] ) ]
    if 40 - 40: i11 * Oo + Oo . OOoOoo000O00 * i1I1IiIIiIi1
    I1iIiii = cv2 . resize ( I1iIiii , ( 224 , 224 ) )
    if 35 - 35: Ooo0o % IiI - o0Ooo0OOO % Oo0Oo - iIi1Ii1i
    oo0IiiI11IIi1I , oOOOO0ooO , O0O0oO = I1iIiii . shape
    IIiI1i = O0O0oO * oOOOO0ooO
    OoOOooO0oOO0Oo = I1iIiii . ctypes . data_as ( ctypes . c_char_p )
    if 4 - 4: iI % Ii1I111 * OOooooOo00 + OOooooOo00 . IiI - iI
    I1iO0OOOOoO0o = time . time ( )
    self . alg_handle_class . alg_run . restype = ctypes . POINTER ( ctypes . c_float )
    o00ooOOO0Oo = self . alg_handle_class . alg_run ( OoOOooO0oOO0Oo )
    if 37 - 37: i11 + Ooo0o % Oo / Ooo0o % Oo0Oo + OOooooOo00
    Oo0o0Oo = time . time ( )
    if 100 - 100: Oo0Oo . Ooo0o * i1I1IiIIiIi1 * i1I1IiIIiIi1
    if int ( o00ooOOO0Oo [ 1 ] ) == 1 :
     if 85 - 85: Ooo0o / ooo0oOoooOOO0 . i11 % OOo0O0oOo0O + OOo0O0oOo0O - I1Ii111i1I
     self . observe_secs , self . observe_secs_pre , Ooo0oO = self . duration ( self . observe_secs , 0.5 ,
 self . observe_secs_pre , 0.5 )
     if Ooo0oO and self . container_red_liquid ( beaker , red_liquid_column ) and not self . dropper_above_sth ( dropper , beaker ) :
      if 59 - 59: ooo0oOoooOOO0
      if 53 - 53: IiI / o00Oo - iIi1Ii1i + i1I1IiIIiIi1 * IiI * Oo0Oo
      if 87 - 87: Oo0Oo - Ooo0o * o0Ooo0OOO % IiI % iI
      self . observe_secs = 0.
      self . observe_secs_pre = 0.
      return True
  return False
  if 81 - 81: iI + IiI * OOo0O0oOo0O - OOo0O0oOo0O * Ii1I111 - OOoOoo000O00
  if 4 - 4: Oo0Oo
 def temperature_measurement_teach_after ( self , hand , glass_column , thermometer_vacuole , beaker , red_liquid_column ) :
  if 8 - 8: ii1I1iII1I1I + ooo0oOoooOOO0 - iI
  if hand . shape [ 0 ] != 0 and glass_column . shape [ 0 ] != 0 and thermometer_vacuole . shape [ 0 ] != 0 and beaker . shape [ 0 ] != 0 and red_liquid_column . shape [ 0 ] == 0 :
   if 68 - 68: Ii1I111 % Ii1I111 / iIi1Ii1i . i1I1IiIIiIi1
   for o00OO0 in beaker :
    iIIiii1iI = o00OO0 [ : 4 ]
    if iou ( thermometer_vacuole [ 0 ] [ : 4 ] , iIIiii1iI ) == box_area ( thermometer_vacuole [ 0 ] [ : 4 ] ) :
     self . flg3_2 = True
  if self . flg3_2 :
   if beaker . shape [ 0 ] != 0 and thermometer_vacuole . shape [ 0 ] != 0 :
    for o00OO0 in beaker :
     iIIiii1iI = o00OO0 [ : 4 ]
     if iou ( thermometer_vacuole [ 0 ] [ : 4 ] , iIIiii1iI ) == box_area ( thermometer_vacuole [ 0 ] [ : 4 ] ) :
      self . flg3_3 = True
   if self . glass_column_beaker ( hand , glass_column , beaker ) [ 0 ] or self . flg3_3 :
    self . observe_secs , self . observe_secs_pre , Ooo0oO = self . duration ( self . observe_secs , 1 ,
 self . observe_secs_pre , 1 )
    if Ooo0oO :
     self . observe_secs = 0.
     self . observe_secs_pre = 0.
     self . flg3_2 = False
     self . flg3_3 = False
     return True
  return False
  if 80 - 80: Ooo0o / ooo0oOoooOOO0 % Oo / o00Oo * o00Oo - i11i1
  if 60 - 60: OOooooOo00 * IiI / Oo
 def dropper_hcl_to_beaker ( self , hand , beaker , reagent_bottle , dropper , red_liquid_column , glass_column ,
 thermometer_vacuole ) :
  if hand . shape [ 0 ] != 0 and beaker . shape [ 0 ] != 0 and reagent_bottle . shape [ 0 ] != 0 :
   if self . hand_sth ( hand , reagent_bottle ) :
    self . flg4_1 = True
  if self . flg4_1 and hand . shape [ 0 ] != 0 and dropper . shape [ 0 ] != 0 and beaker . shape [
 0 ] != 0 :
   if self . hand_sth ( hand , dropper ) and adjoin ( beaker [ 0 ] [ : 4 ] , dropper [ 0 ] [ : 4 ] ) :
    if self . container_red_liquid ( beaker , red_liquid_column ) :
     self . flg4_2 = True
  if self . flg4_2 and hand . shape [ 0 ] != 0 and glass_column . shape [ 0 ] != 0 and thermometer_vacuole . shape [ 0 ] != 0 :
   if 45 - 45: iI111iiIi11i + o00Oo * OOoOoo000O00 - i1I1IiIIiIi1 / Ooo0o
   self . flg4_3 = True
   if 14 - 14: i11 - ii1I1iII1I1I
  if self . flg4_3 and self . hand_sth ( hand , dropper ) and self . container_red_liquid ( beaker , red_liquid_column ) and self . dropper_above_sth ( dropper , beaker ) :
   if 74 - 74: OOoOoo000O00 * i1I1IiIIiIi1 . o00Oo
   if 2 - 2: o0Ooo0OOO * Ooo0o % iI + ii1I1iII1I1I % iI
   self . flg4_1 , self . flg4_2 , self . flg4_3 = False , False , False
   return True
  return False
  if 82 - 82: o00Oo % ooo0oOoooOOO0
  if 81 - 81: o0Ooo0OOO
 def dropwise_hcl_stir ( self , hand , dropper , beaker , red_liquid_column , glass_column ) :
  if 40 - 40: i11 . ooo0oOoooOOO0 + OOoOoo000O00 . Oo0Oo
  if self . hand_sth ( hand , dropper ) and self . container_red_liquid ( beaker , red_liquid_column ) and self . dropper_above_sth ( dropper , beaker ) and self . glass_column_beaker ( hand , glass_column , beaker ) [ 0 ] :
   if 96 - 96: i1iiIII111 / OOooooOo00 / I1Ii111i1I + I1Ii111i1I
   self . flg5_1 = True
   self . diff_flag = True
  if self . flg5_1 and self . stir_check ( self . bbox , glass_column , beaker ) :
   self . flg5_2 = True
  if self . flg5_2 :
   if red_liquid_column . shape [ 0 ] == 0 :
    self . flg5_1 , self . flg5_2 = False , False
    return True
  return False
  if 35 - 35: Ooo0o + OOoOoo000O00
  if 96 - 96: Oo . ooo0oOoooOOO0 . iI
 def beaker_test_tube ( self , hands , test_tube , beaker ) :
  OOo = False
  oO000O0O0 = False
  if hands . shape [ 0 ] == 2 and test_tube . shape [ 0 ] != 0 and beaker . shape [ 0 ] != 0 :
   for IiiIii11iII1 in hands :
    I11I1 = IiiIii11iII1 [ : 4 ]
    if iou ( I11I1 , test_tube [ 0 ] [ : 4 ] ) > 0 :
     OOo = True
    if iou ( I11I1 , beaker [ 0 ] [ : 4 ] ) > 0 :
     oO000O0O0 = True
   if OOo and oO000O0O0 :
    if iou ( beaker [ 0 ] [ : 4 ] , test_tube [ 0 ] [ : 4 ] ) > 0 :
     return True
  else :
   return False
   if 48 - 48: iI
   if 61 - 61: iIi1Ii1i
 def dropwise_NaOH_to_test_tube ( self , hand , test_tube , dropper , red_liquid_column ) :
  if self . hand_sth ( hand , test_tube ) and self . dropper_above_sth ( dropper , test_tube ) :
   self . flg8_1 = True
  if self . flg8_1 :
   if self . hand_sth ( hand , test_tube ) and self . container_red_liquid ( test_tube , red_liquid_column ) :
    self . flg8_1 = False
    return True
  return False
  if 72 - 72: iI % IiI * Oo
  if 90 - 90: iI111iiIi11i * ooo0oOoooOOO0 . o0Ooo0OOO
 def clean_desk ( self , hand_duster_front , hand_duster_top , clean_desk_front , clean_desk_top , clean_desk_side ,
 hand_top , sths , score_list ) :
  Iiii1iIII = score_list
  Iiii1iIII = np . array ( Iiii1iIII )
  o0oO0OOo = np . sum ( Iiii1iIII != 0 )
  if o0oO0OOo >= 5 :
   if hand_duster_front . shape [ 0 ] != 0 or hand_duster_top . shape [ 0 ] != 0 :
    self . flg9_1 = True
  if self . flg9_1 :
   if clean_desk_front . shape [ 0 ] != 0 or clean_desk_top . shape [ 0 ] != 0 or clean_desk_side . shape [ 0 ] != 0 :
    self . flg9_2 = True
  if self . flg9_2 :
   if self . hand_without_sth ( hand_top , sths ) :
    self . flg9_1 = False
    self . flg9_2 = False
    return True
  return False
  if 89 - 89: Oo / iI - ii1I1iII1I1I
  if 13 - 13: OOooooOo00 + ii1I1iII1I1I * i1I1IiIIiIi1 . i1iiIII111 + Oo . IiI
 def score_process ( self , top_true , front_true , side_true ) :
  if top_true or front_true or side_true :
   if top_true :
    iIiii1i1iiIi1 , Ii1I , iiiiIi1IiiIi , Ii1iIII11i , oo000OO0ooO , OoO0OooO0ooo , O00OO00O , i111iIIiIIII , oOO0OOo , ooo = self . preds_top
    if 56 - 56: ii1I1iII1I1I
    if 17 - 17: i11 . OOooooOo00 % OOo0O0oOo0O + ii1I1iII1I1I - iI111iiIi11i
    IIIi11ii1Ii = [ Ii1I , iiiiIi1IiiIi , Ii1iIII11i , oo000OO0ooO , OoO0OooO0ooo ,
 O00OO00O , i111iIIiIIII ]
   if side_true :
    IIiI1iI111 , Ii , OOooo00 , o00o , iIIIiII1 , oo , iiII1II1IIIi , IiI111I1 , oO0oo , IiIII = self . preds_side
    if 16 - 16: Ooo0o
   if front_true :
    oO00 , II1 , II , II1I11IIiIi , oO0OoOooO0O , I1IiIi , i1iII11iii , Ii1i1 , iII11I11111I , ooOO0OO0o = self . preds_front
    if 46 - 46: OOoOoo000O00 . Oo - o0Ooo0OOO . OOoOoo000O00 + IiI
    if 83 - 83: iIi1Ii1i
    if 77 - 77: Oo - OOooooOo00 % o0Ooo0OOO * i11 - i1iiIII111
    if 42 - 42: I1Ii111i1I - o0Ooo0OOO / OOo0O0oOo0O - IiI + I1Ii111i1I
   if self . diff_flag :
    i1II1 = copy . deepcopy ( self . frame_front )
    oo0IiiI11IIi1I , oOOOO0ooO , IIIII11 = i1II1 . shape
    if 7 - 7: Oo0Oo * Oo0Oo . OOooooOo00 . i1I1IiIIiIi1 * o00Oo + iIi1Ii1i
    i1II1 = cv2 . resize ( i1II1 , ( 640 , 360 ) )
    if 20 - 20: i11 . ooo0oOoooOOO0 * ii1I1iII1I1I
    self . bbox = [ ]
    if 40 - 40: i1I1IiIIiIi1 * iIi1Ii1i / IiI * OOooooOo00 + Oo0Oo - ooo0oOoooOOO0
    IIiIIiiIIi = cv2 . getStructuringElement ( cv2 . MORPH_ELLIPSE , ( 9 , 4 ) )
    if 29 - 29: IiI / OOoOoo000O00
    if 13 - 13: I1Ii111i1I % Oo0Oo . ooo0oOoooOOO0 % i1I1IiIIiIi1 % ooo0oOoooOOO0
    i1i1IiII11iI1 = np . ones ( ( 5 , 5 ) , np . uint8 )
    O0oOO = cv2 . cvtColor ( i1II1 , cv2 . COLOR_BGR2GRAY )
    if 25 - 25: i11 * Oo - OOoOoo000O00
    if 100 - 100: I1Ii111i1I % Ii1I111 - iIi1Ii1i / ooo0oOoooOOO0
    O0oOO = cv2 . GaussianBlur ( O0oOO , ( 9 , 9 ) , 0 )
    if 33 - 33: Ooo0o
    if self . background is None :
     self . background = O0oOO
    o0oOooOO0oOoo = cv2 . absdiff ( self . background , O0oOO )
    if 58 - 58: iI111iiIi11i . i1I1IiIIiIi1 . I1Ii111i1I
    if 48 - 48: IiI - ii1I1iII1I1I
    o0oOooOO0oOoo = cv2 . threshold ( o0oOooOO0oOoo , 25 , 255 , cv2 . THRESH_BINARY ) [ 1 ]
    o0oOooOO0oOoo = cv2 . dilate ( o0oOooOO0oOoo , IIiIIiiIIi , iterations = 2 )
    if 29 - 29: Oo0Oo
    IiiI , oOO0oooOoo000 = cv2 . findContours ( o0oOooOO0oOoo . copy ( ) , cv2 . RETR_EXTERNAL , cv2 . CHAIN_APPROX_SIMPLE )
    for ooOooo in IiiI :
     if 54 - 54: Oo % OOo0O0oOo0O . iIi1Ii1i - i11i1 % I1Ii111i1I * i11
     if cv2 . contourArea ( ooOooo ) < 160 :
      continue
     [ iIi1Ii , o0o0Oo00000o , O0 , O0oOoO ] = cv2 . boundingRect ( ooOooo )
     if 31 - 31: OOo0O0oOo0O * Oo0Oo % o0Ooo0OOO / OOooooOo00 + Ii1I111 + Oo
     if 90 - 90: Ii1I111 * IiI / Oo * o0Ooo0OOO
     if 38 - 38: i1iiIII111 . o0Ooo0OOO
     [ OO0OOo0oOO , IiIII1 , OoO0OO0 , oOoO0o0OOooO0 ] = [ ( iIi1Ii / 640 ) * oOOOO0ooO , ( o0o0Oo00000o / 360 ) * oo0IiiI11IIi1I , O0 * ( float ( oOOOO0ooO / 640 ) ) , O0oOoO * ( float ( oo0IiiI11IIi1I / 360 ) ) ]
     if 38 - 38: iIi1Ii1i - iI111iiIi11i * Ii1I111
     if 89 - 89: Oo + ii1I1iII1I1I . iI111iiIi11i % o00Oo
     [ i1I11i11 , OoOOoO000O , O0o0O0o0o , Oo0 ] = [ OO0OOo0oOO , IiIII1 , OO0OOo0oOO + OoO0OO0 , IiIII1 + oOoO0o0OOooO0 ]
     if torch . cuda . is_available ( ) :
      i1II111iii11 = torch . Tensor ( [ i1I11i11 , OoOOoO000O , O0o0O0o0o , Oo0 ] ) . cuda ( )
     else :
      i1II111iii11 = torch . Tensor ( [ i1I11i11 , OoOOoO000O , O0o0O0o0o , Oo0 ] )
     self . bbox . append ( i1II111iii11 )
     if 57 - 57: ooo0oOoooOOO0
     if 9 - 9: ii1I1iII1I1I * ii1I1iII1I1I
   if not self . scorePoint1 :
    if self . pour_NaOH_into_beaker_teach ( oO00 , II1 , II1I11IIiIi , II ) :
     oo0OOOOo0o0 = 0.1
     self . assignScore ( index = 1 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = oo0OOOOo0o0 ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "1.jpg" ,
 preds = self . preds_front
 )
     if 47 - 47: o00Oo + OOo0O0oOo0O / Ii1I111 . Ooo0o
     if 67 - 67: OOo0O0oOo0O % o00Oo + Oo * i1iiIII111
     if 79 - 79: Ooo0o * OOo0O0oOo0O / ooo0oOoooOOO0
   if not self . scorePoint2 :
    if self . pour_Phenolphthalein_into_NaOH_teach ( oO00 , II1 , II1I11IIiIi ,
 II , Ii1i1 ) :
     oo0OOOOo0o0 = 0.1
     self . assignScore ( index = 2 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = oo0OOOOo0o0 ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "2.jpg" ,
 preds = self . preds_front
 )
     self . scorePoint2 = True
     if 10 - 10: Oo / Oo0Oo . ii1I1iII1I1I * IiI
     if 71 - 71: OOoOoo000O00 + Ii1I111 / I1Ii111i1I + OOo0O0oOo0O / i1iiIII111
   if not self . scorePoint3 :
    if 18 - 18: i11i1 - ii1I1iII1I1I
    if 71 - 71: Oo + ooo0oOoooOOO0 % IiI % OOoOoo000O00 . i1I1IiIIiIi1
    if self . temperature_measurement_class ( oO00 , oO0OoOooO0O , II1 ,
 Ii1i1 , II ) :
     oo0OOOOo0o0 = 0.1
     self . assignScore ( index = 3 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = oo0OOOOo0o0 ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "3.jpg" ,
 preds = self . preds_front
 )
     if 92 - 92: I1Ii111i1I - iI111iiIi11i - IiI % Oo0Oo / IiI * Oo
     if 60 - 60: ii1I1iII1I1I % OOooooOo00 / i11 * ooo0oOoooOOO0 / I1Ii111i1I - o0Ooo0OOO
   if not self . scorePoint4 :
    if self . dropper_hcl_to_beaker ( oO00 , II1 , II1I11IIiIi , II ,
 Ii1i1 , oO0OoOooO0O , I1IiIi ) :
     oo0OOOOo0o0 = 0.1
     self . assignScore ( index = 4 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = oo0OOOOo0o0 ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "4.jpg" ,
 preds = self . preds_front
 )
     if 16 - 16: OOoOoo000O00 / Ii1I111 / iI + I1Ii111i1I + OOoOoo000O00
     if 11 - 11: OOooooOo00 / ooo0oOoooOOO0 + OOoOoo000O00
   if not self . scorePoint5 :
    if self . dropwise_hcl_stir ( oO00 , II , II1 , Ii1i1 , oO0OoOooO0O ) :
     if 79 - 79: I1Ii111i1I . Ii1I111 * i11 % Ii1I111 / iIi1Ii1i
     if not self . scorePoint4 :
      oo0OOOOo0o0 = 0.1
      self . assignScore ( index = 4 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = oo0OOOOo0o0 ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "4.jpg" ,
 preds = self . preds_front
 )
      if 93 - 93: i11 + i11i1 . o0Ooo0OOO . i11 * o00Oo
     oo0OOOOo0o0 = 0.1
     self . assignScore ( index = 5 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = oo0OOOOo0o0 ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "5.jpg" ,
 preds = self . preds_front
 )
     self . diff_flag = False
     if not self . scorePoint4 :
      self . assignScore ( index = 4 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = oo0OOOOo0o0 ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "4.jpg" ,
 preds = self . preds_front
 )
      if 84 - 84: iI111iiIi11i % iIi1Ii1i
      if 82 - 82: Ooo0o
   if not self . scorePoint6 :
    if self . temperature_measurement_teach_after ( oO00 , oO0OoOooO0O , I1IiIi ,
 II1 , Ii1i1 ) :
     oo0OOOOo0o0 = 0.1
     self . assignScore ( index = 6 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = oo0OOOOo0o0 ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "6.jpg" ,
 preds = self . preds_front
 )
     if 81 - 81: OOoOoo000O00 + iI - i1I1IiIIiIi1 * Oo + IiI
     if 89 - 89: Ii1I111
   if not self . scorePoint7 :
    if self . beaker_test_tube ( oO00 , i1iII11iii , II1 ) :
     oo0OOOOo0o0 = 0.1
     self . assignScore ( index = 7 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = oo0OOOOo0o0 ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "7.jpg" ,
 preds = self . preds_front
 )
     if 57 - 57: Oo - Oo0Oo / ooo0oOoooOOO0 % Oo0Oo
     if 92 - 92: ii1I1iII1I1I * ooo0oOoooOOO0 - ii1I1iII1I1I
   if not self . scorePoint8 :
    if self . dropwise_NaOH_to_test_tube ( oO00 , i1iII11iii , II , Ii1i1 ) :
     oo0OOOOo0o0 = 0.1
     self . assignScore ( index = 8 ,
 img = self . frame_front ,
 object = self . objects_front ,
 conf = oo0OOOOo0o0 ,
 time_frame = self . time_front ,
 num_frame = self . num_frame_front ,
 name_save = "8.jpg" ,
 preds = self . preds_front
 )
     if 66 - 66: Oo0Oo . Oo / o00Oo . iI - ooo0oOoooOOO0
     if 13 - 13: OOoOoo000O00
   if not self . scorePoint9 :
    OoO00 = [ self . scorePoint1 , self . scorePoint2 , self . scorePoint3 , self . scorePoint4 , self . scorePoint5 ,
 self . scorePoint6 , self . scorePoint7 , self . scorePoint8 ]
    if self . clean_desk ( iII11I11111I , oOO0OOo , ooOO0OO0o , ooo , IiIII ,
 iIiii1i1iiIi1 , IIIi11ii1Ii , OoO00 ) :
     oo0OOOOo0o0 = 0.1
     self . assignScore ( index = 9 ,
 img = self . frame_top ,
 object = self . objects_top ,
 conf = oo0OOOOo0o0 ,
 time_frame = self . time_top ,
 num_frame = self . num_frame_top ,
 name_save = "9.jpg" ,
 preds = self . preds_top
 )
     if 41 - 41: Ooo0o / I1Ii111i1I
     if 60 - 60: Ooo0o + IiI . I1Ii111i1I - Oo
     if 31 - 31: ii1I1iII1I1I % o0Ooo0OOO
     if 7 - 7: iIi1Ii1i - Ooo0o * OOoOoo000O00
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
