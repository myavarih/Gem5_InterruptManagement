# configs/project8/simple_interrupt_test.py

import importlib
import m5
from m5.SimObject import SimObject
# This import is needed for AddrRange
from m5.params import AddrRange
from m5.util import fatal

def simclass(modname, clsname=None):
    """
    Safely fetch the SimObject class from m5.objects.<modname>.
    Avoids 'module is not callable' by never returning the module itself.
    """
    mod = importlib.import_module(f"m5.objects.{modname}")
    name = clsname or modname
    if hasattr(mod, name) and isinstance(getattr(mod, name), type):
        return getattr(mod, name)
    # Fallback: first SimObject subclass in the module whose name endswith clsname
    for n, obj in vars(mod).items():
        if isinstance(obj, type) and issubclass(obj, SimObject):
            if n == name or n.lower().endswith(name.lower()):
                return obj
    raise ImportError(f"Could not find class '{name}' in m5.objects.{modname}")

# Core SimObjects
System         = simclass("System")
Root           = simclass("Root")
SrcClockDomain = simclass("ClockDomain", "SrcClockDomain") # Corrected
VoltageDomain  = simclass("VoltageDomain")
SystemXBar     = simclass("XBar", "SystemXBar")
SimpleMemory   = simclass("SimpleMemory")
Process        = simclass("Process")
SEWorkload     = simclass("Workload", "SEWorkload")

# The script is for RISC-V, so we'll directly use the RISC-V timing CPU.
CPUClass = simclass("RiscvCPU", "RiscvTimingSimpleCPU")

# ---- 1) Build the system ----------------------------------------------------
system = System()

# Clock / voltage
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

# SE mode + memory
system.mem_mode   = "timing"
system.mem_ranges = [AddrRange("512MB")]

# CPU
cpu = CPUClass()
cpu.createInterruptController()
system.cpu = cpu

# Bus + single memory
system.membus = SystemXBar()
cpu.icache_port    = system.membus.cpu_side_ports
cpu.dcache_port    = system.membus.cpu_side_ports
system.system_port = system.membus.cpu_side_ports

system.mem_ctrl = SimpleMemory(range=system.mem_ranges[0])
system.mem_ctrl.port = system.membus.mem_side_ports

# ---- 2) Workload (set this to a real ELF for the ISA you're simulating) -----
BINARY = "/home/mohammad/Projects/Gem5 Interrupt Handling/gem5/tests/test-progs/hello/bin/riscv/linux/hello"   # <-- CHANGE THIS!
system.workload = SEWorkload.init_compatible(BINARY)
process = Process()
process.cmd = [BINARY]
system.cpu.workload = process
system.cpu.createThreads()

# ---- 3) Instantiate & run ---------------------------------------------------
root = Root(full_system=False, system=system)
m5.instantiate()

print("Fast-forwarding to 100M cycles…")
m5.simulate(100000000)

# RISC-V: post the machine-timer interrupt (vector 7) to thread 0
INT_TIMER_MACHINE = 7
cpu.interrupts[0].raiseInterruptPin(INT_TIMER_MACHINE)
print(f"Injected interrupt {INT_TIMER_MACHINE} @ tick {m5.curTick()}")

print("Continuing simulation…")
event = m5.simulate()
print(f"Exited @ {m5.curTick()} because {event.getCause()}")
