# Optuna-Persistent volume driven pattern


## Concept

The following steps are executed from the python code:

1. Place data and executable on the PV.
2. Prepare the SQL server and expose its connection.
3. Connect the PV to pods for computing.
4. Each pod copies executable to its own storage and execute it. The executable will refer to the data on PV.
5. Observe the iteration number from the SQL server and judge current condition meets the convergence criteria.
6. Start the cleanup procedure.
