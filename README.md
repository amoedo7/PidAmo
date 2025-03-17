# PidAmo - Sistema de Pedidos para Restaurantes y Bares

**PidAmo** es una aplicación web diseñada para facilitar la toma de pedidos en restaurantes y bares mediante una interfaz web accesible para los clientes. El sistema permite a los usuarios realizar pedidos desde sus mesas escaneando un QR único, visualizar menús, realizar pagos y gestionar la atención de los mozos, todo desde un único dispositivo móvil. Los propietarios pueden ver el estado de las mesas y el progreso de los pedidos en tiempo real a través de un panel de administración.

## Tabla de Contenidos
1. [Descripción](#descripción)
2. [Características](#características)
3. [Tecnologías Usadas](#tecnologías-usadas)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Instalación y Configuración](#instalación-y-configuración)
6. [Despliegue en Render](#despliegue-en-render)
7. [Cómo Contribuir](#cómo-contribuir)
8. [Licencia](#licencia)

## Descripción
PidAmo es una aplicación web que facilita el proceso de pedidos en restaurantes, bares y heladerías, mejorando la experiencia del cliente y la gestión operativa. Permite realizar pedidos, hacer pagos y gestionar la cocina, barra y atención de mesas de manera centralizada.

**Funcionalidades clave:**
- Generación de un QR único para cada mesa.
- Visualización de menús de productos (pizza, hamburguesas, cervezas, etc.).
- Sistema de pago integrado (con opciones de pago en efectivo o tarjeta).
- Visualización del estado de los pedidos por parte de la cocina y el bar.
- Monitoreo en tiempo real por parte del dueño del restaurante.

## Características
- **Backend**: Python con Flask
- **Frontend**: HTML, CSS, JavaScript (Vanilla o Frameworks como React si es necesario)
- **Base de datos**: Base de datos SQL (Se puede adaptar a MySQL o SQLite)
- **Panel de administración** para propietarios de restaurantes.
- **Interfaz de cliente optimizada** para smartphones y dispositivos móviles.
- **Modo offline** para operar sin conexión a internet.

## Tecnologías Usadas
- **Flask**: Para el backend y la gestión de las rutas de la aplicación.
- **HTML/CSS/JavaScript**: Para el desarrollo del frontend, creando una experiencia de usuario simple y directa.
- **SQLite/MySQL**: Para el almacenamiento de los datos de pedidos, usuarios y productos.
- **Render**: Para el despliegue de la aplicación en la nube.

## Estructura del Proyecto
El proyecto está organizado de la siguiente manera:

```
PidAmo/
│
├── server.py           # Backend de la aplicación (Flask)
├── static/            # Archivos estáticos (CSS, JS, imágenes)
│   ├── script.js
│   └── style.css
├── templates/         # Archivos HTML
│   ├── index.html
│   ├── menu.html
│   ├── mozos.html
│   ├── cocina.html
│   └── boss.html
├── .gitignore        # Archivos y directorios a ignorar por Git
└── requirements.txt  # Dependencias de Python (Flask, etc.)
```

## Instalación y Configuración

### 1. Clonar el Repositorio
Clona este repositorio en tu máquina local:

```bash
git clone https://github.com/tu_usuario/PidAmo.git
cd PidAmo
```

## Despliegue en Render
Para desplegar la aplicación en Render, sigue estos pasos:

1. **Subir el Proyecto a GitHub**
   Asegúrate de que tu repositorio esté en GitHub o en otro servicio de control de versiones.

2. **Crear una Cuenta en Render**
   Si no tienes una cuenta en Render, regístrate e inicia sesión.

3. **Crear un Nuevo Servicio**
   En Render, crea un nuevo servicio seleccionando "Web Service". Luego, vincula tu repositorio de GitHub.

4. **Configuración del Proyecto en Render**
   - En el panel de configuración de Render, asegúrate de que la opción para el servicio sea Python.
   - Asegúrate de especificar la ruta del archivo de inicio, que es server.py.
   - Render detectará automáticamente las dependencias desde el archivo requirements.txt.

5. **Desplegar**
   Render iniciará el despliegue y te proporcionará una URL pública para acceder a la aplicación.

**Nota**: Si tu aplicación requiere una base de datos, puedes usar Render PostgreSQL o MySQL para configurar una base de datos en la nube.

## Cómo Contribuir
Si deseas contribuir al proyecto, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama para tu nueva funcionalidad (git checkout -b feature-nueva-funcionalidad).
3. Haz tus cambios y realiza un commit (git commit -m 'Añadí nueva funcionalidad').
4. Envía un pull request describiendo tus cambios.

## Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles. 