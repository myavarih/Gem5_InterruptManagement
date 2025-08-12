.section .text
.globl _start
_start:
    # Setup stack pointer
    li sp, 0x10000

    # Enable interrupts
    li t0, 0x88
    csrs mstatus, t0

    # Enable timer interrupts
    li t0, 0x80
    csrs mie, t0

    # Set trap vector
    la t0, trap_handler
    csrw mtvec, t0

    # Main loop
loop:
    wfi
    j loop

trap_handler:
    # Print message
    la a0, msg
    li a7, 4
    ecall

    # Clear timer interrupt
    li t0, 0x80
    csrc mip, t0

    mret

.section .data
msg:
    .string "Interrupt received!\n"
