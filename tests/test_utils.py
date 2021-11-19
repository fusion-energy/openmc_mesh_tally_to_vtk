from openmc_mesh_tally_to_vtk.utils import (
    _get_mesh_from_tally,
    _replace_nans_with_zeros,
    _write_vtk,
)
import openmc
import numpy as np
import meshio
import os


class TestUtils:
    def test_get_mesh_from_tally(self):
        """checks that a openmc.RegularMesh object is returned by the
        get_mesh_from_tally function"""

        sp_2_batches = openmc.StatePoint("statepoint.2.h5")
        my_tally = sp_2_batches.get_tally(name="neutron_effective_dose_on_3D_mesh")

        my_mesh = _get_mesh_from_tally(my_tally)

        assert isinstance(my_mesh, openmc.RegularMesh)

    def test_replace_nans_with_zeros(self):
        """Checks that the _replace_nans_with_zeros successfully replaces NaN
        values with 0. values"""

        my_array = np.empty(3)
        my_array[:] = np.NaN
        my_array = my_array.tolist()

        replaced_arrany = _replace_nans_with_zeros(my_array)

        assert replaced_arrany == [0.0, 0.0, 0.0]

        my_array[1] = 2.0

        replaced_arrany = _replace_nans_with_zeros(my_array)

        assert replaced_arrany == [0.0, 2.0, 0.0]

        my_array[0] = 1
        my_array[2] = 3

        replaced_arrany = _replace_nans_with_zeros(my_array)

        assert replaced_arrany == [1.0, 2.0, 3.0]

    def test_write_vtk_without_error(self):
        """Checks that the values in the resulting VTK file are the same as
        the input data and checks error tag does not exist in the vtk file"""

        os.system("rm test_write_vtk")

        xs = np.linspace(0, 10, 3)
        ys = np.linspace(0, 10, 3)
        zs = np.linspace(0, 10, 3)

        # grid is 2*2*2 which is 8 voxels
        tally_data = [1.0] * 8
        filename = "test_write_vtk.vtk"
        label = "test_data"
        output_filename = _write_vtk(
            xs=xs,
            ys=ys,
            zs=zs,
            tally_data=tally_data,
            error_data=None,
            filename=filename,
            label=label,
        )

        assert output_filename == filename

        mesh = meshio.read("test_write_vtk.vtk")

        assert list(mesh.cell_data["test_data"][0]) == [1.0] * 8
        assert list(mesh.cell_data.keys()) == ["test_data"]

    def test_write_vtk_with_error(self):
        """Checks that the values in the resulting VTK file are the same as
        the input data and error and checks that both data and error tags
        exist in the vtk file"""

        os.system("rm test_write_vtk")

        xs = np.linspace(0, 10, 3)
        ys = np.linspace(0, 10, 3)
        zs = np.linspace(0, 10, 3)

        # grid is 2*2*2 which is 8 voxels
        tally_data = [1.0] * 8
        error_data = [2.0] * 8
        filename = "test_write_vtk.vtk"
        label = "test_data"
        output_filename = _write_vtk(
            xs=xs,
            ys=ys,
            zs=zs,
            tally_data=tally_data,
            error_data=error_data,
            filename=filename,
            label=label,
        )

        assert output_filename == filename

        mesh = meshio.read("test_write_vtk.vtk")

        assert list(mesh.cell_data["test_data"][0]) == [1.0] * 8
        assert list(mesh.cell_data["error_tag"][0]) == [2.0] * 8
        assert list(mesh.cell_data.keys()) == ["test_data", "error_tag"]
