import customtkinter
from customtkinter import CTkButton
import os
import subprocess
from PIL import Image
import time
import datetime

class App(customtkinter.CTk):

    def fade_out(self, window, callback=None, alpha=1.0, step=0.05, delay=10):
        if alpha > 0:
            alpha -= step
            window.attributes("-alpha", alpha)
            window.after(delay, self.fade_out, window, callback, alpha, step, delay)
        else:
            window.destroy()
            if callback:
                callback()
    
    def get_dir(self):
        dir = os.getcwd()
        return dir

    def error_popup(self, e):
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "imgs")
        error_popup = customtkinter.CTkToplevel()
        error_popup.geometry("400x200")
        error_popup.title("ERROR")
        error_popup.resizable(False, False)
        screen_width = error_popup.winfo_screenwidth()
        screen_height = error_popup.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 200) // 2
        error_popup.geometry(f"+{x}+{y}")
        error_popup.attributes("-topmost", True)
        error_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "error.png")), size=(100, 100))
        error_label = customtkinter.CTkLabel(master=error_popup, text="", image=error_image)
        error_label.configure(image=error_image)
        error_label.pack()
        error_text = e
        error_label = customtkinter.CTkLabel(master=error_popup, text=error_text, wraplength=300, font=customtkinter.CTkFont(size=15))
        error_label.pack()
        CTkButton(master=error_popup, text="REINTENTAR", command=lambda: error_button_event()).pack(expand=True, pady=10, padx=20)

        def error_button_event():
            error_popup.destroy()

    def success_popup(self, message):
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "imgs")
        success_popup = customtkinter.CTkToplevel()
        success_popup.geometry("400x200")
        success_popup.title("OPERACIÓN EXITOSA")
        success_popup.resizable(False, False)
        screen_width = success_popup.winfo_screenwidth()
        screen_height = success_popup.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 200) // 2
        success_popup.geometry(f"+{x}+{y}")
        success_popup.attributes("-topmost", True)
        error_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "success.png")), size=(100, 100))
        error_label = customtkinter.CTkLabel(master=success_popup, text="", image=error_image)
        error_label.configure(image=error_image)
        error_label.pack()
        error_text = message
        error_label = customtkinter.CTkLabel(master=success_popup, text=error_text, wraplength=300, font=customtkinter.CTkFont(size=15))
        error_label.pack()
        CTkButton(master=success_popup, text="CONTINUAR", command=lambda: error_button_event()).pack(expand=True, pady=10, padx=20)

        def error_button_event():
            success_popup.destroy()

    def start_window(self):
        # Startup verifications
        def verifications():
            docker = check_docker()
            docker_text = "Verificando si Docker Engine está activo..."
            docker_label = customtkinter.CTkLabel(master=start_window, text=docker_text, wraplength=300, font=customtkinter.CTkFont(size=15))
            docker_label.pack()

            if docker:
                message_text = "✅ Docker engine en ejecución"
                start_window.after(1000, lambda: docker_label.configure(text=message_text))
                start_window.after(2000, check_network)
            else:
                error = "❌ Docker engine no está en ejecución"
                start_window.after(1000, lambda: error_window(error))

        def check_docker():
            try:
                subprocess.run(["docker", "ps"], check=True)
                return True
            except subprocess.CalledProcessError:
                return False
            except FileNotFoundError:
                return False

        def check_network():
            try:
                cmd_networks = "docker network ls --format '{{.Name}}'"
                networks = subprocess.check_output(cmd_networks, shell=True, text=True).splitlines()
                if 'odoo-network' in networks:
                    network_text = "✅ Red odoo-network existe"
                    network_label = customtkinter.CTkLabel(master=start_window, text=network_text, wraplength=300, font=customtkinter.CTkFont(size=15))
                    network_label.pack()
                else:
                    network_text = "❌ Red odoo-network no existe\nCreando..."
                    network_label = customtkinter.CTkLabel(master=start_window, text=network_text, wraplength=300, font=customtkinter.CTkFont(size=15))
                    network_label.pack()
                    cmd_create = "docker network create odoo-network"
                    subprocess.run(cmd_create, shell=True)
                    created_text = "✅ Red odoo-network creada"
                    start_window.after(2000, lambda: customtkinter.CTkLabel(master=start_window, text=created_text, wraplength=300, font=customtkinter.CTkFont(size=15)).pack())
                
                start_window.after(2000, check_postgres)
                                
            except subprocess.CalledProcessError as e:
                error_text = f"Error: {e}"
                start_window.after(1000, lambda: customtkinter.CTkLabel(master=start_window, text=error_text, wraplength=300, font=customtkinter.CTkFont(size=15)).pack())

        def check_postgres():
            try:
                cmd_status = "docker inspect -f '{{.State.Status}}' postgres_db"
                status = subprocess.check_output(cmd_status, shell=True, text=True).strip()
                if status == 'running':
                    status_text = "✅ El servicio de postgres está activo"
                    status_label = customtkinter.CTkLabel(master=start_window, text=status_text, wraplength=300, font=customtkinter.CTkFont(size=15))
                    status_label.pack()
                elif status == 'exited':
                    status_text = "El contenedor de postgres se encuentra detenido\nReiniciando..."
                    status_label = customtkinter.CTkLabel(master=start_window, text=status_text, wraplength=300, font=customtkinter.CTkFont(size=15))
                    status_label.pack()
                    cmd_restart = "docker restart postgres_db"
                    subprocess.run(cmd_restart, shell=True)
                    restart_text = "✅ Servicio de postgres puesto en marcha"
                    start_window.after(2000, lambda: status_label.configure(text=restart_text)) 
                else:
                    status_text = f"Estado del servicio de postgres: {status}"
                    status_label = customtkinter.CTkLabel(master=start_window, text=status_text, wraplength=300, font=customtkinter.CTkFont(size=15))
                    status_label.pack()
                    start_text = "✅ Servicio de postgres iniciado"
                    start_window.after(2000, lambda: status_label.configure(text=start_text)) 

                start_window.after(1000, show_continue_button)  

            except subprocess.CalledProcessError as e:
                create_text = "Creando el servicio de postgres..."
                create_label = customtkinter.CTkLabel(master=start_window, text=create_text, wraplength=300, font=customtkinter.CTkFont(size=15))
                create_label.pack()
                cmd_create = ("docker run -d --name postgres_db --restart=unless-stopped --network=odoo-network -v pg_data:/var/lib/postgresql/data:rw -e POSTGRES_USER=pgodoouser -e POSTGRES_PASSWORD=pgOd0op4sswOrd -e POSTGRES_DB=postgres postgres:15")
                subprocess.run(cmd_create, shell=True)
                restart_text = "✅ Servicio de postgres puesto en marcha"
                start_window.after(2000, lambda: create_label.configure(text=restart_text)) 
                start_window.after(1000, show_continue_button)  
        
        def display_init_message():
            init_message = "Realizando comprobaciones iniciales..."
            init_label = customtkinter.CTkLabel(master=start_window, text=init_message, font=customtkinter.CTkFont(size=15))
            init_label.pack()
            start_window.after(1000, verifications)

        def show_continue_button():
            CTkButton(master=start_window, text="Continuar", fg_color="#28a745", hover_color="dark green", command=lambda: continue_button_event()).pack(expand=True, pady=(10, 5), padx=20)

        def continue_button_event():
            self.fade_out(start_window, self.main_window)


        # Start Window
        start_window = customtkinter.CTkToplevel()
        start_window.title("ODOO MANAGER GUI")
        start_window.geometry("450x400")
        start_window.resizable(False, False)
        screen_width = start_window.winfo_screenwidth()
        screen_height = start_window.winfo_screenheight()
        x = (screen_width - 500) // 2
        y = (screen_height - 600) // 2
        start_window.geometry(f"+{x}+{y}")
        start_window.attributes("-topmost", True)

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "imgs")
        image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "docker.png")), size=(150, 150))
        image_label = customtkinter.CTkLabel(master=start_window, text="", image=image)
        image_label.configure(image=image)
        image_label.pack()
        header_message = "BIENVENIDO A ODOO MANAGER"
        header_label = customtkinter.CTkLabel(master=start_window, text=header_message, font=customtkinter.CTkFont(size=25))
        header_label.pack()
        start_window.after(1000, lambda: display_init_message())

        # Generic error window
        def error_window(e):
            error_win = customtkinter.CTkToplevel()
            error_win.geometry("400x200")
            error_win.title("ERROR")
            error_win.resizable(False, False)
            screen_width = error_win.winfo_screenwidth()
            screen_height = error_win.winfo_screenheight()
            x = (screen_width - 400) // 2
            y = (screen_height - 200) // 2
            error_win.geometry(f"+{x}+{y}")
            error_win.attributes("-topmost", True)
            error_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "error.png")), size=(100, 100))
            error_label = customtkinter.CTkLabel(master=error_win, text="", image=error_image)
            error_label.configure(image=error_image)
            error_label.pack()
            error_text = e
            error_label = customtkinter.CTkLabel(master=error_win, text=error_text, wraplength=300, font=customtkinter.CTkFont(size=15))
            error_label.pack()
            CTkButton(master=error_win, text="REINTENTAR", command=lambda: error_button_event()).pack(expand=True, pady=10, padx=20)

            def error_button_event():
                error_win.destroy()
                start_window.destroy()
                self.start_window()

    def welcome_window(self):
        welcome_window = customtkinter.CTkToplevel()
        welcome_window.title("BIENVENIDO")
        welcome_window.geometry("400x280")
        welcome_window.resizable(False, False)
        screen_width = welcome_window.winfo_screenwidth()
        screen_height = welcome_window.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 280) // 2
        welcome_window.geometry(f"+{x}+{y}")
        welcome_window.attributes("-topmost", True)

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "imgs")

        # Load image
        image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "odoo.png")), size=(150, 150))
        image_label = customtkinter.CTkLabel(master=welcome_window, text="", image=image)
        image_label.configure(image=image)
        image_label.pack()

        # Message
        message_text = "Sea bienvenido/a al programa que le permitirá desplegar y administrar múltiples instancias de Odoo de forma local utilizando Docker."
        message_label = customtkinter.CTkLabel(master=welcome_window, text=message_text, wraplength=300, font=customtkinter.CTkFont(size=15))
        message_label.pack()

        welcome_window.after(5000, lambda: self.fade_out(welcome_window))

    def help_window(self):
        help_window = customtkinter.CTkToplevel()
        help_window.title("AYUDA")
        help_window.geometry("500x350")
        help_window.resizable(False, False)
        screen_width = help_window.winfo_screenwidth()
        screen_height = help_window.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 280) // 2
        help_window.geometry(f"+{x}+{y}")
        help_window.attributes("-topmost", True)

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "imgs")

        # Load image
        image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "help.png")), size=(150, 150))
        image_label = customtkinter.CTkLabel(master=help_window, text="", image=image)
        image_label.configure(image=image)
        image_label.pack()

        # Message
        message_text = "El presente programa permite crear, modificar, reiniciar, monitorizar y eliminar instancias de Odoo desplegadas mediante Docker. La ventana principal muestra todos los contenedores existentes de docker especificando su estado actual, pudiendo así interactuar con ellos mediante los botones correspondientes. Se podrá también obtener información detallada sobre cada una de las instancias existentes en el botón Info"
        message_label = customtkinter.CTkLabel(master=help_window, text=message_text, wraplength=350, font=customtkinter.CTkFont(size=15))
        message_label.pack()

    def main_window(self):
        #self.welcome_window()
        self.main_window_instance = customtkinter.CTkToplevel()
        self.main_window_instance.title("ODOO MANAGER GUI")
        self.main_window_instance.geometry("1000x500")
        self.main_window_instance.resizable(False, False)
        screen_width = self.main_window_instance.winfo_screenwidth()
        screen_height = self.main_window_instance.winfo_screenheight()
        x = (screen_width - 1000) // 2
        y = (screen_height - 500) // 2
        self.main_window_instance.geometry(f"+{x}+{y}")

        # Sidebar
        sidebar_frame = customtkinter.CTkFrame(self.main_window_instance, width=140, corner_radius=0)
        sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.main_window_instance.grid_rowconfigure(0, weight=1)
        logo_label = customtkinter.CTkLabel(sidebar_frame, text="ODOO MANAGER", font=customtkinter.CTkFont(size=20, weight="bold"))
        logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "imgs")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "odoo.png")), size=(50, 50))
        update_button = customtkinter.CTkButton(sidebar_frame, text="ACTUALIZAR", command=self.update_button_event)
        update_button.grid(row=1, column=0, padx=20, pady=10)
        new_button = customtkinter.CTkButton(sidebar_frame, text="CREAR INSTANCIA", command=self.new_button_event)
        new_button.grid(row=2, column=0, padx=20, pady=10)
        help_button = customtkinter.CTkButton(sidebar_frame, text="AYUDA", command=self.help_button_event)
        help_button.grid(row=3, column=0, padx=20, pady=10)
        exit_button = customtkinter.CTkButton(sidebar_frame, text="SALIR", fg_color="#E70000", hover_color="dark red", command=self.exit_button_event)
        exit_button.grid(row=4, column=0, padx=20, pady=(10, 20))

        self.show_containers = customtkinter.CTkScrollableFrame(master=self.main_window_instance, label_text="CONTENEDORES DE DOCKER EXISTENTES", label_font=customtkinter.CTkFont(size=15, weight="bold"), corner_radius=5, width=750, height=420)
        self.show_containers.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.show_containers.grid_columnconfigure(0, weight=1)
        self.show_containers.place(relx=0.6, rely=0.5, anchor=customtkinter.CENTER)
        
        containers = self.get_docker_containers()
        for i, (name, status) in enumerate(containers):
            self.create_container_row(self.show_containers, name, status, i)
            
    def get_docker_containers(self):
        try:
            cmd = "docker ps -a --format '{{.Names}}|{{.Status}}'"
            containers = subprocess.check_output(cmd, shell=True, text=True).strip().splitlines()
            return [container.split('|') for container in containers]
        except subprocess.CalledProcessError:
            return []

    def create_container_row(self, master, name, status, row):
        font = customtkinter.CTkFont(size=15, weight="bold")
        name_label = customtkinter.CTkLabel(master, font=font, text=name.upper(), anchor="w")
        name_label.grid(row=row, column=0, padx=10, pady=(5, 5), sticky="w")

        status_label = customtkinter.CTkLabel(master, text=f"Estado: {status}", anchor="w")
        status_label.grid(row=row, column=1, padx=10, pady=(5, 5), sticky="w")

        buttons_frame = customtkinter.CTkFrame(master, fg_color="transparent")
        buttons_frame.grid(row=row, column=2, padx=10, pady=(5, 5), sticky="e")

        # Determine button states based on container name and status
        is_odoo = "odoo" in name.lower()
        is_running = "Up" in status

        start_button = CTkButton(buttons_frame, text="Start", width=5, command=lambda: self.manage_container(name, "start"))
        start_button.pack(side="left", padx=2)
        start_button.configure(state="disabled" if is_running else "normal")

        CTkButton(buttons_frame, text="Stop", width=5, command=lambda: self.manage_container(name, "stop")).pack(side="left", padx=2)
        CTkButton(buttons_frame, text="Delete", width=5, command=lambda: self.manage_container(name, "rm")).pack(side="left", padx=2)
        
        logs_button = CTkButton(buttons_frame, text="Logs", width=5, command=lambda: self.container_logs(name))
        logs_button.pack(side="left", padx=2)
        
        info_button = CTkButton(buttons_frame, text="Info", width=5, command=lambda: self.manage_container(name, "inspect"))
        info_button.pack(side="left", padx=2)
        info_button.configure(state="normal" if is_odoo else "disabled")
    
    def manage_container(self, container_name, action):
        try:
            subprocess.run(["docker", action, container_name], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to {action} container {container_name}: {e}")
        time.sleep(1)
        self.update_containers()
          
    def container_logs(self, container_name):
        try:
            # Create logs directory if it doesn't exist
            logs_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "logs")
            os.makedirs(logs_dir, exist_ok=True)

            # Generate the log filename with timestamp
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            log_filename = f"{timestamp}_{container_name}.log"
            log_filepath = os.path.join(logs_dir, log_filename)

            # Run the docker logs command and save output to the log file
            with open(log_filepath, "w") as log_file:
                subprocess.run(["docker", "logs", container_name], stdout=log_file, stderr=subprocess.STDOUT, check=True)

            # Open the log file with the default application
                if os.name == 'nt':  # For Windows
                    os.startfile(log_filepath)
                elif os.name == 'posix':  # For Unix-like systems
                    if subprocess.run(["uname", "-s"], capture_output=True, text=True).stdout.strip() == "Darwin":
                        subprocess.run(["open", log_filepath])  # For macOS
                    else:
                        subprocess.run(["xdg-open", log_filepath])  # For Linux

        except subprocess.CalledProcessError as e:
            self.error_popup(str(e))
        except Exception as e:
            self.error_popup(str(e))
                    
    def update_containers(self):
        for widget in self.show_containers.winfo_children():
            widget.destroy()

        cmd = "docker ps -a --format '{{.Names}}|{{.Status}}'"
        output = subprocess.check_output(cmd, shell=True, text=True).strip()
        container_info = output.splitlines()

        for i, info in enumerate(container_info):
            name, status = info.split('|')
            self.create_container_row(self.show_containers, name, status, i)
      
    def update_button_event(self):
        self.update_containers()
        
    def new_button_event(self):
        print("new")

    def help_button_event(self):
        self.help_window()

    def exit_button_event(self):
        self.destroy()

    def __init__(self):
        super().__init__()
        self.withdraw()
        #self.start_window()
        self.main_window()

if __name__ == "__main__":
    app = App()
    app.mainloop()
