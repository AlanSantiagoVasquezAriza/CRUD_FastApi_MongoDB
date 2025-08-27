# Mascotas FastAPI

## Descripción

Esta es una API RESTful construida con FastAPI para gestionar información sobre dueños de mascotas y sus mascotas. La aplicación permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) tanto para los dueños como para las mascotas, utilizando MongoDB como base de datos.

## Características

- Gestión de dueños de mascotas:
  - Crear, leer, actualizar y eliminar dueños.
- Gestión de mascotas:
  - Crear, leer, actualizar y eliminar mascotas.
- Relación entre dueños y mascotas.

## Tecnologías Utilizadas

- **FastAPI**: Framework para construir APIs en Python.
- **MongoDB**: Base de datos NoSQL para almacenar la información.
- **Pydantic**: Para la validación de datos.
- **Uvicorn**: Servidor ASGI para ejecutar la aplicación.

## Requisitos

- Python 3.7 o superior
- MongoDB instalado y en ejecución
- Dependencias de Python:
  - fastapi
  - pymongo
  - uvicorn
  - pydantic

## Instalación

1. Clona este repositorio:

```
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_REPOSITORIO>
```

2. Crea un entorno virtual y actívalo:

python -m venv env
source env/bin/activate  # En Windows usa `env\Scripts\activate`

3. Instala las dependencias:

pip install requirements.txt

4. Asegúrate de que MongoDB esté en ejecución. Puedes iniciar MongoDB con el siguiente comando:

mongod

## Ejecución

Para ejecutar la aplicación, utiliza el siguiente comando:

uvicorn main:app --reload --port 3000

## Endpoints

### Dueño
- **GET /dueños:** Obtiene la lista de todos los dueños.
- **GET /dueños/{dueño_id}:** Obtiene un dueño específico por su ID.
- **POST /dueños:** Crea un nuevo dueño.
- **PUT /dueños/{dueño_id}:** Actualiza un dueño existente.
- **DELETE /dueños/{dueño_id}:** Elimina un dueño.
### Mascotas
- **GET /mascotas:** Obtiene la lista de todas las mascotas.
- **GET /mascotas/{mascota_id}:** Obtiene una mascota específica por su ID.
- **POST /mascotas:** Crea una nueva mascota.
- **PUT /mascotas/{mascota_id}:** Actualiza una mascota existente.
- **DELETE /mascotas/{mascota_id}:** Elimina una mascota.

## Estructura de la Base de Datos

La base de datos Mascotas contiene dos colecciones:

1. **dueños**:

- **Estructura**:
    - **_id**: ObjectId (generado automáticamente por MongoDB)
    - **nombre**: String (nombre del dueño)
    - **telefono**: String (número de teléfono del dueño, opcional)
    - **direccion**: String (dirección del dueño, opcional)

2. **mascotas**:

- **Estructura**:
    - **_id**: ObjectId (generado automáticamente por MongoDB)
    - **id_dueño**: String (ID del dueño, referencia al dueño)
    - **nombre**: String (nombre de la mascota)
    - **edad**: Integer (edad de la mascota)
    - **tipo**: String (tipo de mascota, e.g., perro, gato)