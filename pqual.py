import coreFunctions


PROXY_A = ""
PROXY_B = ""
MODES = ["proxy","no_proxy","screenshot"]

def compare(*args,mode="screenshot",report="false"):

    coreFunctions.generateReport = report

    if not 1<=len(args)<=2:
        raise ValueError("Recieved unknown number of arguments. refer to the documentation")

    if mode not in MODES:
        raise ValueError("Wrong mode. refer to the documentation")

    if mode == "proxy":
        if len(args)!=1: raise ValueError("Recieved unknown number of arguments. refer to the documentation")
        print(args)
        return coreFunctions.compareWithProxy(args[0],PROXY_A,PROXY_B)
    elif mode == "no_proxy":
        if len(args)!=2: raise ValueError("Recieved unknown number of arguments. refer to the documentation")
        return coreFunctions.compareWithNoProxy(args[0],args[1])
    elif mode == "screenshot":
        if len(args)!=2: raise ValueError("Recieved unknown number of arguments. refer to the documentation")
        return coreFunctions.compareWithScreenshots(args[0],args[1])
