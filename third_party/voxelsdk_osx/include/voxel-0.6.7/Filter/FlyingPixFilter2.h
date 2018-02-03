/*
 * TI Voxel Lib component.
 *
 * Copyright (c) 2017.6.1 by liudao
 * method: remove jump point
 */

#ifndef VOXEL_FLYINGPIX2_H
#define VOXEL_FLYINGPIX2_H

#include "Filter.h"

#include <string.h>

namespace Voxel
{
  
/**
 * \addtogroup Flt
 * @{
 */

class VOXEL_EXPORT FlyingPixFilter2: public Filter
{
protected:
  uint _phaseDiffTh;		// phase差值阈值
  uint _greaterNum;		// 邻域内大于给定值的元素个数

  FrameSize _size;

  template <typename T>
  bool _filter(const T *in, T *out);

  template <typename PhaseT, typename AmpT>
  bool _filter2(const FramePtr &in_p, FramePtr &out_p);

  virtual bool _filter(const FramePtr &in, FramePtr &out);

  virtual void _onSet(const FilterParameterPtr &f);
  
public:
  FlyingPixFilter2(uint nPhasediffth=10, uint nGreaterNum=4);
  
  virtual void reset();
  
  virtual ~FlyingPixFilter2() {}
};
/**
 * @}
 */

}
#endif // VOXEL_DARKPIX_H
