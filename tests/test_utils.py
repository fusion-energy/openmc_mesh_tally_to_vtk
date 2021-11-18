from openmc_mesh_tally_to_vtk.utils import (
    _get_mesh_from_tally,
    _replace_nans_with_zeros,
    _write_vtk,
)
import openmc
import numpy as np
import meshio


class TestUtils:
    def test_get_mesh_from_tally(self):

        sp = openmc.StatePoint("statepoint.3.h5")
        my_tally = sp.get_tally(name="neutron_effective_dose_on_3D_mesh")
        print(sp.tallies)

        my_mesh = _get_mesh_from_tally(my_tally)

        assert isinstance(my_mesh, openmc.RegularMesh)

    def test_replace_nans_with_zeros(self):

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

    def test_write_vtk(self):

        xs = np.linspace(0, 10, 3)
        ys = np.linspace(0, 10, 3)
        zs = np.linspace(0, 10, 3)

        # grid is 2*2*2 which is 8 voxels
        tally_data = [1.0] * 8
        error_data = None
        filename = "test_write_vtk.vtk"
        label = "test_data"
        output_filename = _write_vtk(
            xs=xs,
            ys=ys,
            zs=zs,
            tally_data=tally_data,
            error_data=tally_data,
            filename=filename,
            label=label,
        )

        assert output_filename == filename

        mesh = meshio.read("test_write_vtk.vtk")

        # not sure why but 8 items are needed here
        assert list(mesh.cell_data["test_data"][0]) == [1.0] * 8
        assert list(mesh.cell_data.keys()) == ["test_data", "error_tag"]
