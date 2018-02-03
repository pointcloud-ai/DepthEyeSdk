
#ifndef TI3DTOF_EXPORT_H
#define TI3DTOF_EXPORT_H

#ifdef TI3DTOF_STATIC_DEFINE
#  define TI3DTOF_EXPORT
#  define TI3DTOF_NO_EXPORT
#else
#  ifndef TI3DTOF_EXPORT
#    ifdef ti3dtof_EXPORTS
        /* We are building this library */
#      define TI3DTOF_EXPORT __attribute__((visibility("default")))
#    else
        /* We are using this library */
#      define TI3DTOF_EXPORT __attribute__((visibility("default")))
#    endif
#  endif

#  ifndef TI3DTOF_NO_EXPORT
#    define TI3DTOF_NO_EXPORT __attribute__((visibility("hidden")))
#  endif
#endif

#ifndef TI3DTOF_DEPRECATED
#  define TI3DTOF_DEPRECATED __attribute__ ((__deprecated__))
#endif

#ifndef TI3DTOF_DEPRECATED_EXPORT
#  define TI3DTOF_DEPRECATED_EXPORT TI3DTOF_EXPORT TI3DTOF_DEPRECATED
#endif

#ifndef TI3DTOF_DEPRECATED_NO_EXPORT
#  define TI3DTOF_DEPRECATED_NO_EXPORT TI3DTOF_NO_EXPORT TI3DTOF_DEPRECATED
#endif

#define DEFINE_NO_DEPRECATED 0
#if DEFINE_NO_DEPRECATED
# define TI3DTOF_NO_DEPRECATED
#endif

#endif
