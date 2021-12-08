
Convert an OpenMC mesh tally to a VTK file with optional unit conversion

# Installation

```python
pip install openmc-mesh-tally-to-vtk
```

# Python API Usage

The package can be used in conjunction with OpenMC to produce a VTK file of a ```openmc.RegularMesh``` tally.

The simplest example is to read in an OpenMC tally and write it out as a VTK file which can then be opened with programs like [Paraview](https://www.paraview.org).

```python
from openmc_mesh_tally_to_vtk import write_mesh_tally_to_vtk
import openmc

# assumes you have a statepoint file from the OpenMC simulation
statepoint = openmc.StatePoint('statepoint.3.h5')

# assumes the statepoint file has a RegularMesh tally with a certain name
my_tally = statepoint.get_tally(name='tally_on_regular_mesh')

# converts the tally result into a VTK file
write_mesh_tally_to_vtk(
    tally=my_tally,
    filename = "vtk_file_from_openmc_mesh.vtk",
)
```

# Acknowledge

This package is based on a [GitHub Gist by](https://gist.github.com/pshriwise/da30da3daf08594dddf1a58b9f10dcc8) by Patrick Shriwise
