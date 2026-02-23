import tkinter as tk
from tkinter import ttk, messagebox
from tkintermapview import TkinterMapView
import requests
from PIL import Image, ImageTk
from io import BytesIO
import threading
from geopy.geocoders import Nominatim
import json

class WorldMapApp(tk.Tk):
    """Главное окно приложения"""
    def __init__(self):
        super().__init__()
        self.title("Интерактивная карта мира")
        self.geometry("1200x700")
        self.configure(bg="#f0f0f0")
        
        self.default_font = ("Arial", 10)
        self.option_add("*Font", self.default_font)
        
        self.info_frame = tk.Frame(self, bg="white", relief=tk.SUNKEN, borderwidth=2, width=300)
        self.info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        self.info_frame.pack_propagate(False)
        
        tk.Label(self.info_frame, text="Информация о стране", font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        
        self.flag_label = tk.Label(self.info_frame, bg="white")
        self.flag_label.pack(pady=5)
        
        self.country_name_var = tk.StringVar(value="---")
        tk.Label(self.info_frame, text="Страна:", font=("Arial", 12), bg="white").pack(anchor=tk.W, padx=10)
        tk.Label(self.info_frame, textvariable=self.country_name_var, font=("Arial", 12, "bold"), bg="white", wraplength=280, justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=(0,10))
        
        self.currency_var = tk.StringVar(value="---")
        tk.Label(self.info_frame, text="Валюта:", font=("Arial", 12), bg="white").pack(anchor=tk.W, padx=10)
        tk.Label(self.info_frame, textvariable=self.currency_var, font=("Arial", 12, "bold"), bg="white", wraplength=280, justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=(0,10))
        
        self.population_var = tk.StringVar(value="---")
        tk.Label(self.info_frame, text="Население:", font=("Arial", 12), bg="white").pack(anchor=tk.W, padx=10)
        tk.Label(self.info_frame, textvariable=self.population_var, font=("Arial", 12, "bold"), bg="white", wraplength=280, justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=(0,10))
        
        self.status_var = tk.StringVar(value="Готов к работе")
        self.status_label = tk.Label(self, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.map_frame = tk.Frame(self, bg="gray")
        self.map_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5,0), pady=5)
        
        self.map_widget = TkinterMapView(self.map_frame, corner_radius=5)
        self.map_widget.pack(fill=tk.BOTH, expand=True)
        
        self.map_widget.set_position(20.0, 0.0)
        self.map_widget.set_zoom(2)

        self.add_initial_markers()
        
        self.map_widget.add_right_click_menu_command("Получить информацию о стране", self.get_country_from_coords)
        
        self.geolocator = Nominatim(user_agent="world_map_app")
    
    def add_initial_markers(self):
        """Добавляет маркеры для нескольких ключевых стран"""
        countries = [
            {"name": "Россия", "code": "RU", "lat": 61.5240, "lng": 105.3188},
            {"name": "США", "code": "US", "lat": 37.0902, "lng": -95.7129},
            {"name": "Китай", "code": "CN", "lat": 35.8617, "lng": 104.1954},
            {"name": "Франция", "code": "FR", "lat": 46.2276, "lng": 2.2137},
            {"name": "Бразилия", "code": "BR", "lat": -14.2350, "lng": -51.9253},
            {"name": "Австралия", "code": "AU", "lat": -25.2744, "lng": 133.7751},
        ]
        for country in countries:
            marker = self.map_widget.set_marker(
                country["lat"], country["lng"],
                text=country["name"],
                command=self.on_marker_click,
                data=country["code"]
            )
    
    def on_marker_click(self, marker):
        """Обработчик клика по маркеру"""
        country_code = marker.data
        self.status_var.set(f"Загрузка данных для страны с кодом {country_code}...")
        threading.Thread(target=self.fetch_country_info_by_code, args=(country_code,), daemon=True).start()
    
    def get_country_from_coords(self, coords):
        """Обработчик правого клика на карте: определяет страну по координатам"""
        lat, lng = coords
        self.status_var.set(f"Определение страны по координатам ({lat:.4f}, {lng:.4f})...")
        threading.Thread(target=self.reverse_geocode, args=(lat, lng), daemon=True).start()
    
    def reverse_geocode(self, lat, lng):
        """Обратное геокодирование через Nominatim (в потоке)"""
        try:
            location = self.geolocator.reverse(f"{lat}, {lng}", language='en', timeout=10)
            if location and 'country_code' in location.raw:
                country_code = location.raw['country_code'].upper()
                self.after(0, lambda: self.status_var.set(f"Найдена страна: {country_code}. Загрузка данных..."))
                self.fetch_country_info_by_code(country_code)
            else:
                self.after(0, lambda: self.show_error("Не удалось определить страну по данным координатам."))
        except Exception as e:
            self.after(0, lambda: self.show_error(f"Ошибка геокодирования: {str(e)}"))
    
    def fetch_country_info_by_code(self, country_code):
        """Запрос информации о стране через REST Countries API (в потоке)"""
        try:
            url = f"https://restcountries.com/v3.1/alpha/{country_code}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data and isinstance(data, list) and len(data) > 0:
                country_data = data[0]
                name_rus = country_data.get("translations", {}).get("rus", {}).get("common", country_data.get("name", {}).get("common", "Неизвестно"))
                currencies = country_data.get("currencies", {})
                if currencies:
                    currency_names = [v.get("name", "") for k, v in currencies.items()]
                    currency_str = ", ".join(currency_names)
                else:
                    currency_str = "Нет данных"
                population = country_data.get("population", 0)
                population_str = f"{population:,}".replace(",", " ")
                
                flag_url = country_data.get("flags", {}).get("png")
                
                self.after(0, self.update_info_panel, name_rus, currency_str, population_str, flag_url)
            else:
                self.after(0, lambda: self.show_error("Страна не найдена в базе данных."))
        except requests.exceptions.RequestException as e:
            self.after(0, lambda: self.show_error(f"Ошибка сети: {str(e)}"))
        except Exception as e:
            self.after(0, lambda: self.show_error(f"Ошибка обработки данных: {str(e)}"))
    
    def update_info_panel(self, country_name, currency, population, flag_url):
        """Обновление элементов интерфейса на главном потоке"""
        self.country_name_var.set(country_name)
        self.currency_var.set(currency)
        self.population_var.set(population)
        self.status_var.set(f"Информация загружена для {country_name}")
        
        if flag_url:
            threading.Thread(target=self.load_flag_image, args=(flag_url,), daemon=True).start()
        else:
            self.flag_label.config(image='', text="[Флаг не найден]", compound=tk.CENTER)
    
    def load_flag_image(self, url):
        """Загрузка изображения флага из URL и отображение в label (в потоке)"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            img_data = BytesIO(response.content)
            pil_image = Image.open(img_data)
            pil_image.thumbnail((280, 150), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(pil_image)
            self.after(0, lambda: self.flag_label.config(image=photo, text=''))
            self.flag_label.image = photo
        except Exception as e:
            self.after(0, lambda: self.flag_label.config(image='', text=f"[Ошибка загрузки флага]", compound=tk.CENTER))
    
    def show_error(self, message):
        """Отображение сообщения об ошибке"""
        messagebox.showerror("Ошибка", message)
        self.status_var.set("Ошибка при выполнении операции.")

if __name__ == "__main__":
    app = WorldMapApp()
    app.mainloop()