import random
import numpy as np
import matplotlib.pyplot as plt

# Constants for the environment
INITIAL_CHEMICALS = {"hydrogen": 1000, "sulfur": 800, "methane": 500}  # Available chemicals for chemosynthesis
ENERGY_YIELD = {"hydrogen": 10, "sulfur": 8, "methane": 5}  # Energy yield from different chemicals

# Species class definition
class Species:
    def __init__(self, name, energy_efficiency, reproduction_rate, predation_rate, chemical_affinity, symbiosis=None):
        self.name = name
        self.energy_efficiency = energy_efficiency  # Efficiency in converting chemical energy to usable energy
        self.reproduction_rate = reproduction_rate  # Rate of reproduction
        self.predation_rate = predation_rate        # Rate of predation on other species
        self.chemical_affinity = chemical_affinity  # Chemical preference for energy
        self.population = random.randint(50, 150)   # Initial population
        self.energy = 0                             # Energy reserve for reproduction and maintenance
        self.symbiosis = symbiosis                  # Optional symbiotic partner species

    def consume_chemicals(self, environment):
        """Species consumes chemicals from the environment to gain energy."""
        chemical = self.chemical_affinity
        if environment[chemical] > 0:
            energy_gained = min(environment[chemical], self.population) * ENERGY_YIELD[chemical] * self.energy_efficiency
            environment[chemical] -= min(environment[chemical], self.population)
            self.energy += energy_gained

    def reproduce(self):
        """Species reproduces based on its energy reserve."""
        energy_needed = self.population * 2
        if self.energy >= energy_needed:
            offspring = int(self.population * self.reproduction_rate)
            self.population += offspring
            self.energy -= energy_needed  # Reproduction consumes energy

    def predation(self, prey):
        """Species preys on another species."""
        if prey.population > 0:
            prey_loss = int(prey.population * self.predation_rate)
            self.population += prey_loss // 2  # Gains energy from prey
            prey.population -= prey_loss

    def symbiotic_interaction(self):
        """Species benefits from a symbiotic relationship."""
        if self.symbiosis:
            self.energy += int(self.symbiosis.population * 0.1)  # Symbiotic species provide energy

    def evolve(self):
        """Species randomly mutates to evolve over generations."""
        mutation_chance = random.random()
        if mutation_chance < 0.1:  # 10% chance of a mutation
            trait = random.choice(["energy_efficiency", "reproduction_rate", "predation_rate"])
            mutation_factor = random.uniform(0.9, 1.1)  # Slight increase or decrease
            if trait == "energy_efficiency":
                self.energy_efficiency *= mutation_factor
            elif trait == "reproduction_rate":
                self.reproduction_rate *= mutation_factor
            elif trait == "predation_rate":
                self.predation_rate *= mutation_factor
            print(f"{self.name} has evolved! New {trait}: {getattr(self, trait)}")

# Environment class definition
class Environment:
    def __init__(self, chemicals):
        self.chemicals = chemicals
    
    def replenish_chemicals(self):
        """Replenishes chemicals in the environment."""
        for chemical in self.chemicals:
            self.chemicals[chemical] += random.randint(10, 50)  # Natural chemical replenishment

# Simulate ecosystem
def simulate_ecosystem(species_list, environment, generations=100):
    population_history = {species.name: [] for species in species_list}
    chemical_history = []

    for gen in range(generations):
        print(f"\n--- Generation {gen + 1} ---")
        
        total_chemicals = sum(environment.chemicals.values())
        chemical_history.append(total_chemicals)

        # Each species consumes chemicals
        for species in species_list:
            species.consume_chemicals(environment.chemicals)
            print(f"{species.name} consumed chemicals and now has energy {species.energy} and population {species.population}")

            # Symbiotic interaction (if any)
            species.symbiotic_interaction()
            print(f"{species.name} benefited from symbiosis (if applicable), energy: {species.energy}")

            # Reproduce based on available energy
            species.reproduce()
            print(f"{species.name} reproduced and now has population {species.population}")

            population_history[species.name].append(species.population)

        # Predation interactions (if any)
        for i in range(len(species_list) - 1):
            predator = species_list[i]
            prey = species_list[i + 1]
            predator.predation(prey)
            print(f"{predator.name} preyed on {prey.name}. Populations are now {predator.population} and {prey.population}")
        
        # Species evolve
        for species in species_list:
            species.evolve()
        
        # Replenish chemicals in the environment
        environment.replenish_chemicals()
        print(f"Environment chemicals: {environment.chemicals}")

    return population_history, chemical_history

# Visualization function
def plot_ecosystem(population_history, chemical_history, generations):
    plt.figure(figsize=(10, 6))
    
    # Plot species population dynamics
    for species, population in population_history.items():
        plt.plot(range(generations), population, label=f"Population of {species}")
    
    # Plot available chemical energy in the environment
    plt.plot(range(generations), chemical_history, label="Total Environment Chemicals", linestyle="--", color="black")
    
    plt.xlabel("Generations")
    plt.ylabel("Population / Chemicals")
    plt.title("Ecosystem Population and Chemical Levels Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()

# Example setup with symbiosis
species_a = Species(name="Chemosynth A", energy_efficiency=0.8, reproduction_rate=0.05, predation_rate=0.02, chemical_affinity="hydrogen")
species_b = Species(name="Chemosynth B", energy_efficiency=0.7, reproduction_rate=0.04, predation_rate=0.03, chemical_affinity="sulfur", symbiosis=species_a)
species_c = Species(name="Chemosynth C", energy_efficiency=0.6, reproduction_rate=0.06, predation_rate=0.04, chemical_affinity="methane")

environment = Environment(chemicals=INITIAL_CHEMICALS)
species_list = [species_a, species_b, species_c]

# Simulate ecosystem for 100 generations
generations = 100
population_history, chemical_history = simulate_ecosystem(species_list, environment, generations)

# Plot the results
plot_ecosystem(population_history, chemical_history, generations)
