import m5
from m5.objects import *
from m5.util import addToPath
import os

addToPath("..")
from common.Caches import *

system = System()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MiB")]

system.cpu = MinorCPU()
system.cpu.isa = RiscvISA()

system.platform = HiFive()

system.membus = SystemXBar()

system.cpu.icache = L1_ICache(size='32kB')
system.cpu.dcache = L1_DCache(size='32kB')
system.cpu.icache_port = system.cpu.icache.cpu_side
system.cpu.dcache_port = system.cpu.dcache.cpu_side

system.l2bus = L2XBar()
system.cpu.icache.mem_side = system.l2bus.cpu_side_ports
system.cpu.dcache.mem_side = system.l2bus.cpu_side_ports

system.l2cache = L2Cache(size='256kB')
system.l2cache.cpu_side = system.l2bus.mem_side_ports
system.l2cache.mem_side = system.membus.cpu_side_ports

system.platform.attachOnChipIO(system.membus)
system.iobus = IOXBar()
system.platform.attachOffChipIO(system.iobus)

system.bridge = Bridge(delay="50ns")
system.bridge.mem_side_port = system.iobus.cpu_side_ports
system.bridge.cpu_side_port = system.membus.mem_side_ports
system.bridge.ranges = system.platform._off_chip_ranges()

system.platform.attachPlic()

system.interrupt_generator = InterruptGenerator()
system.interrupt_generator.interrupt_pin = system.platform.plic.int_pin

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports

thispath = os.path.dirname(os.path.realpath(__file__))
binary = os.path.join(
    thispath,
    "../../",
    "tests/test-progs/hello/bin/riscv/linux/interrupts",
)

system.workload = RiscvBareMetal(bootloader=binary)

root = Root(full_system=True, system=system)
m5.instantiate()

print("Starting simulation...")
event = m5.simulate()
print(f"Exited @ {m5.curTick()} because {event.getCause()}")
