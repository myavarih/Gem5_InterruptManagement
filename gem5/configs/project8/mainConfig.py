import m5
from m5.objects import *
from m5.event import EventWrapper
import sys, select

CYAN = "\033[36m"; R = "\033[0m"
BRIGHTMAGENTA = "\033[95m"
SLICE_TICKS = 10_000_000


binary = "/home/mohammad/Projects/Gem5_Interrupt_Handling/gem5/configs/project8/2SecJob.rv64gc"
interruptBinary = "/home/mohammad/Projects/Gem5_Interrupt_Handling/gem5/configs/project8/ISR.rv64gc"

def printTickInfo(prefix=""):
    print(f"\033[33m{prefix}Current Tick: {m5.curTick()}\033[0m")

def newInterrupt(num):
    printTickInfo("Before raising interrupt: ")
    print("\033[32mLets raise an interrupt...\033[0m")
    system.cpu.interrupts[0].raiseInterruptPin(num)
    m5.simulate(1000)
    printTickInfo("After raising interrupt: ")

interrupt_event = EventWrapper(lambda: newInterrupt(0))


system = System()
system.multi_thread = True
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = "timing"
system.mem_ranges = [AddrRange("2GiB")]

# Two HW threads on one core
system.cpu = RiscvTimingSimpleCPU(numThreads=2)  

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


main_p = Process()
main_p.cmd = [binary]

isr_p = Process(pid=101)
isr_p.cmd = [interruptBinary]


system.cpu.workload = [main_p, isr_p]
system.cpu.createThreads()

root = Root(full_system=False, system=system)
m5.instantiate()


system.cpu.threads[1].suspend()

printTickInfo("Before simulation: ")
print(f"{BRIGHTMAGENTA}▶ Main running on thread 0. Press ENTER to switch to ISR…{R}", flush=True)

# ------------------ Phase 1: run MAIN until Enter ------------------
while True:
    r, _, _ = select.select([sys.stdin], [], [], 0)
    if r:
        _ = sys.stdin.readline()
        print(f"{BRIGHTMAGENTA}⏸ Enter detected – switching to ISR.{R}", flush=True)
        system.cpu.threads[0].suspend()
        break

    m5.simulate(SLICE_TICKS)
    

interrupt_event()

system.cpu.threads[1].activate(0) 

printTickInfo("Switched to ISR thread: ")
print(f"{CYAN}▶ Running ISR (thread 1).{R}")

while True:
    ev = m5.simulate(SLICE_TICKS)
    cause = ev.getCause()
    if cause != "simulate() limit reached":
        print(f"{CYAN}ISR stop cause: {cause}{R}")
        break

# Ensure ISR stays paused if it left the thread active
system.cpu.threads[1].suspend()

# ------------------ Phase 3: resume MAIN ------------------
system.cpu.threads[0].activate(0)
print(f"{BRIGHTMAGENTA}▶ ISR done. Resuming main (thread 0)…{R}")

while True:
    ev = m5.simulate(SLICE_TICKS)
    cause = ev.getCause()
    if cause != "simulate() limit reached":
        print(f"Main stop cause: {cause}")
        break

print(f"Stopped at tick {m5.curTick()}")
printTickInfo("After simulation: ")
