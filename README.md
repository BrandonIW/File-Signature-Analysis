# File-Signature-Analysis
This program takes in a simple txt file of Extension/Signature pairs and builds a sqlite DB from the pairings. The user then can select files to analyze. The program will extract the expected hex signature value from the SQLite DB and compare it to the signature of the given file. The logging system informs the user if there is a successful match or not. 

The program can be easily expanded by simply adding additional extension/signatures to the .txt file 


i.e.
If a JPG image is analyzed, the program will:
1) Lookup the expected Hex signature of a .jpg image in the SQL Database (FF D8 FF)
2) Open up the provided JPG image in binary mode and convert to a Hex representation
3) Extract the first len(expected hex signature) number of hex characters from the beginning of the JPG image
4) Compared the expected signature with the actual to determine if there is a match  


# Compatability
* Runs on Python 3.9
* Currently only tested for the provided extensions in the .txt file
* Tested on Windows 10 Version 10.0.19044 Build 19044


# Quickstart
1) Download .ZIP File and extract to a directory of your choice
2) Example Input files are provided in the 'TestFiles' Folder for testing
3) ```python3 main.py -c ```
4) Input the path of the text file to build the SQLite DB
5) Input the path of the image you want to examine 


# Example Output
1) Successful match
![image](https://user-images.githubusercontent.com/77559638/171912953-d093c41c-cf7e-4cb3-8e7e-213c9e290ff3.png)

![image](https://user-images.githubusercontent.com/77559638/171912981-891bef8c-2793-4e22-b4cd-27c5e8d7e188.png)

2) Unsuccessful match
![image](https://user-images.githubusercontent.com/77559638/171913072-8b623388-6cbe-46d8-8f86-9af1522a0a97.png)

![image](https://user-images.githubusercontent.com/77559638/171913103-eb297141-ccc3-4720-93b0-5805f0e68b0a.png)



