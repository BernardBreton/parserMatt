def Parser():
    print(
        "------ > WARNING : MAKE SURE EACH EACH OF THESE PYTHON LIBRARIES IS INSTALLED AND IN THE CORRECT DIRECTORY <------ ")
    print("------------ > pandas\n------------ > numpy")

    # --path C:\Users\mgrub\Desktop\OutputFolder --.ext .dat --type CSV --delimiter ","
    # --path C:\Users\mgrub\Desktop\OutputFolder --.ext .txt --type FWF --delimiter ","

    # --path C:\Users\mgrub\Desktop\OutputFolder --.ext .dat --type CSV --delimiter "," --dummyRow YES
    # --path C:\Users\mgrub\Desktop\OutputFolder --.ext .txt --type FWF --delimiter "," --dummyRow YES

    # --path C:\Users\mgrub\Desktop\OutputFolder --.ext .txt --type FWF --delimiter "," --train YES

    import sys
    import os

    import tkinter as tk
    from tkinter import messagebox
    import hashlib

    import pandas as pd
    import numpy as np

    print('-> Python: {}'.format(sys.version))
    print('-> numpy: {}'.format(np.__version__))
    print('-> pandas: {}'.format(pd.__version__))

    print()

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    #       @@@ SETUP @@@
    pd.options.display.max_columns = 100
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_columns', 100)
    pd.set_option('expand_frame_repr', False)
    np.set_printoptions(linewidth=400)

    print("\t\tFile Parser v1.0 - Parse all files from the the desired folder")
    print(
        "Please enter the command line arguments in this format:\nName of Python Script --path <input folder path> --.ext <file extension> --type <(CSV) comma seperated OR (FWF) fixed width> (FOR CSV: --delimiter <'delimiter'>)")
    print("For help regarding this script, enter: Name of Python Script --help")

    # CSV column headers that will be used when converting dataframe to csv file later in program
    CSVFileHeaders = ("Filename", "date", "type", "Num Rows", "Mean of Len Rows", "Mean of Cols", "Mean of Len Columns",
                      "Number of Columns Std Dev", "Variance of Number of Columns", "is_FixedLength",
                      "File Size (Bytes)", "Number of Repeating Lines")

    root = tk.Tk()
    root.geometry("100x100")
    root.withdraw()

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    #       @@@ CLASS OBJECTS @@@

    class FILE_INFO:  # class object for storing information about each file

        fullFilename = ""
        folderName = ""
        filename = ""
        fixedLength = 0
        nlines = 0
        averageLenRow = 0
        averageLenCol = 0
        averageNCol = 0
        stdDevCol = 0
        modeNCol = 0
        varNCol = 0
        sizeOfFile = 0
        repeatingLineCount = 0

        def Print(self):  # prints the information for each file to the screen
            print("File Info ")
            print("     fullFilename: ............................. '%s'" % (self.fullFilename))
            print("     folderName: ............................... '%s'" % (self.folderName))
            print("     ------------------------------------------------")
            print("     filename: ................................. '%s'" % (self.filename))
            print("     nLines: ................................... '%d'" % (self.nlines))
            print("     Avg Length of Row: ........................ '%.10f'" % (self.averageLenRow))
            print("     Avg Length of Columns: .................... '%.10f'" % (self.averageLenCol))
            print("     Avg nColumns (10 decimal points): ......... '%.10f'" % (self.averageNCol))
            print("     Std Dev of nCols (10 decimal points): ..... '%.10f'" % (self.stdDevCol))
            print("     Variance of columns (10 decimal points): .. '%.10f'" % (self.varNCol))
            print("     Size of File (Bytes): ..................... '%.d'" % (self.sizeOfFile))
            print("     fixedLength: .............................. '%d'" % (self.fixedLength))
            print("     Number of Repeating Lines : ............... '%.d'" % (self.repeatingLineCount))

            # print("     mode of NCols: ............................ '%.5f'"  %    (self.modeNCol)) GETTING THIS ERROR: TypeError: not all arguments converted during string formatting

        # Constructor method with instance variables name and age
        def __init__(self):
            self.fullFilename = ""
            self.folderName = ""
            self.filename = ""
            self.fixedLength = 0
            self.nLines = 0
            self.averageLenRow = 0
            self.averageLenCol = 0
            self.avgNCol = 0
            self.stdDevCol = 0
            self.varNCol = 0
            self.modeNCol = 0
            self.sizeOfFile = 0

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    #       @@@ READING COMMAND LNE ARGUMENTS AND EXECUTING APPROPRIATE CONDITIONS @@@
    begin = False

    if len(sys.argv) >= 1:
        begin = True

    while begin is True:

        if len(sys.argv) == 1:
            messagebox.showerror("Error", "Program requires the input of command line arguments")
            print("\nError ... Program requires the input of command line arguments.")
            break

        if sys.argv[1] == "--help":
            print("\n\nMachine Learning Parser v0.1 2019")
            print("This program is designed to create data that will be inputted into a machine learning algorithm.")
            print(
                "The program will:\n1) Read files in a specified input folder path\n2) Determine if these files are either fixed width formatted or comma seperated (CSV)")
            print(
                "3) Parse the files based on their format\n4) Give values for each file based on these columns:\n\tFilename\n\tNumber of Rows in file\n\tMean of the length of the rows\n\tStandard deviation of the columns\n\tVariance of the columns\n\tIf it is a fixed length or not")
            print("5) Store the values for each row into a comma seperated file (CSV) \n")
            print(
                "\nTo run program, enter the command line arguments in this format: Name of Python Script --path <input folder path> --.ext <file extension> --type <(CSV) comma seperated OR (FWF) fixed width> (FOR CSV: --delimiter <'delimiter'>)")
            print(
                "\nIf you would like a better understanding of how this program works and how it produces its results, documentation is available.")
            break

        CSVFlag = False
        FWFFlag = False
        if sys.argv[6] == "CSV":
            CSVFlag = True
        if sys.argv[6] == "FWF":
            FWFFlag = True
        if CSVFlag is False and FWFFlag is False:
            messagebox.showerror("Error", "Command line arguments were inputted incorrectly ")
            print(
                "WARNING ... COMMAND LINE ARGUMETNS WERE INPUTTED INCORRECTLY\n\t\t\tCOMMAND LINE ARGUMENT --type DID NOT HAVE EITHER CSV or FWF")
            break

        try:
            isTrain = False
            if sys.argv[10] == "YES":
                isTrain = True
            if sys.argv[10] == "NO":
                pass
            elif sys.argv[10] != "YES":
                messagebox.showerror("Error",
                                     "Did not specify whether or not the files to be parsed will be Train data or Test data. YES for train | NO for test")
                print(
                    "Error .... Did not specify whether or not the files to be parsed will be Train data or Test data. YES for train | NO for test")
                break
        except IndexError:
            messagebox.showerror("Error",
                                 "Did not enter sufficient amount of command line arguments. Enter --help as the first command line argument for more information on this script")
            print(
                "Error .... Did not enter sufficient amount of command line arguments. Enter --help as the first command line argument for more information on this script.")
            break

        if len(sys.argv) > 11:
            messagebox.showerror("Error",
                                 "Command line arguments were incorrectly inputted. Make sure that arguments are correctly formatted and that there are no unwanted characters in the arguments.\n\n"
                                 "To run program, enter the command line arguments in this format: Name of Python Script --path <input folder path> --.ext <file extension> --type <(CSV) comma seperated OR (FWF) fixed width> (FOR CSV: --delimiter <'delimiter'>)")
            print(
                "\nError ... Command line arguments were incorrectly inputted. Make sure that arguments are correctly formatted and that there are no unwanted characters in the arguments")
            print(
                "To run program, enter the command line arguments in this format: Name of Python Script --path <input folder path> --.ext <file extension> --type <(CSV) comma seperated OR (FWF) fixed width> (FOR CSV: --delimiter <'delimiter'>)")
            break

        pathname = ""
        fileExtension = ""
        if len(sys.argv) == 11:
            if sys.argv[1] == "--path" and sys.argv[3] == "--.ext" and sys.argv[5] == "--type" and sys.argv[
                7] == "--delimiter" and sys.argv[9] == "--train":
                if os.path.isdir(sys.argv[2]):
                    print("--> ARGUMENTS ENTERED <--")
                    for arguments in sys.argv:
                        print("Argument: ", arguments)
                    print("\n")
                    pathname = sys.argv[2]
                    fileExtension = sys.argv[4]
                    delimiter = sys.argv[8]
                else:
                    messagebox.showerror("Error", "Input folder directory does not exist")
                    print("ERROR .... Input folder directory does not exist")
                    break
            else:
                messagebox.showerror("Error", "Command line arguments were entered incorrectly")
                print("ERROR .... Command line arguments were entered incorrectly")
                break

        print("Pathname: ", pathname)
        print("File Extension: ", fileExtension)

        fileInfoList = []  # container of class objects for each file

        for (root, subdirs, filename) in os.walk(
                pathname):  # get the pathname of the input folder, any subdirectories in it and all files located in the folder
            print("\n--------------------------------------")
            print("ROOT        %s" % (pathname))
            print("SUBDIRS     %s" % (subdirs))
            print("FILENAME    %s" % (filename))

            for filename in filename:  # for each file in the list of files from the input folder
                # print("Filename:        '%s'" % (filename))
                fileInfo = FILE_INFO()
                fileInfo.fullFilename = "%s\%s" % (root, filename)  # get name of input folder path + filename
                fileInfo.folderName = "%s" % (root)  # get root of input folder name
                fileInfo.filename = "%s" % (filename)  # get filename

                fileInfoList.append(fileInfo)  # ALL THREE OF THESE ARE PUT INTO THE CLASS OBJECT

            print("\n")

        # ---------------------------------------------------------------
        splitLinesList = []
        splitLinesListCOPY = []
        columnList = []
        colCountList = []
        count = 0
        lenRowList = []
        lenColList = []

        FILE_INFO_LIST_PANDAS = []

        FWF_DF = pd.DataFrame()

        read_csv_DF = pd.DataFrame()
        read_fwf_DF = pd.DataFrame()

        # ----------------------------------------------------------------

        # FOR MACHINE LEARNING DEBUGGING

        CLASSnLinesLIST = []
        CLASSaverageLenRowLIST = []
        CLASSaverageNColLIST = []
        CLASSaverageLenColLIST = []
        CLASSstdDevColLIST = []
        CLASSvarNColLIST = []
        CLASSfixedLengthLIST = []
        CLASSsizeOfFileLIST = []
        CLASSrepeatingLineCountLIST = []

        # ----------------------------------------------------------------

        print("@@@@@@@@@@@@@@@@@@ STARTING MAIN PROCESS @@@@@@@@@@@@@@@@@@")
        print(
            "\n--> PROGRAM IS IN PROGRESS ..... depending on size of input folder, the parser may take some time to finish. If program takes an unexpected amount of time, restart the program and run again.\n\n")

        for fInfo in fileInfoList:  # for the file object in fileInfoList
            if (len(fInfo.fullFilename) > 0):  # if the fullFilename for the object exists
                if (FWFFlag is True):
                    if (fInfo.fullFilename.endswith(
                            fileExtension) is True):  # if the file has an extension used for fixed width files.... This for loop is used for FW files
                        with open(fInfo.fullFilename, "r") as f:
                            lines = f.readlines()

                        characterCount = 0
                        for line in lines:  # get the number of rows in the file
                            fInfo.nlines += 1
                            for character in line:  # get length of each row
                                if character != ' ':
                                    characterCount += 1

                            lenRowList.append(characterCount)
                            characterCount = 0
                        lenRowListAVG = np.mean(lenRowList)

                        completed_lines_hash = set()
                        repeatCount = 0
                        for line in lines:  # find number of repeating lines
                            # print(line)
                            hashValue = hashlib.md5(line.rstrip().encode('utf-8')).hexdigest()
                            if hashValue not in completed_lines_hash:
                                completed_lines_hash.add(hashValue)
                            else:
                                repeatCount += 1

                        duplicateRowsDF = read_fwf_DF.duplicated()  # find number of duplicated lines in the dataframe
                        numDuplicateRows = 0
                        for row in duplicateRowsDF:
                            if row == True:
                                numDuplicateRows += 1

                        fInfo.averageLenRow = np.mean(
                            lenRowList)  # calculate average length of all the rows in the file
                        fInfo.fixedLength = 1  # set the fixedLength flag to True since this for loop will only execute on FW files
                        fInfo.averageLenCol = 1  # calculate average length of columns in dataframe.... averageLenCol = avg length of the length of the rows / number of columns in dataframe
                        fInfo.averageNCol = 1  # calculate number of columns
                        fInfo.repeatingLineCount = numDuplicateRows

                        fInfo.stdDevCol = 1
                        fInfo.varNCol = 1

                        sizeOfFile = os.path.getsize(fInfo.fullFilename)  # get size of file
                        fInfo.sizeOfFile = sizeOfFile

                        CLASSnLinesLIST.append(fInfo.nlines)
                        CLASSaverageLenRowLIST.append(fInfo.averageLenRow)
                        CLASSaverageNColLIST.append(fInfo.averageNCol)
                        CLASSaverageLenColLIST.append(fInfo.averageLenCol)
                        CLASSstdDevColLIST.append(fInfo.stdDevCol)
                        CLASSvarNColLIST.append(fInfo.varNCol)
                        CLASSfixedLengthLIST.append(fInfo.fixedLength)
                        CLASSsizeOfFileLIST.append(fInfo.sizeOfFile)
                        CLASSrepeatingLineCountLIST.append(fInfo.repeatingLineCount)

                        fInfo.date = "7/24/2019"

                        if isTrain is True:
                            fInfo.type = "train"
                        if isTrain is False:
                            fInfo.type = "test"

                        fInfo.Print()

                        # append FILE_INFO objects into list
                        FILE_INFO_LIST = [fInfo.filename, fInfo.date, fInfo.type, fInfo.nlines, fInfo.averageLenRow,
                                          fInfo.averageNCol, fInfo.averageLenCol, fInfo.stdDevCol, fInfo.varNCol,
                                          fInfo.fixedLength, fInfo.sizeOfFile, fInfo.repeatingLineCount]

                        FILE_INFO_LIST_PANDAS.append(
                            FILE_INFO_LIST)  # append list into another list (FILE_INFO_LIST_PANDAS) that will be used later in the program to generate the dataframe

                        print("\n!!!! Closing file '%s' from input folder '%s' !!!!!" % (
                        fInfo.filename, fInfo.folderName))

                # =============================================================================================================================================================================================

                if (fInfo.fullFilename.endswith(
                        fileExtension) is True):  # if the file is equal to the extension inputted in the command line
                    if (CSVFlag is True):
                        with open(fInfo.fullFilename, "r") as f:  # open file as f
                            lines = f.readlines()

                        splitLineCount = 0
                        splitLineColCharCount = 0
                        splitLineColCharCountList = []
                        for line in lines:  # split lines based on delimiter (From CL arguments)
                            splitLines = line.rstrip("\n").split(delimiter)
                            splitLinesList.append(splitLines)
                            splitLineCount += 1
                            for splitLine in splitLinesList:
                                for part in splitLine:
                                    for character in part:
                                        splitLineColCharCount += 1
                                    splitLineColCharCountList.append(splitLineColCharCount)
                                    splitLineColCharCount = 0

                        completed_lines_hash = set()
                        # repeatingDict = {}
                        repeatCount = 0
                        for line in lines:
                            # print(line)
                            hashValue = hashlib.md5(line.rstrip().encode('utf-8')).hexdigest()
                            if hashValue not in completed_lines_hash:
                                completed_lines_hash.add(hashValue)

                            else:
                                repeatCount += 1

                        colCount = 0
                        for line in splitLinesList:  # get number of columns
                            fInfo.nlines += 1
                            for piece in line:
                                colCount += 1
                            colCountList.append(colCount)
                            colCount = 0

                        characterCount = 0
                        for line in lines:  # get the length of each row in the file
                            for character in line:
                                characterCount += 1
                            lenRowList.append(characterCount)
                            characterCount = 0

                        sizeOfFile = os.path.getsize(fInfo.fullFilename)  # get size of file
                        fInfo.sizeOfFile = sizeOfFile

                        fInfo.repeatingLineCount = repeatCount  # store number of repeating lines

                        fInfo.averageLenRow = np.mean(
                            lenRowList)  # calculate average length of all the rows in the file
                        # fInfo.averageLenCol = lenRowList
                        fInfo.fixedLength = 0  # set the fixedLength flag to True since this for loop will only execute on FW files

                        # making calculations on the file info

                        fInfo.averageNCol = np.mean(colCountList)  # get average of columns
                        fInfo.averageLenCol = np.mean(splitLineColCharCountList)
                        # fInfo.modeNCol = stats.mode(colCountList)
                        # fInfo.stdDevCol = statistics.stdev(colCountList)  # standard deviation of number of columns
                        # fInfo.varNCol = np.var(colCountList)              # variance of number of columns

                        CLASSnLinesLIST.append(fInfo.nlines)
                        CLASSaverageLenRowLIST.append(fInfo.averageLenRow)
                        CLASSaverageNColLIST.append(fInfo.averageNCol)
                        CLASSaverageLenColLIST.append(fInfo.averageLenCol)
                        CLASSstdDevColLIST.append(fInfo.stdDevCol)
                        CLASSvarNColLIST.append(fInfo.varNCol)
                        CLASSfixedLengthLIST.append(fInfo.fixedLength)
                        CLASSsizeOfFileLIST.append(fInfo.sizeOfFile)
                        CLASSrepeatingLineCountLIST.append(fInfo.repeatingLineCount)

                        fInfo.date = "7/24/2019"

                        if isTrain is True:
                            fInfo.type = "train"
                        if isTrain is False:
                            fInfo.type = "test"

                        # fInfo.Print()

                        FILE_INFO_LIST = [fInfo.filename, fInfo.date, fInfo.type, fInfo.nlines, fInfo.averageLenRow,
                                          fInfo.averageNCol, fInfo.averageLenCol, fInfo.stdDevCol, fInfo.varNCol,
                                          fInfo.fixedLength, fInfo.sizeOfFile,
                                          fInfo.repeatingLineCount]  # append FILE_INFO objects into list
                        FILE_INFO_LIST_PANDAS.append(
                            FILE_INFO_LIST)  # append list into another list (FILE_INFO_LIST_PANDAS) that will be used later in the program to generate the dataframe

                        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

                        # clear used values for the next file in the input folder
                        splitLinesList.clear()
                        colCountList.clear()

                        print("Finished Parsing file: ", fInfo.filename)
                        # print("\n!!!! Closing file '%s' from input folder '%s' !!!!!" % (fInfo.filename, fInfo.folderName))
                        f.close()  # close the file that was just read so that information will not be accidently overwritten into it

                        # print("\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n")

        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        #           @@@ CREATE DATAFRAME AND CONVERT IT TO EXCEL @@@

        # print("\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CREATING EXCEL FILE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n ")

        print(
            " WARNING WARNING .......... PROGRAM IS NOT OUT OF TEST STATE...... SMALL CHANGES MUST BE MADE IN THE CODE BEFORE PUSHING TO PRODUCTION ")

        if os.path.isdir(pathname) is True:
            pass
        else:
            messagebox.showerror("Error", "File location does not exist. Please select a valid location.")
            print("ERROR .... File location does not exist. Please select a valid location.")
            break

        outputFilename = "ParserOUTPUT.csv"
        print("outputFilename : ", outputFilename)

        if outputFilename[-4:] == ".csv":
            pass
        if outputFilename[-4:] != ".csv":
            messagebox.showerror("Error",
                                 "Inputted output filename does not end in '.csv'. Output filename MUST end in a '.csv' file extension")
            print(
                "ERROR .... inputted output filename does not end in '.csv'. Output filename MUST end in a '.csv' file extension.")
            break

        ExcelPath = pathname + "/" + "ParserOUTPUT.csv"  # stores folder path into variable called ExcelPath... easier to use than typing out entire path

        if os.path.exists(
                ExcelPath) is True and isTrain is True:  # detects if file stored in ExcelPath exists. If it does, it deletes the one that exists and creates a new one
            try:
                os.remove(ExcelPath)
                print("--> %s was deleted from folder %s" % (ExcelPath, pathname))
                f = open(ExcelPath, 'w+')
                print("--> A new %s was created in folder %s" % (ExcelPath, pathname))
            except PermissionError:
                messagebox.showerror("Error",
                                     "Could not delete file: '%s'. File might be open or in use by another program")
                print("Error .... Could not delete file: '%s'. File might be open or in use by another program")

        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        #           @@@ DETERMINE IF --train IS YES or NO AND EXECUTE APPROPRIATE ACTIONS @@@
        #           @@@ if --train YES and the .csv file exists ---> parse files as train types and create a dummy file at the end
        #           @@@ if --train NO and the .csv file exists ---> parse files

        if isTrain == True:  # --train YES

            listOfCLASSvars = [CLASSnLinesLIST, CLASSaverageLenRowLIST, CLASSaverageNColLIST, CLASSaverageLenColLIST,
                               CLASSstdDevColLIST, CLASSvarNColLIST, CLASSfixedLengthLIST, CLASSsizeOfFileLIST,
                               CLASSrepeatingLineCountLIST]

            # creating the dummy file
            fInfo.filename = 'dummy.dummy'
            fInfo.date = '7/24/2019'
            fInfo.type = 'train'

            dummyFile = [fInfo.filename, fInfo.date, fInfo.type, fInfo.nlines, fInfo.averageLenRow, fInfo.averageNCol,
                         fInfo.averageLenCol, fInfo.stdDevCol, fInfo.varNCol, fInfo.fixedLength, fInfo.sizeOfFile,
                         fInfo.repeatingLineCount]

            dummyFileCount = 3
            # for list in listOfCLASSvars:
            #     if min(list) == max(list):
            #         newElement = list[-1] + .00001
            #         dummyFile[dummyFileCount] = newElement
            #         newElement = 0
            #
            #     if min(list) != max(list):
            #         newElement = list[-1]
            #         dummyFile[dummyFileCount] = newElement
            #         newElement = 0
            #     dummyFileCount += 1
            #
            # dummyFile_DF = pd.DataFrame(dummyFile)
            # FILE_INFO_LIST_PANDAS.append(dummyFile)

            fileInfoListDF = pd.DataFrame(FILE_INFO_LIST_PANDAS,
                                          columns=CSVFileHeaders)  # creates dataframe fileInfoListDF... columns are based on CSVFileHeaders list located at beginning of program
            # print(fileInfoListDF)

            try:
                fileInfoListDF.to_csv(ExcelPath,
                                      index=False)  # converts dataframe to CSV file ... index=False --> does not put dataframe index into csv file
            except PermissionError:
                messagebox.showerror("Error",
                                     "Permission to write to that location was denied.\nCheck to see if you have permission to write to that location.\nMake sure that an Excel spreadsheet with that filename is not already opened.")
                print(
                    "\nERROR .... Permission to write to that location was denied. \nCheck to see if you have permission to write to that location.\nMake sure that an Excel spreadsheet with that filename is not already opened.")
                break

            messagebox.showinfo("Program has finished",
                                "TRAIN files have been parsed and scored.\n\nScores for each file have been saved to a .csv file titled 'ParserOUTPUT.csv' in folder path: " + pathname)
            print("\n\nProgram has finished...")
            print("Files have been parsed and scored")
            print(
                "Scores for each file have been saved to a .csv file titled 'ParserOUTPUT.csv' in folder path " + pathname)

            print("\n\tBasic info regarding the dataframe\n")
            print(fileInfoListDF.info())
            break

        # ----------------------------------------------------------------------------------

        if isTrain == False:  # --train NO

            fileInfoListDF = pd.DataFrame(FILE_INFO_LIST_PANDAS,
                                          columns=CSVFileHeaders)  # creates dataframe fileInfoListDF... columns are based on CSVFileHeaders list located at beginning of program
            try:
                fileInfoListDF.to_csv(ExcelPath, index=False, mode='a',
                                      header=False)  # converts dataframe to CSV file ... index=False --> does not put dataframe index into csv file
            except PermissionError:
                messagebox.showerror("Error",
                                     "Permission to write to that location was denied.\n\nCheck to see if you have permission to write to that location.\nMake sure that an Excel spreadsheet with that filename is not already opened.")
                print(
                    "\nERROR .... Permission to write to that location was denied. \n\tCheck to see if you have permission to write to that location.\n\tMake sure that an Excel spreadsheet with that filename is not already opened.")
                break

            messagebox.showinfo("Program has finished",
                                "TEST files have been parsed and scored.\n\nScores for each file have been saved to a .csv file titled 'ParserOUTPUT.csv' in folder path: " + pathname)
            print("\n\nProgram has finished...")
            print("Files have been parsed and scored")
            print(
                "Scores for each file have been saved to a .csv file titled 'ParserOUTPUT.csv' in folder path " + pathname)

            print("\n\tBasic info regarding the dataframe.\n")
            print(fileInfoListDF.info())
            break


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

if __name__ == "__main__":
    Parser()
