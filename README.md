# RStoCSV

Easy to use program that converts JSON data exports from [Robot Scouter](https://github.com/SUPERCILEX/Robot-Scouter) to CSV for easy analysis in programs like Tableau and Excel!


## Installation
Make sure you have: 

* [Git](https://git-scm.com/)
* [Python](https://www.python.org/)
* [PIP](https://pypi.org/project/pip/)

1. In your terminal of choice, navigate to where you want the folder to be installed. [Click here if that was gibberish](https://www.davidbaumgold.com/tutorials/command-line/).
2. Enter the following command:
`git clone https://github.com/will-hou/RStoCSV.git`
3. You're good to go! RStoCSV is installed locally on your computer!


## Usage
1. Make sure you're in the RStoCSV directory.
2. To convert your Robot Scouter JSON file to CSV, enter:

`python convert.py -p [path_to_your_json_file]` without brackets and path_to_your_json_file being the path to your JSON file. Note, the file cannot be in the RStoCSV directory.

Optional fields: `-f` Removes any scouts that don't have a value for the "Name" metric. Don't use this if you don't have a "Name" metric in your scouting template
 
 3. RStoCSV will automatically analyze your JSON file and find all of the scouted metrics.
 4. A new `.csv` file with the same name will be made in the same directory.
 5. A HTML file called `table.html` will also be created in the local RStoCSV directory for easy visualization.
 
### Example Usage
  Input:
  `python convert.py -p C:/Users/William/Scouting_Data/scout.json`
  
  Output:
  `C:/Users/William/Scouting_Data/scout.csv`
  
 
 
 
 
 
 
 
  
 ## Happy Analyzing :D
