"""Simple gem5 O3CPU configuration for Assignment 4.

Run this file through build/X86/gem5.opt, not with regular Python.
"""

import argparse
import os

import m5
from m5.objects import (
    AddrRange,
    Cache,
    DDR3_1600_8x8,
    LocalBP,
    L2XBar,
    MemCtrl,
    Process,
    Root,
    SEWorkload,
    SrcClockDomain,
    System,
    SystemXBar,
    TournamentBP,
    VoltageDomain,
    X86O3CPU,
)


class L1ICache(Cache):
    size = "32KiB"
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20


class L1DCache(Cache):
    size = "32KiB"
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20


class L2Cache(Cache):
    size = "256KiB"
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", required=True, help="Path to an x86-64 static binary")
    parser.add_argument("--width", type=int, choices=(1, 4), default=1)
    parser.add_argument(
        "--predictor",
        choices=("minimal", "tournament"),
        default="minimal",
        help="Minimal-size or standard tournament predictor",
    )
    parser.add_argument("--threads", type=int, choices=(1, 2), default=1)
    parser.add_argument(
        "--max-insts",
        type=int,
        default=0,
        help="Optional instruction limit; 0 runs until the program exits",
    )
    return parser.parse_args()


args = parse_args()
binary = os.path.abspath(args.binary)
if not os.path.isfile(binary):
    raise FileNotFoundError(f"Binary not found: {binary}")

system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "2GHz"
system.clk_domain.voltage_domain = VoltageDomain()
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MiB")]
system.cache_line_size = 64

system.cpu = X86O3CPU(cpu_id=0)
system.cpu.numThreads = args.threads

# Width 1 is the single-issue baseline. Width 4 is the superscalar model.
system.cpu.fetchWidth = args.width
system.cpu.decodeWidth = args.width
system.cpu.renameWidth = args.width
system.cpu.dispatchWidth = args.width
system.cpu.issueWidth = args.width
system.cpu.commitWidth = args.width

# gem5 25.1 uses a BranchPredictor wrapper. Replace only its conditional
# predictor component rather than replacing the wrapper itself.
if args.predictor == "minimal":
    system.cpu.branchPred.conditionalBranchPred = LocalBP(
        localPredictorSize=8,
        localCtrBits=1,
    )
else:
    system.cpu.branchPred.conditionalBranchPred = TournamentBP()

if args.max_insts > 0:
    system.cpu.max_insts_any_thread = args.max_insts

system.cpu.icache = L1ICache()
system.cpu.dcache = L1DCache()
system.l2bus = L2XBar()
system.l2cache = L2Cache()
system.membus = SystemXBar()

system.cpu.icache.cpu_side = system.cpu.icache_port
system.cpu.icache.mem_side = system.l2bus.cpu_side_ports
system.cpu.dcache.cpu_side = system.cpu.dcache_port
system.cpu.dcache.mem_side = system.l2bus.cpu_side_ports
system.l2cache.cpu_side = system.l2bus.mem_side_ports
system.l2cache.mem_side = system.membus.cpu_side_ports

system.cpu.createInterruptController()
for interrupt in system.cpu.interrupts:
    interrupt.pio = system.membus.mem_side_ports
    interrupt.int_requestor = system.membus.cpu_side_ports
    interrupt.int_responder = system.membus.mem_side_ports
system.system_port = system.membus.cpu_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

system.workload = SEWorkload.init_compatible(binary)
processes = []
for index in range(args.threads):
    process = Process(pid=100 + index)
    process.cmd = [binary]
    process.cwd = os.getcwd()
    processes.append(process)

system.cpu.workload = processes[0] if args.threads == 1 else processes
system.multi_thread = args.threads > 1
system.cpu.createThreads()

root = Root(full_system=False, system=system)
m5.instantiate()

print(
    f"Starting simulation: width={args.width}, predictor={args.predictor}, "
    f"threads={args.threads}, binary={os.path.basename(binary)}"
)
exit_event = m5.simulate()
print(f"Exiting at tick {m5.curTick()} because {exit_event.getCause()}")
