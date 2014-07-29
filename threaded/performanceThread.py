#Begin Class
class performanceThread(Thread):
        sock = None
        server = None
        hs_dor = None
        hs_name = None
        pm = None

        def __init__(self):
                Thread.__init__(self)

        def printVariable(self):
                print self.hs_name

#End Class
