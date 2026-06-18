# Sistema de Reservas de Espacios - Uniguajira

Aplicación web desarrollada con **Django** para gestionar la reserva de espacios universitarios, controlar disponibilidad en horarios específicos y visualizar reportes básicos del sistema.

## Descripción general
Este proyecto permite a los usuarios:
- registrar espacios y clasificarlos por tipo;
- consultar si un espacio está disponible en un horario determinado;
- crear reservas con información adicional como motivo y servicios;
- revisar una agenda diaria de reservas aprobadas;
- visualizar reportes por estado y por espacio.

También incluye autenticación con **django-allauth** para acceso seguro y administración desde el panel de Django.

## Tecnologías utilizadas
- Python
- Django
- SQLite
- Bootstrap (para la interfaz)
- django-allauth

## Funcionalidades principales
- Inicio del sistema
- Login y registro de usuarios
- Creación de espacios con tipos predefinidos o nuevos
- Verificación de conflictos de horario
- Agenda de reservas aprobadas
- Reportes estadísticos básicos
- Gestión administrativa desde `/admin/`

## Estructura del proyecto
- `apps/reservas/` — lógica principal del sistema
- `templates/` — plantillas HTML del frontend
- `static/` — archivos estáticos (CSS, imágenes, etc.)
- `mi_proyecto/` — configuración del proyecto Django
- `diagramas/` — documentos y diagramas del sistema

## Modelo de datos
El sistema utiliza estas entidades principales:

- `TipoEspacio` — categorías para clasificar un espacio (salón, laboratorio, auditorio, oficina, etc.)
- `Espacio` — lugar físico que puede reservarse
- `Reserva` — solicitud de uso de espacio en una fecha y hora específica
- `DetalleReserva` — información adicional de la reserva
- `ServicioAdicional` — recursos extras asociados a una reserva

Relaciones principales:
- `TipoEspacio` → `Espacio` (1 a muchos)
- `Espacio` → `Reserva` (1 a muchos)
- `Reserva` → `DetalleReserva` (1 a 1)
- `Reserva` ↔ `ServicioAdicional` (muchos a muchos)

## Rutas principales

| Ruta | Descripción |
|------|-------------|
| `/` | Página principal |
| `/disponibilidad/` | Verifica si un espacio está libre |
| `/agenda/` | Muestra reservas aprobadas por fecha |
| `/reporte/` | Reportes por estado y por espacio |
| `/crear/` | Crear una nueva reserva |
| `/espacios/` | Lista de espacios registrados |
| `/espacios/nuevo/` | Crear un nuevo espacio |
| `/admin/` | Panel administrativo |

## Instalación y ejecución

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd proyecto_avanzada
```

### 2. Crear y activar un entorno virtual
```bash
python -m venv venv
.
venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Aplicar migraciones
```bash
python manage.py migrate
```

### 5. Crear un superusuario (opcional, para usar el panel administrativo)
```bash
python manage.py createsuperuser
```

### 6. Ejecutar el servidor
```bash
python manage.py runserver
```

La aplicación quedará disponible en:
- `http://127.0.0.1:8000/`

## Cómo usar la aplicación
1. Inicia sesión o crea una cuenta.
2. Dirígete a la sección de espacios para registrar nuevos lugares.
3. Usa la opción de disponibilidad para verificar horarios.
4. Crea una reserva desde el formulario correspondiente.
5. Revisa la agenda y los reportes para consultar el estado de las solicitudes.

## Pruebas
Para ejecutar las pruebas del proyecto:
```bash
python manage.py test
```

## Notas importantes
- El proyecto usa SQLite como base de datos por defecto.
- La configuración de autenticación social (Google/GitHub) está preparada, pero requiere credenciales reales para funcionar completamente.
- Los diagramas y documentación del sistema se encuentran en la carpeta `diagramas/`.

## Integrantes
- Alexander Arpuhaina
- Cristian Padilla
