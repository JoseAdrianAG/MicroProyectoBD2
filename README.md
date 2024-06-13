Primero clonamos este proyecto, podemos utilizar el comando:
git clone https://github.com/JoseAdrianAG/MicroProyectoBD2.git

Para poder utilizar la aplicacion, primero tendremos que instalar unas librerias. Las encontraras en el fichero Requirements.txt.
Podrás utilizar este comando para descargarlos: pip install -r requirements.txt

Por ultimo en la linea 526, en la que esta "self.client = MongoClient('mongodb://192.168.0.17/') tendrás que cambiar la ip por la de tu dispositivo.

Ahora para que se pueda conectar a la base de datos de MongoDB tendrás que iniciar el servicio. Entramos en MongoDB Compass y ponemos la IP y el puerto del servidor (en este caso, hemos utilizado localhost:27017).

Por ultimo, ejecuta el codigo y crea tu propio usuario, haciendo click en "Registrar Jugador".
