# Drexel Enrollment Checker
This script is used to check if a class opens up on the term master schedule for Drexel University

## Usage
The script takes 1 arguement, interval, which is used to indicate how often to check if a class opens up. 60 (seconds) works well.  

```python check.py <INTERVAL>```

In order to put the classes in that you want to check, put the links to the class information on in the file `links.txt` seperated by new lines.
The script will check if a class is marked as CLOSED or not, and if it is not closed the script will output to the console and provide a windows 10 notification.
