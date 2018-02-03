project(DepthEyeH1Sample)

find_library(LIBUSB_LIBS  
  NAMES  usb 
  PATHS  /usr/local/lib  
)

#add_executable(${PROJECT_NAME} DepthEyeH1Sample.cpp)
#target_link_libraries(${PROJECT_NAME} voxel deptheye)

add_executable(H1AsciiSample H1AsciiSample.cpp)
target_link_libraries(H1AsciiSample voxel deptheye)

#install(TARGETS
#  DepthEyeH1Sample
#  RUNTIME DESTINATION bin
#  COMPONENT test
#)
             
IF(LINUX)
  set(CPACK_COMPONENTS_ALL test)
  set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "library test programs.")
ENDIF()
