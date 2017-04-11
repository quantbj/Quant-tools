class RM3DWriter:
    
    header = 'START-OF-FILE\nDATEFORMAT=YYYYMMDD\nFIELDSEPARATOR=TAB\nSUBFIELDSEPARATOR=PIPE\nDECIMALSEPARATOR=PERIOD\nSTART-OF-DATA'
    footer = 'END-OF-DATA\nEND-OF-FILE\n'
    
    def __init__(self):
        pass
    
    def produce_string(self, rm3d_list):
        out = '\n'.join(['\t'.join(e) for e in rm3d_list])
        return '\n'.join([self.header, out, self.footer])
