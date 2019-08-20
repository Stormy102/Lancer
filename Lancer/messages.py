from helpers import *
from datetime import datetime
from spinner import *
import time, sys, itertools, platform

VERSION = "v0.0.1a1"

def PrintHeader():
	print('''                  `.--:::::::::::::::::---.                 
               `-::----.............-----::/:.              
              ./:----.............---------::/:             
           ``.......--------------------......-..``         
          ....://+//::------/:o:+.------:::///::-..-        
          -../+++/:--...``../:o:+...```..--://+//:..`       
         .-.-//+/:-.........:-/-:..........-://///-..       
         :..:/++/:-....................------:///:-..       
         /../+++/-.--------------------------:////-.-       
         +../+++/:::/osyhddmNNMMMNNNmddhyso+/:////:.-       
         /../://shmNNNNNNNNNNNMMNNNNNNNNNNNNNNy:/::.-       
        /...://:NNNNNNNNNNNNNdhhmNNNNNNMNNNNNNN//-:...      
      `-+-..::/:NNNNNNNNNNh+-----:smNNNNNNNNNNm:/-:..-      
      -+s-..::+/hNNNNNNNNo-:+yyoy+-:hNNNNNNNNN+::::..:.     
     .:dm:..-////NNNNNNd:-.:-....-:-:sNNNNNNNs-/:::..y:`    
     -+NMo..-//+:/dNNNh------...------oNNNNm+-/:/:-.:m/.    
     -+NMh-../++/:-/so-----.-+o+/.-----+dds--::+/:-.sN+.    
     ./hMN:../++/:--------.ydsosyd/-----:----:++/:..md+.    
     `-/oo:..:+++:-------.+d/++++sN---------:+++/-./h+:     
       ..-::.-+o+/-------.oh////+oN:-------:/++++../:.`     
          `/:-////-------.oh///++oN:-:::::::/++++--`        
           .:------------.oh+++++oN--::::---:::::           
            /------------.ohooooosM--::::-------.           
            ::-----------.ohooooosN-::::-------:`           
            `------------.oh+oo+oyN-::::------::            
                `..-------ohoyyyssM-::::----..`             
                    `.----oddmmmdhM-:::-.`                  
                       `.-odydmmhyM-:.                      
                          `..-----.`''')

def Version():
    print (Color("[+]", "Green"), "Starting Lancer", VERSION, "at", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "on", platform.system(), platform.release(), end = ' ')
    with Spinner():
        time.sleep(1)
    print("")

def LineBreak(count):
    '''
        Prints the specified number of line breaks

        count - the number of line breaks to print
    '''

    for i in range(0, count):
        print ("")

def SplashScreen():
    PrintHeader()
    Version()
