import tkinter as tk
from tkinter import messagebox


class FilmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de Films")

        # Initialisation des écrans
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="CONNEXION", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="Login:").pack()
        self.login_entry = tk.Entry(self.root)
        self.login_entry.pack()

        tk.Label(self.root, text="Password:").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Se connecter", command=self.check_login).pack(pady=10)

    def check_login(self):
        # Remplacez par une vraie vérification
        if self.login_entry.get() and self.password_entry.get():
            self.create_main_menu()
        else:
            messagebox.showerror("Erreur", "Veuillez remplir les champs Login et Password.")

    def create_main_menu(self):
        self.clear_screen()

        tk.Label(self.root, text="MENU PRINCIPAL", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Rechercher un film", command=self.create_search_screen).pack(pady=5)
        tk.Button(self.root, text="Voir la liste ou noter un film", command=self.create_list_screen).pack(pady=5)

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
