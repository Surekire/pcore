from parser import Parser,dump
from evaluate import Context
from inputhandler import FileHandler, updateMode, outputMode
import functions

p = FileHandler()

p.register_file("./test.pcore")
p.display_node = "out"
p.outputmode = outputMode.FILE
p.updatemode = updateMode.ON_SAVE
p.start()