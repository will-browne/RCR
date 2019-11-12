from Environment import environment
import random
import os


class TenFolderSpliter:
    def __init__(self,problem_Id, problem_length,Address):

        self.Address=Address

        Env= environment(True, problem_Id, problem_length)
        Env.Initial_Real_Value(problem_Id)
        self.states=Env.state
        self.actions=Env.actions
        self.number_actions=Env.real_actions
        # the size of each group
        self.size=0

        self.Name=Env.problems_involved[problem_Id]


        print (len (self.states))
        print (len (self.actions))
        print (self.number_actions)

        #the sampe group (according tp action)
        self.Groups=self.Balance()
        self.Split()


    #create a single sample
    def Create_single_Sample(self,state,action):
        #0 condition 1 action
        sample=[]
        sample.append(state)
        sample.append(action)
        return sample

    #Find the maximal size of an action 
    def Max_Class(self,Groups):
        Max=0
        print("=======================")
        for group in Groups:
            print(len(group))
            if len(group)>Max:
                Max=len(group)
        return Max

    #create samples group accrouding to number of actions 
    def Produce_Sample_Group(self):
        Groups=[]
        for i in range(0,self.number_actions):
            temp=[]
            Groups.append(temp)

        for i in range(0,len(self.states)):
            Sample=self.Create_single_Sample(self.states[i],self.actions[i])
            Groups[Sample[1]].append(Sample)

        return Groups

    def Balance(self):
        Groups=self.Produce_Sample_Group()
        Max=self.Max_Class(Groups)
        self.size=Max
        for group in Groups:
            if len(group)<Max:
                add_sample=[random.choice(group) for _ in range(int(Max-len(group)))]
                group.extend(add_sample)
        
        return Groups

    def save_performance(self,txt,name):
        f=open(name,'wb')
        f.write(txt.encode())
        f.close()

    def conver_string(self,folders, test_Id):
        result_Train=""
        result_Test=""
        for i in range(0,10):            
            line=""
            for sample in folders[i]:
                for cod in sample[0]:
                    line=line+str(cod)+' '
                line=line+str(sample[1])+'\n'
            if i !=test_Id:
                result_Train+=line
            else:
                result_Test+=line
        return result_Train, result_Test


    def Split(self):
        remainder=self.size%10
        single_size=(self.size-remainder)/10
        #print (remainder)
        #print (single_size)

        
        #initial folders
        folders=[]
        for i in range(0,10):
            temp=[]
            folders.append(temp)

        count=0
        for i in range(0, self.size, single_size):
            #print (self.Groups[1][i:i+single_size])
            #print("================")
            for j in range(0,self.number_actions):
                if count>9:
                    folders[9].extend(self.Groups[j][i:i+single_size])
                else:
                    folders[count].extend(self.Groups[j][i:i+single_size])
            count+=1

        for i in range(0,10):
            test_Id=i
            result_Train, result_Test=self.conver_string(folders,test_Id)
            Train_name= self.Address+ self.Name+"_"+"Train"+"_"+str(test_Id)+".txt"
            Test_name=  self.Address+ self.Name+"_"+"Test"+"_"+str(test_Id)+".txt"
            self.save_performance(result_Train,Train_name)
            self.save_performance(result_Test,Test_name)

            
            





#Address="10_Folder\\Breast_Cancer\\"
#Address="10_Folder\\ZOO\\"
#Address="10_Folder\\Balance\\"
#Address="10_Folder\\Audiology\\"
#Address="10_Folder\\Promoter_Gene_Sequences\\"
#Address="10_Folder\\soybean_small\\"
#Address="10_Folder\\monk1\\"



#ten =TenFolderSpliter(17,9,Address)