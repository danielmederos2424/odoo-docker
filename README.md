# Odoo Manager GUI

Odoo Manager GUI is a custom Tkinter-based application that allows users to manage multiple Odoo instances using Docker. The application provides an interface to create, update, delete, and view information about Odoo instances.

## Features

- **Create Odoo Instances**: Easily create new Odoo instances with customizable options.
- **Delete Odoo Instances**: Remove Odoo instances along with their configuration files.
- **View Instance Information**: Display detailed information about each Odoo instance.
- **Manage Containers**: Start, stop, and view logs of Docker containers running Odoo instances.

## Requirements

- Python 3.6 or higher
- Docker
- CustomTkinter
- PIL (Python Imaging Library)

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/odoo-manager-gui.git
    cd odoo-manager-gui
    ```

2. **Create and activate a virtual environment** (optional but recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install required packages**:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run the application**:
    ```sh
    python odoo_manager_gui.py
    ```

2. **Startup Verification**:
    - The application will verify if Docker is running and if the required Docker network and PostgreSQL service are set up.

3. **Main Window**:
    - The main window displays existing Docker containers with options to start, stop, delete, and view logs.

4. **Create New Instance**:
    - Click "CREAR INSTANCIA" to create a new Odoo instance with customizable options like version, edition, instance name, admin password, and database filter.

5. **Delete Instance**:
    - Use the "Delete" button to remove an Odoo instance and its associated configuration files.

6. **View Instance Information**:
    - Click "Info" to view detailed information about an Odoo instance, with options to open the configuration file and the extra-addons folder.

## Code Overview

### Main Application Class

- **`App(customtkinter.CTk)`**: The main application class that initializes the GUI and manages different windows and functionalities.

### Key Methods

- **`start_window(self)`**: Displays the startup window and performs initial verifications.
- **`main_window(self)`**: Displays the main application window with Docker container management options.
- **`create_instance(self)`**: Creates a new Odoo instance based on user input.
- **`delete_container(self, container_name)`**: Deletes a specified Odoo container and its configuration files.
- **`show_info(self, container_name)`**: Displays detailed information about a specified Odoo instance.
- **`open_file(self, file_path)`**: Opens a specified file using the default system application.
- **`open_folder(self, folder_path)`**: Opens a specified folder using the default system application.

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the custom Tkinter widgets.
- [PIL](https://pillow.readthedocs.io/en/stable/) for image handling.

## Contact

For any questions or feedback, please contact danielmederos2424@gmail.com

