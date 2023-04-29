import tkinter as tk
import importlib, os, json

def getModules(source):
    files = list(filter(lambda o: o.endswith(".py"), os.listdir(source)))
    output = {}
    for f in files:
        fn = f[:-3]
        output.update({fn: getattr(importlib.import_module(".."+fn, source + "."), fn)})
    return output


def main():
    root = tk.Tk()
    root.title("ProtoCore Config Editor")
    root.geometry("500x300")

    config = json.load(open("config.json"))
    frames = {}
    for i in range(len(config["DisplaySources"])):
        ds = config["DisplaySources"][i]
        frame = tk.Frame(root, highlightbackground="black", highlightthickness=2, width=120, height=100)
        frame.grid_propagate(False)

        nameLabel = tk.Label(frame, text=ds["Name"])
        typeLabel = tk.Label(frame, text=ds["Type"])
        nameLabel.grid(column=1, columnspan=2, row=0)
        typeLabel.grid(column=1, columnspan=2, row=1)

        frame.grid(column=0, row=i)
        
    

    root.mainloop()

if __name__ == "__main__":
    main()