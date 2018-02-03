project(deptheye)

find_library(LIBUSB_LIBS  
  NAMES  usb 
  PATHS  /usr/local/lib  
)

add_library(${PROJECT_NAME} STATIC DepthEyeInterface.cpp)

install(
  TARGETS ${PROJECT_NAME}
  LIBRARY DESTINATION lib   
  ARCHIVE DESTINATION lib
)
             
IF(LINUX)
#  set(CPACK_COMPONENTS_ALL test)
#  set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "library test programs.")
ENDIF()
