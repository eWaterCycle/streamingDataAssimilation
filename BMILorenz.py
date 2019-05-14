#! /usr/bin/env python



import numpy as np
import yaml


from BMI import BMI
#from scipy import ndimage

def rk4(state, dt, F):
    k1 = f(state,F)
    k2 = f(state + 0.5 * dt * k1,F)
    k3 = f(state + 0.5 * dt * k2,F)
    k4 = f(state + dt * k3, F)
    return (1/6) * dt * (k1 + 2 * k2 + 2 * k3 + k4)

def f(state,F):
    J = len(state)
    k = np.zeros(J)

    k[0] = (state[1]-state[J-2]) * state[J-1] - state[0]
    k[1] = (state[2] - state[J-1])*state[0] - state[1]
    k[J-1] = (state[0] - state[J-3])*state[J-2] - state[J-1]

    for j in range(2,J-1):
        k[j] =(state[j+1] - state[j-2])*state[j-1] - state[j]

    return k + F


class BMILorenz (BMI):
    _var_units = {'state': '[-]'}
    _name = 'Example Python Lorenz model, BMI'
    _input_var_names = ['state']
    _output_var_names = ['state']

    def __init__ (self):
        self._dt = 0
        self._t = 0.
        self._startTime = 0.
        self._endTime = 0.

        self._state = None
        
        self._value = {}
        
        self._shape = (0, 0)
        self._spacing = (0., 0.)
        self._origin = (0., 0.)


    def initialize (self, settingsFile):

        # Read settings YAML file
        with open(settingsFile, 'r') as stream:
            settings = yaml.safe_load(stream)

        self._dt = settings['dt']
        self._t = 0.
        self._startTime = settings['startTime']
        self._endTime = settings['endTime']
        
        self._J = settings['J']
        self._F = settings['F']



        self._state = settings['startState']
       

        self._value['state'] = "_state"

        self._shape = (self._J, 1)
        self._spacing = (1., 1.)
        self._origin = (0., 0.)

        

    def update (self):
        if self._t >= self._endTime:
            raise "endTime already reached, model not updated"
        self._state = self._state + rk4(self._state, self._dt, self._F)
        
        self._t += self._dt

                
    def update_until (self, t):
        if (t<self._t) or t>self._endTime:
            raise "wrong time input: smaller than model time or larger than endTime"
        while self._t < t:
            self.update ()

    def finalize (self):
        self._dt = 0
        self._t = 0

        self._state = None


    def get_var_type (self, long_var_name):
        return str (self.get_value (long_var_name).dtype)
    def get_var_units (self, long_var_name):
        return self._var_units[long_var_name]
    def get_var_rank (self, long_var_name):
        return self.get_value (long_var_name).ndim

    def get_value (self, long_var_name):
        return getattr(self,self._value[long_var_name])
    def get_value_at_indices (self, long_var_name, indices):
        return self.get_value(long_var_name)[indices]
    def set_value (self, long_var_name, src):
        val = self.get_value (long_var_name)
        val[:] = src
		
    def set_value_at_indices (self, long_var_name, indices, src):
        val = self.get_value (long_var_name)
        val[indices] = src

    def get_component_name (self):
        return self._name
    def get_input_var_names (self):
        return self._input_var_names
    def get_output_var_names (self):
        return self._output_var_names

    def get_grid_shape (self, long_var_name):
        return self.get_value (long_var_name).shape
    def get_grid_spacing (self, long_var_name):
        return self._spacing
    def get_grid_origin (self, long_var_name):
        return self._origin

    def get_grid_type (self, long_var_name):
        if self._value.has_key (long_var_name):
            return BmiGridType.UNIFORM
        else:
            return BmiGridType.UNKNOWN

    def get_start_time (self):
        return self._startTime
    def get_end_time (self):
        return self._endTime
    def get_current_time (self):
        return self._t
    def get_time_units(self):
        return "dimensionless time"
    def get_time_step(self):
        return self._dt

    def get_var_grid(self, name):
        raise("method not implemented")
    def get_var_itemsize(self, name):
        raise("method not implemented")
    def get_var_nbytes(self, name):
        raise("method not implemented")
    def get_var_location(self, name):
        raise("method not implemented")
    def get_value_ptr(self, name):
        raise("method not implemented")
    def get_grid_rank(self, grid):
        raise("method not implemented")
    def get_grid_size(self, grid):
        raise("method not implemented")
    def get_grid_type(self, grid):
        raise("method not implemented")
    def get_grid_shape(self, grid, shape):
        raise("method not implemented")
    def get_grid_spacing(self, grid, spacing):
        raise("method not implemented")
    def get_grid_origin(self, grid, origin):
        raise("method not implemented")
    def get_grid_x(self, grid, x):
        raise("method not implemented")
    def get_grid_y(self, grid, y):
        raise("method not implemented")
    def get_grid_z(self, grid, z):
        raise("method not implemented")
    def get_grid_node_count(self, grid):
        raise("method not implemented")
    def get_grid_edge_count(self, grid):
        raise("method not implemented")
    def get_grid_face_count(self, grid):
        raise("method not implemented")
    def get_grid_edge_nodes(self, grid, edge_nodes):
        raise("method not implemented")
    def get_grid_face_nodes(self, grid, face_nodes):
        raise("method not implemented")
    def get_grid_nodes_per_face(self, grid, nodes_per_face):
        raise("method not implemented")
    
        

def main():
    import doctest
    doctest.testmod ()

if __name__ == '__main__':
    main ()
