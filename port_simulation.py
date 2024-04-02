import random
import itertools
import simpy

class Berth(simpy.Resource):
    """Represents a berth where vessels can dock."""
    def __init__(self, env, capacity):
        super().__init__(env, capacity=capacity)

class Trucks(simpy.Resource):
    """Represents trucks for transporting containers."""
    def __init__(self, env, capacity):
        super().__init__(env, capacity=capacity)

class QuayCrane:
    """Represents a quay crane for offloading containers from vessels."""
    def __init__(self, env, name, trucks):
        self.env = env
        self.name = name
        self.trucks = trucks

    def offload(self, containers):
        """
        Simulate crane offloading container process
        Since there are two berth and two crane and no more than 1 crane can operate on a ship /
        we are considering berth and quaycrane as a single entity
        """
        print(f'{self.env.now} : {self.name} QuayCrane container offloading operation started')
        for i in range(containers):
            yield self.env.timeout(3)  # Time for crane movement
            req = self.trucks.request()
            yield req
            # Comment the below line to supress container offload log
            print(f'{self.env.now} : {self.name} QuayCrane offloading container id {i}')
            yield self.env.timeout(6)  # Time for truck movement
            self.trucks.release(req)
        print(f'{self.env.now} : {self.name} QuayCrane container offloading operation finished')

class Vessel:
    """Represents a vessel arriving at the port."""
    def __init__(self, env, name, berth, trucks, container):
        self.env = env
        self.name = name
        self.berth = berth
        self.trucks = trucks
        self.container = container

    def berth_vessel(self):
        """Simulate vessels berthing at the port and being processed"""
        req = self.berth.request()
        yield req
        print(f'{self.env.now} : {self.name} berthed')
        yield self.env.process(QuayCrane(self.env, self.name, self.trucks).offload(self.container))
        print(f'{self.env.now} : {self.name} leaving the port')
        self.berth.release(req)

class Simulation:
    """Simulate vessels arriving at the port and being processed."""
    def __init__(self, sim_duration, no_container, no_berth, no_trucks, vessel_arival_time):
        self.sim_duration = sim_duration
        self.no_berth = no_berth
        self.no_trucks = no_trucks
        self.no_container =  no_container
        self.vessel_arival_time = vessel_arival_time
        self.env = simpy.Environment()

    def simulate(self):
        """Simulate vessels arriving at the port and being processed"""
        berth = Berth(self.env, capacity=self.no_berth)
        trucks = Trucks(self.env, capacity=self.no_trucks)
        i = itertools.count()
        while True:
            vessel_name = f'Vessel_{next(i)}'
            print(f'{self.env.now} : {vessel_name} arrived to the port')
            self.env.process(Vessel(self.env, vessel_name, berth, trucks, self.no_container).berth_vessel())

            # Adjust time between vessel arrivals based on exponential distribution
            yield self.env.timeout(random.expovariate(1 / self.vessel_arival_time)) 

    def run_simulation(self):
        """Runs the simulation until the specified duration"""
        self.env.process(self.simulate())
        self.env.run(until=self.sim_duration)

def main():
    SIM_DURATION = 24 * 60
    NO_CONTAINER = 150
    NO_BERTH = 2
    NO_TRUCKS = 3
    VESSEL_ARIVAL_TIME = 300 # 5 hours * 60 minutes = 300 minutes

    sim = Simulation(SIM_DURATION, NO_CONTAINER, NO_BERTH, NO_TRUCKS, VESSEL_ARIVAL_TIME)
    sim.run_simulation()

if __name__ == "__main__":
    main()
