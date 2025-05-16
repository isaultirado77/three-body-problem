import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os


def plot_3d_trajectories(data, body_names=['Body 1', 'Body 2', 'Body 3'], 
                         colors=['Orange', 'blue', 'gray'],
                         body_sizes=[150, 30, 15],
                         inital_final = False,
                         show=False, save=False, filename="three_body_simulation"):
    """
    Grafica las trayectorias 3D de los tres cuerpos.    
    """
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Trayectorias
    for i, (color, name) in enumerate(zip(colors, body_names), 1):
        ax.plot(data[f'x{i}'], data[f'y{i}'], data[f'z{i}'], 
                color=color, linewidth=1.5, label=f'{name} Trajectory')
    
    # Posiciones iniciales y finales
    if inital_final: 
        for i, (color, name, size) in enumerate(zip(colors, body_names, body_sizes), 1):
            # Punto inicial
            ax.scatter(data[f'x{i}'][0], data[f'y{i}'][0], data[f'z{i}'][0],
                    color=color, s=size, marker='o', label=f'{name} Start')
            # Punto final
            ax.scatter(data[f'x{i}'][-1], data[f'y{i}'][-1], data[f'z{i}'][-1],
                    color=color, s=size, marker='s', label=f'{name} End')
    
    ax.set_xlabel('X Position (m)')
    ax.set_ylabel('Y Position (m)')
    ax.set_zlabel('Z Position (m)')
    ax.set_title('Three-Body System Trajectories')
    ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1))
    
    ax.view_init(elev=30, azim=45)
    ax.grid(True)

    if save:
        os.makedirs("plots", exist_ok=True)
        imname = f"_{filename}" if filename else ""
        plt.savefig(f"plots/trayectorias_3d{imname}.png", dpi=300, bbox_inches='tight')
        print(f"Gráfico guardado en plots/trayectorias_3d{imname}.png")
    
    if show:
        plt.show()
    
    plt.close()

def plot_energy_momentum(data, body_names=['Sun', 'Earth', 'Moon'], show=False, save=False, filename=""):
    """Grafica energías y momento angular del sistema."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    
    # Energías
    ax1.plot(data['time'], data['E_kin'], 'b-', label='Kinetic Energy', linewidth=1.5)
    ax1.plot(data['time'], data['E_pot'], 'r-', label='Potential Energy', linewidth=1.5)
    ax1.plot(data['time'], data['E_tot'], 'g--', label='Total Energy', linewidth=2.0)
    
    ax1.set_ylabel('Energy (J)')
    ax1.set_title(f'Energy and Angular Momentum Conservation\nSystem: {", ".join(body_names)}')
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.6)
    
    # Momento Angular
    ax2.plot(data['time'], data['Lx'], 'c-', label='Lx', linewidth=1.0)
    ax2.plot(data['time'], data['Ly'], 'm-', label='Ly', linewidth=1.0)
    ax2.plot(data['time'], data['Lz'], 'y-', label='Lz', linewidth=1.0)
    ax2.plot(data['time'], np.sqrt(data['Lx']**2 + data['Ly']**2 + data['Lz']**2), 
             'k--', label='|L|', linewidth=2.0)
    
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Angular Momentum (kg m²/s)')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.6)
    
    plt.tight_layout()

    if save:
        os.makedirs("plots", exist_ok=True)
        imname = f"_{filename}" if filename else ""
        plt.savefig(f"plots/energia_momento{imname}.png", dpi=300, bbox_inches='tight')
        print(f"Gráfico guardado en plots/energia_momento{imname}.png")
    
    if show:
        plt.show()
    
    plt.close()


def plot_relative_distances(data, body_names=['Sun', 'Earth', 'Moon'], show=False, save=False, filename=""):
    """Grafica las distancias relativas entre los cuerpos."""
    plt.figure(figsize=(12, 6))
    
    # Calcular distancias
    r12 = np.sqrt((data['x1']-data['x2'])**2 + (data['y1']-data['y2'])**2 + (data['z1']-data['z2'])**2)
    r13 = np.sqrt((data['x1']-data['x3'])**2 + (data['y1']-data['y3'])**2 + (data['z1']-data['z3'])**2)
    r23 = np.sqrt((data['x2']-data['x3'])**2 + (data['y2']-data['y3'])**2 + (data['z2']-data['z3'])**2)
    
    plt.plot(data['time'], r12, 'r-', label=f'{body_names[0]}-{body_names[1]} Distance', linewidth=1.5)
    plt.plot(data['time'], r13, 'g-', label=f'{body_names[0]}-{body_names[2]} Distance', linewidth=1.5)
    plt.plot(data['time'], r23, 'b-', label=f'{body_names[1]}-{body_names[2]} Distance', linewidth=1.5)
    
    plt.xlabel('Time (s)')
    plt.ylabel('Distance (m)')
    plt.title(f'Relative Distances Between Bodies\n{", ".join(body_names)}')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    
    if save:
        os.makedirs("plots", exist_ok=True)
        imname = f"_{filename}" if filename else ""
        plt.savefig(f"plots/distancias{imname}.png", dpi=300, bbox_inches='tight')
        print(f"Gráfico guardado en plots/distancias{imname}.png")
    
    if show:
        plt.show()
    
    plt.close()


def load_simulation_data(filename="three_body_simulation"):

    filepath = f"data/{filename}.dat"
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No se encontró el archivo {filepath}")
    
    # Cargar datos
    data = np.loadtxt(filepath, comments='#')
    
    # Diccionario con los datos organizados
    return {
        'time': data[:, 0],
        'x1': data[:, 1], 'y1': data[:, 2], 'z1': data[:, 3],
        'x2': data[:, 4], 'y2': data[:, 5], 'z2': data[:, 6],
        'x3': data[:, 7], 'y3': data[:, 8], 'z3': data[:, 9],
        'vx1': data[:, 10], 'vy1': data[:, 11], 'vz1': data[:, 12],
        'vx2': data[:, 13], 'vy2': data[:, 14], 'vz2': data[:, 15],
        'vx3': data[:, 16], 'vy3': data[:, 17], 'vz3': data[:, 18],
        'E_kin': data[:, 19], 'E_pot': data[:, 20], 'E_tot': data[:, 21],
        'Lx': data[:, 22], 'Ly': data[:, 23], 'Lz': data[:, 24]
    }

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Visualización del problema de tres cuerpos")
    parser.add_argument("--filename", type=str, default="sun_earth_moon_test",
                       help="Nombre base del archivo de datos (sin extensión)")
    parser.add_argument("--bodies", nargs=3, type=str, default=['Sun', 'Earth', 'Moon'],
                       help="Nombres de los cuerpos (3 nombres separados por espacios)")
    parser.add_argument("--sizes", nargs=3, type=int, default=None,
                       help="Tamaños de los marcadores (3 valores enteros)")
    parser.add_argument("--save",
                        default=True,
                        action="store_true",
                        help="Guardar gráficos en lugar de mostrarlos")
    
    args = parser.parse_args()
    
    # Cargar datos
    data = load_simulation_data(args.filename)
    
    # Generar gráficos
    plot_3d_trajectories(data, body_names=args.bodies, body_sizes=args.sizes,
                         show=not args.save, save=args.save, filename=args.filename)
    plot_energy_momentum(data, body_names=args.bodies,
                         show=not args.save, save=args.save, filename=args.filename)
    plot_relative_distances(data, body_names=args.bodies,
                         show=not args.save, save=args.save, filename=args.filename)
