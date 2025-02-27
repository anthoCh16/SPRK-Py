import time
import asyncio
import threading
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color

# Variable global para almacenar el ángulo del giroscopio (simulado)
giroscopio_angulo = 0

# Función simulada para leer datos del giroscopio de la prótesis
def leer_giroscopio_simulado():
    global giroscopio_angulo
    while True:
        # Aquí deberías reemplazar la simulación por la lectura real via Bluetooth.
        # Por ejemplo, actualizamos el ángulo entre 0 y 360.
        giroscopio_angulo = (giroscopio_angulo + 10) % 360
        print(f"Ángulo del giroscopio: {giroscopio_angulo}")
        time.sleep(1)

# Función para controlar el Sphero usando la API SpheroEduAPI
def controlar_sphero():
    # Descubre el dispositivo Sphero
    toy = scanner.find_toy()
    
    # Conecta y controla el Sphero en el contexto de SpheroEduAPI
    with SpheroEduAPI(toy) as droid:
        # Cambia el LED principal a azul para indicar que está activo
        droid.set_main_led(Color(r=0, g=0, b=255))
        print("Conectado al Sphero y LED encendido en azul.")
        
        while True:
            # Usamos el ángulo del giroscopio para determinar la dirección
            direccion = giroscopio_angulo  # en grados
            velocidad = 60  # velocidad fija; puedes ajustar según tu lógica
            
            # Enviamos el comando de movimiento: en la API SpheroEduAPI se utiliza set_speed.
            # Nota: La API SpheroEduAPI puede requerir comandos adicionales o tener otra forma de especificar dirección.
            # Si existe un comando específico para girar en una dirección, úsalo. En este ejemplo, solo activamos la velocidad.
            droid.set_speed(velocidad)
            print(f"Moviendo Sphero a velocidad {velocidad} con dirección {direccion}°")
            
            # Espera un tiempo breve antes de actualizar el comando
            time.sleep(1)
            
            # Para simular, detenemos el movimiento cada ciclo breve y luego lo volvemos a enviar
            droid.set_speed(0)
            time.sleep(0.5)

# Inicia un hilo para simular la lectura del giroscopio (en paralelo)
hilo_giroscopio = threading.Thread(target=leer_giroscopio_simulado, daemon=True)
hilo_giroscopio.start()

# Ejecuta el control del Sphero (bloqueante mientras esté activo)
controlar_sphero()