from m5.params import *
from m5.proxy import *
from m5.SimObject import SimObject
from m5.objects.PlicDevice import PlicIntDevice

class InterruptBridge(PlicIntDevice):
    type = 'InterruptBridge'
    cxx_header = "learning_gem5/part3/InterruptBridge.hh"
    cxx_class = 'gem5::InterruptBridge'

    interrupt_id = Param.Int(16, "Interrupt ID")
