import json

width_window = 1000
height_window = 600 
FPS = 60 #Velocidad del juego
path_image = ""
DEBUG = False

#Funciones de volumen 
def plus_volume(current_volume):
    if current_volume < 1.0:
        current_volume += 0.05
        return current_volume
    else:
        return current_volume

def less_volume(current_volume):
    if current_volume > 0.0:
        current_volume -= 0.05
        return current_volume
    else:
        return current_volume
    
def read_json_file(file_name):
        """
        La función se encarga de la lectura del archivo que pasemos por parametro y extraer el valor de la clave "jugadores"
        Recibe: self, str que correponde al nombre del archivo
        Devuelve: list[dict]
        """
        try:
            with open(file_name, "r", encoding = "utf-8") as file:
                loaded_file = json.load(file)
                # lista_jugadores_uno = loaded_file.get("jugadores", "no se obtuvo lista de jugadores")
                return loaded_file
        except Exception:
            print(f"Error trying to open {file_name}")