import m5
from m5.objects import *
from m5.event import *
import time
import os
import sys
import subprocess

CYAN = "\033[36m"; R = "\033[0m"
BRIGHTMAGENTA = "\033[95m"

binary = "/home/mohammad/Projects/Gem5_Interrupt_Handling/gem5/configs/project8/2SecJob.rv64gc"

def printTickInfo(prefix=""):
    print(f"\033[33m{prefix}Current Tick: {m5.curTick()}\033[0m")

# def ResumeWork():
#     printTickInfo("Before checking interrupts: ")
#     print("\033[32mLets check interrupts...\033[0m")
#     fin = system.cpu.interrupts[0].checkForInterrupts()
#     m5.simulate(1000)
#     printTickInfo("After checking interrupts: ")
#     if fin == -1:
#         print("\033[31mNo interrupt found\033[0m")
#     else: 
#         print(f"\033[32mFound interrupt at: {fin}\033[0m")


#     printTickInfo("Before clearing interrupts: ")
#     print("\033[32mClearing Interrupts...\033[0m")
#     system.cpu.interrupts[0].clearAll()
#     m5.simulate(1000)
#     printTickInfo("After clearing interrupts: ")

#     printTickInfo("Before checking interrupts again: ")
#     print("\033[32mLets check interrupts again...\033[0m")
#     fin = system.cpu.interrupts[0].checkForInterrupts()
#     m5.simulate(1000)
#     printTickInfo("After checking interrupts again: ")
#     if fin == -1:
#         print("\033[31mNo interrupt found\033[0m")
#     else: 
#         print(f"\033[32mFound interrupt at: {fin}\033[0m")

#     m5.simulate()


# ResumeWork_event = EventWrapper(ResumeWork)

system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = "timing"
system.mem_ranges = [AddrRange("2GiB")]
system.cpu = RiscvTimingSimpleCPU()

system.membus = SystemXBar()
system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports
system.cpu.createInterruptController()

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports

system.workload = SEWorkload.init_compatible(binary)
p = Process()
p.cmd = [binary]
system.cpu.workload = p
system.cpu.createThreads()
root = Root(full_system=False, system=system)
m5.instantiate("2")
print(f"{BRIGHTMAGENTA}[gem5] Instantiated system for resume simulation.{R}")

# ResumeWork_event()

exit_event = m5.simulate()

print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
