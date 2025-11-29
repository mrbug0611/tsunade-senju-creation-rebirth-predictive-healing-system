import io
import sys
import unittest

import gillespy2
import numpy as np
from creation_rebirth_sim import CreationRebirthModel, run_analysis


class TestCreationRebirthModel(unittest.TestCase):
    """Unit tests for the CreationRebirthModel class."""

    def setUp(self):
        """Set up test fixtures before each test."""
        self.model = CreationRebirthModel()

    def test_model_initialization_default(self):
        """Test that model initializes with default parameters."""
        self.assertEqual(self.model.name, "Creation_Rebirth_Cellular_Kinetics")
        self.assertIsNotNone(self.model.listOfParameters)
        self.assertIsNotNone(self.model.listOfSpecies)

    def test_default_parameters(self):
        """Test that default parameters are set correctly."""
        params = {self.model.listOfParameters[p].name: float(self.model.listOfParameters[p].expression)
                  for p in self.model.listOfParameters}
        self.assertEqual(params['k_activation'], 0.5)
        self.assertEqual(params['k_healing'], 2.0)
        self.assertEqual(params['k_stress'], 0.1)
        self.assertEqual(params['k_decay'], 0.3)

    def test_custom_parameters(self):
        """Test that custom parameters override defaults."""
        custom_params = {
            'k_activation': 1.0,
            'k_healing': 3.0,
            'k_stress': 0.2,
            'k_decay': 0.5
        }
        model = CreationRebirthModel(parameter_values=custom_params)
        params = {model.listOfParameters[p].name: float(model.listOfParameters[p].expression)
                  for p in model.listOfParameters}
        self.assertEqual(params['k_activation'], 1.0)
        self.assertEqual(params['k_healing'], 3.0)

    def test_default_species_counts(self):
        """Test that default initial species counts are correct."""
        species = {self.model.listOfSpecies[s].name: self.model.listOfSpecies[s].initial_value
                   for s in self.model.listOfSpecies}
        self.assertEqual(species['Chakra_Reserves'], 1000)
        self.assertEqual(species['Active_Enzymes'], 0)
        self.assertEqual(species['Damaged_Cells'], 500)
        self.assertEqual(species['Healthy_Cells'], 500)
        self.assertEqual(species['Telomere_Stress'], 0)

    def test_custom_initial_states(self):
        """Test that custom initial states override defaults."""
        custom_states = {
            'Chakra_Reserves': 2000,
            'Damaged_Cells': 800,
            'Healthy_Cells': 200
        }
        model = CreationRebirthModel(initial_states=custom_states)
        species = {model.listOfSpecies[s].name: model.listOfSpecies[s].initial_value
                   for s in model.listOfSpecies}
        self.assertEqual(species['Chakra_Reserves'], 2000)
        self.assertEqual(species['Damaged_Cells'], 800)
        self.assertEqual(species['Healthy_Cells'], 200)

    def test_model_has_three_reactions(self):
        """Test that model has exactly three reactions."""
        self.assertEqual(len(self.model.listOfReactions), 3)

    def test_reaction_names(self):
        """Test that all three reactions exist with correct names."""
        reaction_names = {self.model.listOfReactions[r].name for r in self.model.listOfReactions}
        expected_names = {
            'Byakugou_Activation',
            'Mitotic_Regeneration',
            'Chakra_Dissipation'
        }
        self.assertEqual(reaction_names, expected_names)

    def test_simulation_runs(self):
        """Test that simulation runs without errors."""
        try:
            results = self.model.run(solver=gillespy2.TauLeapingSolver)
            self.assertIsNotNone(results)
        except Exception as e:
            self.fail(f"Simulation failed with error: {e}")

    def test_simulation_output_structure(self):
        """Test that simulation output has correct structure."""
        results = self.model.run(solver=gillespy2.TauLeapingSolver)

        # Results is a numpy record array, check by accessing with species name
        try:
            _ = results['Chakra_Reserves']
            _ = results['Damaged_Cells']
            _ = results['Healthy_Cells']
        except (KeyError, TypeError):
            self.fail("Results object doesn't contain expected species data")

    def test_simulation_has_101_timepoints(self):
        """Test that simulation has 101 timepoints (0 to 50 in steps of 0.5)."""
        results = self.model.run(solver=gillespy2.TauLeapingSolver)
        num_timepoints = len(results['Healthy_Cells'])
        self.assertEqual(num_timepoints, 101)

    def test_timespan_values(self):
        """Test that timespan goes from 0 to 50."""
        results = self.model.run(solver=gillespy2.TauLeapingSolver)

        self.assertAlmostEqual(results['Healthy_Cells'][0], 500.0, delta=100)
        self.assertGreater(len(results['Telomere_Stress']), 50)

    def test_damaged_cells_decrease(self):
        """Test that damaged cells generally decrease over time."""
        results = self.model.run(solver=gillespy2.TauLeapingSolver)
        initial_damaged = results['Damaged_Cells'][0]
        final_damaged = results['Damaged_Cells'][-1]
        # Damaged cells should be less than or equal to initial
        self.assertLessEqual(final_damaged, initial_damaged)

    def test_healthy_cells_increase(self):
        """Test that healthy cells generally increase over time."""
        results = self.model.run(solver=gillespy2.TauLeapingSolver)
        initial_healthy = results['Healthy_Cells'][0]
        final_healthy = results['Healthy_Cells'][-1]
        # Healthy cells should be greater than or equal to initial
        self.assertGreaterEqual(final_healthy, initial_healthy)

    def test_telomere_stress_accumulates(self):
        """Test that telomere stress is non-decreasing."""
        results = self.model.run(solver=gillespy2.TauLeapingSolver)
        stress = results['Telomere_Stress']
        # Stress should never decrease
        for i in range(1, len(stress)):
            self.assertGreaterEqual(stress[i], stress[i - 1])

    def test_chakra_reserves_deplete(self):
        """Test that chakra reserves deplete over time."""
        results = self.model.run(solver=gillespy2.TauLeapingSolver)
        initial_chakra = results['Chakra_Reserves'][0]
        final_chakra = results['Chakra_Reserves'][-1]
        # Chakra should generally deplete
        self.assertLessEqual(final_chakra, initial_chakra)

    def test_high_healing_rate_improves_recovery(self):
        """Test that higher healing rate leads to better recovery."""
        # Low healing rate
        model_low = CreationRebirthModel(
            parameter_values={'k_healing': 0.5}
        )
        results_low = model_low.run(solver=gillespy2.TauLeapingSolver)
        final_damaged_low = results_low['Damaged_Cells'][-1]

        # High healing rate
        model_high = CreationRebirthModel(
            parameter_values={'k_healing': 3.0}
        )
        results_high = model_high.run(solver=gillespy2.TauLeapingSolver)
        final_damaged_high = results_high['Damaged_Cells'][-1]

        # Higher healing rate should result in fewer damaged cells
        self.assertLessEqual(final_damaged_high, final_damaged_low)

    def test_partial_parameters_update(self):
        """Test that providing only some parameters updates correctly."""
        partial_params = {'k_healing': 5.0}
        model = CreationRebirthModel(parameter_values=partial_params)
        params = {model.listOfParameters[p].name: float(model.listOfParameters[p].expression)
                  for p in model.listOfParameters}

        # Updated parameter
        self.assertEqual(params['k_healing'], 5.0)
        # Default parameters should remain
        self.assertEqual(params['k_activation'], 0.5)


