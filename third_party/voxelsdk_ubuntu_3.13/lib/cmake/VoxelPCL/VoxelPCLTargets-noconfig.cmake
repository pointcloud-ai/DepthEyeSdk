#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Voxel::voxelpcl" for configuration ""
set_property(TARGET Voxel::voxelpcl APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(Voxel::voxelpcl PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_NOCONFIG "vtkCommon;vtkFiltering;vtkImaging;vtkGraphics;vtkGenericFiltering;vtkIO;vtkRendering;vtkVolumeRendering;vtkHybrid;vtkWidgets;vtkParallel;vtkInfovis;vtkGeovis;vtkViews;vtkCharts"
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libvoxelpcl.so.0.6.7"
  IMPORTED_SONAME_NOCONFIG "libvoxelpcl.so.34"
  )

list(APPEND _IMPORT_CHECK_TARGETS Voxel::voxelpcl )
list(APPEND _IMPORT_CHECK_FILES_FOR_Voxel::voxelpcl "${_IMPORT_PREFIX}/lib/libvoxelpcl.so.0.6.7" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
