# Sistema de Reservas de Espacios - Uniguajira

Proyecto desarrollado para el Segundo Corte de la asignatura **Programación Avanzada**. Este sistema permite la gestión integral de reservas de espacios universitarios, garantizando la integridad de los horarios y facilitando la administración mediante herramientas visuales y reportes.

## Integrantes
- Yamal Quintero
- Alexander Arpuhaina
- Cristian Padilla

## Requisitos del Proyecto (Entregables)
El sistema cumple con el 100% de los requisitos solicitados:
- **Django 5.2a1** en un entorno virtual (`venv`).
- **Diagramas UML**: Casos de uso y Entidad-Relación (ubicados en la carpeta `diagramas/`).
- **Modelos y ORM**: Implementación de relaciones 1-1, 1-N y N-N.
- **Validación de Conflictos**: Lógica para evitar solapamientos de horario en reservas aprobadas.
- **Funcionalidades Core**:
    - Consulta de Disponibilidad.
    - Agenda de Reservas por día.
    - Reportes por estado y por espacio.
- **Registro en Admin**: Todos los modelos gestionables desde `/admin/`.

## Estructura de Base de Datos (Relaciones)
- **One-to-One (1-1)**: `Reserva` <-> `DetalleReserva` (Información extendida de la reserva).
- **One-to-Many (1-N)**: `TipoEspacio` -> `Espacio`, `Espacio` -> `Reserva`, `User` -> `Reserva`.
- **Many-to-Many (N-N)**: `ServicioAdicional` <-> `Reserva` (Recursos extra como proyectores).

## Instalación y Ejecución

1. **Activar entorno virtual**:
   ```bash
   .\venv\Scripts\activate
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar el servidor**:
   ```bash
   python manage.py runserver
   ```

## Guía de Navegación
- **Portal de Inicio**: `http://127.0.0.1:8000/`
- **Consulta de Disponibilidad**: `/disponibilidad/` (Verificar si un espacio está libre).
- **Agenda Diaria**: `/agenda/` (Listado de reservas aprobadas por fecha).
- **Reportes Estadísticos**: `/reporte/` (Resumen por estado y espacio).
- **Django Admin**: `/admin/` (Gestión total de datos).
    - *Usuario:* `admin`
    - *Clave:* `admin123`

## Documentación y Evidencias
Los archivos de soporte se encuentran en la carpeta `diagramas/`:
- `Diagrama de actores.pdf`: Casos de uso y límites del sistema.
- `diagrama entidad-relacion.pdf`: Diseño de la base de datos.
- `Django Admin evidencia.png`: Captura de pantalla del panel administrativo funcional.
