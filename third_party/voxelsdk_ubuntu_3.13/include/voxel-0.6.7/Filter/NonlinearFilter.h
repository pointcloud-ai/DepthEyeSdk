//
//  NonlinearFilter.hpp
//  Voxel
//
//  Created by 席齐 on 2017/7/26.
//
//

#ifndef NonlinearFilter_hpp
#define NonlinearFilter_hpp
#include "Filter.h"
#include <stdio.h>
#define LIGHT_SPEED 299792458.0
namespace Voxel
{
    
    /**
     * \addtogroup Flt
     * @{
     */
    
    class VOXEL_EXPORT NonlinearFilter : public Filter
    {
    protected:
        float _modFreq;
        Vector<ByteType> _current;
        
        FrameSize _size;
        
        template <typename T>
        bool _filter(const T *in, T *out);
        
        virtual bool _filter(const FramePtr &in, FramePtr &out);
        
        virtual void _onSet(const FilterParameterPtr &f);
        
    public:
        NonlinearFilter(float frequce = 36);
        
        virtual void reset();
        
        virtual ~NonlinearFilter() {}
        float scaleFactor;
        static float phase2distance[];
        static int *nonlinearPhase;
        static int mapArraySize;
    };
    /**
     * @}
     */
    
}

#endif /* NonlinearFilter_hpp */
