import numpy as np
import vtk
import math
import openmc


def write_mesh_tally_to_vtk(
    tally,
    filename: str = "vtk_file_from_openmc_mesh.vtk",
):

    if tally.contains_filter(openmc.MeshFilter):
        mesh_filter = tally.find_filter(filter_type=openmc.MeshFilter)
    else:
        msg = "Tally does not contain a MeshFilter"
        raise ValueError(msg)

    tally_label = tally.name
    mesh = mesh_filter.mesh

    xs = np.linspace(mesh.lower_left[0], mesh.upper_right[0], mesh.dimension[0] + 1)
    ys = np.linspace(mesh.lower_left[1], mesh.upper_right[1], mesh.dimension[1] + 1)
    zs = np.linspace(mesh.lower_left[2], mesh.upper_right[2], mesh.dimension[2] + 1)
    # tally = statepoint.get_tally(name=tally.name)

    print(tally.mean)

    tally_data = tally.mean[:, 0, 0]
    error_data = tally.std_dev[:, 0, 0]

    tally_data = tally_data.tolist()
    error_data = error_data.tolist()

    for content in [tally_data, error_data]:
        for counter, i in enumerate(content):
            if math.isnan(i):
                content[counter] = 0.0

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
    tally_data.SetName(tally_label)
    tally_data.SetArray(tally, tally.size, True)

    error = np.array(error_data)
    error_data = vtk.vtkDoubleArray()
    error_data.SetName("error_tag")
    error_data.SetArray(error, error.size, True)

    vtk_box.GetCellData().AddArray(tally_data)
    vtk_box.GetCellData().AddArray(error_data)

    writer = vtk.vtkRectilinearGridWriter()

    writer.SetFileName(filename)

    writer.SetInputData(vtk_box)

    print("Writing %s" % filename)

    writer.Write()
