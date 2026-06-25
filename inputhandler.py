import os
import time
import re

from enum import Enum

from dataclasses import dataclass

from evaluate import Context

@dataclass
class pcore_file:
    name: str
    path: str
    last_mod: time

class updateMode(Enum):
    MANUEL = "manuel"
    AUTO = "auto"
    ON_SAVE = "on_save"

class outputMode(Enum):
    FILE = "file"
    PRINT = "print"

class FileHandler:

    def __init__(self):
        self.files: dict[str, pcore_file] = {}
        self.ctx = Context()
        self.display_node = None
        self.updatemode: updateMode = updateMode.ON_SAVE
        self.outputmode: outputMode = outputMode.FILE

    def register_file(self,path : str):
        file_name = path.split("/")[-1]
        self.files[file_name] = pcore_file(file_name,path,os.path.getmtime(path))

    def start(self):
        
        try:
            self.parse_all()
            self.output()
        except Exception as e:
            self.output(str(e))

        while True:
            for file in self.files.values():
                curent_mod_time = os.path.getmtime(file.path)

                if (curent_mod_time != file.last_mod) or self.updatemode == updateMode.AUTO:
                    file.last_mod = curent_mod_time
                    
                    try:
                        self.parse_all()
                        self.ctx.cache.clear()
                        self.output()

                    except Exception as e:
                        self.output(str(e))

                    


                time.sleep(0.2)
                    
    def output(self,msg:str=None):
        out = msg or self.ctx.get_node_output(self.display_node)
        if self.outputmode == outputMode.FILE:
            with open("Pcore_preview_output.txt","w") as f:
                f.write(out)
    
        elif self.outputmode == outputMode.PRINT:
            out



    def parse_all(self):
        
        for file in self.files.values():
            file.last_mod = os.path.getmtime(file.path)
            with open(file.path, "r") as f:
                self.parse(f.read())
        


    def parse(self, text: str):
        current_name = None
        current_lines = []

        for line in text.splitlines():
            match = re.match(r'^\$\$(\w+)\$\$\s*$', line)
            if match:
                if current_name is not None:
                    self.ctx.register_node(current_name,"\n".join(current_lines).strip())
                current_name = match.group(1)
                current_lines = []
            else:
                current_lines.append(line.replace(r'\$\$', '$$'))

        if current_name is not None:
            self.ctx.register_node(current_name,"\n".join(current_lines).strip())

        
