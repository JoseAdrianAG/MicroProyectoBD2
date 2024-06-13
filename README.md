Primero clonamos este proyecto, podemos utilizar el comando:
git clone https://github.com/JoseAdrianAG/MicroProyectoBD2.git

Para poder utilizar la aplicacion, primero tendremos que instalar unas librerias. Las encontraras en el fichero Requirements.txt

Por ultimo en la linea 526, en la que esta "self.client = MongoClient('mongodb://192.168.0.17/') tendrás que cambiar la ip por la de tu dispositivo.

Ahora para que se pueda conectar a la base de datos de MongoDB tendrás que iniciar el servicio. Te dejo un video de como instalar el Servidor MongoDB https://www.youtube.com/watch?v=eKXIxSZrJfw

¡¡IMPORTANTE!! En el video nos indica que hay que desactivar la opción de no instalar MongoDB como servicio durante la instalación. Si hay que instalarlo como servicio, porque si no no funciona correctamente.

Por ultimo, ejecuta el codigo y crea tu propio usuario, haciendo click en "Registrar Jugador".
