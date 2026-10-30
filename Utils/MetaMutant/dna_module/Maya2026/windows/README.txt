Epic's dna Python module for Maya 2026 (Python 3.11, Windows x64), used by Meta Mutant.

Built from OpenRigLogic (MIT licence, LICENSE_OpenRigLogic.txt), https://github.com/EpicGames/OpenRigLogic
commit ea253d54dbcd005c139816ecc19c96a5dc0939de Fri Oct 23 14:00:54 2026 +0200
CMake (Visual Studio 2022, MSVC 14.44, Release, static libraries), SWIG 4.5.1, against
Maya 2026's Python 3.11.9 (include/Python311, lib/python311.lib):

    cmake -S . -B build -G "Visual Studio 17 2022" -A x64 -DRL_BUILD_PYTHON_WRAPPER=3.11.9
          -DPython3_EXECUTABLE=<Maya2026>/bin/mayapy.exe
          -DPython3_INCLUDE_DIR=<Maya2026>/include/Python311/Python
          -DPython3_LIBRARY=<Maya2026>/lib/python311.lib
    cmake --build build --config Release --target py3dna

Outputs: build/python/dna/dna.py and build/python/dna/Release/_py3dna13_5_2.pyd.
