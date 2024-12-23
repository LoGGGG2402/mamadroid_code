import os
import platform

def _build_classpath():
    script_dir = os.getcwd()
    soot_dir = os.path.join(script_dir, "soot")
    
    # Include xmlpull jar
    required_jars = [
        "soot-trunk.jar",
        "soot-infoflow.jar",
        "soot-infoflow-android.jar",
        "axml-2.0.jar",
        "slf4j-simple-1.7.5.jar",
        "slf4j-api-1.7.5.jar"
    ]
    
    # Use appropriate path separator based on OS
    separator = ";" if platform.system() == "Windows" else ":"
    
    # Build classpath
    classpath_parts = [script_dir]
    for jar in required_jars:
        jar_path = os.path.join(soot_dir, jar)
        if not os.path.isfile(jar_path):
            raise Exception(f"Error: {jar} not found in {soot_dir}")
        classpath_parts.append(jar_path)
    
    classpath = separator.join(classpath_parts)
    return classpath

def runJavac():
    cmd = f'javac -cp "{_build_classpath()}" Appgraph.java'
    print(cmd)
    os.system(cmd)
    return

runJavac()