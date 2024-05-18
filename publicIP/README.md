# public IP

## Usar con Docker el servicio public IP que lo vamos a llamar Notifier

Nos ubicamos donde tenemos todos los archivos para la imagen. Una vez ahi adentro de la carpeta vamos a ejecutar un comando para compilar el Dockerfile y generar la imagen.

`sudo docker build -t notifier:prod --no-cache .`

Donde nuestro archivo Dockerfile tiene el siguiente contenido:
```Dockerfile
# Utiliza la imagen oficial de Python
FROM python:3.9-alpine

# Establece el directorio de trabajo dentro del contenedor
#WORKDIR /notifier

# Da permisos a la carpeta, e Instala la biblioteca "schedule
# requests y slack-webhook" usando pip
RUN chmod 777 /notifier; pip install schedule requests slack-webhook
#RUN pip install schedule requests slack-webhook

# Copia el script Python y los archivos necesarios
COPY sched_ip_public.py .
COPY config.json .

CMD ["python", "-u", "sched_ip_public.py"]
```

Para ver las imagenes localmente utilizamos `sudo docker image ls`.

Para borrar una imagen `sudo docker image rm <IMAGE ID> -f`

Podemos probar si funciona con el siguiente comando

`docker run --name notifierslack notifier:prod`

Para borrar un contenedor `docker rm <CONTAINER ID> -f`

Tambien podemos lanzarlo con un docker compose

notifier.yml
```yml
version: '3.1'

services:
  notifier:
    image: notifier:prod
    restart: always

```

`sudo docker compose -f notifier.yml  up -d`

