import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os


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

        # Configurer l'arrière-plan principal
        self.root.configure(bg="#141414")

        # Frame pour le champ de recherche et le bouton
        search_frame = tk.Frame(self.root, bg="#141414")
        search_frame.pack(pady=20)

        tk.Label(
            search_frame,
            text="Rechercher un film :",
            font=("Tahoma", 14, "bold"),
            fg="white",
            bg="#141414"
        ).pack(side="left", padx=10)

        self.search_entry = tk.Entry(search_frame, width=40)
        self.search_entry.pack(side="left", padx=10)

        tk.Button(
            search_frame,
            text="Rechercher",
            font=("Tahoma", 14),
            fg="white",
            bg="#e21219",
            command=self.search_film
        ).pack(side="left", padx=10)

        # Frame pour afficher les images et les titres
        self.display_frame = tk.Frame(self.root, bg="#141414")  # Sauvegardé comme attribut pour actualisation
        self.display_frame.pack(pady=20)

        # Frame pour le bouton de retour à l'accueil
        bottom_frame = tk.Frame(self.root, bg="#141414")
        bottom_frame.pack(pady=20)

        tk.Button(
            bottom_frame,
            text="Retour au menu principal",
            font=("Tahoma", 14),
            fg="white",
            bg="#e21219",
            command=self.create_main_menu
        ).pack()

    def search_film(self):
        # Effacer les anciens résultats
        for widget in self.display_frame.winfo_children():
            widget.destroy()

        # ### Exemple de données codées en dur pour tester ###
        results = [
            {"title": "The Big Bang Theory", "image_path": "img/thebigbangtheory.png"},
            {"title": "Friends", "image_path": "img/friends.png"},
            {"title": "Breaking Bad", "image_path": "img/breakingbad.png"}
        ]

        # ### Code réel pour récupérer les résultats dynamiquement ###
        # keyword = self.search_entry.get().strip().lower()
        # results = self.fetch_series_by_keyword(keyword)  # Méthode à implémenter
        # results = results[:3]  # Garder seulement les 3 premiers résultats

        # Si aucun résultat trouvé
        if not results:
            tk.Label(
                self.display_frame,
                text="Aucun résultat trouvé.",
                font=("Tahoma", 14),
                fg="white",
                bg="#141414"
            ).pack()
            return

        # Hiérarchie des tailles pour le top 3
        sizes = [(200, 300), (150, 225), (100, 150)]  # Taille des images (largeur, hauteur)
        fonts = [("Tahoma", 14, "bold"), ("Tahoma", 12), ("Tahoma", 10)]  # Tailles des polices

        # Afficher chaque résultat avec la hiérarchie visuelle
        for i, result in enumerate(results):
            # Créer un sous-frame pour chaque série
            image_frame = tk.Frame(self.display_frame, bg="#141414")
            image_frame.pack(side="left", padx=20)

            # Charger et afficher l'image
            image_label = tk.Label(image_frame, bg="#141414")
            try:
                if os.path.exists(result["image_path"]):
                    img = Image.open(result["image_path"])
                    img = img.resize(sizes[i])  # Ajuster la taille selon le classement
                    photo = ImageTk.PhotoImage(img)
                    image_label.config(image=photo)
                    image_label.image = photo
                else:
                    image_label.config(text="Image introuvable", fg="red")
            except Exception as e:
                image_label.config(text="Erreur lors du chargement", fg="red")
                print(f"Erreur : {e}")

            image_label.pack()

            # Afficher le titre sous l'image
            title_label = tk.Label(
                image_frame,
                text=result["title"],
                font=fonts[i],
                fg="white",
                bg="#141414",
                anchor="center"
            )
            title_label.pack(pady=10)

    def create_list_screen(self):
        self.clear_screen()
        self.root.configure(bg="#141414")

        # Frame pour le titre et le bouton de retour
        title_frame = tk.Frame(self.root, bg="#141414")
        title_frame.pack(pady=10, fill="x")

        # Titre
        tk.Label(
            title_frame,
            text="Liste des films",
            font=("Tahoma", 22, "bold"),
            fg="white",
            bg="#141414"
        ).pack(side="left", padx=20)

        # Bouton Retour au menu principal
        tk.Button(
            title_frame,
            text="Retour au menu principal",
            font=("Tahoma", 14),
            fg="white",
            bg="#e21219",
            command=self.create_main_menu
        ).pack(side="right", padx=20)

        # Frame pour la liste des films
        films_frame = tk.Frame(self.root, bg="#141414")
        films_frame.pack(pady=20, fill="x")

        # Simule une liste de films
        self.films = [
            {"title": "The Big Bang Theory", "image_path": "img/thebigbangtheory.png", "rating": 4},
            {"title": "Friends", "image_path": "img/friends.png", "rating": 5},
            {"title": "Breaking Bad", "image_path": "img/breakingbad.png", "rating": 3},
        ]

        # Afficher les films
        for film in self.films:
            film_frame = tk.Frame(films_frame, bg="#141414", bd=1, relief="solid")
            film_frame.pack(fill="x", pady=5)

            # Charger et afficher l'image
            img_label = tk.Label(film_frame, bg="#141414")
            try:
                if os.path.exists(film["image_path"]):
                    img = Image.open(film["image_path"])
                    img = img.resize((50, 75))  # Taille réduite
                    photo = ImageTk.PhotoImage(img)
                    img_label.config(image=photo)
                    img_label.image = photo
                else:
                    img_label.config(text="Image introuvable", fg="red", font=("Tahoma", 10))
            except Exception as e:
                img_label.config(text="Erreur", fg="red", font=("Tahoma", 10))
                print(f"Erreur : {e}")
            img_label.pack(side="left", padx=10, pady=5)

            # Titre et note
            details_frame = tk.Frame(film_frame, bg="#141414")
            details_frame.pack(side="left", padx=10, pady=5, fill="x")

            # Titre du film
            tk.Label(
                details_frame,
                text=film["title"],
                font=("Tahoma", 14),
                fg="white",
                bg="#141414",
                anchor="w"
            ).pack(anchor="w")

            # Curseur de notation
            slider_frame = tk.Frame(details_frame, bg="#141414")
            slider_frame.pack(anchor="w", pady=5)

            tk.Label(
                slider_frame,
                text="Note :",
                font=("Tahoma", 12),
                fg="white",
                bg="#141414",
                anchor="w"
            ).pack(side="left")

            note_var = tk.IntVar(value=film["rating"])  # Variable pour la note

        def update_stars(value, star_label):
            """Met à jour les étoiles selon la valeur du curseur."""
            stars = "★" * int(value) + "☆" * (5 - int(value))
            star_label.config(text=stars)

        star_label = tk.Label(
            slider_frame,
            text="★" * film["rating"] + "☆" * (5 - film["rating"]),
            font=("Tahoma", 12),
            fg="yellow",
            bg="#141414"
        )
        star_label.pack(side="left", padx=10)

        slider = tk.Scale(
            slider_frame,
            from_=0,
            to=5,
            orient="horizontal",
            bg="#141414",
            fg="white",
            highlightbackground="#141414",
            variable=note_var,
            command=lambda value, s=star_label: update_stars(value, s)
        )
        slider.pack(side="left")
    

    def choose_film(self):
        film = self.selected_film.get()
        if film:
            self.create_film_screen(film)
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner un film.")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = FilmApp(root)
    root.mainloop()
