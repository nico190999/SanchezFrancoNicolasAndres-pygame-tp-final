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