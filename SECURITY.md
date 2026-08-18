# Seguridad

PidAmo es un prototipo histórico y necesita una revisión de seguridad antes de cualquier reutilización productiva.

## Baseline

- Mantener claves, contraseñas, tokens y cadenas de conexión fuera del repositorio.
- Configurar secretos mediante variables de entorno.
- Revisar autenticación, sesiones y permisos de cada rol.
- Añadir protección CSRF cuando corresponda y rate limiting en login/endpoints sensibles.
- Mantener dependencias actualizadas y fijadas de forma reproducible.
- Aplicar migraciones y backups a la base de datos antes de operar con datos reales.
- No registrar contraseñas, tokens ni información de pago sensible.

## Pagos

Un estado interno como `paid`, `approved` o equivalente **no debe considerarse prueba de pago real**. Cualquier integración futura debe verificar la operación mediante evidencia del proveedor o del sistema externo correspondiente.

## Datos

No versionar bases de datos reales, exports de clientes, sesiones ni archivos `.env`.

## Reportes

Los reportes de seguridad deben usar datos de prueba y nunca incluir credenciales reales.
