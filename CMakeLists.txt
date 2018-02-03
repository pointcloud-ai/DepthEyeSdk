cmake_minimum_required (VERSION 2.8.13)
project (depth_eye)

#set(CMAKE_INCLUDE_CURRENT_DIR 1)
string(REPLACE "\n" "" SYSTEM_VERSION ${CMAKE_SYSTEM_VERSION})

string (REGEX REPLACE "^([0-9]+).*" "\\1"
  SYSTEM_MAJOR_VERSION "${SYSTEM_VERSION}")
string (REGEX REPLACE "^[0-9]+\\.([0-9]+).*" "\\1"
  SYSTEM_MINOR_VERSION "${SYSTEM_VERSION}")
string (REGEX REPLACE "^[0-9]+\\.[0-9]+\\.([0-9]+).*" "\\1"
  SYSTEM_PATCH_VERSION ${SYSTEM_VERSION})

message("CMAKE_SYSTEM_NAME = ${CMAKE_SYSTEM_NAME} VERSION=${SYSTEM_VERSION}(${SYSTEM_MAJOR_VERSION}-${SYSTEM_MINOR_VERSION}-${SYSTEM_PATCH_VERSION})") 
message("ARCH = ${CMAKE_SYSTEM_PROCESSOR}")
#set(CMAKE_SYSTEM_NAME "Linux")



if(CMAKE_SYSTEM_NAME STREQUAL "Linux")
  set(CMAKE_CXX_FLAGS  "-msse2 -pthread -std=c++11 -fPIC -ffast-math")
  set(COMMON_LIBS
    /usr/local/lib
    ./lib)

  if(SYSTEM_MAJOR_VERSION STREQUAL "3")
    set(COMMON_INCLUDE
      /usr/include/libusb-1.0
      ./include/
      ./third_party/voxelsdk_ubuntu_3.13/include/voxel-0.6.7)
    set(voxel ./third_party/voxelsdk_ubuntu_3.13/lib)
    message("use Voxel SDK ./third_party/voxelsdk_unbuntu_3.13/lib")
  else(SYSTEM_MAJOR_VERSION STREQUAL "4")
    set(COMMON_INCLUDE
      /usr/include/libusb-1.0
      ./include/
      ./third_party/voxelsdk_ubuntu_4.13/include/voxel-0.6.7)
    set(voxel ./third_party/voxelsdk_ubuntu_4.13/lib)
    message("use Voxel SDK ./third_party/voxelsdk_ubuntu_4.13/lib")
    #message(FATAL_ERROR "This project not support this VERSION=${SYSTEM_VERSION}")
  endif()
  
elseif(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
  set(CMAKE_CXX_FLAGS  "-msse2 -std=c++11 -fPIC -ffast-math")
  set(COMMON_LIBS
    /usr/local/lib
    ./lib)
  set(COMMON_INCLUDE
    /usr/include/libusb-1.0
    ./include/
    ./third_party/voxelsdk_osx/include/voxel-0.6.7/
  )
  set(voxel ./third_party/voxelsdk_osx/lib)
  message("use Voxel SDK ./third_party/voxelsdk_osx/lib")

elseif(CMAKE_SYSTEM_NAME STREQUAL "Android")
  set(CMAKE_CXX_FLAGS "-pthread -std=c++11 -fPIC -ffast-math")
  ADD_DEFINITIONS(-DANDROID)
  set(ANDROID_ABI armeabi-v7a)
  set(COMMON_INCLUDE
      ./include/
      ./third_party/voxelsdk_android_jni/include/
      ./third_party/voxelsdk_android_jni/include/libusb/
      ./third_party/voxelsdk_android_jni/include/voxel-0.6.7/)
  set(LIBUSB_DIR ./third_party/voxelsdk_android_jni/lib/libusb/)
  add_library(usb-1.0 SHARED IMPORTED)
  set_target_properties(usb-1.0 PROPERTIES IMPORTED_LOCATION ${LIBUSB_DIR}/${ANDROID_ABI}/libusb1.0.so)
  set(COMMON_LIBS 
      usb-1.0
      dl)
  set(voxel ./third_party/voxelsdk_android_jni/lib/)
  message("use Voxel SDK ./third_party/voxelsdk_android_jni/lib/")

else()
  message(FATAL_ERROR "This project not support platform:${CMAKE_SYSTEM_NAME}")
endif()

SET(BINDIR bin/)
SET(LIBDIR lib/)
SET(ARCDIR lib/)
SET(SHAREDIR share/)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/${ARCDIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/${LIBDIR})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/${BINDIR})

include_directories(${COMMON_INCLUDE})
link_directories("/usr/local/lib" ${COMMON_LIBS} ${voxel})

#### Packaging related information -- common to both platforms
set(CPACK_PACKAGE_NAME "Depth Eye SDK")
set(CPACK_PACKAGE_VERSION "0.1")
set(CPACK_PACKAGE_CONTACT "Developer@pointcloud.ai")
set(CPACK_COMPONENTS_GROUPING ALL_COMPONENTS_IN_ONE)
set(CPACK_PACKAGE_VENDOR "pointcloud.ai")
set(CPACK_SOURCE_GENERATOR "Developer")

add_subdirectory(src)
add_subdirectory(test)
