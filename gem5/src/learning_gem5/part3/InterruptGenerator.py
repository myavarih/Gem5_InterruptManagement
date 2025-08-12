from m5.params import *
from m5.proxy import *
from m5.SimObject import SimObject
from m5.objects.IntPin import IntSourcePin

class InterruptGenerator(SimObject):
    type = 'InterruptGenerator'
    cxx_header = "learning_gem5/part3/InterruptGenerator.hh"
    cxx_class = 'gem5::InterruptGenerator'

    interrupt_pin = IntSourcePin("The pin to signal an interrupt")
    interrupt_latency = Param.Latency('100us', "Time between interrupts")
