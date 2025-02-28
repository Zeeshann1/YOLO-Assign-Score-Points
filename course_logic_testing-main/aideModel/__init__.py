from configg.global_config import OPENVINO_VERSION
import sys
try:
    if OPENVINO_VERSION<2022:
        from openvino.inference_engine import IECore
        ie = IECore()
        print('加载2021')
    else:
        from openvino.runtime import Core
        ie = Core()
        print('加载2022')
except:
    print('openvino init fail')
    ie = None
pyversion = "".join(sys.version.split(".")[:2])
lib_path = 'aideModel/libs/' + ("py" + pyversion)
sys.path.insert(0, lib_path)
from keypoint_infer import HRliteOpenvinoDetect, HrnentKeyPoint
from class_predict import ClassMobilenetv3, ClassOpenvinoDetect