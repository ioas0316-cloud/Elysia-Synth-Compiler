#!/bin/bash
set -e

# Compile the C++ native kernel into a shared library
echo "Compiling phase_kernel.cpp..."
mkdir -p lib
g++ -O3 -shared -fPIC -o lib/phase_kernel.so src/phase_kernel.cpp
echo "Compilation complete: lib/phase_kernel.so generated."
