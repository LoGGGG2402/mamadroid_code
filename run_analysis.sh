#!/bin/bash

# Enable debug logging
set -x

# Validate inputs first
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <apk-file> <android-platform-path>"
    exit 1
fi

# Set working directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SOOT_DIR="$SCRIPT_DIR/soot"

# Add after REQUIRED_JARS declaration
# Validate Android SDK platform
ANDROID_API_LEVEL=3  # Default to a recent API level
ANDROID_JAR="$2/android-$ANDROID_API_LEVEL/android.jar"

# Verify Android SDK platform exists
if [ ! -f "$ANDROID_JAR" ]; then
    echo "Error: Android platform SDK not found at $ANDROID_JAR"
    echo "Available platforms:"
    ls -1 "$2"
    exit 1
fi

# Continue with existing classpath building...
# Validate inputs
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <apk-file> <android-platform-path>"
    exit 1
fi

# Check Java installation
if ! command -v java &> /dev/null; then
    echo "Error: Java is not installed"
    exit 1
fi

# Set working directory to script location
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SOOT_DIR="$SCRIPT_DIR/soot"

# Check if soot directory exists
if [ ! -d "$SOOT_DIR" ]; then
    echo "Error: soot directory not found in $SCRIPT_DIR"
    exit 1
fi

# Required JAR files
REQUIRED_JARS=(
    "soot-trunk.jar"
    "soot-infoflow.jar" 
    "soot-infoflow-android.jar"
    "axml-2.0.jar"
    "slf4j-simple-1.7.5.jar"
    "slf4j-api-1.7.5.jar"
)

# Build classpath
CLASSPATH="$SCRIPT_DIR"
for jar in "${REQUIRED_JARS[@]}"; do
    if [ ! -f "$SOOT_DIR/$jar" ]; then
        echo "Error: $jar not found in $SOOT_DIR"
        exit 1
    fi
    echo "Found $jar in soot directory"
    CLASSPATH="$CLASSPATH:$SOOT_DIR/$jar"
done

echo "Using classpath: $CLASSPATH"
echo "Running analysis..."

# Run Java application
java -cp "$CLASSPATH" Appgraph "$1" "$2"