import mesa
import random
import numpy as np
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def agent_portrayal(agent):
        portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "blue",
                 "r": 0.5}
        #Caso en el que sea semáforo
        if isinstance(agent,entornoAgent):
            portrayal["Color"] = "black"
        if isinstance(agent,SemaforoAgent1) or isinstance(agent,SemaforoAgent2):
            portrayal["Color"] = agent.status
        return portrayal


def prueba(model):
    return 0

#Conductor que se pasa el semáforo
class CarAgent1(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.nombre = unique_id
    def move(self):
        #list1 = [0,1,2]
        x,y = self.pos
        self.model.grid.move_agent(self,(x + 1, y))

    def compara(self):
        self.neighborhood = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False,radius = 5)
        self.neighbors =  self.model.grid.get_cell_list_contents(self.neighborhood)
        for i in self.neighbors:
            if self.pos == (9,5) and (isinstance(i,SemaforoAgent1)):
                i.status = "yellow"
            if self.pos == (9,5) and (isinstance(i,SemaforoAgent2)):
                i.status = "yellow"

    def step(self):
        self.compara()
        self.move()
#Conductor con comportamiento estable.
class CarAgent2(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.nombre = unique_id
    def move(self):
        x,y = self.pos
        self.model.grid.move_agent(self, (x,y-1))
        
    def compara(self):
        self.neighborhood = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False,radius = 5)
        self.neighbors =  self.model.grid.get_cell_list_contents(self.neighborhood)
        for i in self.neighbors:
            if self.pos == (5,1) and (isinstance(i,SemaforoAgent2)):
                i.status = "yellow"
            if self.pos == (5,1) and (isinstance(i,SemaforoAgent1)):
                i.status = "yellow"
                
        #self.empty_neighbors = [c for c in self.neighborhood if self.model.grid.is_cell_empty(c)]

    def step(self):
        self.compara()
        self.move()


class SemaforoAgent1(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.nombre = unique_id
        self.status = "yellow"
        self.conteo = 0
    def move(self):
        x,y = self.pos
        new_position = x,y
        self.model.grid.move_agent(self,new_position)

    def compara(self):
        self.neighborhood = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False,radius = 2)
        self.neighbors =  self.model.grid.get_cell_list_contents(self.neighborhood)
        #self.empty_neighbors = [c for c in self.neighborhood if self.model.grid.is_cell_empty(c)]
    def step(self):
        self.compara()
        self.move() 
        for i in self.neighbors:
            if isinstance(i,CarAgent1):
                self.status = "red"
                for j in self.neighbors:
                    if isinstance(j,SemaforoAgent2):
                        j.status = "green"

                print("Coche vecino tipo Agente 1" + " en " + str(i.pos) +"acercandose a "+" "+self.unique_id)
class SemaforoAgent2(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.nombre = unique_id
        self.status = "yellow"
        self.conteo = False
    def move(self):
        x,y = self.pos
        new_position = x,y
        self.model.grid.move_agent(self,new_position)

    def compara(self):
        self.neighborhood = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False,radius = 2)
        self.neighbors =  self.model.grid.get_cell_list_contents(self.neighborhood)

    def step(self):
        self.compara()
        self.move() 
        for i in self.neighbors:
            if isinstance(i,CarAgent2):
                self.conteo = True
                self.status = "red"
                for j in self.neighbors:
                    if isinstance(j,SemaforoAgent1):
                        j.status = "green"

                print("Coche vecino tipo Agente 2" + " en " + str(i.pos) +"acercandose a "+" "+self.unique_id)
        

#
class entornoAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.nombre = unique_id
    def move(self):
        x,y = self.pos
        new_position = x,y
        self.model.grid.move_agent(self, new_position)
    def step(self):
        self.move()

class CarModel(mesa.Model):
    def __init__(self, N,width, height):
        self.numAgentsCar = N
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True

            #Creando agentes para carro
        conteo = 0
        
        classes = [CarAgent1,CarAgent2]

      

        for i in range (5):
            for j in range(5):
                c = entornoAgent("E" + str(conteo), self)
                self.schedule.add(c)
                x = i
                y = j
                self.grid.place_agent(c, (x, y))
                conteo += 1
        
        for i in range (5):
            for j in range(6,11):
                c = entornoAgent("E" + str(conteo), self)
                self.schedule.add(c)
                x = i
                y = j
                self.grid.place_agent(c, (x, y))
                conteo += 1
        
        for i in range (6,11):
            for j in range(5):
                c = entornoAgent("E" + str(conteo), self)
                self.schedule.add(c)
                x = i
                y = j
                self.grid.place_agent(c, (x, y))
                conteo += 1

        for i in range (6,11):
            for j in range(6,11):
                c = entornoAgent("E" + str(conteo), self)
                self.schedule.add(c)
                x = i
                y = j
                self.grid.place_agent(c, (x, y))
                conteo += 1
        for i in range(self.numAgentsCar):
            #instance = random.choice(classes)()
            a = random.choice(classes)("C" + str(i), self)
            #a = CarAgent1("C" + str(i), self)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            if isinstance(a,CarAgent1):
                x = 0
                y = 5
                self.grid.place_agent(a,(x,y))

            if isinstance(a,CarAgent2):
                x = 5
                y = 10
                self.grid.place_agent(a,(x,y))

        s1 = SemaforoAgent1("S" + str(1),self)
        self.schedule.add(s1)
        x1 = 4
        y1 = 5 
        self.grid.place_agent(s1,(4,5))
        s2 = SemaforoAgent2("S" + str(2),self)
        self.schedule.add(s2)
        x2 = 4
        y2 = 5 
        self.grid.place_agent(s2,(5,6))


        

        
        self.datacollector = mesa.DataCollector(
            model_reporters={"Gini": prueba}, agent_reporters={"Wealth": "nombre"}
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()


grid = mesa.visualization.CanvasGrid(agent_portrayal, 11, 11, 500, 500)
server = mesa.visualization.ModularServer(
    CarModel, [grid], "Car Model", {"N": 1, "width": 11, "height": 11}
)

server.port = 8521 # The default
server.launch()