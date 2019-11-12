import math
import random
class environment:
    def __init__(self,check_state,Problem_Id,problem_length):
        self.multiplexer_posbits=[1,2,3,4,5,6,7,8,9,10,11]
        self.multiplexer_length=[3,6,11,20,37,70,135,264,521,1034,2059]
        self.problems_involved=['MUX','Carry','Parity','Majority','ZOO','Audiology','Balance','Breast_Cancer','Congressional_Voting','balloon1'
                             ,'balloon2','balloon3','balloon4','soybean_small','tumor','Splice_junction_Gene_Sequences','Promoter_Gene_Sequences','monk1','monk2',
                             'monk3']
        self.maxPayOff=1000
        self.Is_LinuX=False
        #set whether utilize 10 folders cross validation
        self.Is_tenfolder=False
        self.folder_Address=None
        #Real Value
        self.state=None
        self.actions=None
        self.real_length=None
        self.real_actions=None

        if Problem_Id<4 and check_state==True:
            self.real_actions=2
            if problem_length<19:
                CGI=create_global_instance(problem_length)
                self.state=CGI.inputs
            else:
                SampI=Samplae_instances(problem_length,5*1000)
                self.state=SampI.inputs
            self.actions=[]
            for stat in self.state:
                self.actions.append(self.executeAction_supervisor(Problem_Id,stat))

     #Create a state
    def Create_Set_condition(self,length):
        state=[0]*length
        for i in range(0, length):
            random_number=random.randint(0,1)
            if(random_number==0):
                state[i]=0
            else:
                state[i]=1
        return state

    # generate multiplexer result
    def execute_Multiplexer_Action(self,state):
        actual_Action=0
        length=len(state)
        post_Bits=1
        for number in range(0,len(self.multiplexer_length)):
            if length==self.multiplexer_length[number]:
                post_Bits=self.multiplexer_posbits[number]
        place=post_Bits
        for i in range(0,post_Bits):
            if state[i]==1:
                place=place+int(math.pow(2.0,float(post_Bits-1-i)))
                #print place
        if state[place]==1:
            actual_Action=1
        return actual_Action

    # generate carry result
    def execute_Carry_Action(self,state):
        carry=0
        actual_Action=0
        half_condition=int(len(state)/2)
        for i in range(0, half_condition):
            carry=int((carry+int(state[half_condition-1-i])+int(state[half_condition-1-i+half_condition]))/2)
  
        
        if carry==1:
            actual_Action=1
        return actual_Action

    # generate even parity result
    def execute_Even_parity_Action(self,state):
        numbers=0
        actual_Action=0
        for i in range(0,len(state)):
            if state[i]==1:
                numbers=numbers+1
        if numbers%2==0:
            actual_Action=1
        return actual_Action

    # generate the majority on result
    def execute_Majority_On_Action(self,state):
        actual_Action=0
        Numbers=0
        for i in range(0,len(state)):
            if(state[i]==1):
                Numbers=Numbers+1
        if Numbers>(len(state)/2):
            actual_Action=1
        return actual_Action

    # This function is for reinforcement learning     
    def executeAction(self, exenumber,state,action):
        ret=0
        #['multiplexer','carry', 'evenParity', 'majorityOn']
        if exenumber==0:
            #result=self.execute_Multiplexer_Action(state)
            result=self.execute_Multiplexer_Action(state)
        elif exenumber==1:
            #result=self.execute_Carry_Action(state)
            result=self.execute_Carry_Action(state)
        elif exenumber==2:
            result=self.execute_Even_parity_Action(state)
        elif exenumber==3:
            #result=self.execute_Majority_On_Action(state)
            result=self.execute_Majority_On_Action(state)

        if result==action:
            ret=self.maxPayOff
        return ret

    def Read_Information(self,path):
        read_information=open(path,'r')
        information=[]
        for lines in read_information:
            if lines != '' and lines !='\n':
             information.append(lines)
        return information 


    def global_Zoo(self):
        attribute=16
        datas=[]
        actions=[]
        
        if not self.Is_tenfolder:
            raw_information=self.Read_Information('R_env\\Zoo.txt')
        else:
            raw_information=self.Read_Information(self.folder_Address)

        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print first_inf
            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                temp.append(float(first_inf[i]))
            datas.append(temp)

        return actions,datas

    def global_Zoo_old(self):
        attribute=16
        datas=[]
        actions=[]
        
        if not self.Is_tenfolder:
            raw_information=self.Read_Information('R_env\\Zoo.txt')
        else:
            raw_information=self.Read_Information(self.folder_Address)

        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(',')
            #print first_inf
            actions.append( int(first_inf[-1])-1)
            temp=[]
            for i in range(1,len(first_inf)-1):
                temp.append(float(first_inf[i]))
            datas.append(temp)

        return actions,datas

    def executeAction_supervisor(self, exenumber,state):
        #['multiplexer','carry', 'evenParity', 'majorityOn']
        if exenumber==0:
            #result=self.execute_Multiplexer_Action(state)
            result=self.execute_Multiplexer_Action(state)
        elif exenumber==1:
            #result=self.execute_Carry_Action(state)
            result=self.execute_Carry_Action(state)
        elif exenumber==2:
            result=self.execute_Even_parity_Action(state)
        elif exenumber==3:
            #result=self.execute_Majority_On_Action(state)
            result=self.execute_Majority_On_Action(state)

        
        return result

    def Initial_Real_Value(self,exenumber):
        if exenumber==4:
            self.real_length=16
            self.real_actions=7
            self.actions, self.state=self.global_Zoo()
            self.Initial_Action_Set_candidate_Real()
        elif exenumber==5:
            self.real_length=69
            self.real_actions=24
            self.actions, self.state=self.global_Audiology()
            self.Initial_Action_Set_candidate_Real()
            #print self.action_value_candidate
            #print len(self.action_value_candidate)
        elif exenumber==6:
            self.real_length=4
            self.real_actions=3
            self.actions, self.state=self.global_Balance()
            self.Initial_Action_Set_candidate_Real()
            #print self.action_value_candidate
            #print len(self.action_value_candidate)
            #print self.actions
            #print self.state
        elif exenumber==7:
            self.real_length=9
            self.real_actions=2
            self.actions, self.state=self.global_Breast_Cancer()
            self.Initial_Action_Set_candidate_Real()
        elif exenumber==8:
            self.real_length=16
            self.real_actions=2
            self.actions, self.state=self.global_Congressional_Voting()
            self.Initial_Action_Set_candidate_Real()
        #balloon_1
        elif exenumber==9:
            self.real_length=4
            self.real_actions=2
            self.actions, self.state=self.global_balloon_1()
            self.Initial_Action_Set_candidate_Real()
        #balloon_2
        elif exenumber==10:
            self.real_length=4
            self.real_actions=2
            self.actions, self.state=self.global_balloon_2()
            self.Initial_Action_Set_candidate_Real()
        #balloon_3
        elif exenumber==11:
            self.real_length=4
            self.real_actions=2
            self.actions, self.state=self.global_balloon_3()
            self.Initial_Action_Set_candidate_Real()
        #balloon_4
        elif exenumber==12:
            self.real_length=4
            self.real_actions=2
            self.actions, self.state=self.global_balloon_4()
            self.Initial_Action_Set_candidate_Real()
        #soybean small
        elif exenumber==13:
            self.real_length=35
            self.real_actions=4
            self.actions, self.state=self.global_soybean_small()
            self.Initial_Action_Set_candidate_Real()
        #tumor
        elif exenumber==14:
            self.real_length=17
            self.real_actions=22
            self.actions, self.state=self.global_Tumor()
            self.Initial_Action_Set_candidate_Real()
        #Splice_junction_Gene_Sequences
        elif exenumber==15:
            self.real_length=60
            self.real_actions=3
            self.actions, self.state=self.global_Splice_junction_Gene_Sequences()
            self.Initial_Action_Set_candidate_Real()
        #Splice_junction_Gene_Sequences
        elif exenumber==16:
            self.real_length=57
            self.real_actions=2
            self.actions, self.state=self.global_Splice_Promoter_Gene_Sequences()
            self.Initial_Action_Set_candidate_Real()
        #monk1
        elif exenumber==17:
            self.real_length=6
            self.real_actions=2
            self.actions, self.state=self.global_monk1()
            self.Initial_Action_Set_candidate_Real()
        #monk2
        elif exenumber==18:
            self.real_length=6
            self.real_actions=2
            self.actions, self.state=self.global_monk2()
            self.Initial_Action_Set_candidate_Real()
        #monk3
        elif exenumber==19:
            self.real_length=6
            self.real_actions=2
            self.actions, self.state=self.global_monk3()
            self.Initial_Action_Set_candidate_Real()


    def Real_random_state_action(self):
        id=random.randint(0,len(self.state)-1)
        return self.state[id], self.actions[id]


    def global_Audiology(self):
        attribute=69
        datas=[]
        actions=[]
        if not self.Is_tenfolder:
            if self.Is_LinuX:
                raw_information=self.Read_Information(os.getcwd()+'/Parallel_CXCS_V2/R_env/Audiology.txt')
            else:
                raw_information=self.Read_Information('R_env\\Audiology.txt')
        
        else:
            raw_information=self.Read_Information(self.folder_Address)
        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print len(first_inf)

            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                if first_inf[i] !='?':
                    temp.append(int(first_inf[i]))
                else:
                    temp.append(first_inf[i])
            datas.append(temp)

        #print actions
        #print datas
        return actions,datas

    #Balance
    def global_Balance(self):
        attribute=4
        datas=[]
        actions=[]
        if not self.Is_tenfolder:
            if self.Is_LinuX:
                raw_information=self.Read_Information(os.getcwd()+'/Parallel_CXCS_V2/R_env/Balance.txt')
            else:
                raw_information=self.Read_Information('R_env\\Balance.txt')
        else:
            raw_information=self.Read_Information(self.folder_Address)

        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print len(first_inf)

            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                if first_inf[i] !='?':
                    temp.append(int(first_inf[i]))
                else:
                    temp.append(first_inf[i])
            datas.append(temp)

        #print actions
        #print datas
        return actions,datas


    def global_Breast_Cancer(self):
        attribute=9
        datas=[]
        actions=[]
        
        if not self.Is_tenfolder:
            if self.Is_LinuX:
                raw_information=self.Read_Information(os.getcwd()+'/Parallel_CXCS_V2/R_env/Breast_Cancer.txt')
            else:
                raw_information=self.Read_Information('R_env\\Breast_Cancer.txt')
        else:
            raw_information=self.Read_Information(self.folder_Address)
        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print len(first_inf)

            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                if first_inf[i] !='?':
                    temp.append(int(first_inf[i]))
                else:
                    temp.append(first_inf[i])
            datas.append(temp)

        #print actions
        #print datas
        return actions,datas

    #soybean_small

    #Congressional_Voting
    def global_Congressional_Voting(self):
        attribute=16
        datas=[]
        actions=[]
        
        if not self.Is_tenfolder:
            if self.Is_LinuX:
                raw_information=self.Read_Information(os.getcwd()+'/Parallel_CXCS_V2/R_env/Congressional_Voting.txt')
            else:
                raw_information=self.Read_Information('R_env\\Congressional_Voting.txt')
        else:
            raw_information=self.Read_Information(self.folder_Address)
        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print len(first_inf)

            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                if first_inf[i] !='?':
                    temp.append(int(first_inf[i]))
                else:
                    temp.append(first_inf[i])
            datas.append(temp)

        #print actions
        #print datas
        return actions,datas

    #Initial an action-set for the real domains' actions
    def Initial_Action_Set_candidate_Real(self):
        value_result=[]
        for i in range(0,self.real_length):
            temp=[]
            value_result.append(temp)


        for j in range(0,len(self.state)):
            #print self.state
            #print len(self.state[j]), self.real_length
            for s_id in range(0,len(self.state[j])):
                if not self.state[j][s_id] in value_result[s_id] and self.state[j][s_id]!='?':
                    value_result[s_id].append(self.state[j][s_id])

        for temp in value_result:
            temp.sort()
        #print (value_result)

        self.action_value_candidate= value_result

   #balloon1
    def global_balloon_1(self):
        attribute=2
        datas=[]
        actions=[]
        if self.Is_LinuX:
            raw_information=self.Read_Information(os.getcwd()+'/Parallel_CXCS_V2/R_env/balloon_1.txt')
        else:
            raw_information=self.Read_Information('R_env\\balloon_1.txt')
        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print len(first_inf)

            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                if first_inf[i] !='?':
                    temp.append(int(first_inf[i]))
                else:
                    temp.append(first_inf[i])
            datas.append(temp)

        #print actions
        #print datas
        return actions,datas

     #balloon2
    def global_balloon_2(self):
        attribute=2
        datas=[]
        actions=[]
        if self.Is_LinuX:
            raw_information=self.Read_Information(os.getcwd()+'/Parallel_CXCS_V2/R_env/balloon_2.txt')
        else:
            raw_information=self.Read_Information('R_env\\balloon_2.txt')
        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print len(first_inf)

            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                if first_inf[i] !='?':
                    temp.append(int(first_inf[i]))
                else:
                    temp.append(first_inf[i])
            datas.append(temp)

        #print actions
        #print datas
        return actions,datas

    #balloon3
    def global_balloon_3(self):
        attribute=2
        datas=[]
        actions=[]
        if self.Is_LinuX:
            raw_information=self.Read_Information(os.getcwd()+'/Parallel_CXCS_V2/R_env/balloon_3.txt')
        else:
            raw_information=self.Read_Information('R_env\\balloon_3.txt')
        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print len(first_inf)

            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                if first_inf[i] !='?':
                    temp.append(int(first_inf[i]))
                else:
                    temp.append(first_inf[i])
            datas.append(temp)

        #print actions
        #print datas
        return actions,datas

    #balloon4
    def global_balloon_4(self):
        attribute=2
        datas=[]
        actions=[]
        if self.Is_LinuX:
            raw_information=self.Read_Information(os.getcwd()+'/Parallel_CXCS_V2/R_env/balloon_4.txt')
        else:
            raw_information=self.Read_Information('R_env\\balloon_4.txt')
        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print len(first_inf)

            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                if first_inf[i] !='?':
                    temp.append(int(first_inf[i]))
                else:
                    temp.append(first_inf[i])
            datas.append(temp)

        #print actions
        #print datas
        return actions,datas

    #soybean_small
    def global_soybean_small(self):
        attribute=35
        datas=[]
        actions=[]
        
        if not self.Is_tenfolder:
            if self.Is_LinuX:
                raw_information=self.Read_Information(os.getcwd()+'/Parallel_CXCS_V2/R_env/soybean_small.txt')
            else:
                raw_information=self.Read_Information('R_env\\soybean_small.txt')
        else:
            raw_information=self.Read_Information(self.folder_Address)

        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print len(first_inf)

            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                if first_inf[i] !='?':
                    temp.append(int(first_inf[i]))
                else:
                    temp.append(first_inf[i])
            datas.append(temp)

        #print actions
        #print datas
        return actions,datas

    #Tumor
    def global_Tumor(self):
        attribute=17
        datas=[]
        actions=[]
        if self.Is_LinuX:
            raw_information=self.Read_Information(os.getcwd()+'/Parallel_CXCS_V2/R_env/tumor.txt')
        else:
            raw_information=self.Read_Information('R_env\\tumor.txt')
        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print len(first_inf)

            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                if first_inf[i] !='?':
                    temp.append(int(first_inf[i]))
                else:
                    temp.append(first_inf[i])
            datas.append(temp)

        #print actions
        #print datas
        return actions,datas

    #Splice_junction_Gene_Sequences
    def global_Splice_junction_Gene_Sequences(self):
        datas=[]
        actions=[]
        if self.Is_LinuX:
            raw_information=self.Read_Information(os.getcwd()+'/Parallel_CXCS_V2/R_env/Splice_junction_Gene_Sequences.txt')
        else:
            raw_information=self.Read_Information('R_env\\Splice_junction_Gene_Sequences.txt')
        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print len(first_inf)

            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                if first_inf[i] !='?':
                    temp.append(int(first_inf[i]))
                else:
                    temp.append(first_inf[i])
            datas.append(temp)

        #print actions
        #print datas
        return actions,datas


    #Promoter_Gene_Sequences
    def global_Splice_Promoter_Gene_Sequences(self):
        datas=[]
        actions=[]
        if not self.Is_tenfolder:
            if self.Is_LinuX:
                raw_information=self.Read_Information(os.getcwd()+'/Parallel_CXCS_V2/R_env/Promoter_Gene_Sequences.txt')
            else:
                raw_information=self.Read_Information('R_env\\Promoter_Gene_Sequences.txt')
        else:
            raw_information=self.Read_Information(self.folder_Address)

        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print len(first_inf)

            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                if first_inf[i] !='?':
                    temp.append(int(first_inf[i]))
                else:
                    temp.append(first_inf[i])
            datas.append(temp)

        #print actions
        #print datas
        return actions,datas

    #monk1
    def global_monk1(self):
        datas=[]
        actions=[]
        if not self.Is_tenfolder:
            if self.Is_LinuX:
                raw_information=self.Read_Information(os.getcwd()+'/Parallel_CXCS_V2/R_env/monk1.txt')
            else:
                raw_information=self.Read_Information('R_env\\monk1.txt')
        else:
            raw_information=self.Read_Information(self.folder_Address)

        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print len(first_inf)

            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                if first_inf[i] !='?':
                    temp.append(int(first_inf[i]))
                else:
                    temp.append(first_inf[i])
            datas.append(temp)

        #print actions
        #print datas
        return actions,datas

    #monk2
    def global_monk2(self):
        datas=[]
        actions=[]
        if self.Is_LinuX:
            raw_information=self.Read_Information(os.getcwd()+'/Parallel_CXCS_V2/R_env/monk2.txt')
        else:
            raw_information=self.Read_Information('R_env\\monk2.txt')
        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print len(first_inf)

            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                if first_inf[i] !='?':
                    temp.append(int(first_inf[i]))
                else:
                    temp.append(first_inf[i])
            datas.append(temp)

        #print actions
        #print datas
        return actions,datas


        #monk3
    def global_monk3(self):
        datas=[]
        actions=[]
        if self.Is_LinuX:
            raw_information=self.Read_Information(os.getcwd()+'/Parallel_CXCS_V2/R_env/monk3.txt')
        else:
            raw_information=self.Read_Information('R_env\\monk3.txt')
        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print len(first_inf)

            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                if first_inf[i] !='?':
                    temp.append(int(first_inf[i]))
                else:
                    temp.append(first_inf[i])
            datas.append(temp)

        #print actions
        #print datas
        return actions,datas


class create_global_instance:
    def __init__(self,length):
        self.inputs=[[0]*length for i in range(2**length)]
        for i in range(2**length):
            value=i
            divisor=2**length
            #fill the input bits
            for j in range(length):
                divisor/=2
                if value >=divisor:
                    self.inputs[i][j]=1
                    value -=divisor

class Samplae_instances:
    def __init__(self,length,size):
        self.inputs=[]
        for i in range(0,size):
            self.inputs.append(self.Create_Set_condition(length))


    def Create_Set_condition(self,length):
        state=[0]*length
        for i in range(0, length):
            random_number=random.randint(0,1)
            if(random_number==0):
                state[i]=0
            else:
                state[i]=1
        return state
