# LabelDroid

## To run this project on your own machine:
  
  ### What You need:
    - Visual Studio
    - An emulator 
    - ADB (Android Debug Bridge)
    - Python (either 2 or 3 is fine)
    - Matlab (any release after 2012)



### Feature Extraction:


    
#### To Extract Widgets (in a csv report) without labeling them:
    1. Clone this repo, or download the project code onto your machine
    2. Put the names of the packages that you'd like to extract the widget information for in a .text file called PackageNames.txt
    3. Place the file in widgeExtractors directory (or directly adit the sample file we have placed there)
    4. Start an emulator (make sure there is only 1 instance of emulator is running)
    5. Make sure the packages that you intend to process are actually installed on the emulator
    6. Go to the directory where widDumper_hsVersion.py file is located (widgetExtractors in this case)
    7. Run the widDumper_hsVersion.p script in python (ie. issue the commant "python widDumper_hsVersion.py")
    * This script will start each application on the emulator and extract the properties of the widgets that are displayed on the first activity of each application.
    * Extracted properties and calculated features will be compiled ina .csv report. 
    
    
#### To Extract Widgets (in a csv report) and label them as username/ password using human expert:
    1. Clone this repo, or download the project code onto your machine
    2. Put the names of the packages that you'd like to extract the widget information for in a .text file called PackageNames.txt
    3. Place the file in widgeLabelers directory (or directly adit the sample file we have placed there)
    4. Start an emulator (make sure there is only 1 instance of emulator is running)
    5. Make sure the packages that you intend to process are actually installed on the emulator
    6. Go to the directory where labelDroid.py file is located (widgeLabelers in this case)
    7. Run the labelDroid.py script in python (ie. issue the commant "python widDumper_hsVersion.py")
    
   
##### labelDroid.py operation:
* This script will start the applications listed in PackageNames.txt one-by-one for each application:
1. The user is prompted to navigate to the desired activity in the application
2. The user is asked to enter the depth of the activity (the initial activity (startup) of an application has a depth of 1), each new activity will be one level deeper. 
* At this point, the user can chose to select a particular widget on an emulator (by tapping on it) and enter a label for that particular widget. Ones the widget is labeled the first 2 steps should be repeated for the same activity, to label other widgets. 
* If none of the widgets on the activity are selected, no labeles will be recorded. 
* Make sure you enter the same depth for the same activity each time you visit it (ones to label username, ones to label password, and a final one to label all othe widgets as not username or password)


#### To Extract Widgets (in a csv report) and label them as username/ password using hint texts:
    1. Clone this repo, or download the project code onto your machine
    2. Put the names of the packages that you'd like to extract the widget information for in a .text file called PackageNames.txt
    3. Place the file in widgeLabelers directory (or directly adit the sample file we have placed there)
    4. Start an emulator (make sure there is only 1 instance of emulator is running)
    5. Make sure the packages that you intend to process are actually installed on the emulator
    6. Go to the directory where labelDroid_automated.py file is located (widgeLabelers in this case)
    7. Run the labelDroid_automated.py script in python (ie. issue the commant "python widDumper_hsVersion.py")
    
   ##### labelDroid_automated.py operation:
* This script will start the applications listed in PackageNames.txt one-by-one for each application:
1. The user is prompted to navigate to the desired activity in the application.
 1. The user is prompted to select the username field and press enter. 
 2. The user is prompted to select the password field and press enter. 
 * Note: This script does not capture the depth on an activity at this point. 
    
    
### Widget Classification:
    
#### To classify widgets using Naiive (string based) approach:
1. Open Matlab and navigate to classifiers/nattiveMethod directory (i.e. set the working directory to this location).
2. You can use the bags of words we have provided or add/remove keywords as you wish. 
3. Load the .csv report you compiled during the Feature Extraction step in Matlab. 
4. Run "labelCombiner.m"
5. Run "naiiveLoader.m"
6. Run "naiiveTester.m"


#### To classify widgets using Logistic Regression:
1. Open Matlab and navigate to classifiers/logisticRegression directory (i.e. set the working directory to this location).
2. Load your training set into Matlab 
* This is should be a .csv report generated using above tools and it must contain labeled examples.
3. Run "train_LrModel_For_UserCred.m" to train a logistic regression model using the labeled features in your .csv report.
* Reported accuracy is the precentage of widgets in your training set that were labeled correctly. 
4. Load you test set. 
* Again this should be a .csv report generated using above tools and it must contain labeled examples.
5. run "calculateAccuracies_For_UserCred.m". This script will report the number of widgets that were correctly classified in the test set, the precision, and the recall of your classifier. 
