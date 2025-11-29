import gillespy2
import numpy as np


class CreationRebirthModel(gillespy2.Model):
    """
    A GillesPy2 model simulating the creation rebirth jutsu

   Dynamics:
   1. Chakra Activation = convert latent biological energy into active mitotic enzymes
   2. Cellular Regeneration = Mitotic enzymes convert damaged cells to healthy cells
   3. Telomere Shortening = Rapid Division generates cellular stress which shortens lifespan
    """

    def __init__(self, parameter_values=None, initial_states=None):

        # initialize the model
        super().__init__(name="Creation_Rebirth_Cellular_Kinetics")

        # Define Parameters (constants)
        # k_activation = rate at which the Byakugou Seal releases chakra
        # k_healing = rate of cell repair
        # k_stress = rate of telomere damage accumulation

        params = {
            "k_activation": 0.5,
            "k_healing": 2.0,
            "k_stress": 0.1,
            "k_decay": 0.3,
        }

        # Override defaults if provided
        if parameter_values:
            params.update(parameter_values)



        # Iterates over the params dictionary assigning keys as k and values as v
        # gillespy2.Parameter() Create one instance of the parameter class in for each entry of the dictionary
        # self.add_parameter() takes 1 parameter object or list of parameter objects and
        # registers them in the models internal structure making them available for use later
        self.add_parameter([gillespy2.Parameter(name=k, expression=v) for k, v in params.items()])

        # Defines Species (The values being tracked)
        # Initial State: High Damage, Stored Chakra, low active healing factor
        species_config = {
            "Chakra_Reserves": 1000, # Yin seal storage
            "Active_Enzymes": 0, # Active Healing Chakra / Enzymes
            "Damaged_Cells": 500, # Severity of Injury
            "Healthy_Cells": 500, # Baseline Tissue
            "Telomere_Stress": 0, # Side Effect Counter
        }

        if initial_states:
            species_config.update(initial_states)

        self.add_species([gillespy2.Species(name=k, initial_value=v) for k, v in species_config.items()])

        # Define Reactions (transformation rules for how species are altered based on parameters)

        # Reaction 1: Seal Release
        # Chakra Reserves to Active Enzymes
        r1 = gillespy2.Reaction(
            name="Byakugou_Activation",
            reactants={"Chakra_Reserves": 1}, # Perfect 1 to 1 ratio
            products={"Active_Enzymes": 1},
            rate=self.listOfParameters["k_activation"],
        )

        # Reaction 2: Mitotic Regeneration
        # Damaged Cells + Active Enzymes to Healthy Cells + Active Enzymes + Telomere Stress
        r2 = gillespy2.Reaction(
            name="Mitotic_Regeneration",
            reactants={"Damaged_Cells": 1, "Active_Enzymes": 1},
            products={"Healthy_Cells": 1, "Active_Enzymes": 1, "Telomere_Stress": 1},
            rate=self.listOfParameters["k_healing"],
        )

        # Reaction 3: Chakra Exhaustion/Decay
        # Active Enzymes to Null (dissipation after use)
        r3 = gillespy2.Reaction(
            name="Chakra_Dissipation",
            reactants={"Active_Enzymes": 1},
            products={},
            rate=self.listOfParameters["k_decay"],
        )

        self.add_reaction([r1, r2, r3])

        # Set the timespan for the simulation (0 to 50 time units)
        # 101 snapshots taken
        self.timespan(np.linspace(0, 50, 101))

def run_analysis(parameter_values=None, initial_states=None):
    """
   Runs the simulation and prints a summary of the 'medical' results.

    Args:
        parameter_values: Optional custom reaction rates
        initial_states: Optional custom initial conditions    """

    print("Initial Creation Rebirth Algorithm...")
    model = CreationRebirthModel(parameter_values=parameter_values, initial_states=initial_states)

    # Runs simulation using stochastic simulation solver
    # Uses Tau_Leaping Solver for faster tau_leaping
    results = model.run(solver=gillespy2.TauLeapingSolver)

    # Extract Final Stats
    final_healthy = results["Healthy_Cells"][-1]
    final_damaged = results["Damaged_Cells"][-1]
    stress_level = results["Telomere_Stress"][-1]

    print("-" * 40)
    print("TREATMENT REPORT: PATIENT ZERO")
    print("-" * 40)
    print(f"Final Healthy Tissue Count: {final_healthy}")
    print(f"Remaining Damaged Tissue:   {final_damaged}")
    print(f"Telomere Stress Accumulated: {stress_level}")

    if final_damaged < 10:
        print("\nSTATUS: COMPLETE RECOVERY")
        print("Note: Patient requires immediate rest. Life expectancy slightly reduced.")
    else:
        print("\nSTATUS: PARTIAL RECOVERY - INSUFFICIENT CHAKRA")

if __name__ == "__main__":
    run_analysis()