import numpy as np
import openmc_tally_unit_converter as otuc

from .utils import (
    _get_mesh_from_tally,
    _replace_nans_with_zeros,
    _write_vtk,
    _find_coords_of_mesh,
)

# def write_effective_dose_mesh_tally_to_vtk(
# todo add specific converters for dose
# ):

# def write_dpa_mesh_tally_to_vtk(
# todo add specific converters for dpa
# ):


def write_mesh_tally_to_vtk(
    tally,
    filename: str = "vtk_file_from_openmc_mesh.vtk",
    required_units: str = None,
    source_strength: float = None,
):

    if required_units is None:
        tally_data = tally.mean[:, 0, 0]
        error_data = tally.std_dev[:, 0, 0]
    else:
        tally_data = otuc.process_tally(
            tally, required_units=required_units, source_strength=source_strength
        )

    tally_data = tally_data.tolist()
    error_data = error_data.tolist()

    mesh = _get_mesh_from_tally(tally)
    tally_data = _replace_nans_with_zeros(tally_data)
    print(tally_data)
    error_data = _replace_nans_with_zeros(error_data)
    xs, ys, zs = _find_coords_of_mesh(mesh)

    output_filename = _write_vtk(
        xs=xs,
        ys=ys,
        zs=zs,
        tally_data=tally_data,
        error_data=error_data,
        filename=filename,
        label=tally.name,
    )

    return output_filename
