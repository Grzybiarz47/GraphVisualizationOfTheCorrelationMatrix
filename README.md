# GraphVisualizationOfTheCorrelationMatrix
##### A project created for the needs of Master Thesis

### Installation 
It is recommended to use virtual environment during installation.  
All required dependencies can be downloaded by running script _./setup.sh_.  
Downloaded requirements can be removed with _./clean.sh_ script.  
To open application type _python main.py_ command.

### Interface
##### Set data directory
First section of app interface allows to read folder with csv files containing data about stock exchange companies. Setting a path to directory is obligatory. User can also choose column from csv file. Example data for the application is placed in _/data_ folder.  
![alt text](docs\header.png)
##### Choose plotting option
In second section, user can choose to:
- draw graph representation for given window
- draw correlation matrix for given window
- plot metrics for given window size and window step

For first two options user must set window start and window end
For third option user must set window size and window step
Additional option "Draw stats together" allows to plot results for classical covariance matrix estimator and RIE estimator together.  
![alt text](docs\plotting_section.png)
##### Choose type of the graph
If user chose not to draw correlation matrix in previous section, graph type should be selected. For second and third graph it is necessary to enter number of edges or number of neighbours parameter.  
![alt text](docs\graph_type.png)
##### Shrinkage option
In this section, user can decide whether to apply shrinkage or not.
![alt text](docs\shrinkage_options.png)
##### Graph representation
In graph representation section, the user can choose arrangement of vertices in graph layout.

![alt text](docs\graph_repr.png)

### Sample results
![alt text](docs\graph_example.png)
![alt text](docs\metrics_example.png)