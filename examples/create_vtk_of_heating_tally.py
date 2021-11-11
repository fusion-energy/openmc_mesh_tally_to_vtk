from openmc_mesh_tally_to_vtk import write_mesh_tally_to_vtk
import openmc


# loads in the statepoint file containing tallies
statepoint = openmc.StatePoint(filepath="statepoint.2.h5")
my_tally = statepoint.get_tally(name="heating_on_3D_mesh")


write_mesh_tally_to_vtk(
    tally=my_tally,
    # required_units= TODO add openmc-post-processor
)