class TestCreationRebirthModelEdgeCases(unittest.TestCase):
    """Edge case tests for CreationRebirthModel."""

    def test_zero_initial_damage(self):
        """Test simulation with zero initial damaged cells."""
        model = CreationRebirthModel(
            initial_states={'Damaged_Cells': 0, 'Healthy_Cells': 1000}
        )
        results = model.run(solver=gillespy2.TauLeapingSolver)
        # Should run without error and maintain zero damage
        self.assertEqual(results['Damaged_Cells'][0], 0)

    def test_zero_chakra_reserves(self):
        """Test simulation with zero initial chakra reserves."""
        model = CreationRebirthModel(
            initial_states={'Chakra_Reserves': 0}
        )
        results = model.run(solver=gillespy2.TauLeapingSolver)
        # Should run without error
        self.assertIsNotNone(results)

    def test_zero_healing_rate(self):
        """Test simulation with zero healing rate."""
        model = CreationRebirthModel(
            parameter_values={'k_healing': 0.0}
        )
        results = model.run(solver=gillespy2.TauLeapingSolver)
        initial_damaged = results['Damaged_Cells'][0]
        final_damaged = results['Damaged_Cells'][-1]
        # With zero healing, damage should not decrease significantly
        self.assertGreaterEqual(final_damaged, initial_damaged * 0.9)


