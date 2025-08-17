import m5
from m5.objects import *
from m5.event import *
import time
import os
import sys
import subprocess
import select

CYAN = "\033[36m"; R = "\033[0m"
BRIGHTMAGENTA = "\033[95m"
SLICE_TICKS = 10_000_000 

binary = "/home/mohammad/Projects/Gem5_Interrupt_Handling/gem5/configs/project8/2SecJob.rv64gc"

def printTickInfo(prefix=""):
    print(f"\033[33m{prefix}Current Tick: {m5.curTick()}\033[0m")

def newInterrupt(num):
    printTickInfo("Before raising interrupt: ")
    print("\033[32mLets raise an interrupt...\033[0m")
    system.cpu.interrupts[0].raiseInterruptPin(num)
    m5.simulate(1000)
    printTickInfo("After raising interrupt: ")
    printTickInfo("Before checking interrupts: ")
    print("\033[32mLets check interrupts...\033[0m")
    fin = system.cpu.interrupts[0].checkForInterrupts()
    m5.simulate(1000)
    printTickInfo("After checking interrupts: ")
    if fin == -1:
        print("\033[31mNo interrupt found\033[0m")
    else: 
        print(f"\033[32mFound interrupt at: {fin}\033[0m")


    printTickInfo("Before clearing interrupts: ")
    print("\033[32mClearing Interrupts...\033[0m")
    system.cpu.interrupts[0].clearAll()
    m5.simulate(1000)
    printTickInfo("After clearing interrupts: ")

    printTickInfo("Before checking interrupts again: ")
    print("\033[32mLets check interrupts again...\033[0m")
    fin = system.cpu.interrupts[0].checkForInterrupts()
    m5.simulate(1000)
    printTickInfo("After checking interrupts again: ")
    if fin == -1:
        print("\033[31mNo interrupt found\033[0m")
    else: 
        print(f"\033[32mFound interrupt at: {fin}\033[0m")
        
    m5.checkpoint("2")



interrupt_event = EventWrapper(lambda: newInterrupt(0))


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
m5.instantiate()

printTickInfo("Before simulation: ")

print(f"{BRIGHTMAGENTA}▶ Simulation running. Press ENTER to pause…{R}", flush=True)
while True:
    r, _, _ = select.select([sys.stdin], [], [], 0)
    if r:
        _ = sys.stdin.readline() 
        print(f"{BRIGHTMAGENTA}⏸ Enter detected – pausing simulation.{R}", flush=True)
        break

    ev = m5.simulate(SLICE_TICKS)

print(f"Stopped at tick {m5.curTick()}")

interrupt_event()

printTickInfo("After simulation: ")

print(f"\033[32mmoving to ISR\033[0m")

