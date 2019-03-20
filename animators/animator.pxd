#from abc import ABC

cdef class Animator():

    cdef:
        audio_source, screen 
    
    cpdef start(self)
    cdef animate(self, list data)