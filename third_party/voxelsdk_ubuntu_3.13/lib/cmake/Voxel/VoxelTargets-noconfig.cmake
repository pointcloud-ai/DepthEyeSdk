#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Voxel::voxel" for configuration ""
set_property(TARGET Voxel::voxel APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(Voxel::voxel PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libvoxel.so.0.6.7"
  IMPORTED_SONAME_NOCONFIG "libvoxel.so.34"
  )

list(APPEND _IMPORT_CHECK_TARGETS Voxel::voxel )
list(APPEND _IMPORT_CHECK_FILES_FOR_Voxel::voxel "${_IMPORT_PREFIX}/lib/libvoxel.so.0.6.7" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
