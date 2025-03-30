import os
import numpy as np
import argparse

class ThreeBodySystem:
    def __init__(self, masses, initial_positions, initial_velocities, G=6.67430e-11):
        """
        Inicializa el sistema de tres cuerpos.
        
        :param masses: Lista de masas [m1, m2, m3] en kg.
        :param initial_positions: Lista de posiciones iniciales [[x1, y1, z1], [x2, y2, z2], [x3, y3, z3]] en m.
        :param initial_velocities: Lista de velocidades iniciales [[vx1, vy1, vz1], [vx2, vy2, vz2], [vx3, vy3, vz3]] en m/s.
        :param G: Constante gravitacional (N m²/kg²).
        """
        self.masses = np.array(masses)
        self.G = G
        
        # Estado del sistema: [x1, y1, z1, vx1, vy1, vz1, x2, y2, z2, vx2, vy2, vz2, x3, y3, z3, vx3, vy3, vz3]
        self.state = np.concatenate([np.array(initial_positions).flatten(), 
                                    np.array(initial_velocities).flatten()])
    
    def acceleration(self, i, positions):
        """Calcula la aceleración del cuerpo i debido a los otros dos cuerpos."""
        mi = self.masses[i]
        ri = positions[i]
        acc = np.zeros(3)
        
        for j in range(3):
            if j != i:
                rj = positions[j]
                rij = rj - ri
                r = np.linalg.norm(rij)
                acc += self.G * self.masses[j] * rij / (r**3)
        
        return acc
    
    def equations_of_motion(self, state):
        """Devuelve las derivadas del estado (18 ecuaciones)."""
        positions = state[:9].reshape(3, 3)  # [x1, y1, z1, x2, y2, z2, x3, y3, z3]
        velocities = state[9:].reshape(3, 3)  # [vx1, vy1, vz1, ..., vz3]
        
        derivatives = np.zeros_like(state)
        
        # dx/dt = v (para los 3 cuerpos)
        derivatives[:9] = state[9:]
        
        # dv/dt = a (aceleración calculada para cada cuerpo)
        for i in range(3):
            derivatives[9 + 3*i : 12 + 3*i] = self.acceleration(i, positions)
        
        return derivatives
    
    def kinetic_energy(self):
        """Calcula la energía cinética total del sistema."""
        velocities = self.state[9:].reshape(3, 3)
        return 0.5 * np.sum(self.masses * np.sum(velocities**2, axis=1))
    
    def potential_energy(self):
        """Calcula la energía potencial gravitacional total del sistema."""
        positions = self.state[:9].reshape(3, 3)
        pe = 0.0
        
        for i in range(3):
            for j in range(i+1, 3):
                rij = positions[j] - positions[i]
                r = np.linalg.norm(rij)
                pe -= self.G * self.masses[i] * self.masses[j] / r
        
        return pe
    
    def total_energy(self):
        """Calcula la energía total del sistema."""
        return self.kinetic_energy() + self.potential_energy()
    
    def angular_momentum(self):
        """Calcula el momento angular total del sistema."""
        positions = self.state[:9].reshape(3, 3)
        velocities = self.state[9:].reshape(3, 3)
        L = np.zeros(3)
        
        for i in range(3):
            L += self.masses[i] * np.cross(positions[i], velocities[i])
        
        return L

class ThreeBodySimulator:
    def __init__(self, system, filename="three_body_simulation"):
        """
        Inicializa el simulador del sistema de tres cuerpos.
        """
        self.system = system
        self.filename = filename
        os.makedirs("data", exist_ok=True)
    
    def runge_kutta_step(self, state, dt):
        """Realiza un paso de integración con RK4."""
        k1 = dt * self.system.equations_of_motion(state)
        k2 = dt * self.system.equations_of_motion(state + 0.5 * k1)
        k3 = dt * self.system.equations_of_motion(state + 0.5 * k2)
        k4 = dt * self.system.equations_of_motion(state + k3)
        return state + (k1 + 2*k2 + 2*k3 + k4) / 6
    
    def simulate(self, t_max, dt):
        """Ejecuta la simulación y guarda los datos."""
        steps = int(t_max / dt)
        state = self.system.state
        
        with open(f"data/{self.filename}.dat", "w") as file:
            # Encabezado del archivo de salida
            file.write("# t x1 y1 z1 x2 y2 z2 x3 y3 z3 ")
            file.write("vx1 vy1 vz1 vx2 vy2 vz2 vx3 vy3 vz3 ")
            file.write("E_kin E_pot E_tot Lx Ly Lz\n")
            
            time = 0.0
            for _ in range(steps):
                self.system.state = state  # Actualizar estado del sistema
                
                E_kin = self.system.kinetic_energy()
                E_pot = self.system.potential_energy()
                E_tot = self.system.total_energy()
                L = self.system.angular_momentum()
                
                file.write(f"{time:.5f} ")
                file.write(" ".join([f"{val:.5e}" for val in state]) + " ")
                file.write(f"{E_kin:.5e} {E_pot:.5e} {E_tot:.5e} ")
                file.write(f"{L[0]:.5e} {L[1]:.5e} {L[2]:.5e}\n")
                
                state = self.runge_kutta_step(state, dt)
                time += dt
        
        print(f"Simulación completada. Datos guardados en data/{self.filename}.dat")

