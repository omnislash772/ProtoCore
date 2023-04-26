import importlib
import os, json
from DisplaySources import DisplaySource
from InputSources import InputSource
from Outputs import Output

def loadModules():
    moduleSources = ["Outputs", "DisplaySources", "InputSources", "Transforms"]
    for m in moduleSources:
        files = list(filter(lambda o: o.endswith(".py"), os.listdir(m)))
        for f in files:
            print(f"Loading {f}")
            fn = f[:-3]
            globals()[fn] = getattr(importlib.import_module(".."+fn, m + "."), fn)

def loadObjects(objectDesc):
    objects = {}
    for o in objectDesc:
        if "Name" not in o.keys() or "Type" not in o.keys():
            print("Object missing Name or Type, skipping")
            continue
        if o["Type"] not in globals().keys():
            print(f"Object {o['Name']} specified invalid type: {o['Type']}")
            continue

        print(f"Loading {o['Name']}")
        try:
            args = o.get("Args", {})
            objects[o["Name"]] = globals()[o["Type"]](o["Name"], **args)
            print(f"Loaded Object: {o['Name']}")
        except Exception as e:
            print(f"Failed to load Object: {o['Name']}: {repr(e)}")
    return objects

def loadObjectList(descList, config):
    output = {}
    for desc in descList:
        output.update(loadObjects(config[desc]))
    return output

def getVars(objects):
    vars = {}
    for o in objects.values():
        if isinstance(o, InputSource):
            vars.update(o.getValues())
    return vars

def getSourceFrames(objects, vars):
    frames = {}
    for o in objects.values():
        if isinstance(o, DisplaySource):
            frames.update({o.name: o.Output(vars)})
    return frames

def runTransforms(transforms, frames, vars):
    newFrames = frames
    updateCount = -1

    while updateCount != 0:
        updateCount = 0
        for t in transforms.values():
            if t.name in newFrames.keys():
                continue
            if not all(item["name"] in newFrames.keys() for item in t.inputs):
                continue
            result = t.process(newFrames, vars)
            newFrames.update({t.name: result})
            updateCount = updateCount + 1
    
    return newFrames

def sendOutputs(objects, config, frames):
    for m in config["Mappings"]:
        if "Output" not in m.keys():
            continue
        if m["Input"] not in frames.keys():
            continue
        objects[m["Output"]].Input(frames[m["Input"]])

            


if __name__ == "__main__":
    loadModules()
    config = json.load(open("config.json"))
    configGroups = ["DisplaySources", "InputSources", "Outputs"]
    objects = loadObjectList(configGroups, config)
    transforms = loadObjects(config["Transforms"])
    while(True):
        vars = getVars(objects)
        print(vars)
        frames = getSourceFrames(objects, vars)
        frames = runTransforms(transforms, frames, vars)
        sendOutputs(objects, config, frames)