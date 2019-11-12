from Environment import environment
import copy
#from Read_Agent import Read_List_Address

###############################################
#CRA was developed by Wilson

#Population: A LCS trained population
#Problem_Id: see Environment.py
#[0:'MUX',1:'Carry',2:'Parity',3:'Majority',4:'ZOO',5:'Audiology',6:'Balance',7:'Breast_Cancer',8:'Congressional_Voting',9:'balloon1'
# 10:'balloon2',11:'balloon3',12:'balloon4',13:'soybean_small',14:'tumor',15:'Splice_junction_Gene_Sequences',16:'Promoter_Gene_Sequences',17:'monk1',18:'monk2',
# 19: 'monk3']
#Problem_length: number of considered features
#System_Id: 0: UCS 1: XCS
#Is_ten_Folder: identify did population is based on 10 folder over validation. None:Not Other value: Yes

class CRA:
    def __init__(self,population,Problem_Id,Problem_length,System_Id,Is_ten_Folder=None):


        self.system_Id=System_Id

        self.population=population

        self.Problem_Id=Problem_Id

        if Is_ten_Folder==None:
            self.env=environment(True,self.Problem_Id,Problem_length)
            if self.Problem_Id>3:
                self.env.Initial_Real_Value(self.Problem_Id)
        else:
            self.env=environment(True,self.Problem_Id,Problem_length)
            self.env.Is_tenfolder=True
            self.env.folder_Address=Is_ten_Folder.Train_Address
            self.env.Initial_Real_Value(self.Problem_Id)

            self.Test_env=environment(True,self.Problem_Id,Problem_length)
            self.Test_env.Is_tenfolder=True
            self.Test_env.folder_Address=Is_ten_Folder.Test_Address
            self.Test_env.Initial_Real_Value(self.Problem_Id)
            

        

        self.final_acc, self.final_size,self.final_set =self.CRA_Implement(self.population)

        #print("F_Accuracy",self.final_acc)
        print(self.final_size)
        #self.Print_Rule_Set(self.final_set)
        self.un_cover_count,self.correct,self.error=self.Final_Accuracy_Test(self.final_set)

        self.final_test_accuracy=None

        if Is_ten_Folder!=None:
            self.final_test_accuracy=self.Accuracy_Test_tenfolders(self.final_set)

    def CRA_Implement(self,population):
        print('==================================')
        print('CRA')
        print(len(population))

        #2 numerosity (XCS,UCS)
        population.sort(key=lambda x:x[2],reverse=True)
        #print population[-1]
        original_accu=self.Accuracy_Test(population)
        print("O_Accuracy",original_accu)
        new_accuracy=0
        
        subset=[]

        #stage 1
        #Find a maximally correct rule-set
        count=0
        while new_accuracy<original_accu and len(subset)<len(population):
            
            subset.append(population[count])
            new_accuracy=self.Accuracy_Test(subset)
            count+=1


        #stage 2 remove rules which is potential redundant
        subset.sort(key=lambda x:x[2],reverse=False)
        #print population[-1]
        refaccu=original_accu
        circle_size=len(subset)
        for i in range(0,circle_size):
            hold_rule=subset[-1]
            subset.pop()
            new_accuracy=self.Accuracy_Test(subset)
            if new_accuracy<refaccu:
                subset.insert(0,hold_rule)

        #stage 3 again remove replaceable rules
        self.Review_all_train_instance(subset)
        #ranked by matched size #15 size of matched instances (XCS UCS)
        subset.sort(key=lambda x:x[15],reverse=True)

        final_set=[]

        D_set_state=copy.deepcopy(self.env.state)

        while len(subset)>0 and len(D_set_state)>0:
            final_set.append(subset[0])
            
            del_list=[]
            for id in range(0,len(D_set_state)):
                if self.isConditionMatched(subset[0],D_set_state[id]):
                    del_list.append(id)

            count=0
            for d_id in del_list:
                D_set_state.pop(d_id-count)
                count+=1
            subset.pop(0)



        final_acc=self.Accuracy_Test(final_set)
        print (final_acc)
        print (len(final_set))
        return final_acc, len(final_set),final_set


    #review the training_set
    def Review_all_train_instance(self,population):

        self.Add_additional_column_list(population)

        for id in range(0,len(self.env.state)):
            for rule in population:
                #0 condition
                if self.isConditionMatched(rule[0],self.env.state[id]):
                    if self.Problem_Id<4:
                        action=self.env.executeAction_supervisor(self.Problem_Id,self.env.state[id])
                        if action==rule[1]:
                            rule[13]+=1
                        else:
                            rule[14]+=1
                    else:
                        action=self.env.actions[id]
                        if action==rule[1]:
                            rule[13]+=1
                        else:
                            rule[14]+=1

        for rule in population:
            rule[15]=rule[13]+rule[14]


    #add additional column
    def Add_additional_column_list(self,population):
        for rule in population:
            temp=[]
            #11 correct match
            temp_1=[]
            #12 incorrect match
            c_size=0
            #13 correct match size
            Ic_size=0
            #14 incorrect match size
            match_size=0
            #15 match size

            #16 entropy value
            rule.append(temp)
            rule.append(temp)
            rule.append(c_size)
            rule.append(Ic_size)
            rule.append(match_size)


    def Accuracy_Test(self,population):
        correct=0
        for id in range(0,len(self.env.state)):
            Match_Set=self.getMatchSet(self.env.state[id],population)
            P_action=self.Prediction(Match_Set,population)
            if self.Problem_Id<4:
                action=self.env.executeAction_supervisor(self.Problem_Id,self.env.state[id])
            else:
                action=self.env.actions[id]

            if P_action==action:
                correct+=1
        accu=1.0*correct/len(self.env.state)
        return accu


    def Accuracy_Test_tenfolders(self,population):
        correct=0
        for id in range(0,len(self.Test_env.state)):
            Match_Set=self.getMatchSet(self.Test_env.state[id],population)
            P_action=self.Prediction(Match_Set,population)
            if self.Problem_Id<4:
                action=self.Test_env.executeAction_supervisor(self.Problem_Id,self.Test_env.state[id])
            else:
                action=self.Test_env.actions[id]

            if P_action==action:
                correct+=1
        accu=1.0*correct/len(self.Test_env.state)
        return accu

    def getMatchSet(self,state,population):
        match_set=[]
        #print "begin"
        for i in range(0,len(population)):
            #0: condition
            if(self.isConditionMatched(population[i][0],state)):
                #add matching classifier to the matchset
                match_set.append(i)
        return match_set

    def Prediction(self,match_set,population):
        actions_value=[]
        for i in range(0,self.env.real_actions):
            actions_value.append(0)

        for id in match_set:
            #1: action 2:numerosity 3: # 3: fitness (0UCS, 1XCS)
            if self.system_Id==0:
                actions_value[population[id][1]]+=population[id][2]*population[id][3]
            # 6 prediction 4 fitness
            elif self.system_Id==1:
                actions_value[population[id][1]]+=population[id][6]*population[id][4]

        #deault maxi
        max_id=0
        max_value=actions_value[0]
        for i in range(1,self.env.real_actions):
            if actions_value[i]>max_value:
                max_value=actions_value[i]
                max_id=i
        if len(match_set)==0:
            max_id=None
        return max_id

    #Judge whether condition is matched
    def isConditionMatched(self,condition,state):
        for i in range(0,len(condition)):
            if condition[i]!='#' and condition[i] != state[i]:
                return False
        return True


    def Print_Rule_Set(self,population):
        for rule in population:
            print (rule)

    def Final_Accuracy_Test(self,population):
        correct=0
        un_cover_count=0
        error=0

        for id in range(0,len(self.env.state)):
            Match_Set=self.getMatchSet(self.env.state[id],population)
            P_action=self.Prediction(Match_Set,population)
            if self.Problem_Id<4:
                action=self.env.executeAction_supervisor(self.Problem_Id,self.env.state[id])
            else:
                action=self.env.actions[id]

            if P_action==None:
                un_cover_count+=1

            if P_action!=None and P_action!=action:
                error+=1

            if P_action==action:
                correct+=1
        accu=1.0*correct/len(self.env.state)
        #print('Uncover',un_cover_count)
        #print('correct',correct)
        #print('error',error)
        #print('size',len(population))
        return un_cover_count,correct,error
