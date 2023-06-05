# TeachMePlay

TeachMePlay es una aplicación web desarrollada como trabajo de fin de grado de Ingeniería Informática en la Universidad de Burgos.

Se trata de un repositorio de juegos docentes que brinda a los usuarios la posibilidad de buscar, filtrar, valorar y contribuir con juegos. 
Su principal objetivo es facilitar la visualización e interacción con una amplia variedad de juegos docentes relevantes para la enseñanza en diferentes materias.
El proyecto se ha desarrollado utilizando principalmente las siguientes herramientas: Python, PostgreSQL, Visual Studio Code, HTML, CSS y Bootstrap.
Al contar con una base de datos centralizada, se simplifica la gestión y organización de los juegos entre los docentes. 
Además, a través de sistemas de puntuación e interacción, los usuarios pueden realizar búsquedas adaptadas a sus intereses y preferencias.

## Instalación en local
Para utilizar la aplicación de forma local, es necesario hacer uso de un entorno virtual e instalar 
todas las librerías necesarias disponibles en el archivo requirements.txt.
Además, se debe disponer del archivo .env que contiene las variables de entorno necesarias 
para la conexión a la base de datos.

Para la creación del entorno virtual y su activación se deben ejecutar los siguientes comandos respectivamente:

bash
$ python -m venv env

bash
$ env\Scripts\activate

Las librerías de Python se deben instalar de la siguiente forma:

bash
$ pip install [librería]

Y finalmente para ejecutar el proyecto se debe ejcutar el comando:
bash
$ flask run

## Aplicación desplegada
Tanto la aplicación como la base de datos se encuentran desplegadas en Heroku. 
Para visualizar la página web, simplemente se debe acceder al siguiente enlace: https://teachmeplay.herokuapp.com/ 
