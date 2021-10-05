# Optuna-Persistent volume driven pattern

## Concept

1. Place data and executable on the PV.
2. Prepare the SQL and monitoring Pod.
3. Connect the PV to pods for computing.
4. Each pod copies executable to its own storage and execute it. The executable will refer to the data on PV.
5. The monitoring pod will check the optimization is converged and save the result on 
6. 