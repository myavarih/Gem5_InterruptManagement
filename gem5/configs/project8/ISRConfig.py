import m5
from m5.objects import *
from m5.event import *
import time
import os
import sys
import subprocess

CYAN = "\033[36m"; R = "\033[0m"
BRIGHTMAGENTA = "\033[95m"

interruptBinary = "/home/mohammad/Projects/Gem5_Interrupt_Handling/gem5/configs/project8/ISR.rv64gc"

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

system.workload = SEWorkload.init_compatible(interruptBinary)
p = Process()
p.cmd = [interruptBinary]
system.cpu.workload = p
system.cpu.createThreads()
root = Root(full_system=False, system=system)
m5.instantiate()

print(f"{BRIGHTMAGENTA}[gem5] Instantiated system for ISR simulation.{R}")

m5.simulate()

print(f"Exiting @ tick {m5.curTick()}")