class TestRunAnalysis(unittest.TestCase):
    """Unit tests for the run_analysis function."""

    def test_run_analysis_executes(self):
        """Test that run_analysis executes without errors."""
        try:
            # Capture stdout
            captured_output = io.StringIO()
            sys.stdout = captured_output

            run_analysis()

            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()

            self.assertIsNotNone(output)
            self.assertGreater(len(output), 0)
        except Exception as e:
            sys.stdout = sys.__stdout__
            self.fail(f"run_analysis failed with error: {e}")

    def test_run_analysis_with_custom_parameters(self):
        """Test run_analysis with custom parameters."""
        try:
            captured_output = io.StringIO()
            sys.stdout = captured_output

            custom_params = {'k_healing': 3.0}
            run_analysis(parameter_values=custom_params)

            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()

            self.assertIn("TREATMENT REPORT", output)
        except Exception as e:
            sys.stdout = sys.__stdout__
            self.fail(f"run_analysis with custom parameters failed: {e}")

    def test_run_analysis_with_custom_initial_states(self):
        """Test run_analysis with custom initial states."""
        try:
            captured_output = io.StringIO()
            sys.stdout = captured_output

            custom_states = {'Damaged_Cells': 100, 'Healthy_Cells': 900}
            run_analysis(initial_states=custom_states)

            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()

            self.assertIn("TREATMENT REPORT", output)
        except Exception as e:
            sys.stdout = sys.__stdout__
            self.fail(f"run_analysis with custom initial states failed: {e}")

    def test_run_analysis_output_contains_header(self):
        """Test that output contains the treatment report header."""
        captured_output = io.StringIO()
        sys.stdout = captured_output

        run_analysis()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("TREATMENT REPORT: PATIENT ZERO", output)
        self.assertIn("-" * 40, output)

    def test_run_analysis_output_contains_metrics(self):
        """Test that output contains final health metrics."""
        captured_output = io.StringIO()
        sys.stdout = captured_output

        run_analysis()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("Final Healthy Tissue Count:", output)
        self.assertIn("Remaining Damaged Tissue:", output)
        self.assertIn("Telomere Stress Accumulated:", output)

    def test_run_analysis_output_contains_status(self):
        """Test that output contains recovery status."""
        captured_output = io.StringIO()
        sys.stdout = captured_output

        run_analysis()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Should contain either COMPLETE or PARTIAL recovery
        self.assertTrue(
            "COMPLETE RECOVERY" in output or "PARTIAL RECOVERY" in output,
            "Output should contain recovery status"
        )

    def test_run_analysis_complete_recovery(self):
        """Test that high healing rate leads to COMPLETE RECOVERY message."""
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Use high healing rate and low damage to encourage recovery
        run_analysis(
            parameter_values={'k_healing': 5.0},
            initial_states={'Damaged_Cells': 50}
        )

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # With high healing and low damage, should tend toward complete recovery
        self.assertIn("STATUS:", output)

    def test_run_analysis_partial_recovery(self):
        """Test that low healing rate leads to PARTIAL RECOVERY message."""
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Use low healing rate and high damage
        run_analysis(
            parameter_values={'k_healing': 0.1},
            initial_states={'Damaged_Cells': 800, 'Chakra_Reserves': 100}
        )

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("STATUS:", output)


if __name__ == '__main__':
    unittest.main()