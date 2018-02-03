/*
 * TI Voxel Lib component.
 *
 * Copyright (c) 2017.5.31 by liudao
 */

#ifndef VOXEL_FLYINGPIX_H
#define VOXEL_FLYINGPIX_H

#include "Filter.h"

#include <string.h>

namespace Voxel
{
  
/**
 * \addtogroup Flt
 * @{
 */

class  FlyingPixFilter: public Filter
{
protected:
  float _flyingThresh;

  FrameSize _size;

  template <typename T>
  bool _filter(const T *in, T *out);

  template <typename PhaseT, typename AmpT>
  bool _filter2(const FramePtr &in_p, FramePtr &out_p);

  virtual bool _filter(const FramePtr &in, FramePtr &out);

  virtual void _onSet(const FilterParameterPtr &f);
  
public:
  FlyingPixFilter(float flyingThresh = 100);
  
  virtual void reset();
  
  virtual ~FlyingPixFilter() {}

  // liudao add in 2017.06.13
  public:
     Vector<ByteType> m_frameIn;
     Vector<ByteType> m_frameNoFill;		// remove flying pix
     Vector<ByteType> m_frameOut;			// fill flying pix
};
/**
 * @}
 */

}
#endif // VOXEL_DARKPIX_H
