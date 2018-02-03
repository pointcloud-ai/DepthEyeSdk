#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Voxel::ti3dtof" for configuration ""
set_property(TARGET Voxel::ti3dtof APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(Voxel::ti3dtof PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libti3dtof.so.0.6.7"
  IMPORTED_SONAME_NOCONFIG "libti3dtof.so.34"
  )

list(APPEND _IMPORT_CHECK_TARGETS Voxel::ti3dtof )
list(APPEND _IMPORT_CHECK_FILES_FOR_Voxel::ti3dtof "${_IMPORT_PREFIX}/lib/libti3dtof.so.0.6.7" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
