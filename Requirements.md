Para utilizar la aplicación, primero se necesita instalar algunas librerias librerias con estos comandos:

pip install tk

pip install pymongo

Despues en el codigo de python se importarian asi (ya estan importados en este codigo):

import tkinter as tk
import tkinter.simpledialog as simpledialog
form tkinter import ttk, messagebox
from pymongo import MongoClient, errors

Por ultimo en la linea 389, en la que esta "self.client = MongoClient('mongodb://192.168.200.144/')
tendrás que cambiar la ip por la de dispositivo.

Ahora para que se pueda conectar a la base de datos de MongoDB tendrás que iniciar el servicio
Te dejo un video de como instalar el Servidor MongoDB
https://www.youtube.com/watch?v=eKXIxSZrJfw

¡¡IMPORTANTE!!
En el video nos indica que hay que desactivar la opción de no instalar MongoDB como servicio durante la instalación. Si hay que instalarlo como servicio, porque si no no funciona correctamente



