
#ifndef VOXEL_EXPORT_H
#define VOXEL_EXPORT_H

#ifdef VOXEL_STATIC_DEFINE
#  define VOXEL_EXPORT
#  define VOXEL_NO_EXPORT
#else
#  ifndef VOXEL_EXPORT
#    ifdef voxel_EXPORTS
        /* We are building this library */
#      define VOXEL_EXPORT __attribute__((visibility("default")))
#    else
        /* We are using this library */
#      define VOXEL_EXPORT __attribute__((visibility("default")))
#    endif
#  endif

#  ifndef VOXEL_NO_EXPORT
#    define VOXEL_NO_EXPORT __attribute__((visibility("hidden")))
#  endif
#endif

#ifndef VOXEL_DEPRECATED
#  define VOXEL_DEPRECATED __attribute__ ((__deprecated__))
#endif

#ifndef VOXEL_DEPRECATED_EXPORT
#  define VOXEL_DEPRECATED_EXPORT VOXEL_EXPORT VOXEL_DEPRECATED
#endif

#ifndef VOXEL_DEPRECATED_NO_EXPORT
#  define VOXEL_DEPRECATED_NO_EXPORT VOXEL_NO_EXPORT VOXEL_DEPRECATED
#endif

#define DEFINE_NO_DEPRECATED 0
#if DEFINE_NO_DEPRECATED
# define VOXEL_NO_DEPRECATED
#endif

#endif
