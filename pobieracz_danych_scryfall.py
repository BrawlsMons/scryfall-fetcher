    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog
    import requests
    import json
    from PIL import Image, ImageTk
    import io

    class PobieraczDanychScryfall:
        def __init__(self, root):
            self.root = root
            self.root.title("Złodziej ze Scryfall")
            self.root.geometry("900x600")
            self.root.configure(bg="#2C0042")

            # Ładowanie tła
            response = requests.get("https://d1mehngj2gp76v.cloudfront.net/k90dku%2Fpreview%2F66931092%2Fmain_large.png?response-content-disposition=inline%3Bfilename%3D%22main_large.png%22%3B&response-content-type=image%2Fpng&Expires=1746643996&Signature=B11mutvpGKAhXvrSxgh7eMU~uFmfqnSsWMQ8-LPUNQOcAEhfQ6Pqke8hrqyKzMTYhHKn7ZSoVNo-8NrsYR-QMH94wxLNUCrLHoE2rXrH27WsOokpoRHF-RvGBX-Fpfx7PLy76vUYvl0~VVox~xgH-YW7-A~ZWLG8tNptPZIKWgiaf7KOGSWN3Hw6qw38hpceIPxtX9YfVhfmn9ozi74qvx6lbkR27vDqkM8BopAxzmCVzNC4y~LWm3ZnEivVBctv~Fttc7W6k-w7cG0I7wWp6PS0DnEsgCPcK9JN9hX1JK8u7vSk6BIUJM1e6MFRquiXs1b0-UGIdI5jxPxw0t6bJQ__&Key-Pair-Id=APKAJT5WQLLEOADKLHBQ")
            image_data = response.content
            image = Image.open(io.BytesIO(image_data))
            image = image.resize((900, 600), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(image)
            bg_label = tk.Label(root, image=self.bg_image)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)

            # Nagłówek
            naglowek = tk.Label(root, text="Pobieracz Danych ze Scryfall", font=("Arial", 24, "bold"), fg="#00FFFF", bg="#2C0042", bd=0)
            naglowek.place(x=20, y=20)

            # Ramka
            ramka = tk.Frame(root, bg="#420063", bd=0)
            ramka.place(x=20, y=80, width=860, height=500)

            # Etykieta i lista rozwijana
            tk.Label(ramka, text="Wybierz zestaw:", font=("Arial", 14), fg="white", bg="#420063").place(x=20, y=20)
            self.lista_zestawow = ttk.Combobox(ramka, values=[], state="readonly", width=40, font=("Arial", 12))
            self.lista_zestawow.place(x=150, y=20)
            self.zestawy_mapa = {}  # mapowanie
            self.laduj_zestawy()

            # Styl dla przycisków
            style = ttk.Style()
            style.configure("Custom.TButton", font=("Arial", 12), padding=0, background="#FF69B4", foreground="black")
            style.map("Custom.TButton", background=[("active", "#FF85C1")])

            # Przycisk "Pobierz i Zapisz"
            przycisk_pobierz = ttk.Button(ramka, text="Pobierz i Zapisz", style="Custom.TButton", command=self.pobierz_dane)
            przycisk_pobierz.place(x=600, y=20, width=200, height=40)

            # Pole tekstowe z info
            self.tekst_info = tk.Text(ramka, height=20, width=90, bg="#2C0042", fg="white", font=("Arial", 12), bd=0, relief="flat", wrap="word")
            self.tekst_info.insert(tk.END, "Wybierz zestaw Magic: The Gathering z listy.\nKliknij 'Pobierz i Zapisz', żeby ściągnąć dane i zapisać je jako plik JSON.\nDane będą zawierały wszystkie karty z wybranego zestawu.")
            self.tekst_info.config(state="disabled")
            self.tekst_info.place(x=20, y=80)

        def laduj_zestawy(self):
            try:
                odpowiedz = requests.get("https://api.scryfall.com/sets")
                dane = odpowiedz.json()
                zestawy = []
                for dane_zestawu in dane["data"]:
                    nazwa = dane_zestawu["name"]
                    kod = dane_zestawu["code"]
                    self.zestawy_mapa[nazwa] = kod
                    zestawy.append(nazwa)
                self.lista_zestawow['values'] = zestawy
                self.lista_zestawow.current(0)
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się załadować zestawów: {e}")

        def pobierz_dane(self):
            if not self.lista_zestawow.get():
                messagebox.showwarning("Uwaga", "Wybierz jakiś zestaw!")
                return

            file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Pliki JSON", "*.json")], title="Zapisz plik JSON")
            if not file_path:
                return

            wybrany_zestaw = self.lista_zestawow.get()
            set_code = self.zestawy_mapa.get(wybrany_zestaw)
            if not set_code:
                messagebox.showerror("Błąd", "Nie znaleziono kodu dla wybranego zestawu!")
                return

            try:
                wszystkie_karty = []
                url = f"https://api.scryfall.com/cards/search?order=set&q=e:{set_code}"
                while url:
                    odpowiedz = requests.get(url)
                    dane = odpowiedz.json()
                    wszystkie_karty.extend(dane["data"])
                    # Obsługa paginacji
                    if dane.get("has_more"):
                        url = dane.get("next_page")
                    else:
                        url = None

                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(wszystkie_karty, f, indent=4, ensure_ascii=False)
                messagebox.showinfo("Sukces", f"Dane zapisane do {file_path}")
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się pobrać danych: {e}")

    if __name__ == "__main__":
        root = tk.Tk()
        app = PobieraczDanychScryfall(root)
        root.mainloop()