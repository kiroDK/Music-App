class myvalidate:
    def required(self,frm):
        for f in frm:
            if f=="":
                return False
        return True