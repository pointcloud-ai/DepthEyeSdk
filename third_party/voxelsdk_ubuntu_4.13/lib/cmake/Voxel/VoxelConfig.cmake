# - Config file for the FooBar package
# It defines the following variables
#  VOXEL_INCLUDE_DIRS - include directories for FooBar
#  VOXEL_LIBRARIES    - libraries to link against
 
# Compute paths
get_filename_component(VOXEL_CMAKE_DIR "${CMAKE_CURRENT_LIST_FILE}" PATH)

set(VOXEL_INCLUDE_DIRS ${VOXEL_CMAKE_DIR}/../../../include/voxel-0.6.7 /usr/include/libusb-1.0;Util/)

set(VOXEL_ABI_VERSION 34)
 
# Our library dependencies (contains definitions for IMPORTED targets)
if(NOT TARGET Voxel::voxel AND NOT Voxel_BINARY_DIR)
  include("${VOXEL_CMAKE_DIR}/VoxelTargets.cmake")
endif()
 
# These are IMPORTED targets created by FooBarTargets.cmake
set(VOXEL_LIBRARIES Voxel::voxel)
