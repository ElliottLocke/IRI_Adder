'''
Created on Aug 21, 2013

@author: Elliott Locke
'''

import os, sys
from tkFileDialog import askopenfilename
from Tkinter import Tk
import tkMessageBox


def main():
    #this is the main part of the script.  You can tell it is the main because it is called main.  
    Tk().withdraw() #Not a full GUI
    titlePrep = "Choose your .iri file! the .csv"
    messagePrep = "This will add this IRI file to a new RSP file.  The one ending in .CSV!!!"
    iriPath = askopenfilename(title = titlePrep, message = messagePrep)#show an open dialog box - This is for the IRI file.
    
    titlePrep2 = "Choose your RSP file that is associated with the chosen IRI file.  It should end in .RSP"
    messagePrep2 = "This will create a new rsp file with the info from the IRI file."
    rspPath = askopenfilename(title = titlePrep2, message = messagePrep2)#show an open dialog box - This is for the RSP file.  The RSP and IRI do not have exactly the same name, otherwise I would have made this a batch process.  
    
    #Make a new rep_new file.  rspbasename[1] should be changed to 'iri' but I did not know that until I completed everything.  
    rspbasename = os.path.basename(rspPath).rsplit('.',1)
    newRSPpath = os.path.join(os.path.dirname(rspPath), ".".join([rspbasename[0]+"_new", rspbasename[1]]))

    #open the iri and rsp as 'r' read only.  open the new one as 'w' write.
    iriFile = open(iriPath, 'r')
    rspFile = open(rspPath, 'r')
    newRSPFile = open(newRSPpath, 'w')
    
    # Put the iri file into a list.  Probably not the most efficient way to do this, but I okay wit dat.  
    iriList = list()
    for thisline in iriFile:
        thislinesplit = thisline.split(',')
        if thislinesplit[1] != thislinesplit[2]:  #Column one and two in the iri file are the distances from the start and stop of the iri summary.  For some reason, some of them had 0 distance - 1 and 2 were the same numbers instead of being 1/1000th different.   
            iriList.append(thislinesplit)
    iriFile.close()
    
    #Write each line from the old rsp file to the newrspfile.      
    n = 0
    for line in rspFile:
        lineparts = line.split(',')
        if lineparts[0] == '5406': #lineparts[0] is the first item in the line.  
            try:
                newRSPFile.write(', '.join(iriList[n]) + '\r')  #Write the iri list to the new rsp file.  Join the list together and separated by commas.  I added the space for prettyness.  
            except IndexError:
                pass #Go on if there is an error.  This will make is so the new rsp file skips over the rest of the 5406 lines.  
            n = n + 1
        else:
            newRSPFile.write(line)

    rspFile.close()
    newRSPFile.close()
    
    #Tell the user that the script is complete.
    window = Tk()
    window.wm_withdraw()
    tkMessageBox.showinfo(title="The End", message = "The new RSP file is complete.")
if __name__ == '__main__':
    main()
    sys.exit()