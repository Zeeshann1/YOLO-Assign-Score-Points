#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2021/08/27 13:00
# @Author: wangqingfeng
# @FileName: experiment_model_info_collect.py

import os

from config import CO2ZQYYP01
from config.bio_seed_starch_conf import BYZZZZHYDF01
from config.bio_observe_yeasts_molds_with_microscope import BXWJGCJMJHMJ01
from configg.experiment_model_id import ExperimentModelID,ExperimentModelFULL
from config.phy_explore_buoyancy_factors_conf import PTJFLDXYNXYSYG01
from config.chem_co2_produce_property_01_conf import CCO2ZQHXZ01
from config.chem_co2_produce_property_sz_conf import CCO2ZQHXZ_sz
from config.chem_allocate_solution_conf import CNACLRYPZ01
from config.chem_weigh_dissolve_conf import CWZDCLYRJ01
from config.chem_filter_cou_conf import CHEMGL01
from config.chem_o2_conf import CO2ZQ01
from config.chem_explore_combustion_conditions_conf import CTJRSTJ01
from config.chem_allocate_solution_01_conf import CPZYDNDDLHNRY01
from .bio_make_onion_conf import BZZYCBPZP01
from .chem_allocate_solution_02_conf import CNACLRYPZ02
from .chem_allocate_solution_03_conf import CNACLRYPZ03
from .chem_allocate_solution_04_conf import CNACLRYPZ04
from .chem_allocate_solution_sz_conf import CNACLRYPZ_sz
from .chem_carbonate_inspection_conf import CTSYJY01  # 碳酸盐检验
from .chem_metal_active_order_conf import CJSHDXSX01  # 金属活动性顺序探究
from .chem_metal_active_order_02_conf import CJSHDXSX02  # 金属活动性顺序探究——上海中考
from .chem_metal_chemical_property_conf import CJSHXXZ01  # 金属的化学性质

from .chem_check_Na2CO3_NaCl import CHEMJYTSNHLHN
from .chem_acid_base_check_conf import CHEMSJJC01
from .chem_hcl_h2so4_check_conf import CHEMXYSYXLSDJB01
from .chem_properties_of_acids_conf import CHEMSDHXXZ01
from .chem_properties_of_base_conf import CHEMJDHXXZ01
from .chem_separate_phenol_and_check_conf import CHEMFLBHBFJBFDJY
from .chem_NH4_produce_conf import CNH4ZQPQ
from .bio_make_kq_conf import BZZRKQZP01
from .phy_plane_mirror_imaging_conf import PHYPMJCX01

from config.phy_measure_density_scale_conf import PCLWKMD02
from config.phy_measure_density_metal_block_01_conf import PCLWKMD01
from config.phy_measure_voltage_conf import PYDYBCDY01, PYDYBCDY02
from config.phy_convex_lens_imaging import PTJTTJCX01, PTJTTJCX02, PTJTTJCX03
from config.phy_sring_balance_measurement_conf import PYTHCLJCL01
from config.phy_two_spring_dynamometer import PCLJELPH01
from .phy_reflex import PTJGDFS01
from .phy_electricity_string_merge_conf import PJDDDLCBLSY01
from .phy_small_light_test_power_conf import PXDPCGL01
from .phy_lever_balance_conf import PTJGGPHDTJ01
from .phy_magnitic_field import PTJTDLXGCC01
from .phy_conservation_mechanical_energy_cq import PYZJXNSHDL01
from .phy_water_pressure_public_conf import PTJYTNBYQGGK01
from .phy_induced_current_conf import PTJDTCCGYDL02
from .phy_small_light_test_power_public_conf import PXDPCGLGKK01
from .chem_acid_base_neutralization_reaction_conf import CHEMSJZHFY01
from .chem_evaporation_crystallization_conf import CHEMJJHZF01
from .phy_mean_velocity_conf import PCLWTDPJSD01
from .phy_mechanical_efficiency_conf import PXMJXXLCD01
from .phy_sliding_friction_conf import PSPYDHDMCL01
from .phy_measure_metal_density_conf import PTPTPCJSMD01
from .phy_measure_liquid_density_conf import PTPTPCYTMD01
from .phy_salver_balance_measure_mass_conf import PTPTPCZL01
from .phy_archimedes_principle_conf import PAJMDYL01, PAJMDJMCL01
from .phy_measure_slide_rheostat_conf import PYHDBZQGBDLZDDL01, PYHDBZQGBDLZDDL02
from .phy_measure_A_conf import PYDLBCDL01
from .phy_relationship_M_V_01_conf import PTJZLHTJDGX01
from .phy_relationship_M_V_02_conf import PTJZLHTJDGX02
from .phy_induced_current_ration_conf import PTJGYDLDXFX01
from .bio_make_leaf_sz_conf import BZZBCYZP01
from .bio_make_leaf_sz_conf import BZZBCYZP02
from config.phy_measure_length_time_conf import PYKDCCLCDYBCLSJ01  # 用刻度尺测量长度用表测量时间
from config.phy_measure_temperature_conf import PCJWDJCLWD01  # 常见温度计测温度
from .phy_water_boiling_temperature_conf import PTJSFTSWDBHDTD01  # 探究水沸腾时温度变化的特点
from .phy_heat_capacity_conf import PCDWZDBRR01  # 测定物质的比热容
from .chem_access_and_heat_beaker_liquid_heat_conf import CSJDQYYJRZSBZYTJR01  # 试剂的取用与加热之烧杯中液体加热
from .chem_access_and_heat_tube_liquid_heat_conf import CSJDQYYJRZSGZYTJR01  # 试剂的取用与加热之试管中液体加热
from .chem_access_and_heat_solid_heat_conf import CSJDQYYJRZGTDJR01  # 试剂的取用与加热之固体加热
from .bio_make_observ_yeast_conf import BZZGCJMJZP01  # 制作观察酵母菌装片
from .bio_observ_peni_conf import BGCQMYJZP01  # 观察青霉永久装片
from .bio_explore_peanut_01_conf import BTJHSGSDXDBY01  # 探究花生果实大小的变异
from .bio_observ_blood_conf import BGCRXTP01  # 观察人血涂片
from .bio_breathe_CO2_change_conf import BTJHXCO2BH01  # 探究呼吸过程中二氧化碳含量的变化
from .bio_identify_foods_for_protein_starch_and_fat_01_conf import BJDSWZHYDBZDFHZF01  # 鉴定食物中含有蛋白质、淀粉和脂肪


class ModelAllInfo:
    def __init__(self):
        self.model_all = {}
        self.experimentId_All = []
        #
        self.load_all_model_info()
        self.get_all_experiment()

    def load_all_model_info(self):
        # a = ['BZZBCYZP02','CCO2ZQHXZ01','CHEMGL01','PTPTPCZL01','PXDPCGLGKK01']
        for key in ExperimentModelFULL.keys():
            self.model_all[globals()[key]['experimentId']] = globals()[key]

    def get_all_experiment(self):
        for item in self.model_all:
            self.experimentId_All.append(item)

    def get_score_pts_sent(self):
        all_sent_score_points = {}
        for itemOneName in self.model_all:
            itemOne = self.model_all[itemOneName]
            one_score_info = {
                'name': itemOne['name'],
                'experimentId': itemOne['experimentId'],
                'scorePointInfo': itemOne['scorePointInfo']
            }
            all_sent_score_points[itemOne['experimentId']] = one_score_info

        return all_sent_score_points


if __name__ == '__main__':
    model_info = ModelAllInfo()
    mmmmm = model_info.get_score_pts_sent()
    print(mmmmm)
    for item in model_info.experimentId_All:
        print(item)
