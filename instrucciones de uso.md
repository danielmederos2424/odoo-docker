# Documentación de Uso del Odoo Manager GUI

## Ventana Principal

### Descripción General
- La ventana principal muestra una lista de los contenedores Docker existentes que ejecutan instancias de Odoo.
- Cada fila de contenedor incluye el nombre del contenedor, su estado y botones de acción.

### Actualización de Contenedores
- Haz clic en el botón "ACTUALIZAR" para refrescar la lista de contenedores y mostrar el estado más reciente y cualquier nuevo contenedor.

### Crear una Nueva Instancia
1. Haz clic en el botón "CREAR INSTANCIA" para abrir la ventana de creación de instancia.
2. Completa los detalles requeridos:
   - **Versión**: Selecciona la versión de Odoo del menú desplegable.
   - **Edición**: Elige entre las ediciones Community y Enterprise.
   - **Nombre de la Instancia**: Opcionalmente, proporciona un nombre personalizado para la instancia.
   - **Contraseña de Administrador**: Ingresa la contraseña del administrador. Este campo es obligatorio.
   - **Filtro de Base de Datos**: Selecciona si deseas habilitar el filtro de base de datos.
3. Haz clic en "Crear Instancia" para crear la nueva instancia de Odoo. La instancia se agregará a la lista de contenedores una vez creada.

### Gestión de Contenedores
- **Start**: Haz clic en el botón "Start" para iniciar un contenedor detenido. Este botón está deshabilitado si el contenedor ya está en funcionamiento.
- **Stop**: Haz clic en el botón "Stop" para detener un contenedor en funcionamiento. Este botón está deshabilitado si el contenedor ya está detenido.
- **Delete**: Haz clic en el botón "Delete" para eliminar un contenedor detenido junto con sus archivos de configuración. Este botón está deshabilitado si el contenedor está en funcionamiento.
- **Logs**: Haz clic en el botón "Logs" para ver los registros del contenedor. Los registros se muestran en una nueva ventana o en el visor de texto predeterminado.
- **Info**: Haz clic en el botón "Info" para ver información detallada sobre el contenedor.

## Ventana de Información Detallada

### Acceder a la Información
- Haz clic en el botón "Info" junto a un contenedor para abrir la ventana de información de ese contenedor.

### Ventana de Información
- Un encabezado "INFORMACION DE LA INSTANCIA" se muestra en la parte superior.
- Se muestra información detallada sobre la instancia, alineada a la izquierda.
- La información incluye detalles como el nombre de la instancia, puerto, versión, edición, contraseña de administrador y estado del filtro de base de datos.
- La ventana también incluye botones para:
  - **Abrir odoo.conf**: Abre el archivo `odoo.conf` correspondiente usando la aplicación predeterminada del sistema.
  - **Abrir extra-addons**: Abre la carpeta extra-addons para la instancia usando el explorador de archivos predeterminado.

### Botones en la Ventana de Información
- **Abrir odoo.conf**: Abre el archivo de configuración para la instancia.
- **Abrir extra-addons**: Abre la carpeta extra-addons donde se almacenan módulos adicionales para la instancia.

## Ventanas Emergentes de Error y Éxito
- **Ventana Emergente de Error**: Muestra mensajes de error cuando una acción falla. La ventana emergente incluye un botón de reintentar.
- **Ventana Emergente de Éxito**: Muestra mensajes de éxito cuando una acción se completa con éxito. La ventana emergente incluye un botón de continuar.

## Ventana de Ayuda
- Haz clic en el botón "AYUDA" en la barra lateral para abrir la ventana de ayuda, que proporciona información detallada e instrucciones sobre el uso de la aplicación.

## Salir de la Aplicación
- Haz clic en el botón "SALIR" en la barra lateral para cerrar la aplicación.

Para cualquier problema o asistencia adicional, consulta la ventana de ayuda dentro de la aplicación o contacta al equipo de soporte.
