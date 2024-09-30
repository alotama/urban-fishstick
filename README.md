# Documento de Arquitectura del Sistema

## Introducción

Este documento describe la arquitectura y los componentes del sistema, incluyendo un diagrama de arquitectura que ilustra la interacción entre los diferentes componentes. 

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

## Justificación de Tecnologías y Decisiones de Diseño

- **Flask:** Seleccionado por su simplicidad y flexibilidad para construir aplicaciones web ligeras.
- **Flask-JWT-Extended:** Utilizado para manejar la autenticación basada en tokens JWT.
- **Flask-Limiter:** Implementado para proteger la API de abusos mediante limitación de tasa.
- **JSONSchema:** Utilizado para validar las solicitudes entrantes, asegurando que cumplan con el esquema definido.
- **Caché:** Implementado para mejorar el rendimiento y reducir la carga del sistema al almacenar resultados de comparación de nombres.

