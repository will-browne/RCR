from Environment import environment
import copy



class QRC:
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

        self.final_acc, self.final_size,self.final_set =self.QRC_Implement(self.population)

        print(self.final_acc)
        print(self.final_size)
        #self.Print_Rule_Set(self.final_set)
        self.un_cover_count,self.correct,self.error=self.Final_Accuracy_Test(self.final_set)

        if Is_ten_Folder!=None:
            self.final_test_accuracy=self.Accuracy_Test_tenfolders(self.final_set)

        #print("test Accuracy",self.final_test_accuracy)

    # Called QCRA in the paper. It uses fitness to rank rules and guide covering. It's the same as Approach 15, but the code is re-written in 
     #   order to speed up.
    def QRC_Implement(self,population):
        print('==================================')
        print('QRC')
        #print("O_Accuracy",self.Accuracy_Test(population))
        print(len(population))

        #3 fitness UCS
        if self.system_Id==0:
            population.sort(key=lambda x:x[3],reverse=True)
        #4 fitness XCS
        elif self.system_Id==1:
            population.sort(key=lambda x:x[4],reverse=True)


        T_state=copy.deepcopy( self.env.state)

        c_population=[]
        #for rule in population:
        #    print rule[0],rule[3]
        while len(T_state)>0 and len(population)>0:
            new_T_state=[]
            match_count=0
            rule=population[0]
            for state in T_state:
                if self.isConditionMatched(rule[0],state):
                    match_count+=1
                else:
                    new_T_state.append(state)

            if match_count>0:
                c_population.append(rule)

            #remove tested rule
            population.pop(0)

            T_state=copy.deepcopy(new_T_state)

        final_acc=self.Accuracy_Test(c_population)
        print (final_acc)
        print (len(c_population))
        return final_acc, len(c_population),c_population

    

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

