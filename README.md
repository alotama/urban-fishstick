# Introducción

Este documento describe la arquitectura y los componentes del sistema, incluyendo un diagrama de arquitectura que ilustra la interacción entre los diferentes componentes. 

## Configuración del proyecto

Asegúrate de tener el archivo de configuración config.json en el directorio config/. Este archivo debe contener las claves necesarias para la configuración del proyecto, como env_encryption_key y env_JWT_SECRET_KEY.

```json
{
    "env_encryption_key": "TU_CLAVE_DE_CIFRADO",
    "env_JWT_SECRET_KEY": "TU_CLAVE_SECRETA_JWT",
    "default_limits": "60 per minute"
}
```

## Ejecutar la Aplicación

Para ejecutar la aplicación en modo desarrollo, utiliza el siguiente comando:

```
python app.py
```

La aplicación estará disponible en http://127.0.0.1:5000.

## Endpoints Disponibles

### POST /login

- **Descripción:** Autentica a un usuario mediante credenciales.
- **Ruta:** `routes/login.py`
- **Parámetros:**
  - `username`: Nombre de usuario.
  - `password`: Contraseña del usuario.
- **Respuesta:**
  - `200 OK`: Devuelve un token JWT si la autenticación es exitosa.
  - `401 Unauthorized`: Si las credenciales son incorrectas.

### POST /areCompromisedNames

- **Descripción:** Compara una lista de nombres para determinar si están comprometidos.
- **Ruta:** `routes/areCompromisedNames.py`
- **Parámetros:**
  - `names`: Lista de nombres a comparar.
- **Respuesta:**
  - `200 OK`: Devuelve los nombres comprometidos.
  - `429 Too Many Requests`: Si se excede el límite de tasa.
  - `400 Bad Request`: Si la solicitud no cumple con el esquema definido.

### GET /status

- **Descripción:** Verifica el estado del servicio.
- **Ruta:** `routes/status.py`
- **Respuesta:**
  - `200 OK`: Devuelve el estado del servicio.

## Diagrama de Arquitectura

![Diagrama de Arquitectura](assets/doc_diagrama_arq.png)

## Descripción de Componentes

| Componente                       | Archivo                      | Descripción                                                                                                                 |
| -------------------------------- | ---------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Inicialización de la App         | `app.py`                     | Inicializa la aplicación Flask, carga la configuración y el esquema de solicitud, y registra los blueprints para las rutas. |
| Configuración                    | `config/config.py`           | Contiene funciones para cargar la configuración (`load_config`) y el esquema de solicitud (`load_request_schema`).          |
| Esquema de Solicitud             | `config/request_schema.json` | Define el esquema JSON para validar las solicitudes de comparación de nombres.                                              |
| Autenticación por Login          | `routes/login.py`            | Maneja la autenticación de usuarios mediante un endpoint POST `/login`.                                                     |
| Limitador de Tasa                | `app.py`                     | Implementa un limitador de tasa para proteger la API de abusos.                                                             |
| Servicio de Caché                | `services/cache_service.py`  | Proporciona funcionalidades de caché para almacenar y recuperar resultados de comparación de nombres.                       |
| Comparación de Nombres           | `services/compare_names.py`  | Contiene la lógica para comparar nombres y determinar si están comprometidos.                                               |
| Carga de Nombres                 | `utils/load_names.py`        | Proporciona funciones para cargar nombres desde un archivo CSV.                                                             |
| Cifrado y Descifrado de Archivos | `utils/encryption.py`        | Contiene funciones para cifrar y descifrar archivos.                                                                        |
| Manejo de Respuestas             | `utils/handle_response.py`   | Proporciona funciones para manejar y formatear las respuestas de la API.                                                    |
| Dataset de Nombres               | `assets/names_dataset.csv`   | Archivo CSV que contiene la lista de nombres a comparar.                                                                    |

## Justificación de Librerías y Decisiones de Diseño

- **Flask:** Seleccionado por su simplicidad y flexibilidad para construir aplicaciones web ligeras.
- **Flask-JWT-Extended:** Utilizado para manejar la autenticación basada en tokens JWT.
- **Flask-Limiter:** Implementado para proteger la API de abusos mediante limitación de tasa.
- **JSONSchema:** Utilizado para validar las solicitudes entrantes, asegurando que cumplan con el esquema definido.
- **Caché:** Implementado para mejorar el rendimiento y reducir la carga del sistema al almacenar resultados de comparación de nombres.