def main(masses=[1.0, 1.0, 1.0], 
         initial_positions=[[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]], 
         initial_velocities=[[0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [-1.0, 0.0, 0.0]], 
         dt=0.001, t_max=10.0, filename="three_body_simulation"):
    
    system = ThreeBodySystem(
        masses=masses,
        initial_positions=initial_positions,
        initial_velocities=initial_velocities
    )
    
    # Guardar parámetros de la simulación
    os.makedirs("data", exist_ok=True)
    with open(f"data/{filename}_params.txt", "w") as param_file:
        param_file.write("# Simulation parameters\n")
        param_file.write("{\n")
        param_file.write(f"    'masses': {masses},\n")
        param_file.write(f"    'initial_positions': {initial_positions},\n")
        param_file.write(f"    'initial_velocities': {initial_velocities},\n")
        param_file.write(f"    'dt': {dt},\n")
        param_file.write(f"    't_max': {t_max},\n")
        param_file.write(f"    'G': {system.G}\n")
        param_file.write("}\n")
    
    simulator = ThreeBodySimulator(system, filename)
    simulator.simulate(t_max, dt)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulador del problema de tres cuerpos usando RK4.")
    
    # Masas de los cuerpos
    parser.add_argument("--m1", type=float, default=1.0, help="Masa del primer cuerpo (kg)")
    parser.add_argument("--m2", type=float, default=1.0, help="Masa del segundo cuerpo (kg)")
    parser.add_argument("--m3", type=float, default=1.0, help="Masa del tercer cuerpo (kg)")
    
    # Posiciones iniciales (x, y, z para cada cuerpo)
    parser.add_argument("--x1", type=float, default=0.0, help="Posición x inicial del cuerpo 1 (m)")
    parser.add_argument("--y1", type=float, default=0.0, help="Posición y inicial del cuerpo 1 (m)")
    parser.add_argument("--z1", type=float, default=0.0, help="Posición z inicial del cuerpo 1 (m)")
    
    parser.add_argument("--x2", type=float, default=1.0, help="Posición x inicial del cuerpo 2 (m)")
    parser.add_argument("--y2", type=float, default=0.0, help="Posición y inicial del cuerpo 2 (m)")
    parser.add_argument("--z2", type=float, default=0.0, help="Posición z inicial del cuerpo 2 (m)")
    
    parser.add_argument("--x3", type=float, default=0.0, help="Posición x inicial del cuerpo 3 (m)")
    parser.add_argument("--y3", type=float, default=1.0, help="Posición y inicial del cuerpo 3 (m)")
    parser.add_argument("--z3", type=float, default=0.0, help="Posición z inicial del cuerpo 3 (m)")
    
    # Velocidades iniciales (vx, vy, vz para cada cuerpo)
    parser.add_argument("--vx1", type=float, default=0.0, help="Velocidad x inicial del cuerpo 1 (m/s)")
    parser.add_argument("--vy1", type=float, default=0.0, help="Velocidad y inicial del cuerpo 1 (m/s)")
    parser.add_argument("--vz1", type=float, default=0.0, help="Velocidad z inicial del cuerpo 1 (m/s)")
    
    parser.add_argument("--vx2", type=float, default=0.0, help="Velocidad x inicial del cuerpo 2 (m/s)")
    parser.add_argument("--vy2", type=float, default=1.0, help="Velocidad y inicial del cuerpo 2 (m/s)")
    parser.add_argument("--vz2", type=float, default=0.0, help="Velocidad z inicial del cuerpo 2 (m/s)")
    
    parser.add_argument("--vx3", type=float, default=-1.0, help="Velocidad x inicial del cuerpo 3 (m/s)")
    parser.add_argument("--vy3", type=float, default=0.0, help="Velocidad y inicial del cuerpo 3 (m/s)")
    parser.add_argument("--vz3", type=float, default=0.0, help="Velocidad z inicial del cuerpo 3 (m/s)")
    
    # Parámetros de simulación
    parser.add_argument("--dt", type=float, default=0.001, help="Paso de tiempo (s)")
    parser.add_argument("--t_max", type=float, default=10.0, help="Tiempo total de simulación (s)")
    parser.add_argument("--filename", type=str, default="three_body_simulation", help="Nombre base para los archivos de salida")
    
    args = parser.parse_args()
    
    masses = [args.m1, args.m2, args.m3]
    
    initial_positions = [
        [args.x1, args.y1, args.z1],
        [args.x2, args.y2, args.z2],
        [args.x3, args.y3, args.z3]
    ]
    
    initial_velocities = [
        [args.vx1, args.vy1, args.vz1],
        [args.vx2, args.vy2, args.vz2],
        [args.vx3, args.vy3, args.vz3]
    ]
    
    main(
        masses=masses,
        initial_positions=initial_positions,
        initial_velocities=initial_velocities,
        dt=args.dt,
        t_max=args.t_max,
        filename=args.filename
    )