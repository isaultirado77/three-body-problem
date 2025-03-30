import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import os

class ThreeBodyAnimation:
    def __init__(self, data, save_path="animations", anim_name="three_body", 
                 show_trails=True, trail_length=100, 
                 body_labels=['Cuerpo 1', 'Cuerpo 2', 'Cuerpo 3'],
                 body_colors=['red', 'blue', 'gray'],
                 body_sizes=[15, 10, 8],
                 title='Problema de Tres Cuerpos'):
        self.data = data
        self.save_path = save_path
        self.anim_name = anim_name
        self.show_trails = show_trails
        self.trail_length = trail_length
        self.body_labels = body_labels
        self.body_colors = body_colors
        self.body_sizes = body_sizes
        self.title = title
        
        # Crear directorio si no existe
        os.makedirs(self.save_path, exist_ok=True)
        
        # Inicializar la figura
        self.fig = plt.figure(figsize=(10, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Configuración inicial del gráfico
        self.setup_plot()
        
        # Inicializar elementos de la animación
        self.init_animation()
    
    def setup_plot(self):
        """Configuración inicial del gráfico 3D."""
        self.ax.set_xlabel('Coordenada X')
        self.ax.set_ylabel('Coordenada Y')
        self.ax.set_zlabel('Coordenada Z')
        self.ax.set_title(self.title)
        
        # Calcular límites para los ejes
        all_x = np.concatenate([self.data['x1'], self.data['x2'], self.data['x3']])
        all_y = np.concatenate([self.data['y1'], self.data['y2'], self.data['y3']])
        all_z = np.concatenate([self.data['z1'], self.data['z2'], self.data['z3']])
        
        max_range = max(all_x.max()-all_x.min(), 
                        all_y.max()-all_y.min(), 
                        all_z.max()-all_z.min()) / 2.0
        
        mid_x = (all_x.max() + all_x.min()) * 0.5
        mid_y = (all_y.max() + all_y.min()) * 0.5
        mid_z = (all_z.max() + all_z.min()) * 0.5
        
        self.ax.set_xlim(mid_x - max_range, mid_x + max_range)
        self.ax.set_ylim(mid_y - max_range, mid_y + max_range)
        self.ax.set_zlim(mid_z - max_range, mid_z + max_range)
        
        # Añadir leyenda
        self.ax.legend(loc='upper right')
    
    def init_animation(self):
        """Inicializa los elementos de la animación."""
        # Crear puntos para los cuerpos
        self.bodies = [
            self.ax.plot([], [], [], 'o', color=self.body_colors[i], 
                         markersize=self.body_sizes[i], label=self.body_labels[i])[0]
            for i in range(3)
        ]
        
        # Crear estelas si están habilitadas
        self.trails = []
        if self.show_trails:
            self.trails = [
                self.ax.plot([], [], [], '-', color=self.body_colors[i], alpha=0.5)[0]
                for i in range(3)
            ]
    
    def update(self, frame):
        """Actualiza la animación para cada frame."""
        # Actualizar posiciones de los cuerpos
        for i, body in enumerate(self.bodies):
            x = self.data[f'x{i+1}'][frame]
            y = self.data[f'y{i+1}'][frame]
            z = self.data[f'z{i+1}'][frame]
            body.set_data([x], [y])
            body.set_3d_properties([z])
        
        # Actualizar estelas si están habilitadas
        if self.show_trails:
            for i, trail in enumerate(self.trails):
                start = max(0, frame - self.trail_length)
                x = self.data[f'x{i+1}'][start:frame+1]
                y = self.data[f'y{i+1}'][start:frame+1]
                z = self.data[f'z{i+1}'][start:frame+1]
                trail.set_data(x, y)
                trail.set_3d_properties(z)
        
        return self.bodies + self.trails
    
    def animate(self, frames=None, interval=250, blit=True):
        if frames is None:
            frames = len(self.data['x1'])
        
        anim = FuncAnimation(
            self.fig, 
            self.update, 
            frames=frames, 
            interval=interval, 
            blit=blit, 
            init_func=lambda: self.bodies + self.trails
        )
        
        save_file = os.path.join(self.save_path, f"{self.anim_name}.gif")
        anim.save(save_file, writer='pillow', fps=30)
        print(f"Animación guardada en: {save_file}")
        
        plt.close()