import os
import numpy as np
import time
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
from Read_Agent import Read_Multiple_Populations
from Read_Agent import Read_Single_Population
from TimeCalculater import Time_Calculate
from Read_Agent import Read_List_Address


class Compaction:

    def __init__(self, Address, SystemId, ProblemId, Problem_Length,test_list,Data_Address_R,Is_tenfolder):
        print("begin")
        self.IsLinux=False
        self.Is_tenfolder=Is_tenfolder
        
        self.Real_Data_Address=Data_Address_R

        self.problems_involved=['MUX','Carry','Parity','Majority','ZOO','Audiology','Balance','Breast_Cancer','Congressional_Voting','balloon1'
                             ,'balloon2','balloon3','balloon4','soybean_small','tumor','Splice_junction_Gene_Sequences','Promoter_Gene_Sequences','monk1','monk2',
                             'monk3']

        
        self.TC=Time_Calculate()
        Result_performance=""
        for Id in test_list:
            if Id==0:
                MP=Read_Multiple_Populations(SystemId,Address)

                Accuracy_list=[]
                Size_List=[]
                Time_List=[]

                un_cover_count_list=[]
                correct_list=[]
                error_list=[]

                ten_folder_list=[]
                #self.un_cover_count,self.correct,self.error
                for population in MP.population:

                    format_time_2,Hour_2,Min_2,second_2,day_2=self.TC.startTimer()
                    if self.Is_tenfolder:
                        RLD=Read_List_Address(MP.FileList[0],self.Real_Data_Address)
                    else:
                        RLD=None

                    CRA_t=CRA(population,ProblemId,Problem_Length,SystemId,RLD)
                    Type="CRA"
                    Accuracy=CRA_t.final_acc
                    Accuracy_list.append(Accuracy)
                    Size=CRA_t.final_size
                    Size_List.append(Size)
                    format_time_1,Hour_1,Min_1,second_1,day_1=self.TC.startTimer()
                    r_time=self.TC.elapsed(Hour_1,Hour_2,Min_1,Min_2,second_1,second_2,day_1,day_2)
                    Time_List.append(r_time)
                    #print("time",r_time)
                    rule_result=self.Population_String(CRA_t.final_set)
                    NAME=self.Generate_Store_Name(Type,self.problems_involved[ ProblemId]+str(Problem_Length))
                    self.save_performance(rule_result,NAME)

                    un_cover_count_list.append(CRA_t.un_cover_count)
                    correct_list.append(CRA_t.correct)
                    error_list.append(CRA_t.error)

                    ten_folder_list.append(CRA_t.final_test_accuracy)

                Result_performance+=self.Performance_String(Accuracy_list,Size_List,Time_List,Type,un_cover_count_list,correct_list,error_list,ten_folder_list)
                

            if Id==1:
                MP=Read_Multiple_Populations(SystemId,Address)

                Accuracy_list=[]
                Size_List=[]
                Time_List=[]

                un_cover_count_list=[]
                correct_list=[]
                error_list=[]

                ten_folder_list=[]

                for population in MP.population:

                    format_time_2,Hour_2,Min_2,second_2,day_2=self.TC.startTimer()

                    if self.Is_tenfolder:
                        RLD=Read_List_Address(MP.FileList[0],self.Real_Data_Address)
                    else:
                        RLD=None

                    Fu1_t=Fu1(population,ProblemId,Problem_Length,SystemId,RLD)
                    Type="FU1"
                    Accuracy=Fu1_t.final_acc
                    Accuracy_list.append(Accuracy)
                    Size=Fu1_t.final_size
                    Size_List.append(Size)
                    format_time_1,Hour_1,Min_1,second_1,day_1=self.TC.startTimer()
                    r_time=self.TC.elapsed(Hour_1,Hour_2,Min_1,Min_2,second_1,second_2,day_1,day_2)
                    Time_List.append(r_time)
                    #print("time",r_time)
                    rule_result=self.Population_String(Fu1_t.final_set)
                    NAME=self.Generate_Store_Name(Type,self.problems_involved[ ProblemId]+str(Problem_Length))
                    self.save_performance(rule_result,NAME)

                    un_cover_count_list.append(Fu1_t.un_cover_count)
                    correct_list.append(Fu1_t.correct)
                    error_list.append(Fu1_t.error)

                    ten_folder_list.append(Fu1_t.final_test_accuracy)

                Result_performance+=self.Performance_String(Accuracy_list,Size_List,Time_List,Type,un_cover_count_list,correct_list,error_list,ten_folder_list)
                #print(Result_performance)
            if Id==2:
                MP=Read_Multiple_Populations(SystemId,Address)

                Accuracy_list=[]
                Size_List=[]
                Time_List=[]

                un_cover_count_list=[]
                correct_list=[]
                error_list=[]

                ten_folder_list=[]

                for population in MP.population:

                    format_time_2,Hour_2,Min_2,second_2,day_2=self.TC.startTimer()

                    if self.Is_tenfolder:
                        RLD=Read_List_Address(MP.FileList[0],self.Real_Data_Address)
                    else:
                        RLD=None

                    Fu3_t=Fu3(population,ProblemId,Problem_Length,SystemId,RLD)
                    Type="FU3"
                    Accuracy=Fu3_t.final_acc
                    Accuracy_list.append(Accuracy)
                    Size=Fu3_t.final_size
                    Size_List.append(Size)
                    format_time_1,Hour_1,Min_1,second_1,day_1=self.TC.startTimer()
                    r_time=self.TC.elapsed(Hour_1,Hour_2,Min_1,Min_2,second_1,second_2,day_1,day_2)
                    #print("time",r_time)
                    Time_List.append(r_time)
                    rule_result=self.Population_String(Fu3_t.final_set)
                    NAME=self.Generate_Store_Name(Type,self.problems_involved[ ProblemId]+str(Problem_Length))
                    self.save_performance(rule_result,NAME)

                    un_cover_count_list.append(Fu3_t.un_cover_count)
                    correct_list.append(Fu3_t.correct)
                    error_list.append(Fu3_t.error)

                    #ten_folder_list.append(Fu3_t.final_test_accuracy)

                Result_performance+=self.Performance_String(Accuracy_list,Size_List,Time_List,Type,un_cover_count_list,correct_list,error_list,ten_folder_list)
                #print(Result_performance)
            if Id==3:
                MP=Read_Multiple_Populations(SystemId,Address)

                Accuracy_list=[]
                Size_List=[]
                Time_List=[]

                un_cover_count_list=[]
                correct_list=[]
                error_list=[]

                ten_folder_list=[]

                for population in MP.population:

                    format_time_2,Hour_2,Min_2,second_2,day_2=self.TC.startTimer()

                    if self.Is_tenfolder:
                        RLD=Read_List_Address(MP.FileList[0],self.Real_Data_Address)
                    else:
                        RLD=None

                    CRA_t=CRA2(population,ProblemId,Problem_Length,SystemId,RLD)
                    Type="CRA2"
                    Accuracy=CRA_t.final_acc
                    Accuracy_list.append(Accuracy)
                    Size=CRA_t.final_size
                    Size_List.append(Size)
                    format_time_1,Hour_1,Min_1,second_1,day_1=self.TC.startTimer()
                    r_time=self.TC.elapsed(Hour_1,Hour_2,Min_1,Min_2,second_1,second_2,day_1,day_2)
                    #print("time",r_time)
                    Time_List.append(r_time)
                    rule_result=self.Population_String(CRA_t.final_set)
                    NAME=self.Generate_Store_Name(Type,self.problems_involved[ ProblemId]+str(Problem_Length))
                    self.save_performance(rule_result,NAME)

                    un_cover_count_list.append(CRA_t.un_cover_count)
                    correct_list.append(CRA_t.correct)
                    error_list.append(CRA_t.error)

                    #ten_folder_list.append(CRA_t.final_test_accuracy)

                Result_performance+=self.Performance_String(Accuracy_list,Size_List,Time_List,Type,un_cover_count_list,correct_list,error_list,ten_folder_list)
                #print(Result_performance)
            if Id==4:
                MP=Read_Multiple_Populations(SystemId,Address)

                Accuracy_list=[]
                Size_List=[]
                Time_List=[]

                un_cover_count_list=[]
                correct_list=[]
                error_list=[]

                ten_folder_list=[]


                for population in MP.population:

                    format_time_2,Hour_2,Min_2,second_2,day_2=self.TC.startTimer()

                    if self.Is_tenfolder:
                        RLD=Read_List_Address(MP.FileList[0],self.Real_Data_Address)
                    else:
                        RLD=None

                    CRA_t=K1(population,ProblemId,Problem_Length,SystemId,RLD)
                    Type="k1"
                    Accuracy=CRA_t.final_acc
                    Accuracy_list.append(Accuracy)
                    Size=CRA_t.final_size
                    Size_List.append(Size)
                    format_time_1,Hour_1,Min_1,second_1,day_1=self.TC.startTimer()
                    r_time=self.TC.elapsed(Hour_1,Hour_2,Min_1,Min_2,second_1,second_2,day_1,day_2)
                    #print("time",r_time)
                    Time_List.append(r_time)
                    rule_result=self.Population_String(CRA_t.final_set)
                    NAME=self.Generate_Store_Name(Type,self.problems_involved[ ProblemId]+str(Problem_Length))
                    self.save_performance(rule_result,NAME)

                    un_cover_count_list.append(CRA_t.un_cover_count)
                    correct_list.append(CRA_t.correct)
                    error_list.append(CRA_t.error)

                    #ten_folder_list.append(CRA_t.final_test_accuracy)

                Result_performance+=self.Performance_String(Accuracy_list,Size_List,Time_List,Type,un_cover_count_list,correct_list,error_list,ten_folder_list)
                #print(Result_performance)
            if Id==5:
                MP=Read_Multiple_Populations(SystemId,Address)

                Accuracy_list=[]
                Size_List=[]
                Time_List=[]

                un_cover_count_list=[]
                correct_list=[]
                error_list=[]

                ten_folder_list=[]

                for population in MP.population:

                    format_time_2,Hour_2,Min_2,second_2,day_2=self.TC.startTimer()

                    if self.Is_tenfolder:
                        RLD=Read_List_Address(MP.FileList[0],self.Real_Data_Address)
                    else:
                        RLD=None

                    CRA_t=QRC(population,ProblemId,Problem_Length,SystemId,RLD)
                    Type="QRC"
                    Accuracy=CRA_t.final_acc
                    Accuracy_list.append(Accuracy)
                    Size=CRA_t.final_size
                    Size_List.append(Size)
                    format_time_1,Hour_1,Min_1,second_1,day_1=self.TC.startTimer()
                    r_time=self.TC.elapsed(Hour_1,Hour_2,Min_1,Min_2,second_1,second_2,day_1,day_2)
                    #print("time",r_time)
                    Time_List.append(r_time)
                    rule_result=self.Population_String(CRA_t.final_set)
                    NAME=self.Generate_Store_Name(Type,self.problems_involved[ ProblemId]+str(Problem_Length))
                    self.save_performance(rule_result,NAME)

                    un_cover_count_list.append(CRA_t.un_cover_count)
                    correct_list.append(CRA_t.correct)
                    error_list.append(CRA_t.error)

                    #ten_folder_list.append(CRA_t.final_test_accuracy)

                Result_performance+=self.Performance_String(Accuracy_list,Size_List,Time_List,Type,un_cover_count_list,correct_list,error_list,ten_folder_list)
                #print(Result_performance)
            if Id==6:
                MP=Read_Multiple_Populations(SystemId,Address)

                Accuracy_list=[]
                Size_List=[]
                Time_List=[]

                un_cover_count_list=[]
                correct_list=[]
                error_list=[]

                ten_folder_list=[]

                for population in MP.population:

                    format_time_2,Hour_2,Min_2,second_2,day_2=self.TC.startTimer()

                    if self.Is_tenfolder:
                        RLD=Read_List_Address(MP.FileList[0],self.Real_Data_Address)
                    else:
                        RLD=None

                    CRA_t=PDRC(population,ProblemId,Problem_Length,SystemId,RLD)
                    Type="PDRC"
                    Accuracy=CRA_t.final_acc
                    Accuracy_list.append(Accuracy)
                    Size=CRA_t.final_size
                    Size_List.append(Size)
                    format_time_1,Hour_1,Min_1,second_1,day_1=self.TC.startTimer()
                    r_time=self.TC.elapsed(Hour_1,Hour_2,Min_1,Min_2,second_1,second_2,day_1,day_2)
                    #print("time",r_time)
                    Time_List.append(r_time)
                    rule_result=self.Population_String(CRA_t.final_set)
                    NAME=self.Generate_Store_Name(Type,self.problems_involved[ ProblemId]+str(Problem_Length))
                    self.save_performance(rule_result,NAME)

                    un_cover_count_list.append(CRA_t.un_cover_count)
                    correct_list.append(CRA_t.correct)
                    error_list.append(CRA_t.error)

                    #ten_folder_list.append(CRA_t.final_test_accuracy)

                Result_performance+=self.Performance_String(Accuracy_list,Size_List,Time_List,Type,un_cover_count_list,correct_list,error_list,ten_folder_list)
                #print(Result_performance)
            if Id==7:
                    MP=Read_Multiple_Populations(SystemId,Address)

                    Accuracy_list=[]
                    Size_List=[]
                    Time_List=[]

                    un_cover_count_list=[]
                    correct_list=[]
                    error_list=[]

                    ten_folder_list=[]

                    format_time_2,Hour_2,Min_2,second_2,day_2=self.TC.startTimer()

                    if self.Is_tenfolder:
                        RLD=Read_List_Address(MP.FileList[0],self.Real_Data_Address)
                    else:
                        RLD=None

                    RCRT=RCR(MP.population,SystemId,ProblemId,Problem_Length,RLD)
                    Type="RCR"
                    Accuracy=RCRT.final_acc
                    Accuracy_list.append(Accuracy)
                    Size=RCRT.final_size
                    Size_List.append(Size)
                    format_time_1,Hour_1,Min_1,second_1,day_1=self.TC.startTimer()
                    r_time=self.TC.elapsed(Hour_1,Hour_2,Min_1,Min_2,second_1,second_2,day_1,day_2)
                    #print("time",r_time)
                    Time_List.append(r_time)
                    rule_result=self.Population_String(RCRT.result)
                    NAME=self.Generate_Store_Name(Type,self.problems_involved[ ProblemId]+str(Problem_Length))
                    self.save_performance(rule_result,NAME)

                    un_cover_count_list.append(RCRT.un_cover_count)
                    correct_list.append(RCRT.correct)
                    error_list.append(RCRT.error)

                    #ten_folder_list.append(RCRT.final_test_accuracy)

                    Result_performance+=self.Performance_String(Accuracy_list,Size_List,Time_List,Type,un_cover_count_list,correct_list,error_list,ten_folder_list)
                    print(Result_performance)
            if Id==8:
                    MP=Read_Multiple_Populations(SystemId,Address)

                    Accuracy_list=[]
                    Size_List=[]
                    Time_List=[]

                    un_cover_count_list=[]
                    correct_list=[]
                    error_list=[]

                    ten_folder_list=[]

                    format_time_2,Hour_2,Min_2,second_2,day_2=self.TC.startTimer()

                    if self.Is_tenfolder:
                        RLD=Read_List_Address(MP.FileList[0],self.Real_Data_Address)
                    else:
                        RLD=None

                    RCRT=RCR2(MP.population,SystemId,ProblemId,Problem_Length,RLD)
                    Type="RCR2"
                    Accuracy=RCRT.final_acc
                    Accuracy_list.append(Accuracy)
                    Size=RCRT.final_size
                    Size_List.append(Size)
                    format_time_1,Hour_1,Min_1,second_1,day_1=self.TC.startTimer()
                    r_time=self.TC.elapsed(Hour_1,Hour_2,Min_1,Min_2,second_1,second_2,day_1,day_2)
                    #print("time",r_time)
                    Time_List.append(r_time)
                    rule_result=self.Population_String(RCRT.result)
                    NAME=self.Generate_Store_Name(Type,self.problems_involved[ ProblemId]+str(Problem_Length))
                    self.save_performance(rule_result,NAME)

                    un_cover_count_list.append(RCRT.un_cover_count)
                    correct_list.append(RCRT.correct)
                    error_list.append(RCRT.error)

                    #ten_folder_list.append(RCRT.final_test_accuracy)

                    Result_performance+=self.Performance_String(Accuracy_list,Size_List,Time_List,Type,un_cover_count_list,correct_list,error_list,ten_folder_list)
                    print(Result_performance)
            if Id==9:
                    MP=Read_Multiple_Populations(SystemId,Address)

                    Accuracy_list=[]
                    Size_List=[]
                    Time_List=[]

                    un_cover_count_list=[]
                    correct_list=[]
                    error_list=[]

                    ten_folder_list=[]

                    format_time_2,Hour_2,Min_2,second_2,day_2=self.TC.startTimer()

                    if self.Is_tenfolder:
                        RLD=Read_List_Address(MP.FileList[0],self.Real_Data_Address)
                    else:
                        RLD=None

                    RCRT=RCR3(MP.population,SystemId,ProblemId,Problem_Length,RLD)
                    Type="RCR3"
                    Accuracy=RCRT.final_acc
                    Accuracy_list.append(Accuracy)
                    Size=RCRT.final_size
                    Size_List.append(Size)
                    format_time_1,Hour_1,Min_1,second_1,day_1=self.TC.startTimer()
                    r_time=self.TC.elapsed(Hour_1,Hour_2,Min_1,Min_2,second_1,second_2,day_1,day_2)
                    #print("time",r_time)
                    Time_List.append(r_time)
                    rule_result=self.Population_String(RCRT.result)
                    NAME=self.Generate_Store_Name(Type,self.problems_involved[ ProblemId]+str(Problem_Length))
                    self.save_performance(rule_result,NAME)


                    un_cover_count_list.append(RCRT.un_cover_count)
                    correct_list.append(RCRT.correct)
                    error_list.append(RCRT.error)

                    #ten_folder_list.append(RCRT.final_test_accuracy)

                    Result_performance+=self.Performance_String(Accuracy_list,Size_List,Time_List,Type,un_cover_count_list,correct_list,error_list,ten_folder_list)
                    print(Result_performance)
        performance_name=self.Generate_Store_Name_Performance( self.problems_involved[ ProblemId])
        self.save_performance(Result_performance,performance_name)

    def save_performance(self,txt,name):
        f=open(name,'wb')
        f.write(txt.encode())
        f.close()

    def Generate_Store_Name(self,Compact_name,problem_name):
        F,H,M,S,Ye,Mo,Da=self.GetTimer()
        file_type='.txt'
        if self.IsLinux==False:
            name='Result/'+problem_name+Compact_name+str(Ye)+'_'+str(Mo)+'_'+str(Da)+'_'+str(H
            )+'_'+str(M)+'_'+str(S)+file_type
        else:
            name=os.getcwd()+'/RuleCompaction/Result/'+problem_name+Compact_name+str(Ye)+'_'+str(Mo)+'_'+str(Da)+'_'+str(H
            )+'_'+str(M)+'_'+str(S)+file_type
        return name

    def Generate_Store_Name_Performance(self,problem_name):
        F,H,M,S,Ye,Mo,Da=self.GetTimer()
        file_type='.txt'
        if self.IsLinux==False:
            name='Result/'+"Performance"+problem_name+str(Ye)+'_'+str(Mo)+'_'+str(Da)+'_'+str(H
            )+'_'+str(M)+'_'+str(S)+file_type
        else:
            name=os.getcwd()+'/RuleCompaction/Result/'+"Performance"+problem_name+str(Ye)+'_'+str(Mo)+'_'+str(Da)+'_'+str(H
            )+'_'+str(M)+'_'+str(S)+file_type
        return name

    def Population_String(self,population):
        result=""
        for rule in population:
            condition=""
            for cod in rule[0]:
                condition=condition+ str(cod)+" "
            result=result+condition+" : " + str(rule[1])+"\n"
        return result

    def Performance_String(self, accuracy, size, time, type, uncover, correct, error, ten_folder_list):
        result=type+": \n"
        acc_s=""
        for accu in accuracy:
            acc_s+=  str(round(accu,4))+" "
        result+="Train Accuracy: "+ acc_s +"MAX "+  str(round(max(accuracy),4))+" "+"MIN "+ str(round(min(accuracy),4)) + " MEAN "+str(round(np.mean(accuracy),4))+"\n"

        unc_s=""
        for unc in uncover:
            unc_s+=  str(round(unc,3))+" "
        result+="Uncovered: "+ unc_s +"MAX "+  str(round(max(uncover),4))+" "+"MIN "+ str(round(min(uncover),4)) + " MEAN "+str(round(np.mean(uncover),4))+"\n"



        correct_s=""
        for cor in correct:
            correct_s+=  str(round(cor,3))+" "
        result+="Correct: "+ correct_s +"MAX "+  str(round(max(correct),4))+" "+"MIN "+ str(round(min(correct),4)) + " MEAN "+str(round(np.mean(correct),4))+"\n"



        error_s=""
        for err in error:
            error_s+=  str(round(err,3))+" "
        result+="Error: "+ error_s +"MAX "+  str(round(max(error),4))+" "+"MIN "+ str(round(min(error),4)) + " MEAN "+str(round(np.mean(error),4))+"\n"



        size_s=""
        for si in size:
            size_s+=  str(round(si,3))+" "
        result+="Size: "+ size_s +"MAX "+  str(round(max(size),2))+" "+"MIN "+ str(round(min(size),2)) + " MEAN "+str(round(np.mean(size),2))+"\n"



        tize_s=""
        for ti in time:
            tize_s+=  str(round(ti,3))+" "
        result+="Time: "+ tize_s +"MAX "+  str(round(max(time),2))+" "+"MIN "+ str(round(min(time),2)) + " MEAN "+str(round(np.mean(time),2))+"\n"

        if self.Is_tenfolder:
            fold_s=""
            for folde in ten_folder_list:
                fold_s+=  str(round(folde,3))+" "
            result+="Test Accuracy: "+ fold_s +"MAX "+  str(round(max(ten_folder_list),2))+" "+"MIN "+ str(round(min(ten_folder_list),2)) + " MEAN "+str(round(np.mean(ten_folder_list),2))+"\n"

        return result

    def GetTimer(self):
        local_time= time.localtime(time.time())
        format_time=time.strftime('DAY: %Y-%m-%d  Time: %H : %M : %S',local_time)
        #print format_time
        #print local_time
        Year= local_time[0]
        Month=local_time[1]
        day=local_time[2]
        Hour= local_time[3]
        Min= local_time[4]
        second= local_time[5]
        return format_time,Hour,Min,second,Year,Month,day

#test_list=[]
#0: CRA 1: FU1 2: FU3 3: CRA2
#4: k1 5: QRC 6: PDRC 7: RCR
#8: RCR2 9:RCR3
test_list=[0,1,2,3,4,5,6,7,8,9]
#test_list=[2]
Address="Population\\XCS\\Carry_8"
#Address="Population\\XCS\\Breast_Cancer\\"
#Data_Address="R_env\\Breast_Cancer\\"
#Address="Population\\UCS\\MUX_70SUB"
#Address="Population\\UCS\\Majorityon9"


#Address=os.getcwd()+'/RuleCompaction/Check'
#Address="Check\\"
#SystemId:   0: ucs 1:xcs
#C=Compaction(Address,1,1,8,test_list)
#0 Mux 1 Carry 3 Majority-On
# Address, SystemId, ProblemId, Problem_Length,test_list
C=Compaction(Address,1,1,8,test_list,Address,False)
#C=Compaction(Address,1,1,8,test_list,Data_Address,True)