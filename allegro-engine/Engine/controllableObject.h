#ifndef CONTROLLABLEOBJECT_H
#define CONTROLLABLEOBJECT_H

class ControllableObject{
    public:
        typedef int action_t;
        virtual void doAction(action_t action, int magnitude);
};
#endif

