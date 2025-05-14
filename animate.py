import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter

from mpl_toolkits.mplot3d import Axes3D
import os
import argparse

class ThreeBodyAnimation:
    def __init__(self, data, body_names=['Body 1', 'Body 2', 'Body 3'], 
                 colors=['gold', 'blue', 'gray'], sizes=[100, 40, 20], 
                 trail_length=100, interval=50):
        """
        Inicializa la animación del sistema de tres cuerpos.
        """
        self.data = data
        self.body_names = body_names
        self.colors = colors
        self.sizes = sizes
        self.trail_length = trail_length
        self.interval = interval
        
        # Configurar figura 3D
        self.fig = plt.figure(figsize=(12, 10))
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Inicializar elementos de la animación
        self.bodies = []
        self.trails = []
        
    def init_animation(self):
        """Inicializa los elementos gráficos para la animación."""
        # Calcular límites del gráfico
        all_positions = np.array([
            self.data['x1'], self.data['y1'], self.data['z1'],
            self.data['x2'], self.data['y2'], self.data['z2'],
            self.data['x3'], self.data['y3'], self.data['z3']
        ])
        
        max_range = np.max(np.abs(all_positions)) * 1.1
        
        self.ax.set_xlim([-max_range, max_range])
        self.ax.set_ylim([-max_range, max_range])
        self.ax.set_zlim([-max_range, max_range])
        
        self.ax.set_xlabel('X Position (m)')
        self.ax.set_ylabel('Y Position (m)')
        self.ax.set_zlabel('Z Position (m)')
        self.ax.set_title('Three-Body System Animation')
        
        # Crear cuerpos y trayectorias
        for i, (name, color, size) in enumerate(zip(self.body_names, self.colors, self.sizes)):
            # Cuerpo (punto)
            body, = self.ax.plot([], [], [], 'o', 
                                color=color, markersize=size/10, 
                                label=name)
            # Trayectoria (línea)
            trail, = self.ax.plot([], [], [], '-', 
                                 color=color, alpha=0.5, 
                                 linewidth=1)
            
            self.bodies.append(body)
            self.trails.append(trail)
            
        self.ax.legend(loc='upper right', fontsize=10)
        self.ax.grid(False)
        
        return self.bodies + self.trails
    
    def update(self, frame):
        """Actualiza la animación para cada frame."""
        for i in range(3):
            # Índices para las columnas de posición
            x_idx = 1 + i*3
            y_idx = 2 + i*3
            z_idx = 3 + i*3
            
            # Obtener datos hasta el frame actual
            x = self.data['x'+str(i+1)][:frame+1]
            y = self.data['y'+str(i+1)][:frame+1]
            z = self.data['z'+str(i+1)][:frame+1]
            
            # Mostrar solo los últimos 'trail_length' puntos para el rastro
            start_idx = max(0, frame - self.trail_length)
            
            # Actualizar posición del cuerpo
            self.bodies[i].set_data([x[-1]], [y[-1]])
            self.bodies[i].set_3d_properties([z[-1]])
            
            # Actualizar trayectoria
            self.trails[i].set_data(x[start_idx:frame+1], y[start_idx:frame+1])
            self.trails[i].set_3d_properties(z[start_idx:frame+1])
            
            # Actualizar título con tiempo de simulación
            # time = self.data['time'][frame]
            # self.ax.set_title(f'Three-Body System Animation\nTime: {time:.2f} s')
        
        return self.bodies + self.trails
    
    def animate(self, save=False, filename="three_body_animation"):
        """Ejecuta la animación."""
        frames = len(self.data['time'])
        
        anim = FuncAnimation(
            self.fig, 
            self.update, 
            frames=frames,
            init_func=self.init_animation,
            interval=self.interval,
            blit=False
        )
        
        if save:
            writer = FFMpegWriter(fps=30, bitrate=1800)
            save_path = f"animations/{filename}.mp4"
            print(f"Guardando animación en {save_path}...")
            anim.save(save_path, writer=writer, dpi=200)
        else:
            plt.show()

def load_animate_data(filename="sun_earth_moon_simulation", skip_steps=5):
    """Carga datos submuestreados cada 'skip_steps' pasos"""
    filepath = f"data/{filename}.dat"
    data = np.loadtxt(filepath, comments='#')
    
    # Submuestreo de datos
    data = data[::skip_steps]  # Salta 'skip_steps' pasos
    
    return {
        'time': data[:, 0],
        'x1': data[:, 1], 'y1': data[:, 2], 'z1': data[:, 3],
        'x2': data[:, 4], 'y2': data[:, 5], 'z2': data[:, 6],
        'x3': data[:, 7], 'y3': data[:, 8], 'z3': data[:, 9]
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Animación del problema de tres cuerpos')
    parser.add_argument('--filename', type=str, default='sun_earth_moon_test',
                       help='Nombre base del archivo de datos (sin extensión)')
    parser.add_argument('--names', nargs=3, type=str, default=['Sun', 'Earth', 'Moon'],
                       help='Nombres de los cuerpos (3 nombres)')
    parser.add_argument('--colors', nargs=3, type=str, default=['orange', 'blue', 'gray'],
                       help='Colores para cada cuerpo (3 colores)')
    parser.add_argument('--sizes', nargs=3, type=int, default=[150, 30, 15],
                       help='Tamaños de los marcadores (3 enteros)')
    parser.add_argument('--trail', type=int, default=100,
                       help='Longitud del rastro de trayectoria')
    parser.add_argument('--interval', type=int, default=50,
                       help='Intervalo entre frames en ms')
    parser.add_argument('--save', default=True, action='store_true',
                       help='Guardar animación como MP4 en lugar de mostrar')
    
    args = parser.parse_args()
    
    # Cargar datos
    data = load_animate_data(args.filename)
    
    # Crear y ejecutar animación
    animation = ThreeBodyAnimation(
        data,
        body_names=args.names,
        colors=args.colors,
        sizes=args.sizes,
        trail_length=args.trail,
        interval=args.interval
    )
    
    animation.animate(save=args.save, filename=args.filename)