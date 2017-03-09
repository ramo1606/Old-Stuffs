#ifndef CONTROLMANAGER_H
#define CONTROLMANAGER_H

#include <vector>
#include "control.h"
#include "peripheral.h"

#define MAXPERIPHERALS 5

namespace Advanced2D
{
    /*Esta clase contiene todos los perifericos y controles permitiendo acceder a ellos*/
    class ControlManager{
        public:
            /*Constructor*/
            ControlManager();
            /*Destructor*/
            ~ControlManager();

            //estructura que sirve para mapear el control
            typedef struct{
                Peripheral *p;
                Peripheral::component_t comp;
            }change_t;

            /*Obtiene el change_t*/
            change_t get_change();

            /*agrega un control a la lista*/
            int add_control(Control *ctrl);
            /*Agrega un periferico a la lista*/
            int add_peripheral(Peripheral *periph);
            /*Obtiene un control a partir de number*/
            Control *get_control(int number);
            /*Obtiene un periferico a partir de number*/
            Peripheral *get_peripheral(int number);
            /**/
            void update();

        protected:
            std::vector<Control*> controls; //lista de controles
            std::vector<Control*>::iterator controls_iter; //iterador de la lista de controles
            std::vector<Peripheral*> peripherals; //lista de perifericos
            std::vector<Peripheral*>::iterator peripherals_iter; //iterador de la lista de perifericos
            int old_state[MAXPERIPHERALS]; //estados anteriores de los perifericos
    };
}; //namespace
#endif
