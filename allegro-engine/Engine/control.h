#ifndef CONTROL_H
#define CONTROL_H

#include <list>
#include <string>
#include "peripheral.h"
#include "controllableObject.h"

/*Esta clase conoce todas las asociaciones (accion, periferico, componente y nombre) y permite que otras
 *clases agreguen nuevas asociaciones, permite establecer a que objeto pertenece el mismo, revisa todas las
 *asociaciones y envia las acciones al objeto que es dueño del control
 */
class Control{
    public:
        /*Esta es la estructura de una asociacion*/
        typedef struct{
            ControllableObject::action_t act; //accion
            std::string name; //nombre
            Peripheral *peri; //periferico
            Peripheral::component_t comp; //componente
            Peripheral::event_t old_event; //evento anterior
            Peripheral::event_t event; //evento actual
        }association_t;

        /*Agrega una accion y un nombre descriptivo*/
        void add_action_name(ControllableObject::action_t act, std::string str);
        /*Agrega una asociacion*/
        void add_association(association_t asoc);

        /**/
        void set_actionperipheral(ControllableObject::action_t act, Peripheral* peri, Peripheral::component_t comp,
        Peripheral::event_t e);

        /*Establece a que objeto se le enviaran las acciones del control*/
        void set_owner(ControllableObject*);
        /*recorre todas las asociaciones para ver si hay que enviar una accion*/
        void update();
        /*retorna el nombre de una accion*/
        std::string get_name_action(ControllableObject::action_t);
        void reset();

    protected:
        ControllableObject *owner; //objeto que recibira las acciones
        std::list<association_t> associations; //lista de asociaciones
        std::list<association_t>::iterator associations_iter; //iterador de la lista
};
#endif

