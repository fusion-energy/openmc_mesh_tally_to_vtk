import os
from pathlib import Path

import numpy as np
import openmc
from openmc_mesh_tally_to_vtk import write_mesh_tally_to_vtk
import meshio


class TestWriteMeshTallyToVtk:
    def test_written_file_exists(self):

        os.system("rm vtk_file_from_openmc_mesh.vtk")

        # assumes you have a statepoint file from the OpenMC simulation
        statepoint = openmc.StatePoint("statepoint.3.h5")

        # assumes the statepoint file has a RegularMesh tally with a certain name
        my_tally = statepoint.get_tally(name="neutron_effective_dose_on_3D_mesh")

        # converts the tally result into a VTK file
        write_mesh_tally_to_vtk(
            tally=my_tally, filename="vtk_file_from_openmc_mesh.vtk"
        )

        assert Path("vtk_file_from_openmc_mesh.vtk").is_file()

    def test_written_file_contents(self):

        # assumes you have a statepoint file from the OpenMC simulation
        statepoint = openmc.StatePoint("statepoint.3.h5")

        # assumes the statepoint file has a RegularMesh tally with a certain name
        my_tally = statepoint.get_tally(name="neutron_effective_dose_on_3D_mesh")

        # converts the tally result into a VTK file
        write_mesh_tally_to_vtk(
            tally=my_tally, filename="vtk_file_from_openmc_mesh.vtk"
        )

        mesh = meshio.read("vtk_file_from_openmc_mesh.vtk")

        assert list(mesh.cell_data.keys()) == [
            "neutron_effective_dose_on_3D_mesh",
            "error_tag",
        ]
        assert isinstance(
            mesh.cell_data["neutron_effective_dose_on_3D_mesh"][0][0], float
        )
        assert mesh.cell_data["neutron_effective_dose_on_3D_mesh"][0].sum() > 0
