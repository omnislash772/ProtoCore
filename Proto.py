import importlib
import os, json, time
import multiprocessing
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
            
            skip = False
            for input in t.inputs:
                if input["name"] not in newFrames.keys():
                    skip = True
            if not skip:
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

def main(cfg, sharedDict):
    print(__name__)
    loadModules()
    config = json.load(open(cfg))
    configGroups = ["DisplaySources", "InputSources", "Outputs"]
    objects = loadObjectList(configGroups, config)
    transforms = loadObjects(config["Transforms"])
    sharedDict.update(getVars(objects))
    time.sleep(5)

    while(True):
        sharedDict.update(getVars(objects))
        frames = getSourceFrames(objects, dict(sharedDict))
        frames = runTransforms(transforms, frames, dict(sharedDict))
        sendOutputs(objects, config, frames)

def subMain(cfg, sharedDict):
    proc = multiprocessing.Process(target=main, args=(cfg, sharedDict,), daemon=True, name=cfg.split(".")[0])
    proc.start()
if __name__ == "__main__":
    manager = multiprocessing.Manager()
    sharedDict = manager.dict()
    subMain("config-hud.json", sharedDict)
    subMain("config.json", sharedDict)
    while(True):
        time.sleep(1)
