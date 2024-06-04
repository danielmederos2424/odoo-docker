# Odoo Manager GUI Usage Documentation

## Main Window

### Overview
- The main window displays a list of existing Docker containers running Odoo instances.
- Each container row includes the container name, its status, and action buttons.

### Updating Containers
- Click the "ACTUALIZAR" button to refresh the list of containers to show the latest status and any new containers.

### Creating a New Instance
1. Click the "CREAR INSTANCIA" button to open the instance creation window.
2. Fill in the required details:
   - **Version**: Select the Odoo version from the dropdown menu.
   - **Edition**: Choose between Community and Enterprise editions.
   - **Instance Name**: Optionally, provide a custom name for the instance.
   - **Admin Password**: Enter the admin password. This field is mandatory.
   - **DB Filter**: Select whether to enable database filtering.
3. Click "Crear Instancia" to create the new Odoo instance. The instance will be added to the list of containers once created.

### Managing Containers
- **Start**: Click the "Start" button to start a stopped container. This button is disabled if the container is already running.
- **Stop**: Click the "Stop" button to stop a running container. This button is disabled if the container is already stopped.
- **Delete**: Click the "Delete" button to delete a stopped container along with its configuration files. This button is disabled if the container is running.
- **Logs**: Click the "Logs" button to view the logs of the container. The logs are displayed in a new window or the default text viewer.
- **Info**: Click the "Info" button to view detailed information about the container.

## Detailed Info Window

### Accessing Info
- Click the "Info" button next to a container to open the info window for that container.

### Info Window
- A header "INFORMACION DE LA INSTANCIA" is displayed at the top.
- Detailed information about the instance is shown, aligned to the left.
- The information includes details such as the instance name, port, version, edition, admin password, and DB filter status.
- The window also includes buttons to:
  - **Abrir odoo.conf**: Open the corresponding `odoo.conf` file using the default system application.
  - **Abrir extra-addons**: Open the extra-addons folder for the instance using the default file explorer.

### Buttons in Info Window
- **Abrir odoo.conf**: Opens the configuration file for the instance.
- **Abrir extra-addons**: Opens the extra-addons folder where additional modules for the instance are stored.

## Error and Success Popups
- **Error Popup**: Displays error messages when an action fails. The popup includes a retry button.
- **Success Popup**: Displays success messages when an action is completed successfully. The popup includes a continue button.

## Help Window
- Click the "AYUDA" button on the sidebar to open the help window, which provides detailed information and instructions on using the application.

## Exiting the Application
- Click the "SALIR" button on the sidebar to close the application.

For any issues or further assistance, refer to the help window within the application or contact the support team.
