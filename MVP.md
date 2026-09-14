# MVP · PidAmo (si se reactiva)

## Resultado mínimo
Un cliente escanea QR, ve menú, crea pedido y el comercio lo recibe/cambia de estado desde un panel.

## Flujo mínimo
1. negocio configura productos;
2. mesa/QR identifica contexto;
3. cliente arma pedido;
4. confirma;
5. operación recibe pedido;
6. cambia estado: recibido → preparando → listo/entregado;
7. cliente ve estado;
8. auditoría básica conserva quién cambió qué.

## Antes de declararlo operable
- secretos por variables de entorno;
- migraciones y base durable;
- sesiones/autorización revisadas;
- CSRF/rate limiting donde aplique;
- tests de pedido/estado;
- responsive;
- pagos, si existen, verificados externamente.

El código actual es histórico; este documento define el umbral de una reactivación, no afirma producción.
