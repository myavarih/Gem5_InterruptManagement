import subprocess

gem5_dir = "/home/mohammad/Projects/Gem5_Interrupt_Handling/gem5"

subprocess.run(
    ["./build/RISCV/gem5.opt",  "configs/project8/startConfig.py"],
    cwd=gem5_dir
)
subprocess.run(
    ["./build/RISCV/gem5.opt", "configs/project8/ISRConfig.py"],
    cwd=gem5_dir
)
subprocess.run(
    ["./build/RISCV/gem5.opt", "configs/project8/ResumeConfig.py"],
    cwd=gem5_dir
)
