---
title: Pannotia FW Test
tags:
    - x86
    - amdgpu
layout: default
permalink: resources/pannotia/fw
shortdoc: >
    Resources to build a disk image with the VEGA Pannotia FW workload.
---

Floyd-Warshall (FW) is a graph analytics application that is part of the Pannotia benchmark suite.
It is a classical dynamic-programming algorithm designed to solve the all-pairs shortest path (APSP) problem.
The provided version is for use with the gpu-compute model of gem5.  Thus, it has been ported from the prior CUDA and OpenCL variants to HIP, and validated on a Vega-class AMD GPU.

Compiling FW, compiling the VEGA_X86/Vega_X86 versions of gem5, and running FW on gem5 is dependent on the gcn-gpu docker image, `util/dockerfiles/gcn-gpu/Dockerfile` on the [gem5 stable branch](https://github.com/gem5/gem5).

## Compilation and Running

To compile FW:

```
cd src/gpu/pannotia/fw
docker run --rm -v ${PWD}:${PWD} -w ${PWD} -u $UID:$GID ghcr.io/gem5/gcn-gpu make gem5-fusion; make default
```

If you use the Makefile.default file instead, the Makefile will generate code designed to run on the real GPU instead.  Moreover, note that Makefile.gem5-fusion requires you to set the GEM5_ROOT variable (either on the command line or by modifying the Makefile), because the Pannotia applications have been updated to use [m5ops](https://www.gem5.org/documentation/general_docs/m5ops/).  By default, the Makefile builds for gfx902 and gfx900, and is placed in the src/gpu/pannotia/fw/bin folder. FW can be run on a non-mmapped input file, used to generate an mmapped input file, or run on an mmapped input file. To run FW using an mmapped input file, you must generate it first. An input file can be reused until it is overwritten by another file generation.  

## Compiling VEGA_X86/gem5.opt

FW is a GPU application, which requires that gem5 is built with the VEGA_X86 (or Vega_X86, although this has been less heavily tested) architecture.
The test is run with the VEGA_X86 gem5 variant, compiled using the gcn-gpu docker image:

```
git clone https://github.com/gem5/gem5
cd gem5
docker run -u $UID:$GID --volume $(pwd):$(pwd) -w $(pwd) ghcr.io/gem5/gcn-gpu:latest scons build/VEGA_X86/gem5.opt -j <num cores>
```

## Compiling FW
The Pannotia applications have been updated to use [m5ops](https://www.gem5.org/documentation/general_docs/m5ops/).

The docker command needs visibility to the gem5 repository for usage of the m5ops.
Thus we run the docker command from a directory with visibility and cd into the folder before running the make command.  
  
Note that Makefile.gem5-fusion requires you to set the GEM5_ROOT variable (either on the command line or by modifying the Makefile)  
  
To compile FW assuming the gem5 and gem5-resources repositories are in your working directory:

```
docker run --rm -v ${PWD}:${PWD} -w ${PWD} -u $UID:$GID ghcr.io/gem5/gcn-gpu:latest bash -c "cd gem5-resources/src/gpu/pannotia/fw ; make gem5-fusion"
```

If you use the Makefile.default file instead, the Makefile will generate code designed to run on the real GPU instead.
By default, the Makefile builds for gfx902 and gfx900, and is placed in the src/gpu/pannotia/fw/bin folder.
FW can be run on a non-mmapped input file, used to generate an mmapped input file, or run on an mmapped input file.
To run FW using an mmapped input file, you must generate it first. An input file can be reused until it is overwritten by another file generation.  

# Running FW on VEGA_X86/gem5.opt

## Run FW without using a mmapped input file

Assuming gem5 and gem5-resources are in your working directory

```
wget http://dist.gem5.org/dist/develop/datasets/pannotia/bc/1k_128k.gr
docker run --rm -v ${PWD}:${PWD} -w ${PWD} -u $UID:$GID ghcr.io/gem5/gcn-gpu:latest gem5/build/VEGA_X86/gem5.opt gem5/configs/example/apu_se.py -n3 --mem-size=8GB --benchmark-root=gem5-resources/src/gpu/pannotia/fw/bin -c fw_hip.gem5 --options="-f 1k_128k.gr -m default"
```

## Generate a mmapped input file

We recommend running mmap generation on the actual CPU instead of simulating it.

```
wget http://dist.gem5.org/dist/develop/datasets/pannotia/bc/1k_128k.gr
docker run --rm -v ${PWD}:${PWD} -w ${PWD} -u $UID:$GID ghcr.io/gem5/gcn-gpu:latest bash -c "./gem5-resources/src/gpu/pannotia/fw/bin/fw_hip -f ./gem5-resources/src/gpu/pannotia/fw/1k_128k.gr -m generate"
```

## Run FW using a mmapped input file

To run FW using an mmapped input file, you must generate it first. An input file can be reused until it is overwritten by another file generation.  

```
docker run --rm -v ${PWD}:${PWD} -w ${PWD} -u $UID:$GID ghcr.io/gem5/gcn-gpu:latest gem5/build/VEGA_X86/gem5.opt gem5/configs/example/apu_se.py -n3 --mem-size=8GB --benchmark-root=gem5-resources/src/gpu/pannotia/fw/bin -c fw_hip.gem5 --options="-f 1k_128k.gr -m usemmap"
```
                  
Note that the datasets from the original Pannotia suite have been uploaded to: <http://dist.gem5.org/dist/develop/datasets/pannotia>.
We recommend you start with the 1k_128k.gr input (<http://dist.gem5.org/dist/develop/datasets/pannotia/fw/1k_128k.gr>), as this is the smallest input that can be run with FW.
Note that 1k_128k is not designed for FW specifically though -- the above link has larger graphs designed to run with FW that you should consider using for larger experiments.

## Pre-built binary

SE mode:
<https://storage.googleapis.com/dist.gem5.org/dist/v24-0/test-progs/pannotia/fw_hip.gem5>
