#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Voxel::voxelpcl" for configuration ""
set_property(TARGET Voxel::voxelpcl APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(Voxel::voxelpcl PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_NOCONFIG "vtkImagingStencil;vtkCommonComputationalGeometry;vtkCommonDataModel;vtkCommonMath;vtkCommonCore;vtksys;vtkCommonMisc;vtkCommonSystem;vtkCommonTransforms;vtkImagingCore;vtkCommonExecutionModel;vtkFiltersAMR;vtkFiltersGeneral;vtkFiltersCore;vtkParallelCore;vtkIOLegacy;vtkIOCore;vtkInteractionWidgets;vtkFiltersHybrid;vtkImagingSources;vtkRenderingCore;vtkCommonColor;vtkFiltersExtraction;vtkFiltersStatistics;vtkImagingFourier;vtkalglib;vtkFiltersGeometry;vtkFiltersSources;vtkFiltersModeling;vtkImagingGeneral;vtkImagingHybrid;vtkIOImage;vtkDICOMParser;vtkmetaio;vtkInteractionStyle;vtkRenderingAnnotation;vtkImagingColor;vtkRenderingFreeType;vtkftgl;vtkRenderingVolume;vtkIOParallelNetCDF;vtkParallelMPI;vtkRenderingOpenGL;vtkIOLSDyna;vtkIOXML;vtkIOGeometry;vtkIOXMLParser;vtkLocalExample;vtkInfovisCore;vtkGeovisCore;vtkInfovisLayout;vtkViewsCore;vtkTestingGenericBridge;verdict;vtkIOMovie;vtkFiltersImaging;vtkIOMINC;vtkRenderingLOD;vtkViewsQt;vtkGUISupportQt;vtkViewsInfovis;vtkChartsCore;vtkRenderingContext2D;vtkRenderingLabel;vtkRenderingImage;vtkFiltersFlowPaths;vtkxdmf2;vtkFiltersReebGraph;vtkViewsContext2D;vtkIOXdmf2;vtkIOAMR;vtkRenderingContextOpenGL;vtkImagingStatistics;vtkIOParallel;vtkFiltersParallel;vtkIONetCDF;vtkexoIIc;vtkGUISupportQtOpenGL;vtkIOParallelLSDyna;vtkFiltersParallelGeometry;vtkGUISupportQtWebkit;vtkIOPLY;vtkFiltersHyperTree;vtkRenderingVolumeOpenGL;vtkIOExodus;vtkIOPostgreSQL;vtkIOSQL;vtkWrappingJava;vtkFiltersParallelFlowPaths;vtkFiltersParallelStatistics;vtkFiltersProgrammable;vtkFiltersParallelImaging;vtkRenderingParallelLIC;vtkRenderingLIC;vtkInteractionImage;vtkFiltersPython;vtkWrappingPythonCore;vtkIOParallelExodus;vtkFiltersGeneric;vtkIOVideo;vtkRenderingQt;vtkFiltersTexture;vtkIOInfovis;vtkGUISupportQtSQL;vtkRenderingFreeTypeOpenGL;vtkInfovisBoostGraphAlgorithms;vtkRenderingGL2PS;vtkIOGeoJSON;vtkFiltersVerdict;vtkViewsGeovis;vtkIOImport;vtkTestingIOSQL;vtkPythonInterpreter;vtkIOODBC;vtkIOEnSight;vtkIOMySQL;vtkRenderingMatplotlib;vtkDomainsChemistry;vtkIOExport;vtkFiltersParallelMPI;vtkIOParallelXML;vtkTestingRendering;vtkIOMPIParallel;vtkParallelMPI4Py;vtkFiltersSMP;vtkFiltersSelection;vtkIOVPIC;VPIC;vtkImagingMath;vtkImagingMorphological;vtkRenderingParallel;vtkRenderingFreeTypeFontConfig;vtkIOFFMPEG;vtkIOMPIImage;vtkIOGDAL"
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libvoxelpcl.so.0.6.7"
  IMPORTED_SONAME_NOCONFIG "libvoxelpcl.so.34"
  )

list(APPEND _IMPORT_CHECK_TARGETS Voxel::voxelpcl )
list(APPEND _IMPORT_CHECK_FILES_FOR_Voxel::voxelpcl "${_IMPORT_PREFIX}/lib/libvoxelpcl.so.0.6.7" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
