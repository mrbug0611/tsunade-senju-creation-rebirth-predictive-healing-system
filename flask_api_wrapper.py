import gillespy2
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
sys.path.insert(0, 'C:/Users/mdwil/PycharmProjects/TsunadeSenju') # Add current directory to the path
from creation_rebirth_sim import CreationRebirthModel # Import the original class
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route("/api/simulate", methods=["POST"])
def simulate():
    """
    Endpoints to run Creation Rebirth simulation using the original model
    Expects JSON with 'parameters' and 'initial_states' keys
    :return:
    """
    try:
        data = request.get_json()

        # Extract Parameters and initial state
        # {} = default if key doesn't exist
        parameters = data.get("parameters", {})
        initial_states = data.get("initial_states", {})

        # Map frontend state names to model state names
        state_mapping = {
            'chakra_reserves': 'Chakra_Reserves',
            'active_enzymes': 'Active_Enzymes',
            'damaged_cells': 'Damaged_Cells',
            'healthy_cells': 'Healthy_Cells',
            'telomere_stress': 'Telomere_Stress'
        }

        # Convert initial state to model format
        converted_states = {}
        if initial_states:
            for key, value in initial_states.items():
                model_key = state_mapping.get(key, key) # return the key value if nothing found
                converted_states[model_key] = value

        # Create model with custom parameters and initial states
        model = CreationRebirthModel(
            parameter_values=parameters if parameters else None,
            initial_states=converted_states if converted_states else None,
        )

        # Run the simulation
        results = model.run(solver=gillespy2.TauLeapingSolver)

        # extract results and format for json
        output_data = []

        # Get the length from any species
        num_timepoints = len(results["Healthy_Cells"]) # Tells how many time points were created
        # (array has 1 value per time point)

        for i in range(num_timepoints):
            output_data.append({
                'time': float(i), # what time point it is
                'chakra': int(results['Chakra_Reserves'][i]),
                'active_enzymes': int(results['Active_Enzymes'][i]),
                'damaged_cells': int(results['Damaged_Cells'][i]),
                'healthy_cells': int(results['Healthy_Cells'][i]),
                'telomere_stress': int(results['Telomere_Stress'][i])
            })

        # Calculate Summary Statistics
        final_state = output_data[-1]
        summary = {
            'finalHealthy': final_state['healthy_cells'],
            'finalDamaged': final_state['damaged_cells'],
            'stressLevel': final_state['telomere_stress'],
            'recovered': final_state['damaged_cells'] < 10
        }

        return jsonify({
            "success": True,
            "data": output_data,
            "summary": summary,}
        )

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),

        }), 400

@app.route("/api/health", methods=["GET"])
def health():
    """
    Health check endpoint
    :return:
    """
    return jsonify({"status": "API is Running! "}), 200



if __name__ == "__main__":
    app.run(debug=True, port=5000)