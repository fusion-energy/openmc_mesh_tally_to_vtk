
from openmc_mesh_tally_to_vtk import write_mesh_tally_to_vtk
import openmc

# assumes you have a statepoint file from the OpenMC simulation
statepoint = openmc.StatePoint('statepoint.3.h5')

# assumes the statepoint file has a RegularMesh tally with a certain name
my_tally = statepoint.get_tally(name='heating_on_3D_mesh')


# the simplest creation of a vtk file with no unit conversion
write_mesh_tally_to_vtk(
    tally=my_tally,
    filename= "heating_tally_in_base_units.vtk",
)

# scaling the units from the base units of eV per source particle to joules per source particle
write_mesh_tally_to_vtk(
    tally=my_tally,
    filename= "heating_tally_in_joules.vtk",
    required_units= 'joules / source_particle',
)


# scaling eV to joules as before but also converting joules to watts. To do this source strength is needed
write_mesh_tally_to_vtk(
    tally=my_tally,
    filename= "heating_tally_in_watts.vtk",
    required_units= 'watts',
    source_strength=1e20,  # in units of neutrons per second
)

# scaling as before but requesting per unit volume (/cm3) as well, the voxel volume is found automatically from the mesh
write_mesh_tally_to_vtk(
    tally=my_tally,
    filename= "heating_tally_in_watts_per_cm3.vtk",
    required_units= 'watts / cm**3',
    source_strength=1e20,  # in units of neutrons per second
)
