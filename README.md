# PidAmo

Sistema web experimental para **pedidos en restaurantes, bares y comercios gastronómicos mediante QR**, creado dentro del ecosistema DesarrollAMO.

## Estado

**Prototipo funcional histórico.** Dentro de los tres repos `PidAmo`, `PidAmoFrontend` y `PidAmoBackend`, este es el que contiene la implementación sustancial de aquella etapa: servidor Flask, autenticación, modelos, templates y assets.

Los repos `PidAmoFrontend` y `PidAmoBackend` quedaron esencialmente como placeholders y no deben confundirse con implementaciones independientes completas.

## Idea del producto

```text
mesa / cliente
      ↓ QR
menú → pedido → estado → atención
      ↓
panel de operación
```

El objetivo era reducir fricción en la toma de pedidos y dar al negocio una vista central de mesas, cocina/bar y atención.

## Stack histórico

- Python / Flask;
- HTML, CSS y JavaScript;
- modelos y autenticación propios;
- templates server-side;
- despliegue pensado para Render;
- persistencia SQL/SQLite según la etapa.

## Estructura principal

```text
PidAmo/
├── server.py
├── auth.py
├── models.py
├── extensions.py
├── templates/
├── static/
├── requirements.txt
└── Procfile
```

## Ejecución local

```bash
git clone https://github.com/amoedo7/PidAmo.git
cd PidAmo
python -m venv .venv
# activar el entorno según tu sistema
pip install -r requirements.txt
python server.py
```

## Antes de reutilizarlo

Este código es anterior a la arquitectura actual de DesarrollAMO. Antes de ponerlo en producción hay que revisar:

- secretos y configuración por variables de entorno;
- autenticación y sesiones;
- esquema y migraciones de base de datos;
- CSRF/rate limiting según endpoints;
- dependencias;
- flujo de pagos: no asumir que un estado interno equivale a pago real;
- responsive/accessibility;
- observabilidad y backups.

## Relación con DesarrollAMO

PidAmo sigue siendo una buena referencia de producto vertical: una necesidad concreta convertida en interfaz + operación + backend. Se conserva como prototipo y material reutilizable, no como servicio actual garantizado.

## Licencia

El README histórico mencionaba MIT, pero este repositorio no muestra actualmente un archivo `LICENSE` en su raíz. No asumir una licencia hasta que se defina explícitamente.

---

**DesarrollAMO** · producto histórico preservado con su contexto técnico real.
