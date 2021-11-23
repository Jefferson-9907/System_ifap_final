# Import Modules
import random
from _datetime import datetime
from time import strftime
from tkinter import *
from tkinter import messagebox

import connection
import database_connected
import users_registration

import login_form
import Principal_Window_S
import Student_Window_S
import Matricula_Window_S
import Assesor_Window_S
import Course_Window_S
import Paralelo_Window_S


class Password_S:
    def __init__(self, root):
        self.root = root
        self.root.title("SYST_CONTROL--›Usuarios")
        self.root.attributes('-fullscreen', True)
        self.root.resizable(False, False)
        self.root.iconbitmap('recursos\\ICONO_SIST_CONTROL (IFAP®)2.0.ico')
        self.root.configure(bg='#a27114')

        imagenes = {
            'nuevo': PhotoImage(file='recursos\\icon_aceptar.png'),
            'matricular': PhotoImage(file='recursos\\icon_add.png'),
            'editar': PhotoImage(file='recursos\\icon_update.png'),
            'eliminar': PhotoImage(file='recursos\\icon_del.png'),
            'limpiar': PhotoImage(file='recursos\\icon_clean.png'),
            'buscar': PhotoImage(file='recursos\\icon_buscar.png'),
            'todo': PhotoImage(file='recursos\\icon_ver_todo.png'),
            'actualizar': PhotoImage(file='recursos\\icon_upd.png')

        }

        # =============================================================
        # BANNER PANTALLA ASESORES
        # =============================================================

        self.txt = "SYSTEM CONTROL IFAP (ASESORES)"
        self.count = 0
        self.text = ''
        self.color = ["#4f4e4d", "#f29844", "red2"]
        self.heading = Label(self.root, text=self.txt, font=("Cooper Black", 35), bg="#000000",
                             fg='black', bd=5, relief=FLAT)
        self.heading.place(x=0, y=0, width=1367)

        self.slider()
        self.heading_color()

        # ======================Backend connection=============
        self.db_connection = connection.DatabaseConnection()

        # =============================================================
        # CREACIÓN DE LA BARRA DE MENÚ
        # =============================================================
        self.menubarra = Menu(self.root)

        # =============================================================
        # CREACIÓN DEL MENÚ
        # =============================================================
        self.menubarra.add_cascade(label='ASESORES')
        self.root.config(menu=self.menubarra)
        self.menus = Menu(self.root)
        self.Column1 = Menu(self.menus, tearoff=0)

        # =============================================================
        # AÑADIENDO OPCIONES AL MENÚ PRINCIPAL
        # =============================================================
        self.menus.add_cascade(label='INICIO', menu=self.Column1)
        self.Column1.add_command(label='Menú Inicio', command=self.principal_btn)
        self.Column2 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # AÑADIENDO OPCIONES AL MENÚ ALUMNO
        # =============================================================
        self.menus.add_cascade(label='ALUMNOS', menu=self.Column2)
        self.Column2.add_command(label='Alumnos', command=self.student_btn)
        self.Column2.add_command(label='Matriculación', command=self.matricula_btn)
        self.Column3 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # CREACIÓN DEL MENÚ ASESORES
        # =============================================================
        self.menus.add_cascade(label='ASESORES', menu=self.Column3)
        self.Column4 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # CREACIÓN DEL DE MENÚ CURSOS
        # =============================================================
        self.menus.add_cascade(label='CURSOS', menu=self.Column4)
        self.Column4.add_command(label='Cursos', command=self.courses_btn)
        self.Column4.add_command(label='Paralelos', command=self.paralelos_btn)
        self.Column5 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # CREACIÓN DEL DE MENÚ AYUDA
        # =============================================================
        self.menus.add_cascade(label='USUARIOS', menu=self.Column5)
        self.Column5.add_command(label='Cambiar Usuario', command=self.logout)
        self.Column5.add_command(label='Cambiar Contraseña', command=self.principal_btn)
        self.Column5.add_separator()
        self.Column5.add_command(label='Cerrar Sesión', command=self.salir_principal)
        self.Column5.add_separator()
        self.Column6 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # CREACIÓN DEL DE MENÚ INFO
        # =============================================================
        self.menus.add_cascade(label='INFO', menu=self.Column6)
        self.Column6.add_command(label='Sobre SIST_CONTROL (IFAP®)', command=self.caja_info_sist)
        self.Column6.add_separator()
        self.root.config(menu=self.menus)

        # =============================================================
        # CREACIÓN DE PIÉ DE PANTALLA
        # =============================================================
        self.footer_4 = Label(self.root, text='J.C.F DESING® | Derechos Reservados 2021', width=195, bg='black',
                              fg='white')
        self.footer_4.place(x=0, y=725)

        data = datetime.now()
        fomato_f = " %A %d/%B/%Y"

        self.footer = Label(self.root, text='  FECHA Y HORA: ', font=("Cooper Black", 9), bg='black',
                            fg='white')
        self.footer.place(x=930, y=725)
        self.footer_1 = Label(self.root, text=str(data.strftime(fomato_f)), font=("Lucida Console", 10), bg='black',
                              fg='white')
        self.footer_1.place(x=1040, y=727)

        self.clock = Label(self.root)
        self.clock['text'] = '00:00:00'
        self.clock['font'] = 'Tahoma 9 bold'
        self.clock['bg'] = 'black'
        self.clock['fg'] = 'white'
        self.clock.place(x=1275, y=725)
        self.tic()
        self.tac()

        # Manage Frame
        self.Manage_Frame = Frame(self.root, relief=RIDGE, bd=4, bg='#a27114')
        self.Manage_Frame.place(x=375, y=200, width=600, height=300)

        self.m_title = Label(self.Manage_Frame, text="-ADMINISTAR USUARIOS-\nCAMBIAR CONTRASEÑA",
                             font=("Copperplate Gothic Bold", 16, "bold"), bg='#a27114', fg="White")
        self.m_title.grid(row=0, column=0, columnspan=1, padx=130, pady=30)

        # Variables
        self.username = StringVar()
        self.old_password = StringVar()
        self.new_password = StringVar()
        self.new_password_r = StringVar()

        self.User_Frame = Frame(self.Manage_Frame, bg='#a27114')
        self.User_Frame.place(x=100, y=100, width=350, height=150)

        self.lbl_us = Label(self.User_Frame, text="USUARIO", width='10', font=('Copperplate Gothic Bold', 10),
                            bg='#808080', fg="#0A090C")
        self.lbl_us.grid(row=1, column=0, padx=0, pady=5, sticky="E")

        self.e_us = Entry(self.User_Frame, textvariable=self.username, bd=5, relief=GROOVE)
        self.e_us.grid(row=1, column=1, padx=10, pady=5, sticky="W")
        self.e_us.focus()

        self.l_c_ant = Label(self.User_Frame, text="CONTRASEÑA ANTERIOR", font=('Copperplate Gothic Bold', 10),
                             bg='#808080', fg="#0A090C")
        self.l_c_ant.grid(row=2, column=0, padx=0, pady=5, sticky="S")

        self.e_c_ant = Entry(self.User_Frame, show="*", textvariable=self.old_password, bd=5, relief=GROOVE)
        self.e_c_ant.grid(row=2, column=1, padx=10, pady=5, sticky="W")

        self.l_n_cont = Label(self.User_Frame, text="NUEVA CONTRASEÑA", font=('Copperplate Gothic Bold', 10),
                              bg='#808080', fg="#0A090C")
        self.l_n_cont.grid(row=3, column=0, padx=0, pady=5, sticky="E")

        self.e_n_cont = Entry(self.User_Frame, show="*", textvariable=self.new_password, bd=5, relief=GROOVE)
        self.e_n_cont.grid(row=3, column=1, padx=10, pady=5, sticky="W")

        self.l_n_cont_r = Label(self.User_Frame, text="REPITA CONTRASEÑA", font=('Copperplate Gothic Bold', 10),
                                bg='#808080', fg="#0A090C")
        self.l_n_cont_r.grid(row=4, column=0, padx=0, pady=5, sticky="E")

        self.e_n_cont_r = Entry(self.User_Frame, show="*", textvariable=self.new_password_r, bd=5, relief=GROOVE)
        self.e_n_cont_r.grid(row=4, column=1, padx=10, pady=5, sticky="W")

        self.chg_btn = Button(self.Manage_Frame, image=imagenes['nuevo'], text='CAMBIAR CONTRASEÑA', width=150,
                              command=self.change_pass, compound="right")
        self.chg_btn.image = imagenes['nuevo']
        self.chg_btn.place(x=225, y=250)

    def tic(self):
        self.clock["text"] = strftime("%H:%M:%S %p")

    def tac(self):
        self.tic()
        self.clock.after(1000, self.tac)

    def slider(self):
        """creates slides for heading by taking the text,
        and that text are called after every 100 ms"""
        if self.count >= len(self.txt):
            self.count = -1
            self.text = ''
            self.heading.config(text=self.text)

        else:
            self.text = self.text + self.txt[self.count]
            self.heading.config(text=self.text)
        self.count += 1

        self.heading.after(100, self.slider)

    def heading_color(self):
        """
        configures heading label
        :return: every 50 ms returned new random color.

        """
        fg = random.choice(self.color)
        self.heading.config(fg=fg)
        self.heading.after(50, self.heading_color)

    def change_pass(self):
        if self.username.get() == '':
            messagebox.showerror("SYST_CONTROL(IFAP®) (ERROR)", "POR FAVOR INGRESE EL CAMPO: USUARIO")
        elif self.old_password.get() == "":
            messagebox.showerror("SYST_CONTROL(IFAP®) (ERROR)", "POR FAVOR INGRESE EL CAMPO: CONTRASEÑA ANTERIOR")

        elif self.new_password.get() == "":
            messagebox.showerror("SYST_CONTROL(IFAP®) (ERROR)", "POR FAVOR INGRESE EL CAMPO: CONTRASEÑA NUEVA")

        else:
            username = self.username.get()
            userpassword = self.old_password.get()

            obj_login_users = database_connected.GetDatabase('use ddbb_sys_ifap;')
            self.db_connection.create(obj_login_users.get_database())

            query = "select * from usuarios where usuario=%s;"
            values = username
            data = self.db_connection.search(query, (values,))

            if data:
                query = "select * from usuarios where contrasena=%s;"
                values = userpassword
                data = self.db_connection.search(query, (values,))

                if data:
                    try:
                        obj_students_database = users_registration.GetDatabase('use ddbb_sys_ifap;')
                        self.db_connection.create(obj_students_database.get_database())

                        query = f"""UPDATE usuarios SET contrasena=%s WHERE usuario=%s"""

                        values = (self.new_password.get(), self.username.get())
                        self.db_connection.update(query, values)

                        messagebox.showinfo("SYST_CONTROL(IFAP®)-->(ÉXITO)", "CAMBIO DE CONTRASEÑA EXITOSO\nUSUARIO: " +
                                            self.username.get() + "\nCONTRASEÑA: " + self.new_password.get())
                        messagebox.showwarning("SYST_CONTROL(IFAP®)-->(RE-INGRESO)", "UD REALIZÓ UN CAMBIO DE "
                                                                                     "CONTRASEÑA RECIENTEMENTE\n"
                                                                                     "DEBE DE INGRESAR NUEVAMENTE")
                        self.logout()

                    except BaseException as msg:
                        messagebox.showerror("SYST_CONTROL(IFAP®)-->(ERROR)",
                                             f"NO FUÉ POSIBLE CONECTARSE CON EL SERVIDOR,\n"
                                             f"REVISE LA CONEXIÓN: {msg}")

                else:
                    messagebox.showwarning("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)", f"CONTRASEÑA NO VÁLIDA")
                    self.old_password.set("")
                    self.e_c_ant.focus()

            else:
                messagebox.showwarning("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)", f"USUARIO NO VÁLIDO")
                self.username.set("")
                self.e_us.focus()

    def limpiar(self):
        self.username.set('')
        self.old_password.set('')
        self.new_password.set('')
        self.e_us.focus()

    def logout(self):
        root = Toplevel()
        login_form.Login(root)
        self.root.withdraw()
        root.deiconify()

    def student_btn(self):
        root = Toplevel()
        Student_Window_S.Student_S(root)
        self.root.withdraw()
        root.deiconify()

    def matricula_btn(self):
        root = Toplevel()
        Matricula_Window_S.Matricula_S(root)
        self.root.withdraw()
        root.deiconify()

    def assesor_btn(self):
        root = Toplevel()
        Assesor_Window_S.Assesor_S(root)
        self.root.withdraw()
        root.deiconify()

    def courses_btn(self):
        root = Toplevel()
        Course_Window_S.Course_S(root)
        self.root.withdraw()
        root.deiconify()

    def paralelos_btn(self):
        root = Toplevel()
        Paralelo_Window_S.Paralelo_S(root)
        self.root.withdraw()
        root.deiconify()

    def principal_btn(self):
        root = Toplevel()
        Principal_Window_S.Principal_S(root)
        self.root.withdraw()
        root.deiconify()

    def salir_principal(self):
        self.sa = messagebox.askyesno('CERRAR SESIÓN', 'CERRAR SYST_CONTROL(IFAP®)')
        if self.sa:
            raise SystemExit

    # =============================================================
    # FUNCIÓN CAJA DE INFORMACIÓN DEL INSTITUTO(INFO)
    # =============================================================
    def caja_info_ifap(self):
        self.men1 = messagebox.showinfo('SIST_CONTROL (IFAP®)', 'INSTITUTO DE FORMACIÓN ACADEMICA PROEZAS(IFAP®)')

    # =============================================================
    # FUNCIÓN CAJA DE INFORMACIÓN DEL SISTEMA(INFO)
    # =============================================================
    def caja_info_sist(self):
        self.men2 = messagebox.showinfo('SIST_CONTROL (IFAP®)',
                                        'SIST_CONTROL (IFAP®) v2.0\n'
                                        'El uso de este software queda sujeto a los términos y condiciones del '
                                        'contrato "BJM DESING®-CLIENTE".    \n'
                                        'El uso de este software queda sujeto a su contrato. No podrá utilizar '
                                        'este software para fines de distribución\n'
                                        'total o parcial.\n\n\n© 2021 BJM DESING®. Todos los derechos reservados')


if __name__ == '__main__':
    root = Tk()
    application = Password_S(root)
    root.mainloop()
