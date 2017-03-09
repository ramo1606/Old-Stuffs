#ifndef AUDIOMANAGER_H
#define AUDIOMANAGER_H

#include "advanced2d.h"

#include <vector>
#include <string>

namespace Advanced2D
{
    class Sample
    {
        private:
            std::string name;

        public:
            FMOD_SOUND *sample;
            FMOD_CHANNEL *channel;

        public:
            Sample(void);
            ~Sample(void);

            std::string getName() { return name; }
            void setName(std::string value) { name = value; }
    };


    class AudioManager
    {
        public:
            AudioManager();
            virtual ~AudioManager();

            /*Inicializa el sistema*/
            bool init();
            /*Actualiza el sistema de audio*/
            void update(); //must be called once per frame
            /*Carga un sonido y lo agrega a la lista de sonidos*/
            bool load(std::string filename, std::string name);
            /*Carga un sonido independiente*/
            Sample* load(std::string filename);
            /*Reproduce el sonido name*/
            bool play(std::string name);
            /*Reproduce un sonido independiente*/
            bool play(Sample *sample);
            /*Detiene la reproduccion del sonido name*/
            void stop(std::string name);
            /*Detiene la reproduccion de todos los sonidos de la lista*/
            void stopAll();
            /*Detiene la reproduccion de todos los sonidos de la lista menos name*/
            void stopAllExcept(std::string name);
            /*Indica si el sonido play esta en reproduccion*/
            bool isPlaying(std::string name);
            /*Indica si el sonido name esta en la lista*/
            bool sampleExists(std::string name);
            /*Busca el sonido name en la lista y lo devuelve*/
            Sample *findSample(std::string name);

        protected:
        private:
            FMOD_SYSTEM *system;
            typedef std::vector<Sample*> Samples;
            typedef std::vector<Sample*>::iterator Iterator;
            Samples samples;
    };

};

#endif // AUDIOMANAGER_H
