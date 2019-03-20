#from abc import ABC

cdef class Animator():
    def __init__(self, AudioSource, Screen):
        self.audio_source = AudioSource
        self.screen = Screen
    
    cpdef start(self):
        self.audio_source.start()
    
    cdef animate(self, list data):
        """Animate the color screen; require a call to Animator.screen.display
        
        Args:
            data ([np float array]): sound data from the AudioSource
        """
        pass
    