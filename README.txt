The Wind Energy Toolkit
------------------------

1     Introduction
------------------------
The Wind Energy Toolkit is a compilation of software tools aimed towards students. It
performs functions that relate to preliminary wind turbine design and analysis. It features
six core libraries that cover topics in wind data analysis, data synthesis, aerodynamics,
vibrations, electrodynamics and system performance. The code is designed to be used in
conjunction with a course using the text Wind Energy Explained by James Manwell, et.
al. This software is a Python port and hopefully advancement of the original Wind Energy
Engineering Toolkit that was written in Visual Basic. This document describes how to use
the functions that the software can currently perform. More information can be found at
http://umass.edu/windenergy in the research tools section. 

The code can be obtained at http://code.google.com/p/windenergytk.
    
For comments or questions, please feel free to email me: akoumjian@gmail.com.

2     Installation
------------------------
The toolkit may be installed as a Python module using the easy install utilities. At the
moment the dependencies have to be obtained from their respective website or the Python
Package Index.
    
Dependencies for the Core Libraries:
   1. Numpy = 1.3
   2. Scipy = 0.7.0
   3. Scikits.timeseries

Dependencies for the graphic interface:
   1. Matplotlib = .98
   2. wxPython = 2.8
   3. wxmpl
    
Once the dependencies are sucessfully installed, download and untar the toolkit source.
   
   # tar -xzf windenergy-0.10.54.tgz

Then use the python install script from within the untarred directory and the toolkit
should be added to your path. Depending on your system you may need root privileges.

   # cd windenergytk/
   # python setup.py install

3    For more help please see ../docs/user_manual.pdf
