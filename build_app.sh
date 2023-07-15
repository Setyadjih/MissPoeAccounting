# Freeze application to exe
pyinstaller app.spec

# Get version, awk to split text on quotes
ver=$(grep "VER" ./core/constants.py | awk -F'"' '{print $2}')

# Zip Executable
tar -a -c -f "dist/Poe Excel Automator $ver.zip" "dist/Poe Excel Automator $ver.exe"