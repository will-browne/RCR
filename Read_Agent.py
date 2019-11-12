import os

from Read_UCS_Population import Read_UCS_Population
from Read_XCS_Population import Read_XCS_Population
from CRA import CRA
from Fu1 import Fu1
from Fu3 import Fu3
from CRA2 import CRA2
from K1 import K1
from QRC import QRC
from PDRC import PDRC
from RCR import RCR
from RCR2 import RCR2
from RCR3 import RCR3


class Read_Single_Population:
    #0 UCS, 1XCS
    def __init__(self,type,address):
        if type==0:
            Read=Read_UCS_Population(address)
            #Read.Print_Population()
            #read a population
            self.population=Read.population
        elif type==1:
            Read=Read_XCS_Population(address)
            self.population=Read.population
            #Read.Print_Population()

class Read_Multiple_Populations:
    #0 UCS 1XCS
    def __init__(self,type,address):
        self.type=type
        self.read_list=[]
        self.population=[]
        self.FileList=[]
        self.Read(address)

    def Is_File_Exist(self,file_Name):
        return os.path.exists(file_Name)


    def GetFileList(self,path,type):
        FileList=[]
        FindPath=path
        if self.Is_File_Exist(FindPath):
            FileNames=os.listdir(FindPath)
            for i in FileNames:
                if type in i:
                    self.FileList.append(path+'\\'+i)
        return self.FileList

    def Read(self,address):
        read_list=self.GetFileList(address,'.txt')
        for add in read_list:
            Single_population=Read_Single_Population(self.type,add)
            self.population.append(Single_population.population)

class Read_List_Address:
    def __init__(self,Address_Agent,Address_Dataset):
        #style could be either Train or Test 
     
        print("Begin")
        self.Test_Id=self.Get_Id(Address_Agent)
        print(self.Test_Id)
        self.Train_Address=self.Get_Train_address(self.Test_Id,Address_Dataset)
        self.Test_Address=self.Get_Test_address(self.Test_Id,Address_Dataset)

    def Is_File_Exist(self,file_Name):
        return os.path.exists(file_Name)

    def GetFileList(self,path,type):
        FileList=[]
        FindPath=path
        if self.Is_File_Exist(FindPath):
            FileNames=os.listdir(FindPath)
            for i in FileNames:
                if type in i:
                    FileList.append(path+'\\'+i)
        return FileList

    def Get_Id(self,address):
        infor=address.split('_')[-1].split('.')[0]
        return infor

    def Get_Test_address(self,Id,Address):
        Test_address=self.GetFileList(Address,"Test")
        for add in Test_address:
            T_Id=self.Get_Id(add)
            if T_Id == Id:
                return add

    def Get_Train_address(self,Id,Address):
        Test_address=self.GetFileList(Address,"Train")
        for add in Test_address:
            T_Id=self.Get_Id(add)
            if T_Id == Id:
                return add


#Address="Population\\UCS\\Majority_on\\Majority_6_2018_11_13_21_13_16.txt"
#Address="Population\\UCS\\Majority_on"

#Address="Population\\XCS\\MUX6\\XCS_45598a9f_15e3_4393_b4e4_da00bc199dfdAgent_7c2c1321_3909_42ad_bcd0_ddf52463c8b2Problem_multiplexerPlength_6FTime_DAY__2019_04_12__Time__18___11___16.txt"
#Address="Population\\XCS\\MUX6"
#Address="Population\\UCS\\MUX37"

#Address="Population\\UCS\\MUX37SUB"
#Address="Population\\UCS\\MUX_70SUB"
#Address="Population\\XCS\\Carry_8"
#RSP=Read_Single_Population(0,Address)
#CRA_t=CRA(RSP.population,3,6,0)
#Fu1_t=Fu1(RSP.population,3,6,0)
#RSP=Read_Single_Population(0,Address)
#Fu3_t=Fu3(RSP.population,3,6,0)
#CRA_t=CRA2(RSP.population,3,6,0)
#CRA_t=K1(RSP.population,3,6,0)
#CRA_t=QRC(RSP.population,3,6,0)
#RSP=Read_Single_Population(0,Address)

#MP=Read_Multiple_Populations(0,Address)
#CRA_t=PDRC(MP.population[0],3,6,0)
#RCRT=RCR(MP.population,0,0,70)


#RCRT=RCR2(MP.population,0,0,37)
#MP=Read_Multiple_Populations(1,Address)
#populations,system_ID,problem_ID,Problem_Length
#RCRT=RCR3(MP.population,0,3,6)
