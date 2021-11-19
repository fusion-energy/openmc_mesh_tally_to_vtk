import numpy as np
import vtk
import math
import openmc


def _get_mesh_from_tally(tally: openmc.Tally):
    """Extracts the mesh from a tally

    Args: the tally to extract the mesh from. Should have a MeshFilter as one
        of the filters.

    Returns: an openmc.RegularMesh object
    """

    if tally.contains_filter(openmc.MeshFilter):
        mesh_filter = tally.find_filter(filter_type=openmc.MeshFilter)
    else:
        msg = "Tally does not contain a MeshFilter"
        raise ValueError(msg)

    mesh = mesh_filter.mesh

    return mesh


def _replace_nans_with_zeros(list_of_numbers: list):
    """Replaces any NaN present in a list with 0.

    Args: a list of floats and which optionally contains NaNs

    Returns: a list of floats
    """

    for counter, i in enumerate(list_of_numbers):
        if math.isnan(i):
            list_of_numbers[counter] = 0.0
    return list_of_numbers


def _find_coords_of_mesh(mesh: openmc.RegularMesh):
    """Finds x, y, z coordinates of the voxels in a openmc.RegularMesh object.

    Args: the openmc.RegularMesh to find coordinates of.

    Returns: A tuple of three numpy.linspace arrays for x, y, z values
    """

    xs = np.linspace(mesh.lower_left[0], mesh.upper_right[0], mesh.dimension[0] + 1)
    ys = np.linspace(mesh.lower_left[1], mesh.upper_right[1], mesh.dimension[1] + 1)
    zs = np.linspace(mesh.lower_left[2], mesh.upper_right[2], mesh.dimension[2] + 1)

    return xs, ys, zs


def _write_vtk(
    xs,
    ys,
    zs,
    tally_data,
    filename: str,
    label: str = "made with openmc_mesh_tally_to_vtk",
    error_data=None,
):

    vtk_box = vtk.vtkRectilinearGrid()

    vtk_box.SetDimensions(len(xs), len(ys), len(zs))

    vtk_x_array = vtk.vtkDoubleArray()
    vtk_x_array.SetName("x-coords")
    vtk_x_array.SetArray(xs, len(xs), True)
    vtk_box.SetXCoordinates(vtk_x_array)

    vtk_y_array = vtk.vtkDoubleArray()
    vtk_y_array.SetName("y-coords")
    vtk_y_array.SetArray(ys, len(ys), True)
    vtk_box.SetYCoordinates(vtk_y_array)

    vtk_z_array = vtk.vtkDoubleArray()
    vtk_z_array.SetName("z-coords")
    vtk_z_array.SetArray(zs, len(zs), True)
    vtk_box.SetZCoordinates(vtk_z_array)

    tally = np.array(tally_data)
    tally_data = vtk.vtkDoubleArray()
    tally_data.SetName(label)
    print("tally.size", tally.size)
    print("tally", tally)
    tally_data.SetArray(tally, tally.size, True)

    if error_data is not None:
        error = np.array(error_data)
        error_data = vtk.vtkDoubleArray()
        error_data.SetName("error_tag")
        error_data.SetArray(error, error.size, True)

    vtk_box.GetCellData().AddArray(tally_data)
    if error_data is not None:
        vtk_box.GetCellData().AddArray(error_data)

    writer = vtk.vtkRectilinearGridWriter()

    writer.SetFileName(filename)

    writer.SetInputData(vtk_box)

    print("Writing %s" % filename)

    writer.Write()

    return filename
