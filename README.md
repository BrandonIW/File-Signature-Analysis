# File-Signature-Analysis
This program takes in a simple txt file of Extension/Signature pairs and builds a sqlite DB from the pairings. The user then can select files to analyze. The program will extract the expected hex signature value from the SQLite DB and compare it to the signature of the given file. The logging system informs the user if there is a successful match or not. 
