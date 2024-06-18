import customtkinter
from customtkinter import CTkButton, CTkLabel, CTkEntry, CTkOptionMenu, CTkToplevel
import os
import subprocess
from PIL import Image
import time

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
        CTkButton(master=error_popup, text="RETRY", command=lambda: error_button_event()).pack(expand=True, pady=10, padx=20)

        def error_button_event():
            error_popup.destroy()

    def success_popup(self, message):
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "imgs")
        success_popup = customtkinter.CTkToplevel()
        success_popup.geometry("400x200")
        success_popup.title("SUCCESS")
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
        CTkButton(master=success_popup, text="OK", command=lambda: error_button_event()).pack(expand=True, pady=10, padx=20)

        def error_button_event():
            success_popup.destroy()

    def start_window(self):
        # Startup verifications
        def verifications():
            docker = check_docker()
            docker_text = "Checking if Docker engine is active..."
            docker_label = customtkinter.CTkLabel(master=start_window, text=docker_text, wraplength=300, font=customtkinter.CTkFont(size=15))
            docker_label.pack()

            if docker:
                message_text = "✅ Docker engine is running"
                start_window.after(1000, lambda: docker_label.configure(text=message_text))
                start_window.after(2000, check_network)
            else:
                error = "❌ Docker engine is not running"
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
                    network_text = "✅ odoo-network exists"
                    network_label = customtkinter.CTkLabel(master=start_window, text=network_text, wraplength=300, font=customtkinter.CTkFont(size=15))
                    network_label.pack()
                else:
                    network_text = "❌ odoo-network doesn't exists\nCreating..."
                    network_label = customtkinter.CTkLabel(master=start_window, text=network_text, wraplength=300, font=customtkinter.CTkFont(size=15))
                    network_label.pack()
                    cmd_create = "docker network create odoo-network"
                    subprocess.run(cmd_create, shell=True)
                    created_text = "✅ odoo-network created"
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
                    status_text = "✅ The postgres database service is running"
                    status_label = customtkinter.CTkLabel(master=start_window, text=status_text, wraplength=300, font=customtkinter.CTkFont(size=15))
                    status_label.pack()
                elif status == 'exited':
                    status_text = "Postgres database container is stopped\nRestarting..."
                    status_label = customtkinter.CTkLabel(master=start_window, text=status_text, wraplength=300, font=customtkinter.CTkFont(size=15))
                    status_label.pack()
                    cmd_restart = "docker restart postgres_db"
                    subprocess.run(cmd_restart, shell=True)
                    restart_text = "✅ Postgres database service is now running"
                    start_window.after(2000, lambda: status_label.configure(text=restart_text)) 
                else:
                    status_text = f"Postgres status: {status}"
                    status_label = customtkinter.CTkLabel(master=start_window, text=status_text, wraplength=300, font=customtkinter.CTkFont(size=15))
                    status_label.pack()
                    start_text = "✅ Postgres service started"
                    start_window.after(2000, lambda: status_label.configure(text=start_text)) 

                start_window.after(1000, show_continue_button)  

            except subprocess.CalledProcessError as e:
                create_text = "Creating postgres service..."
                create_label = customtkinter.CTkLabel(master=start_window, text=create_text, wraplength=300, font=customtkinter.CTkFont(size=15))
                create_label.pack()
                cmd_create = ("docker run -d --name postgres_db --restart=unless-stopped --network=odoo-network -v pg_data:/var/lib/postgresql/data:rw -e POSTGRES_USER=pgodoouser -e POSTGRES_PASSWORD=pgOd0op4sswOrd -e POSTGRES_DB=postgres postgres:15")
                subprocess.run(cmd_create, shell=True)
                restart_text = "✅ Postgres database service is now running"
                start_window.after(2000, lambda: create_label.configure(text=restart_text)) 
                start_window.after(1000, show_continue_button)  
        
        def display_init_message():
            init_message = "Performing startup verifications..."
            init_label = customtkinter.CTkLabel(master=start_window, text=init_message, font=customtkinter.CTkFont(size=15))
            init_label.pack()
            start_window.after(1000, verifications)

        def show_continue_button():
            CTkButton(master=start_window, text="OK", fg_color="#28a745", hover_color="dark green", command=lambda: continue_button_event()).pack(expand=True, pady=(10, 5), padx=20)

        def continue_button_event():
            self.fade_out(start_window, self.main_window)


        # Start Window
        start_window = customtkinter.CTkToplevel()
        start_window.title("ODOO MANAGER GUI")
        start_window.geometry("450x400")
        start_window.resizable(False, False)
        screen_width = start_window.winfo_screenwidth()
        screen_height = start_window.winfo_screenheight()
        x = (screen_width - 450) // 2
        y = (screen_height - 400) // 2
        start_window.geometry(f"+{x}+{y}")
        start_window.attributes("-topmost", True)

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "imgs")
        image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "docker.png")), size=(150, 150))
        image_label = customtkinter.CTkLabel(master=start_window, text="", image=image)
        image_label.configure(image=image)
        image_label.pack()
        header_message = "WELCOME TO ODOO MANAGER"
        header_label = customtkinter.CTkLabel(master=start_window, text=header_message, font=customtkinter.CTkFont(size=25))
        header_label.pack()
        start_window.after(1000, lambda: display_init_message())

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
            CTkButton(master=error_win, text="RETRY", command=lambda: error_button_event()).pack(expand=True, pady=10, padx=20)

            def error_button_event():
                error_win.destroy()
                start_window.destroy()
                self.start_window()

    def welcome_window(self):
        welcome_window = customtkinter.CTkToplevel()
        welcome_window.title("WELCOME")
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
        message_text = "Welcome to the program that will allow you to deploy and manage multiple instances of Odoo locally using Docker."
        message_label = customtkinter.CTkLabel(master=welcome_window, text=message_text, wraplength=300, font=customtkinter.CTkFont(size=15))
        message_label.pack()

        welcome_window.after(5000, lambda: self.fade_out(welcome_window))

    def help_window(self):
        help_window = customtkinter.CTkToplevel()
        help_window.title("HELP")
        help_window.geometry("500x650")
        help_window.resizable(False, False)
        screen_width = help_window.winfo_screenwidth()
        screen_height = help_window.winfo_screenheight()
        x = (screen_width - 500) // 2
        y = (screen_height - 650) // 2
        help_window.geometry(f"+{x}+{y}")
        help_window.attributes("-topmost", True)

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "imgs")

        # Load image
        image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "help.png")), size=(150, 150))
        image_label = customtkinter.CTkLabel(master=help_window, text="", image=image, pady=5)
        image_label.configure(image=image)
        image_label.pack()

        # Message
        message_text = """                               USEFUL INFORMATION:

        - This program allows you to create, modify, restart, monitor, and delete Odoo instances deployed using Docker.
        - The main window displays all existing Docker containers specifying their current status, thus allowing interaction with them through the corresponding buttons.
        - Detailed information about each of the existing instances can also be obtained in the Info button.
        - To delete an instance, you must first stop it. By performing this action, the selected container will be deleted along with its related information and configuration, but the modules will remain in the corresponding folder.
        - More detailed information can be found in the ‘usage.md’ file present in the app repository or in the root folder of the project. """
        message_label = customtkinter.CTkLabel(master=help_window, text=message_text, wraplength=400, font=customtkinter.CTkFont(size=15), pady=5, anchor="w", justify="left")
        message_label.pack()
        copyright_text = "© Daniel Mederos, 2024. github.com/Daniel-WICKED"
        copyright_label = customtkinter.CTkLabel(master=help_window, text=copyright_text, wraplength=400, font=customtkinter.CTkFont(size=10), pady=25, anchor="w", justify="left")
        copyright_label.pack()


    def main_window(self):
        self.welcome_window()
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
        update_button = customtkinter.CTkButton(sidebar_frame, text="REFRESH", command=self.update_button_event)
        update_button.grid(row=1, column=0, padx=20, pady=10)
        new_button = customtkinter.CTkButton(sidebar_frame, text="NEW INSTANCE", command=self.new_button_event)
        new_button.grid(row=2, column=0, padx=20, pady=10)
        help_button = customtkinter.CTkButton(sidebar_frame, text="HELP", fg_color="#28a745", hover_color="dark green", command=self.help_button_event)
        help_button.grid(row=3, column=0, padx=20, pady=10)
        exit_button = customtkinter.CTkButton(sidebar_frame, text="EXIT", fg_color="#E70000", hover_color="dark red", command=self.exit_button_event)
        exit_button.grid(row=4, column=0, padx=20, pady=(10, 20))

        self.show_containers = customtkinter.CTkScrollableFrame(master=self.main_window_instance, label_text="EXISTING DOCKER CONTAINERS", label_font=customtkinter.CTkFont(size=15, weight="bold"), corner_radius=5, width=750, height=420)
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

    def new_instance(self):
        ## Functions
        def get_next_instance_number():
            info_dir = os.path.join(os.getcwd(), "info")
            if not os.path.exists(info_dir):
                os.makedirs(info_dir)
            files = os.listdir(info_dir)
            instance_numbers = [int(f.split('odoo')[1].split('.')[0]) for f in files if f.startswith('odoo') and f.endswith('.txt')]
            return max(instance_numbers, default=0) + 1

        def create_instance():
            dir = os.getcwd()
            version = version_var.get()
            instance_name = instance_name_var.get()
            admin_password = password_var.get()
            db_filter = db_filter_var.get()
            edition = edicion_var.get()
            if edition == "Community": 
                ent_addons = ""
            elif edition == "Enterprise":
                ent_addons = f"-v {dir}/odoo/ent_addons/{version}:/mnt/extra-addons2:rw "
            instance_number = get_next_instance_number()
            port = 8069 + (instance_number -1)

            instance_name_suffix = f"_{instance_name}" if instance_name else ""
            
            if not admin_password:
                self.error_popup("You must provide an admin password.")
                return
            
            cmd = (
                f"docker run -d --name odoo{instance_number}_{version}{edition}{instance_name_suffix} "
                f"--restart=unless-stopped --network=odoo-network -p {port}:8069 "
                f"-v odoo_data:/var/lib/odoo:rw "
                f"-v {dir}/odoo/odoo{instance_number}.conf:/etc/odoo/odoo.conf "
                f"-v {dir}/odoo/odoo{instance_number}_addons:/mnt/extra-addons:rw "
                f"{ent_addons}odoo:{version}"
            )

            try:
                generate_config(dir, instance_number, db_filter, instance_name_suffix, version, edition, admin_password)
                generate_info_file(dir, instance_number, version, instance_name, port, edition, admin_password, db_filter)
                subprocess.run(cmd, shell=True, check=True)
                self.success_popup(f"Instance Odoo {version} {edition} successfully created, accessible on port {port}")
                self.new_instance_window.destroy()
                self.update_containers()  # Corrected call
            except subprocess.CalledProcessError as e:
                self.error_popup(f"Error creating odoo instance: {e}")

        def generate_config(dir, instance_number, db_filter, instance_name_suffix, version, edition, admin_password):
            conf_text = "[options]\n"
            conf_text += f"; This is the configuration file for Odoo {instance_number}\n"
            conf_text += "addons_path = /mnt/extra-addons"
            if edition == "Enterprise":
                conf_text += ", /mnt/extra-addons2"
            conf_text += "\n"
            conf_text += "data_dir = /var/lib/odoo\n"
            conf_text += f"admin_passwd = {admin_password}\n"
            if db_filter == "No":
                conf_text += ";"
            conf_text += f"dbfilter = ^(.*)odoo{version}_{edition}{instance_name_suffix}$\n"
            conf_text += "db_host = postgres_db\n"
            conf_text += "db_password = pgOd0op4sswOrd\n"
            conf_text += "db_port = 5432\n"
            conf_text += "db_template = template0\n"
            conf_text += "db_user = pgodoouser\n"
            conf_text += "list_db = True\n"

            with open(f"{dir}/odoo/odoo{instance_number}.conf", "w") as conf_file:
                conf_file.write(conf_text)

        def generate_info_file(dir, instance_number, version, instance_name, port, edition, admin_password, db_filter):
            info_dir = os.path.join(dir, "info")
            if not os.path.exists(info_dir):
                os.makedirs(info_dir)

            file_path = os.path.join(info_dir, f"odoo{instance_number}.txt")
            db_filter_status = "Sí" if db_filter == "Sí" else "No"

            with open(file_path, 'w') as info_file:
                info_file.write(f"Nmae: odoo{instance_number}_{version}{edition}{instance_name}\n")
                info_file.write(f"Port: {port}\n")
                info_file.write(f"Version: {version}\n")
                info_file.write(f"Edition: {edition}\n")
                info_file.write(f"Admin password: {admin_password}\n")
                info_file.write(f"DB Filter: {db_filter_status}\n")

        ## UI configuration
        self.new_instance_window = CTkToplevel(self)
        self.new_instance_window.title("CREATE NEW ODOO INSTANCE")
        self.new_instance_window.geometry("400x600")
        self.new_instance_window.resizable(False, False)
        screen_width = self.new_instance_window.winfo_screenwidth()
        screen_height = self.new_instance_window.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 600) // 2
        self.new_instance_window.geometry(f"+{x}+{y}")

        version_var = customtkinter.StringVar(value="16")
        edicion_var = customtkinter.StringVar(value="Community")
        instance_name_var = customtkinter.StringVar(value="")
        password_var = customtkinter.StringVar(value="")
        db_filter_var = customtkinter.StringVar(value="No")

        CTkLabel(self.new_instance_window, text="Choose Odoo version:").pack(pady=10)
        CTkOptionMenu(self.new_instance_window, variable=version_var, values=["14", "15", "16", "17"]).pack(pady=10)
        
        CTkLabel(self.new_instance_window, text="Choose edition:").pack(pady=10)
        CTkOptionMenu(self.new_instance_window, variable=edicion_var, values=["Community", "Enterprise"]).pack(pady=10)

        CTkLabel(self.new_instance_window, text="Name the instance (optional):").pack(pady=10)
        CTkEntry(self.new_instance_window, textvariable=instance_name_var).pack(pady=10)

        CTkLabel(self.new_instance_window, text="Admin password (required):").pack(pady=10)
        CTkEntry(self.new_instance_window, textvariable=password_var, show="*").pack(pady=10)

        CTkLabel(self.new_instance_window, text="Apply filter to the databases?").pack(pady=10)
        CTkOptionMenu(self.new_instance_window, variable=db_filter_var, values=["Sí", "No"]).pack(pady=10)

        CTkButton(self.new_instance_window, text="Create instance", fg_color="#28a745", hover_color="dark green", command=create_instance).pack(pady=20)

    def create_container_row(self, master, name, status, row):
        font = customtkinter.CTkFont(size=15, weight="bold")
        name_label = customtkinter.CTkLabel(master, font=font, text=name.upper(), anchor="w")
        name_label.grid(row=row, column=0, padx=10, pady=(5, 5), sticky="w")

        status_label = customtkinter.CTkLabel(master, text=f"Status: {status}", anchor="w")
        status_label.grid(row=row, column=1, padx=10, pady=(5, 5), sticky="w")

        buttons_frame = customtkinter.CTkFrame(master, fg_color="transparent")
        buttons_frame.grid(row=row, column=2, padx=10, pady=(5, 5), sticky="e")

        # Determine button states based on container status
        is_odoo = "odoo" in name.lower()
        is_running = "Up" in status

        start_button = CTkButton(buttons_frame, text="Start", width=5, command=lambda: self.manage_container(name, "start"))
        start_button.pack(side="left", padx=2)
        start_button.configure(state="disabled" if is_running else "normal")

        stop_button = CTkButton(buttons_frame, text="Stop", width=5, command=lambda: self.manage_container(name, "stop"))
        stop_button.pack(side="left", padx=2)
        stop_button.configure(state="normal" if is_running else "disabled")

        delete_button = CTkButton(buttons_frame, text="Delete", width=5, command=lambda: self.delete_container(name))
        delete_button.pack(side="left", padx=2)
        delete_button.configure(state="disabled" if is_running else "normal")

        logs_button = CTkButton(buttons_frame, text="Logs", width=5, command=lambda: self.container_logs(name))
        logs_button.pack(side="left", padx=2)

        info_button = CTkButton(buttons_frame, text="Info", width=5, command=lambda: self.show_info(name))
        info_button.pack(side="left", padx=2)
        info_button.configure(state="normal" if is_odoo else "disabled")
      
    def delete_container(self, container_name):
        try:
            subprocess.run(["docker", "rm", container_name], check=True)
            
            instance_number = container_name.split('_')[0].replace('odoo', '')

            os.remove(f"odoo/odoo{instance_number}.conf")
            os.remove(f"info/odoo{instance_number}.txt")

            self.success_popup(f"Container {container_name} and related files deleted successfully.")
            self.update_containers()
        except Exception as e:
            self.error_popup(str(e))

    def show_info(self, container_name):
        try:
            instance_number = container_name.split('_')[0].replace('odoo', '')

            with open(f"info/odoo{instance_number}.txt", 'r') as file:
                info_text = file.read()

            info_window = CTkToplevel(self)
            info_window.title(f"Info - {container_name}")
            info_window.geometry("400x380")
            info_window.resizable(False, False)
            screen_width = info_window.winfo_screenwidth()
            screen_height = info_window.winfo_screenheight()
            x = (screen_width - 350) // 2
            y = (screen_height - 320) // 2
            info_window.geometry(f"+{x}+{y}")
            info_window.attributes("-topmost", True)
        
            CTkLabel(info_window, text="INSTANCE INFO", font=customtkinter.CTkFont(size=20, weight="bold")).pack(pady=30)

            info_label = customtkinter.CTkLabel(info_window, text=info_text, wraplength=300, font=customtkinter.CTkFont(size=15), anchor="w", justify="left")
            info_label.pack(pady=10, padx=20, fill="both", expand=True)

            CTkButton(info_window, text="Abrir odoo.conf", command=lambda: self.open_file(f"odoo/odoo{instance_number}.conf")).pack(pady=0)
            CTkButton(info_window, text="Abrir extra-addons", command=lambda: self.open_folder(f"odoo/odoo{instance_number}_addons")).pack(pady=20)

        except Exception as e:
            self.error_popup(str(e))

    def open_file(self, file_path):
        try:
            if os.name == 'nt':  
                os.startfile(file_path)
            elif os.name == 'posix':
                if subprocess.run(["uname", "-s"], capture_output=True, text=True).stdout.strip() == "Darwin":
                    subprocess.run(["open", file_path])
                else:
                    subprocess.run(["xdg-open", file_path]) 
        except Exception as e:
            self.error_popup(str(e))

    def open_folder(self, folder_path):
        try:
            if os.name == 'nt':  
                os.startfile(folder_path)
            elif os.name == 'posix':  
                if subprocess.run(["uname", "-s"], capture_output=True, text=True).stdout.strip() == "Darwin":
                    subprocess.run(["open", folder_path]) 
                else:
                    subprocess.run(["xdg-open", folder_path]) 
        except Exception as e:
            self.error_popup(str(e))

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
        self.new_instance()

    def help_button_event(self):
        self.help_window()

    def exit_button_event(self):
        self.destroy()

    def __init__(self):
        super().__init__()
        self.withdraw()
        self.start_window()
        #self.main_window()

if __name__ == "__main__":
    app = App()
    app.mainloop()
