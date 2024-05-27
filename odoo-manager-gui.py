import customtkinter
from customtkinter import CTkButton
import os
import subprocess
import docker
from PIL import Image

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

    def main_window(self):
        self.welcome_window()

        main_window = customtkinter.CTkToplevel()
        main_window.title("ODOO MANAGER GUI")
        main_window.geometry("1000x500")
        main_window.resizable(False, False)
        screen_width = main_window.winfo_screenwidth()
        screen_height = main_window.winfo_screenheight()
        x = (screen_width - 1000) // 2
        y = (screen_height - 500) // 2
        main_window.geometry(f"+{x}+{y}")

        # Sidebar
        sidebar_frame = customtkinter.CTkFrame(main_window, width=140, corner_radius=0)
        sidebar_frame.grid(row=0, column=0, sticky="nsew")
        main_window.grid_rowconfigure(0, weight=1)
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


    def update_button_event(self):
        print("update")

    def new_button_event(self):
        print("new")

    def help_button_event(self):
        print("help")

    def exit_button_event(self):
        self.fade_out(self.main_window)

    def __init__(self):
        super().__init__()
        self.withdraw()
        self.start_window()
        #self.main_window()


if __name__ == "__main__":
    app = App()
    app.mainloop()
