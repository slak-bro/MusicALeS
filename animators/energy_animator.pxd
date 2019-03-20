from animators.animator cimport Animator
import numpy as np


cdef class EnergyAnimator(Animator):

    cdef:
        int val
        list buffer
        float last_value

    cdef smooth_value(self, int value)
    cpdef start(self)