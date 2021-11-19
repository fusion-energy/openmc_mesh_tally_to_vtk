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
    include_std_dev: bool = True,
):
    """Writes a regular mesh tally to a VTK file. If required units are specified
    then the openmc_tally_unit_converter package will attempt to convert the tally
    values into the required units.

    Args:
        tally:
        filename: the filename of the vtk produced.
        required_units: units to convert the tally results into.
        source_strength: particles per second or particles per pulse which can
            also be provided to assist with unit conversion.
        include_std_dev: controls whether the std dev of the tally is written
            to the vtk file. Assuming std dev data is present then it will be
            written to the vtk file by default. This option allows std dev to
            not be written to the vtk file which can help reduce the file size
            of the vtk file.

    Returns: The filename of the vtk file produced
    """

    if required_units is None:
        tally_data = tally.mean[:, 0, 0]
        tally_data = tally_data.tolist()
        tally_data = _replace_nans_with_zeros(tally_data)
        if include_std_dev:
            error_data = tally.std_dev[:, 0, 0]
            # if std_dev is all nan values then batches was 1 and there is no need
            # to add this to the vtk
            if np.isnan(error_data).all():
                error_data = None
            else:
                error_data = error_data.tolist()
                error_data = _replace_nans_with_zeros(error_data)
        else:
            error_data = None
    else:
        tally_data, error_data = otuc.process_tally(
            tally, required_units=required_units, source_strength=source_strength
        )

    mesh = _get_mesh_from_tally(tally)

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
