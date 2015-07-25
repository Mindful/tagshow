import os
import stat



class ShowBuilder:

    def __init__(self):
        self.commands = []
        self.name = ""


    def record_command(self, cmd):
        self.commands.append(cmd)


    def output(self, name, importpath):
        output = "#!/usr/bin/env python3\nimport sys\nsys.path.append(\""+importpath+"\")\nfrom tagshow import *\n\n"
        for cmd in self.commands:
            output += cmd +"\n"
        output += "\n\n"
        out_name = name+"_builder"
        with open(out_name, 'w') as f:
            f.write(output)
        st = os.stat(out_name)
        os.chmod(out_name, st.st_mode |  stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


