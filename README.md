## Creation Rebirth (Sōzō Saisei) Simulator

**A simulation of the most powerful medical ninjutsu in the Naruto series** 

View Live Demo: https://tsunade-senju-jutsu-frontend.onrender.com/ (Spins down after 15 minutes of inactivity)

### About 
This is a full-stack simulation of the Creation Rebirth Jutsu from the Naruto series. This application runs a Stochastic Simulation Algorithm (SSA) on the back end. This is to simulate and model cellular kinetics. The model treats chakra as the biological fuel. It uses Mitotic Enzymes as the catalyst. It uses Telomere shortening as a biological cost. 

### Features 
- **Stochastic Modeling**: Uses the GillesPy2 library to run Tau-Leaping simulations of the chemical reaction networks
-  **Real-Time Visualizations**: Interactive charts using Chakra reserves, cell counts, and biological stress over time.
-  **Adjustable Parameters**: The user can experiment with Chakra activation rates, Healing efficiency, and Enzyme decay.
-  **Stress Analysis**: Calculates the permanent cost of the technique via telomere shortening. The amount of telomere shortening is based on the healing intensity.

### Tech Stack 

**Backend**
- **Python 3.8+**
- **Flask**: Rest API to expose the simulation engine.
- **GillesPy2**: Bio-Simulation library to solve coupled chemical differential equations
- **NumPy**: For numerical computing

**Frontend**
- **React (Vite)**: For the UI Framework
- **Tailwind CSS**: For styling and responsive design
- **Recharts**: For the visualization Libraries
- **Lucide React**: For the iconography

### Simulation Logic 

The backend models the jutsu as a set of chemical reactions

- 1. **Seal Activation**: ```Chakra -> Active Enzymes```
     - _Rate_: The rate is controlled by the user. (done by adjusting the Chakra Activation Slider)
- 2. **Mitotic Regeneration**: ```Damaged Cell + Enzyme -> Healthy Cell + Enzyme + Telomere Stress```
     - _Note_: The Enzymes only act as the catalyst; they are not consumed here
     - _Cost_: Every healed cell generates stress. This stress can shorten telomere length (lifespan)
- 3. **Chakra Dissipation**: ```Enzyme -> Null```
     - _Dynamics_: The active healing Chakra decays over time. So you need a constant supply.  

### Local Setup 

**Prerequisites**: 
- Node.js and npm
- Python 3.8+

- 1. **Backend Setup**
     Navigate to the root directory
     ```
      # Create virtual environment
      python -m venv venv
      source venv/bin/activate  # Windows: venv\Scripts\activate
      
      # Install dependencies
      pip install flask flask-cors gillespy2 numpy gunicorn
      
      # Run the server
      python flask_api_wrapper.py 
     ```

     _The server will start on http://localhost:5000_

- 2. **Frontend Setup**
    Navigate to the client directory
  ```

  cd client

  # Install dependencies
  npm install
  
  # Start the development server
  npm run dev
  ```
  _The application will open at http://localhost:5173_

### Environmental Variables
I use the following environment variable from Render to connect the front end to the backend in production. 
```VITE_API_URL``` = ```https://your-backend-url.onrender.com```

### License 
This project is open source. The concept was based on the Naruto Series written by Masashi Kishimoto


### Contact (Support and Spin up Non Local Website)
- Open an Issue: The best way to report bugs or suggest features is by using the GitHub Issues tab in this repository.

- Creator Contact: mmdwilliams0611@gmail.com : https://github.com/mrbug0611 



