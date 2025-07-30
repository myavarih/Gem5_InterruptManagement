---
title: Pannotia Color Test
tags:
    - x86
    - amdgpu
layout: default
permalink: resources/pannotia/color
shortdoc: >
    Resources to build a disk image with the VEGA Pannotia Color workload.
---

Graph Coloring (CLR) is a graph analytics application that is part of the Pannotia benchmark suite.
It is used to label the vertices of a graph with colors such that no two adjacent vertices share the same color.
The provided version is for use with the gpu-compute model of gem5.
Thus, it has been ported from the prior CUDA and OpenCL variants to HIP, and validated on a Vega-class AMD GPU.

Compiling both CLR variants, compiling the VEGA_X86/Vega_X86 versions of gem5, and running both CLR variants on gem5 is dependent on the gcn-gpu docker image, `util/dockerfiles/gcn-gpu/Dockerfile` on the [gem5 stable branch](https://github.com/gem5/gem5).

## Compiling VEGA_X86/gem5.opt

Color is a GPU application, which requires that gem5 is built with the VEGA_X86 (or Vega_X86, although this has been less heavily tested) architecture.
The test is run with the VEGA_X86 gem5 variant, compiled using the gcn-gpu docker image:

```
git clone https://github.com/gem5/gem5
cd gem5
docker run -u $UID:$GID --volume $(pwd):$(pwd) -w $(pwd) ghcr.io/gem5/gcn-gpu:latest scons build/VEGA_X86/gem5.opt -j <num cores>
```

## Compiling Color
The Pannotia applications have been updated to use [m5ops](https://www.gem5.org/documentation/general_docs/m5ops/).

The docker command needs visibility to the gem5 repository for usage of the m5ops.
Thus we run the docker command from a directory with visibility and cd into the folder before running the make command.  
  
Note that Makefile.gem5-fusion requires you to set the GEM5_ROOT variable (either on the command line or by modifying the Makefile)  
  
Color has two variants: max and maxmin.  To compile the "max" variant assuming the gem5 and gem5-resources are in your working directory:

```
docker run --rm -v ${PWD}:${PWD} -w ${PWD} -u $UID:$GID ghcr.io/gem5/gcn-gpu:latest bash -c "cd gem5-resources/src/gpu/pannotia/color ; make gem5-fusion"
```

To compile the "maxmin" variant assuming the gem5 and gem5-resources are in your working directory:

```
docker run --rm -v ${PWD}:${PWD} -w ${PWD} -u $UID:$GID ghcr.io/gem5/gcn-gpu:latest bash -c "cd gem5-resources/src/gpu/pannotia/color ; export VARIANT=MAXMIN ; make gem5-fusion"
```

If you use the Makefile.default file instead, the Makefile will generate code designed to run on the real GPU instead.
By default, for both variants the Makefile builds for gfx902 and gfx900, and the binaries are placed in the src/gpu/pannotia/clr/bin folder.
Moreover, by default the VARIANT variable Color's Makefile assumes the max variant is being used, hence why this variable does not need to be set for compiling it.


# Running Color on VEGA_X86/gem5.opt

Assuming gem5 and gem5-resources are in your working directory.
The following command shows how to run the CLR max version:
```
wget http://dist.gem5.org/dist/develop/datasets/pannotia/bc/1k_128k.gr
docker run --rm -v ${PWD}:${PWD} -w ${PWD} -u $UID:$GID ghcr.io/gem5/gcn-gpu:latest gem5/build/VEGA_X86/gem5.opt gem5/configs/example/apu_se.py -n3 --mem-size=8GB --benchmark-root=gem5-resources/src/gpu/pannotia/clr/bin -c color_max.gem5 --options="1k_128k.gr 0"
```

Assuming gem5, pannotia (input graphs, see below), and gem5-resources are in your working directory.
To run the CLR maxmin version:
```
wget http://dist.gem5.org/dist/develop/datasets/pannotia/bc/1k_128k.gr
docker run --rm -v ${PWD}:${PWD} -w ${PWD} -u $UID:$GID ghcr.io/gem5/gcn-gpu:latest gem5/build/VEGA_X86/gem5.opt gem5/configs/example/apu_se.py -n3 --mem-size=8GB --benchmark-root=gem5-resources/src/gpu/pannotia/clr/bin -c color_maxmin.gem5 --options="1k_128k.gr 0"
```

Note that the datasets from the original Pannotia suite have been uploaded to: <http://dist.gem5.org/dist/develop/datasets/pannotia>.
We recommend you start with the 1k_128k.gr input (<http://dist.gem5.org/dist/develop/datasets/pannotia/bc/1k_128k.gr>), as this is the smallest input that can be run with CLR.
Note that 1k_128k is not designed for Color specifically though -- the above link has larger graphs designed to run with Color that you should consider using for larger experiments.

## Pre-built binary

SE mode:
<https://storage.googleapis.com/dist.gem5.org/dist/v24-0/test-progs/pannotia/color_max.gem5>
<https://storage.googleapis.com/dist.gem5.org/dist/v24-0/test-progs/pannotia/color_maxmin.gem5>
