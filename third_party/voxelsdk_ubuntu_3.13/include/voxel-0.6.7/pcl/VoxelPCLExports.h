
#ifndef VOXELPCL_EXPORT_H
#define VOXELPCL_EXPORT_H

#ifdef VOXELPCL_STATIC_DEFINE
#  define VOXELPCL_EXPORT
#  define VOXELPCL_NO_EXPORT
#else
#  ifndef VOXELPCL_EXPORT
#    ifdef voxelpcl_EXPORTS
        /* We are building this library */
#      define VOXELPCL_EXPORT __attribute__((visibility("default")))
#    else
        /* We are using this library */
#      define VOXELPCL_EXPORT __attribute__((visibility("default")))
#    endif
#  endif

#  ifndef VOXELPCL_NO_EXPORT
#    define VOXELPCL_NO_EXPORT __attribute__((visibility("hidden")))
#  endif
#endif

#ifndef VOXELPCL_DEPRECATED
#  define VOXELPCL_DEPRECATED __attribute__ ((__deprecated__))
#endif

#ifndef VOXELPCL_DEPRECATED_EXPORT
#  define VOXELPCL_DEPRECATED_EXPORT VOXELPCL_EXPORT VOXELPCL_DEPRECATED
#endif

#ifndef VOXELPCL_DEPRECATED_NO_EXPORT
#  define VOXELPCL_DEPRECATED_NO_EXPORT VOXELPCL_NO_EXPORT VOXELPCL_DEPRECATED
#endif

#define DEFINE_NO_DEPRECATED 0
#if DEFINE_NO_DEPRECATED
# define VOXELPCL_NO_DEPRECATED
#endif

#endif
