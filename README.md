# PCore

PCore is a lightweight, extensible text replacement tool designed to eliminate repetitive manual updates across unrelated parts of a codebase. Define your values once, and let PCore propagate changes everywhere automatically.

# Example

### test.pcore
```
$$a$$
<div>
    <p>@i</p>
</div>

$$b$$
l(hier könnte irgendwas stehen, oder auch das hier einfach,noch irgendwas wenn dir langweilig ist)

$$c$$
for(<div>
    <p>@i</p>
</div>\n,l(i),$b$)

$$out$$
$c$
```

### output

```
<div>
    <p>hier könnte irgendwas stehen</p>
</div>
<div>
    <p>oder auch das hier einfach</p>
</div>
<div>
    <p>noch irgendwas wenn dir langweilig ist</p>
</div>
```

### Usage

Take a look in [main.py](./main.py). Here you can see how to register a inputfile, of wich you can have multiple (not teste yet). You can adjuste some settings, but moste of them will be implemented in later versions. the display node is the node wich will be evaluated and output. With the start function the programm will run untill terminatet, then it will fetch text in the registerd files, registers the Nodes in the Context and evaluates the displayed node wich may evaluate other nodes in the process.

The outputfile (if outputMode is File) will be generaded and will updated when even one of the registed files is modified

```[python]
p = FileHandler()

p.register_file("./test.pcore")
p.display_node = "out"
p.outputmode = outputMode.FILE
p.updatemode = updateMode.ON_SAVE
p.start()
```

### custom functions
You may introduce your own functions to the project by adding the function definition in [functions.py](./functions.py)

take a carefull look on the given functions and remeber that the args are not text! but the AST of the inner living of the function inputs which may wanna by lazy evaluated with

`ctx.evaluate[args[...]]`


#### Example
```
#args[0] to reapeatet Text
#args[1] number of repeats
@pcore_function("r")
def repeat(ctx : Context, args):
    args = [ ctx.evaluate(a) for a in args ]
    a = int(args[1])
    return args[0]*a
```

the decorator function `@pcore_function` is used to register the functions in the Context. you can juse like in the example a name to easaly call your function in the programm

```
$$a$$
r(Hello,2)
```

```
HelloHello
```


## Sytax


### System
`$$<nodeID>$$` - Use that to specifie a node. its impotend to write it in the beginning of the line and do a line brake right after for recognition. as the nodes might contain arbitray text this is importend till later fix


### Node

`$<nodeID>$` - Use this to replace it with the node that has this exacte node ID

`@<varName>` - Used for variables like in the for loop in the example. There is no garantie that a variable is still existent outside of a loop, they might just get overwritten by other function so look into the execution of the functions your using!

`<FunctionName>(<args>)` - This is a Function call that can get any number of arguments, delimited by ",". feel free to use "\\" to escape some charcters like , for special cases.





## Keep in mind!
this is still under developmend and might change Rapidly!

The tool and i are not Reliable for any damage that might result in any way used.

The outputfile is hardcoded at the moment to be namded Pcore_preview_putput.txt. if you have a file with that name, i will get overwritten!

untill a stable and tested version is provided all Rights are reserved. 

Contibution is wellcome

