User Guide for Simple Viewer
This tool is written in python scripts, and it needs python version 2.7 to run
Following commands are some dependencies you need to install before running this tool
	
	sudo apt-get install qt4-qmake
	sudo apt-get install qt4-dev-tools
	sudo pip isntall PySide
	sudo pip isntall numpy
	sudo pip install pyqtgraph
	sudo pip install PyOpenGL

Next you need to modified your environment to let Simple Viewer know your SDK position.
You can either modified ~/.bashrc file OR just export the following Environment values

##SDK environment
export VOXEL_SDK_PATH={path to depth-eye-sdk-ubuntu}
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$VOXEL_SDK_PATH/lib
export PATH=$VOXEL_SDK_PATH/lib:$VOXEL_SDK_PATH/bin:$PATH
export PYTHONPATH=$VOXEL_SDK_PATH/lib/python2.7:$PYTHONPATH

Then you can go to tools/SimpleViewer directory to execute the following command
python ./SimpleViewer.py