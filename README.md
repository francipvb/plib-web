# Plib Web

Este es el repositorio para el proyecto de la web del partido libertario.

Las commits están escritas en inglés, así como el código. Solo el material visual, como este _README_ lo tengo escrito en español, es mas por comodidad que otra cosa.

## Herramientas utilizadas

- [Poetry][poetry]: Para el manejo de las dependencias.
- [Pytest][pytest]: Para pruebas unitarias (de momento no hay).
- [Whitenoise][whitenoise]: Para servir la aplicación, el mecanismo estándar de django no sirve muy bien a ese propósito.
- [Django][django]: Para todo lo relativo al backend.
- [Django Rest Framework][drf]: Para desarrollar la _API_.
- [Django storages][storages]: Para cargar los archivos a la nuve, depende de algunas librerías de terceros.

## Despliegue en contenedor

Por ahora solo hay un dockerfile, pero funciona bien. Agregar un archivo para desplegar a swarm debería ser trivial.

## Base de datos

El proyecto emplea una librería que lee la mayor parte de la configuración desde variables de entorno, por lo que no es problema el cambio de entorno.

## Problemas y preguntas

Cualquier problema o inquietud, cargarlo mediante la pestaña de issues.

[poetry]: https://python-poetry.org/ "Poetry python dependency management"
[pytest]: https://pytest.org/ "Pytest test framework"
[whitenoise]: http://whitenoise.evans.io/
[django]: https://djangoproject.com/ "The web framework for perfectionists"
[drf]: https://www.django-rest-framework.org/
[storages]: https://django-storages.readthedocs.io/ "File storage backends for django"
