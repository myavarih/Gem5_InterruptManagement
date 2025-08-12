import m5
from m5.objects import *
from m5.event import create, getEventQueue
import time
import os

system = System()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MiB")]
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

thispath = os.path.dirname(os.path.realpath(__file__))
binary = os.path.join(
    thispath,
    "../../",
    "tests/test-progs/hello/bin/riscv/linux/hello",
)

system.workload = SEWorkload.init_compatible(binary)

process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system=False, system=system)
m5.instantiate()

def printTickInfo(prefix=""):
    print(f"\033[33m{prefix}Current Tick: {m5.curTick()}\033[0m")

def newInterrupt(num):
    printTickInfo("Before raising interrupt: ")
    print("\033[32mLets raise an interrupt...\033[0m")
    system.cpu.interrupts[0].raiseInterruptPin(num)

    printTickInfo("After raising interrupt: ")
    print("\033[32mLets check interrupts...\033[0m")
    fin = system.cpu.interrupts[0].checkForInterrupts()
    printTickInfo("After checking interrupt: ")
    if fin == -1:
        print("\033[31mNo interrupt found\033[0m")
    else:
        print(f"\033[32mFound interrupt at: {fin}\033[0m")
    printTickInfo("End of newInterrupt: ")

printTickInfo("Before simulation: ")
interrupt_event = create(lambda: newInterrupt(0))
getEventQueue().schedule(interrupt_event, m5.curTick() + 10)
print("Beginning simulation!")
exit_event = m5.simulate()

# newInterrupt(1)

printTickInfo("After simulation: ")

print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
