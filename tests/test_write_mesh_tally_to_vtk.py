import os
from pathlib import Path

import numpy as np
import openmc
from openmc_mesh_tally_to_vtk import write_mesh_tally_to_vtk
import meshio
import unittest


class TestWriteMeshTallyToVtk(unittest.TestCase):
    def setUp(self):

        statepoint = openmc.StatePoint("statepoint.1.h5")
        self.my_tally_1_batches = statepoint.get_tally(
            name="neutron_effective_dose_on_3D_mesh"
        )

        statepoint = openmc.StatePoint("statepoint.2.h5")
        self.my_tally_2_batches = statepoint.get_tally(
            name="neutron_effective_dose_on_3D_mesh"
        )

    def test_written_file_exists_2_batches(self):

        os.system("rm vtk_file_from_openmc_mesh.vtk")

        # converts the tally result into a VTK file
        write_mesh_tally_to_vtk(
            tally=self.my_tally_2_batches, filename="vtk_file_from_openmc_mesh.vtk"
        )

        assert Path("vtk_file_from_openmc_mesh.vtk").is_file()

    def test_written_file_exists_1_batches(self):

        os.system("rm vtk_file_from_openmc_mesh.vtk")

        # converts the tally result into a VTK file
        write_mesh_tally_to_vtk(
            tally=self.my_tally_1_batches, filename="vtk_file_from_openmc_mesh.vtk"
        )

        assert Path("vtk_file_from_openmc_mesh.vtk").is_file()

    def test_written_file_contents_2_batches(self):

        os.system("rm vtk_file_from_openmc_mesh_2_batches.vtk")

        # converts the tally result into a VTK file
        write_mesh_tally_to_vtk(
            tally=self.my_tally_2_batches,
            filename="vtk_file_from_openmc_mesh_2_batches.vtk",
        )

        mesh = meshio.read("vtk_file_from_openmc_mesh_2_batches.vtk")

        assert list(mesh.cell_data.keys()) == [
            "neutron_effective_dose_on_3D_mesh",
            "error_tag",
        ]
        assert isinstance(
            mesh.cell_data["neutron_effective_dose_on_3D_mesh"][0][0], float
        )
        assert mesh.cell_data["neutron_effective_dose_on_3D_mesh"][0].sum() > 0

    def test_written_file_contents_1_batches(self):

        os.system("rm vtk_file_from_openmc_mesh_1_batches.vtk")

        # converts the tally result into a VTK file
        write_mesh_tally_to_vtk(
            tally=self.my_tally_1_batches,
            filename="vtk_file_from_openmc_mesh_1_batches.vtk",
        )

        mesh = meshio.read("vtk_file_from_openmc_mesh_1_batches.vtk")

        assert list(mesh.cell_data.keys()) == ["neutron_effective_dose_on_3D_mesh"]
        assert isinstance(
            mesh.cell_data["neutron_effective_dose_on_3D_mesh"][0][0], float
        )
        assert mesh.cell_data["neutron_effective_dose_on_3D_mesh"][0].sum() > 0

    def test_written_file_contents_2_batches_but_not_including_std_dev(self):

        os.system("rm vtk_file_from_openmc_mesh_2_batches.vtk")

        # converts the tally result into a VTK file
        write_mesh_tally_to_vtk(
            tally=self.my_tally_2_batches,
            filename="vtk_file_from_openmc_mesh_2_batches.vtk",
            include_std_dev=False,
        )

        mesh = meshio.read("vtk_file_from_openmc_mesh_2_batches.vtk")

        assert list(mesh.cell_data.keys()) == [
            "neutron_effective_dose_on_3D_mesh",
        ]
        assert isinstance(
            mesh.cell_data["neutron_effective_dose_on_3D_mesh"][0][0], float
        )
        assert mesh.cell_data["neutron_effective_dose_on_3D_mesh"][0].sum() > 0
