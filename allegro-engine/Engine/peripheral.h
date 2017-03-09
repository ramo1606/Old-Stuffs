#ifndef PERIPHERAL_H
#define PERIPHERAL_H

#include <string>
#define INVALID_STATE       -2
#define INVALID_COMPONENT   -2

/*Conoce el estado de los componentes*/
class Peripheral{
    public:
        /*Eventos que se van a manejar*/
        typedef enum event_t{
            NO_EVENT,
            ON_PRESS,
            ON_RELEASE,
            ON_PRESSING,
            ON_RELEASSING,
        }event_t;

        typedef int state_t; //estado de un componente
        typedef int component_t; //componente

        /*Constructor*/
        Peripheral();
        /*Obtiene el estado del componente comp*/
        virtual state_t get_state(component_t comp);
        /*obtiene un componente que cambio*/
        virtual component_t get_change();
        /*Obtiene el nombre del componente comp*/
        virtual std::string get_component_name(component_t comp);
        /*reset*/
        virtual void reset();
};
#endif
