# Introduction #

The Wind Energy Toolkit is a compilation of software tools aimed towards students. It
performs functions that relate to preliminary wind turbine design and analysis. It features
six core libraries that cover topics in wind data analysis, data synthesis, aerodynamics,
vibrations, electrodynamics and system performance. The code is designed to be used in
conjunction with a course using the text Wind Energy Explained by James Manwell, et.
al. This software is a Python port and hopefully advancement of the original Wind Energy
Engineering Toolkit that was written in Visual Basic.

For comments or questions, please feel free to email me: akoumjian@gmail.com.

# Components #
The toolkit is a Python package that includes modules for each group of codes. In addition, a rudimentary graphical interface is included but is currently under serious development.

| **Analysis** | 100% |
|:-------------|:-----|
|Statistics of a file | ✓ |
|Histogram of a file | ✓ |
|Weibull parameters from a wind file | ✓ |
|Autocorrelation of a file | ✓ |
|Crosscorrelation of 2 files | ✓ |
|Block averaging of a file | ✓ |
|Power spectral density of a file | ✓ |
| **Synthesis** | 66.7% |
|ARMA Time Series Generator | ✓ |
|Markov process transition probability matrix Generator | ✓ |
|Use of Markov process TPM to generate data | ✓ |
|Hourly wind speed generator including diurnal scaling | ✓ |
|Hourly load generator including diurnal scaling | X |
|Turbulent wind generator (Shinozuka method) | X |
| **Rotor Aerodynamics** | 100% |
|Optimum rotor design | ✓ |
|Rotor analysis/linearized method | ✓ |
|Rotor analysis using blade element momentum theory | ✓ |
|**Rotor Mechanics** | 60% |
|Vibration of a uniform beam (Euler method) | ✓ |
|Vibration of non-uniform, possibly rotating, beam (Myklestad method) | ✓ |
|Hinge-spring blade rotor flapping dynamics (Eggleston and Stoddard) | ✓ |
|Rotating system dynamics (Holzer) | X |
|Rainflow cycle counting | X |
| **Electrodynamics** | 0% |
| **System Performance** | 0% |
| **Graphical Interface** | 40% |
| **File Utilities** | 50% |
|Reading Wind Data Files | ✓ |
|Reading Blade Dimension Files | X |


# Installation #
  1. Select a release from the Downloads section.
  1. Untar the archive
  1. Use setuptools to install:
> > `$ python setup.py install `