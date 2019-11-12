from Environment import environment




class K1:
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

        self.final_acc, self.final_size,self.final_set =self.K1_Implement(self.population)

        print(self.final_acc)
        print(self.final_size)
        self.Print_Rule_Set(self.final_set)
        self.un_cover_count,self.correct,self.error=self.Final_Accuracy_Test(self.final_set)

        if Is_ten_Folder!=None:
            self.final_test_accuracy=self.Accuracy_Test_tenfolders(self.final_set)

        #print("test Accuracy",self.final_test_accuracy)

    #A method introduced by Kharbat, 2008. Add the rule with the highest entropy to the final compact set. A rule's entropy is
    #    Defined as (correct matched cases - wrong matched cases)/ number of cases.

    def K1_Implement(self,population):
        print('==================================')
        print('K1')
        print(len(population))


        selected_ids=[]

        self.Review_all_train_instance(population)


        for i in range(0,len(self.env.state)):
            
            M_Set=self.getMatchSet(self.env.state[i],population)
            C_Set=[]
            #form the correct id
            for id in M_Set:
                #1 action
                action=self.env.actions[i]
                if population[id][1]==action:
                    C_Set.append(id)

            best_score=-1000000000
            best_Id=None

            for c_id in C_Set:

                #entropy
                score=1.0*(population[c_id][13]-population[c_id][14])/len(self.env.state)
                #print(score)
                if score>best_score:
                    best_score=score
                    best_Id=c_id

            if best_Id!=None: 
                if not best_Id in selected_ids:
                    selected_ids.append(best_Id)
            #else:
            #    print("No")

        c_population=[]
        for id in selected_ids:
            c_population.append(population[id])

        acc=self.Accuracy_Test(c_population)
        size=len(c_population)
        print ('accuracy: ',acc)
        print ('size: ',size)
        return acc, size, c_population

    

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
        print('Uncover',un_cover_count)
        print('correct',correct)
        print('error',error)
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