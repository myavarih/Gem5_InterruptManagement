# se_all_in_one_stdlib.py
from pathlib import Path
from gem5.utils.requires import requires
from gem5.isas import ISA

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes

from gem5.simulate.simulator import Simulator
from gem5.simulate.exit_event import ExitEvent
from gem5.simulate.exit_event_generators import save_checkpoint_generator
from gem5.resources.resource import BinaryResource

# ---- EDIT THESE ----
BIN_A = "/home/mohammad/Projects/Gem5 Interrupt Handling/gem5/configs/project8/2SecJob.rv64gc"
BIN_B = "/home/mohammad/Projects/Gem5 Interrupt Handling/gem5/configs/project8/ISR.rv64gc"
N_TICKS = 500000000000
CKPT_A = Path("chkptA")

# Require a RISC-V build
requires(isa_required=ISA.RISCV)

def build_board(binary: BinaryResource) -> SimpleBoard:
    cache = NoCache()
    mem   = SingleChannelDDR3_1600(size="512MiB")
    cpu   = SimpleProcessor(cpu_type=CPUTypes.TIMING, isa=ISA.RISCV, num_cores=1)
    board = SimpleBoard(clk_freq="1GHz", processor=cpu, memory=mem, cache_hierarchy=cache)
    # SE workload: just a plain RISC-V binary
    board.set_se_binary_workload(binary=binary, arguments=[])
    return board

# 1) Run A for N_TICKS and checkpoint
board_a = build_board(BinaryResource(BIN_A))
sim_a = Simulator(
    board=board_a,
    on_exit_event={
        # When the scheduled max-tick fires, auto-save a checkpoint
        ExitEvent.MAX_TICK: save_checkpoint_generator(CKPT_A)
    },
)
sim_a.set_max_ticks(N_TICKS)
print(f"[A] Running {BIN_A} for {N_TICKS} ticks, then saving {CKPT_A}")
sim_a.run()

# 2) Run B UNTIL IT FINISHES (no stop scheduled)
board_b = build_board(BinaryResource(BIN_B))
sim_b = Simulator(board=board_b)
print(f"[B] Running {BIN_B} until program exit")
sim_b.run()  # no schedule_* call -> runs until the binary exits

# 3) Restore A and continue for RESUME_TICKS
#    (Most stdlib versions support passing 'checkpoint=' into Simulator)
board_a2 = build_board(BIN_A)
print(f"[A] Restoring from {CKPT_A} and running")
sim_a2 = Simulator(board=board_a2, checkpoint=CKPT_A)
sim_a2.run()
