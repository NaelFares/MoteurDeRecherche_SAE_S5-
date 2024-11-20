import tkinter as tk
from tkinter import messagebox


class FilmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de Films")
        
        # Dimensions de la fenêtre
        width, height = 500, 300  # Ajuste les dimensions comme tu veux
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calcul pour centrer la fenêtre
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # Définir la géométrie
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Configuration globale
        self.root.configure(bg="#141414")  # Couleur de fond de la fenêtre
        # Configuration globale
        self.root.configure(bg="#141414")  # Couleur de fond de la fenêtre
        self.text_color = "#f4f4f4"  # Couleur des textes (blanc)
        self.font_title = ("Tahoma", 16, "bold")  # Police pour les titres
        self.font_normal = ("Tahoma", 12)  # Police standard

        # Initialisation des écrans
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        
        # Dimensions de la fenêtre
        width, height = 500, 300  # Ajuste les dimensions comme tu veux
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calcul pour centrer la fenêtre
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # Définir la géométrie
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # Créer un Canvas pour dessiner un rectangle en fond
        canvas = tk.Canvas(self.root, width=400, height=400, bg="#141414", bd=0, highlightthickness=0)
        canvas.pack(expand=True)

        # Dessiner un rectangle dans le Canvas
        canvas.create_rectangle(60, 50, 350, 250, outline="#f4f4f4", width=2)

        # Créer un conteneur (Frame) pour le formulaire à l'intérieur du rectangle
        form_frame = tk.Frame(self.root, bg="#141414")
        canvas.create_window(205, 150, window=form_frame)  # Positionner le Frame au centre du Canvas (ajusté)

        # Titre centré en gros et blanc
        tk.Label(form_frame, text="S'identifier", font=("Tahoma", 24, "bold"), fg="white", bg="#141414").grid(row=0, column=0, columnspan=2, pady=20)

        # Ligne 1 : Login
        tk.Label(form_frame, text="Login:", font=self.font_normal, bg="#141414", fg=self.text_color).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.login_entry = tk.Entry(form_frame, bg="#313131", fg=self.text_color)
        self.login_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Ligne 2 : Password
        tk.Label(form_frame, text="Password:", font=self.font_normal, bg="#141414", fg=self.text_color).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = tk.Entry(form_frame, show="*", bg="#313131", fg=self.text_color)
        self.password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Bouton "Se connecter", centré sous le formulaire
        tk.Button(form_frame, text="Se connecter", bg="#e21219", font=("Tahoma", 13, "bold"), fg=self.text_color, command=self.check_login).grid(row=3, column=0, columnspan=2, pady=20)

    def check_login(self):
        # Remplacez par une vraie vérification
        if self.login_entry.get() and self.password_entry.get():
            self.create_main_menu()
        else:
            messagebox.showerror("Erreur", "Veuillez remplir les champs Login et Password.")
            
    def logout(self):
        """Réinitialise l'application et ramène l'utilisateur à la page de connexion."""
        self.create_login_screen()

            
    # def check_login(self):
    #     # Récupérer les valeurs des champs
    #     login = self.login_entry.get()
    #     password = self.password_entry.get()

    #     # Exemple de logique de vérification (à adapter à vos besoins)
    #     if login == "admin" and password == "password123":
    #         print("Connexion réussie !")
    #         # Vous pouvez appeler une méthode pour changer d'écran ou afficher un message
    #     else:
    #         print("Login ou mot de passe incorrect")

    def create_main_menu(self):
        self.clear_screen()

        # Dimensions de la fenêtre
        width, height = 800, 600

        # Obtenir les dimensions de l'écran
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculer les coordonnées pour centrer la fenêtre
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Configurer la taille et la position de la fenêtre
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # Ajouter les widgets du menu principal
        tk.Label(self.root, text="Nom de l'application", font=("Tahoma", 20, "bold"), fg="white", bg="#141414").pack(pady=20)

        tk.Button(self.root, text="Rechercher un film", font=("Tahoma", 14), fg="white", bg="#141414", command=self.create_search_screen).pack(pady=10)
        tk.Button(self.root, text="Voir la liste ou noter un film", font=("Tahoma", 14), fg="white", bg="#141414", command=self.create_list_screen).pack(pady=10)
        tk.Button(self.root, text="Deconnexion", font=("Tahoma", 14), fg="white", bg="#e21219", command=self.logout).pack(pady=10)


    def create_search_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Moteur de recherche", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Rechercher:").pack()
        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack()

        tk.Button(self.root, text="Rechercher", command=self.search_film).pack(pady=5)
        tk.Button(self.root, text="Retour au menu principal", command=self.create_main_menu).pack(pady=5)

    def search_film(self):
        query = self.search_entry.get()
        if query:
            # Remplacez par un vrai moteur de recherche
            messagebox.showinfo("Résultat", f"Résultats pour: {query}")
        else:
            messagebox.showerror("Erreur", "Veuillez entrer un terme de recherche.")

    def create_list_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Liste des films", font=("Arial", 16)).pack(pady=10)

        # Simule une liste de films
        self.films = {"film 1": 9, "film 2": 5, "film 3": "X", "film 4": "X"}
        self.selected_film = tk.StringVar(value="")

        for film, note in self.films.items():
            tk.Radiobutton(
                self.root,
                text=f"{film} - Note: {note}",
                variable=self.selected_film,
                value=film,
            ).pack(anchor="w")

        tk.Button(self.root, text="Choisir", command=self.choose_film).pack(pady=5)
        tk.Button(self.root, text="Retour au menu principal", command=self.create_main_menu).pack(pady=5)

    def choose_film(self):
        film = self.selected_film.get()
        if film:
            self.create_film_screen(film)
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner un film.")

    def create_film_screen(self, film):
        self.clear_screen()

        tk.Label(self.root, text=f"Film: {film}", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Noter le film", command=lambda: self.rate_film(film)).pack(pady=5)
        tk.Button(self.root, text="Retour à la liste des films", command=self.create_list_screen).pack(pady=5)

    def rate_film(self, film):
        note = tk.simpledialog.askinteger("Note", f"Entrez une note pour {film} (0-10):", minvalue=0, maxvalue=10)
        if note is not None:
            self.films[film] = note
            messagebox.showinfo("Succès", f"Vous avez noté {film} avec {note}.")
            self.create_list_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = FilmApp(root)
    root.mainloop()
