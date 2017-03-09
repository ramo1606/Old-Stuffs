#ifndef CONTROLLABLEACTOR_H
#define CONTROLLABLEACTOR_H

#include "advanced2d.h"
#include "actor.h"
#include "controllableObject.h"

namespace Advanced2D
{
    class ControllableActor : public Actor, public ControllableObject
    {
        public:
            ControllableActor(){}
    };
}; //namespace
#endif

