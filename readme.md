# Port Simulation

This Python script simulates the operations of a port, including vessel berthing, container offloading using quay cranes, and truck transportation.

## Features
- **Berth Management**: Vessels can dock at the port's berths, which have a limited capacity. If all berths are occupied, arriving vessels must wait until a berth becomes available.
- **Quay Crane Operations**: Quay cranes are responsible for offloading containers from vessels onto trucks. Each quay crane can handle one berth at a time and requires a certain amount of time for crane and truck movements.
- **Truck Transportation**: Trucks transport containers from the port to their destinations. If all trucks are in use, the quay crane must wait until a truck becomes available.

## Requirements
- Python 3.x
- SimPy library (install using `pip install simpy`)

## Usage
1. Install SimPy library
2. Run the script using Python:

    ```
    python port_simulation.py
    ```

3. The simulation will run for a specified duration (24 hours by default), and it will display logs of vessel arrivals, berthings, container offloading, and departures.

## Customization
- **Simulation Duration**: You can adjust the simulation duration by changing the `SIM_DURATION` variable in the `main` function of the script.
- **Resource Capacities**: The number of berths and trucks, as well as their capacities, can be modified by adjusting the parameters when initializing the `NO_BERTH` , `NO_TRUCKS` and `NO_CONTAINER` objects.

## Logic
1. **Simulation Initialization**: The simulation environment is initialized, including the duration of the simulation.
2. **Berth and Truck Setup**: Berths and trucks are set up with specified capacities.
3. **Vessel Arrival Process**: Vessels arrive at the port at random intervals, with inter-arrival times following an exponential distribution.
4. **Vessel Berthing**: When a vessel arrives, it requests a berth. If a berth is available, the vessel berths; otherwise, it waits until a berth becomes available.
5. **Container Offloading**: Once berthed, the vessel initiates the container offloading process using a quay crane. The quay crane offloads containers onto trucks, with each container taking a certain amount of time to handle. Since there are two berth and two crane and no more than 1 crane can operate on a ship we are considering berth and quaycrane as a single entity
6. **Truck Handling**: The quay crane requests a truck to transport each container. If all trucks are in use, the quay crane waits until a truck becomes available.
7. **Simulation Termination**: The simulation runs until the specified duration is reached.



