import numpy as np
import random
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import os
import matplotlib.lines as mlines
import matplotlib as mpl
import copy
import os

#Read a compacted population (only consist condition and action)
class Read_Compacted_Solution:
    def __init__(self,address):
        #whether read information from works for CEC
        self.CEC_version=False
        self.address=address
        self.population=[]
        self.Read()
        self.read_population()
        
        #print len(self.population)

    def Read_Information(self,address):
        read_information=open(address,'r')
        information=[]
        for lines in read_information:
            if lines != '' and lines !='\n':
             information.append(lines)
        #print (information)
        return information

    def Read(self):
        informations=self.Read_Information(self.address)
        for raw in informations:
            if self.CEC_version==True:
                extracted= raw.split('\n')[0].split('-->')
            else:
                extracted= raw.split('\n')[0].split(' :')
            action=int(extracted[1].split(' ')[-1])
            condition=extracted[0].split(' ')[0:-1]
            for i in range(0,len(condition)):
                if condition[i]!='#':
                    if not '.' in condition[i]:
                        condition[i]=int(condition[i])
                    else:
                        condition[i]=float(condition[i])
            rule=self.create_rule(condition,action)
            self.population.append(rule)
         


    def create_rule(self,condition,action):
        rule=[]
        rule.append(condition)
        rule.append(action)
        return rule

    def count_dontcare(self,rule):
        count=0
        for i in range(0,len(rule[0])):
            if rule[0][i]=='#':
                count+=1
        return count

    def count_one(self,rule):
        count=0
        for i in range(0,len(rule[0])):
            if rule[0][i]==1:
                count+=1
        return count

    def count_zero(self,rule):
        count=0
        for i in range(0,len(rule[0])):
            if rule[0][i]==0:
                count+=1
        return count

    def read_population(self):
        for rule in self.population:
            if self.count_dontcare(rule)!=5:
                print rule
            if self.count_one(rule)>0:
                print rule
      


#translate rules to patterns
class Value_knowledge:
    def __init__(self,address,action_list):


        Read_UCS=Read_Compacted_Solution(address)

        self.action_list=action_list

        self.Raw_Population=Read_UCS.population

        self.clustered=self.Conver_to_Cluster()

        self.attribute_List=self.Calculate_Attribute_importance_distribution_Value()

        #self.attribute_List=self.Calculate_Attribute_importance_distribution_PureImportance()

        
        
    def Conver_to_Cluster(self):
        length=len(self.Raw_Population[0][0])
        cluster=[]
        for i in range(0,length+1):
            temp=[]
            cluster.append(temp)

        for rule in self.Raw_Population:
            level=self.General_Level(rule[0])
            cluster[level].append(rule)

        return cluster


    def General_Level(self,condition):
        count=0
        for cod in condition:
            if cod=='#':
                count+=1
        return count

    def Calculate_Attribute_importance_distribution_Value(self):
        
        #Initial the action based distribution list
        distribution_list=[]
        length=len(self.Raw_Population[0][0])
        #print len(self.negative_set)
        for i in range(0,len(self.clustered)):
            temp=[]
            for j in range(0,length):               
                temp.append(0)
            distribution_list.append(temp)

        #Action distributed list
        G_distribution_list=[]
        for i in range(0,len(self.action_list)):
            temp=copy.deepcopy(distribution_list)
            G_distribution_list.append(temp)

        G_count_list=copy.deepcopy(G_distribution_list)

        #Z_count_list=copy.deepcopy(G_distribution_list)

        #Z_distribution_list=copy.deepcopy(G_distribution_list)


        #print distribution_list
        for i in range(0,len(self.clustered)):
            if len(self.clustered[i])!=0:
                for rule in self.clustered[i]:
                    for cond_l in range(0,length):
                        if rule[0][cond_l]!='#':
                            if rule[1]==1:
                                G_distribution_list[rule[1]][i][cond_l]+=rule[0][cond_l]
                                G_count_list[rule[1]][i][cond_l]+=1

                            if rule[1]==0:
                                G_distribution_list[rule[1]][i][cond_l]+=rule[0][cond_l]-1
                                G_count_list[rule[1]][i][cond_l]+=1


                for d_l in range(0,length):
                    for action in self.action_list:
                        if G_count_list[action][i][d_l]!=0:
                            G_distribution_list[action][i][d_l]=1.0*G_distribution_list[action][i][d_l]/G_count_list[action][i][d_l]
                            #if G_distribution_list[action][i][d_l]==0:
                             #   G_distribution_list[action][i][d_l]=-1
        print (G_distribution_list)
        #print len(distribution_list)



        return G_distribution_list


    def Calculate_Attribute_importance_distribution_PureImportance(self):
        
        #Initial the action based distribution list
        distribution_list=[]
        length=len(self.Raw_Population[0][0])
        #print len(self.negative_set)
        for i in range(0,len(self.clustered)):
            temp=[]
            for j in range(0,length):               
                temp.append(0)
            distribution_list.append(temp)

        #Action distributed list
        G_distribution_list=[]
        for i in range(0,len(self.action_list)):
            temp=copy.deepcopy(distribution_list)
            G_distribution_list.append(temp)

        G_count_list=copy.deepcopy(G_distribution_list)

        #Z_count_list=copy.deepcopy(G_distribution_list)

        #Z_distribution_list=copy.deepcopy(G_distribution_list)


        #print distribution_list
        for i in range(0,len(self.clustered)):
            if len(self.clustered[i])!=0:
                for rule in self.clustered[i]:
                    for cond_l in range(0,length):
                        if rule[0][cond_l]!='#':
                            G_distribution_list[rule[1]][i][cond_l]+=1
                            G_count_list[rule[1]][i][cond_l]+=1
                        else:
                            G_count_list[rule[1]][i][cond_l]+=1


                for d_l in range(0,length):
                    for action in self.action_list:
                        if G_count_list[action][i][d_l]!=0:
                            G_distribution_list[action][i][d_l]=1.0*G_distribution_list[action][i][d_l]/G_count_list[action][i][d_l]
                            #if G_distribution_list[action][i][d_l]==0:
                            #    G_distribution_list[action][i][d_l]=-1
        print (G_distribution_list)
        #print len(distribution_list)



        return G_distribution_list


#visualizing patterns
class Visualize_value_pattern:
    def __init__(self,address,action_list,path):
        self.action_list=action_list
        V_K=Value_knowledge(address,action_list)
        self.png_path=path
        self.distribution_list=V_K.attribute_List

        self.Drew()
       
        #self.Drew_Real()
    def Rainbown_color(self,length):
        R=0xff
        G_begin=0x66
        B_begin=0x66
        step=G_begin//length
        color='#'
        colors=[]
        for i in range(0,length):
            #color=color+str(hex(R))+str(hex(B_begin+step*i))+str(hex(G_begin-step*i))
            color=color+self.translate_sixteen_string(R)+self.translate_sixteen_string(B_begin+step*i)+self.translate_sixteen_string(B_begin-step*i)
            colors.append(color)
            color='#'
        #for co in colors:
        #    print co
        return colors


    def translate_sixteen_string(self,value):
        if abs(value)<0x10:
            #print value, '           ', 0x10
            result='0'
            result=result+str(hex(value)).split('x')[-1]
        else:
         result=str(hex(value)).split('x')[-1]
        return result   


    def Detect_Inforative_levels(self,list):
         result=[]
         for i in range(0,len(list)):
             for j in list[i]:
                 if j!=0:
                    result.append(i)
                    break
         print result
         return result


    def Drew(self):
        fig=plt.figure(figsize=(10, 10), dpi=150)
        ax1=fig.add_subplot(111,projection='3d')
        z_first=np.asarray( self.distribution_list[0])
        z=z_first.T


        
        xlabels_t=[]       
        for i in range(0,len(z)):
            xlabels_t.append(str(i))
        xlabels=np.array(xlabels_t)
        xpos=np.arange(xlabels.shape[0])

        ylabels_t=[]       
        for i in range(0,len(z[0])):
            ylabels_t.append(str(i))
        ylabels=np.array(ylabels_t)
        ypos=np.arange(ylabels.shape[0])



        xposM, yposM=np.meshgrid(xpos,ypos,copy=False)

        dx=0.3
        dy=0.1

        ax1.w_xaxis.set_ticks(xpos + dx/2.)
        ax1.w_xaxis.set_ticklabels(xlabels)

        ax1.w_yaxis.set_ticks(ypos + dy/3.)
        ax1.w_yaxis.set_ticklabels(ylabels)

        color_list=['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan','tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']

        line_list=['--',':','--',':','--',':','--',':','--',':','--',':','--',':','--',':','--',':']
        #for act in range(6,7):
        for act in range(0,len(self.action_list)):
            important_list=self.Detect_Inforative_levels(self.distribution_list[act])
            z_first=np.asarray( self.distribution_list[act])
            z=z_first.T

            y=[]

            for i in range(0,len(z[0])):
                y.append(i)



            for i in range(0,len(z)):
                x=[i]*len(z[i])
                if len(z)>=20:


                    ax1.plot(x, y, z[i], line_list[act],color=color_list[act],lw=3,alpha=3)

                    ax1.legend()
                    for j in range(0,len(z[i])):
                        if z[i][j] !=0 and i%4==0:

                            ax1.text(i, j, z[i][j]+0.1, str(round(z[i][j],2)), color=color_list[act])  
                else:
                    ax1.plot(x, y, z[i], line_list[act], color=color_list[act],lw=2)
                    ax1.legend()
                    for j in range(0,len(z[i])):
                        if z[i][j]!=0:
                            ax1.text(i, j, z[i][j]+0.01, str(round(z[i][j],2)), color=color_list[act])
   
        



            
            #y=[]
            #count=0
            #for i in range(0,len(z_first[0])):
            #    y.append(i)
         
            #for level in important_list:
            #    x=[level]*len(z_first[level])
            #    n_z=z_first[level]
            
            #    ax1.plot( y, x,n_z, '--', color=color_list[count],lw=1,alpha=3)

                    
            #    ax1.scatter(y, x,n_z,color=color_list[count]) 
            #    count+=1
            #    if count>len(color_list):
            #        count=0

            
                       


        ax1.set_xlabel('X ', fontsize=20)
        #ax1.set_title('6-BIT MUX', fontsize=30)
        ax1.set_ylabel('Y', fontsize=20)
        ax1.set_zlabel("Z", fontsize=20)

        for angle in range(1, 360,10):
            ax1.view_init(30, angle)
            plt.draw()
            png_complete_name = self.png_path + str(angle) + ".png"
            # fig.savefig(png_complete_name, dpi=(400))
            #fig.savefig(png_complete_name,bbox_inches='tight')
            fig.savefig(png_complete_name)
            plt.pause(.001)

    def Drew_Real(self):
        fig=plt.figure(figsize=(10, 10), dpi=150)
        ax1=fig.add_subplot(111,projection='3d')
        z_first=np.asarray( self.distribution_list[0])
        z=z_first.T


        
        
        action_list=['Mammal','Bird','Reptile','Fish','Amphibian','Insect','Sea_others']
        color_list=['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan','tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']

        line_list=['--',':','--',':','--',':','--',':','--',':','--',':','--',':','--',':','--',':']
        path_list=['UCS_V\\ZOO0\\','UCS_V\\ZOO1\\','UCS_V\\ZOO2\\','UCS_V\\ZOO3\\','UCS_V\\ZOO4\\','UCS_V\\ZOO5\\','UCS_V\\ZOO6\\']
        #for act in range(6,7):
        for act in range(0,len(self.action_list)):
        #for act in range(1,2):
            xlabels_t=[]       
            for i in range(0,len(z)):
                xlabels_t.append(str(i))

            #xlabels_t=['hair','feathers','eggs','milk','airborne','aquatic','predator','toothed','backbone','breathes','venomous','fins','legs','tail','domestic','catsize'] 
            xlabels=np.array(xlabels_t)
            xpos=np.arange(xlabels.shape[0])

            ylabels_t=[]       
            for i in range(0,len(z[0])):
                ylabels_t.append(str(i))
            ylabels=np.array(ylabels_t)
            ypos=np.arange(ylabels.shape[0])



            xposM, yposM=np.meshgrid(xpos,ypos,copy=False)

            dx=0.3
            dy=0.1

            ax1.w_xaxis.set_ticks(xpos + dx/2.)
            #ax1.w_xaxis.set_ticks(xpos + dx*5)
            ax1.w_xaxis.set_ticklabels(xlabels)

            ax1.w_yaxis.set_ticks(ypos + dy/3.)
            ax1.w_yaxis.set_ticklabels(ylabels)

            important_list=self.Detect_Inforative_levels(self.distribution_list[act])
            z_first=np.asarray( self.distribution_list[act])
            z=z_first.T

            y=[]

            for i in range(0,len(z[0])):
                y.append(i)



            for i in range(0,len(z)):
                x=[i]*len(z[i])
                if len(z)>=20:

                    ax1.plot(x, y, z[i], line_list[act],color=color_list[act],lw=3,alpha=3)

                    ax1.legend()
                    for j in range(0,len(z[i])):
                        if z[i][j] !=0 and i%4==0:

                            ax1.text(i, j, z[i][j]+0.1, str(round(z[i][j],2)), color=color_list[act])  
                else:
                    ax1.plot(x, y, z[i], line_list[act], color=color_list[act],lw=2)
                    ax1.legend()
                    for j in range(0,len(z[i])):
                        if z[i][j]>0:
                            ax1.text(i, j, z[i][j]+0.01, str(round(z[i][j],2)), color=color_list[act])
   
        



            
            #y=[]
            #count=0
            #for i in range(0,len(z_first[0])):
            #    y.append(i)
         
            #for level in important_list:
            #    x=[level]*len(z_first[level])
            #    n_z=z_first[level]
            
            #    ax1.plot( y, x,n_z, '--', color=color_list[count],lw=1,alpha=3)

                    
            #    ax1.scatter(y, x,n_z,color=color_list[count]) 
            #    count+=1
            #    if count>len(color_list):
            #        count=0

            
                       


            ax1.set_xlabel('X ', fontsize=20)
            ax1.set_title(action_list[act], fontsize=30)
            ax1.set_ylabel('Y', fontsize=20)
            ax1.set_zlabel("Z", fontsize=20)

            for angle in range(1, 360,20):
                ax1.view_init(10, angle)
                plt.draw()
                png_complete_name = path_list[act] + str(angle) + ".png"
                # fig.savefig(png_complete_name, dpi=(400))
                fig.savefig(png_complete_name,bbox_inches='tight')
                #fig.savefig(png_complete_name)
                plt.pause(.001)

            ax1.clear()

#Address="Compacted\\Carry8CRA2019_7_11_8_36_30.txt"
#PATH="VS\\12Carry\\"

#Address="Compacted\\MUX70RCR2019_7_22_19_32_7.txt"
#PATH="VS\\70MUX\\"

#Address="Compacted\\Majority11RCR32019_8_1_21_28_10.txt"
#PATH="VS\\11Maj\\"


#Address="Compacted\\MUX6RCR2019_7_10_17_27_20.txt"
#PATH="VS\\MUX6\\MUX6_RCR\\"


#Address="Compacted\\MUX6RCR22019_7_10_17_27_21.txt"
#PATH="VS\\MUX6\\MUX6_RCR2\\"



#Address="Compacted\\MUX11\\MUX11CRA2019_7_10_17_57_5.txt"
#PATH="VS\\MUX11\\MUX11_CRA\\"



#Address="Compacted\\MUX11\\MUX11CRA22019_7_11_5_56_37.txt"
#PATH="VS\\MUX11\\MUX11_CRA2\\"



#Address="Compacted\\MUX11\\MUX11FU12019_7_10_18_27_42.txt"
#PATH="VS\\MUX11\\MUX11_FU1\\"



#Address="Compacted\\MUX6RCR32019_7_10_17_27_22.txt"
#PATH="VS\\MUX6\\MUX6_RCR3\\"


#Address="Compacted\\MUX11\\MUX11FU32019_7_11_0_23_36.txt"
#PATH="VS\\MUX11\\MUX11_FU3\\"



#Address="Compacted\\MUX11\\MUX11k12019_7_11_5_56_48.txt"
#PATH="VS\\MUX11\\MUX11_K1\\"


#Address="Compacted\\MUX11\\MUX11PDRC2019_7_11_5_57_45.txt"
#PATH="VS\\MUX11\\MUX11_PDRC\\"


#Address="Compacted\\MUX11\\MUX11QRC2019_7_11_5_57_40.txt"
#PATH="VS\\MUX11\\MUX11_QRC\\"


#Address="Compacted\\MUX11\\MUX11RCR2019_7_11_5_58_34.txt"
#PATH="VS\\MUX11\\MUX11_RCR\\"


#Address="Compacted\\MUX11\\MUX11RCR22019_7_11_5_58_59.txt"
#PATH="VS\\MUX11\\MUX11_RCR2\\"


#Address="Compacted\\MUX11\\MUX11RCR32019_7_11_5_59_24.txt"
#PATH="VS\\MUX11\\MUX11_RCR3\\"


#Address="Compacted\\MUX11\\MUX11RCR32019_7_11_5_59_24.txt"
#PATH="VS\\MUX11\\MUX11_RCR3\\"


#Address="Compacted\\MUX20RCR2019_7_12_15_2_49.txt"
#PATH="VS\\MUX20\\"


#Address="Compacted\\MUX37RCR2019_7_13_6_32_10.txt"
#PATH="VS\\MUX37\\"


#Address="Compacted\\Carry6RCR2019_7_10_17_23_17.txt"
#PATH="VS\\CAR6\\"


#Address="Compacted\\Carry8RCR2019_7_11_10_35_49.txt"
#PATH="VS\\CAR8\\"

#Address="Compacted\\Carry10RCR32019_7_13_3_15_47.txt"
#PATH="VS\\CAR10\\RCR\\"


#Address="Compacted\\Carry12RCR32019_7_29_9_5_6.txt"
#PATH="VS\\CAR12\\"


#Address="Compacted\\CAR10\\Carry10CRA2019_7_12_0_51_1.txt"
#PATH="VS\\CAR10\\CRA"


#Address="Compacted\\CAR10\\Carry10FU32019_7_12_16_22_57.txt"
#PATH="VS\\CAR10\\FU3\\"


Address="Compacted\\CAR10\\Carry10k12019_7_13_3_11_57.txt"
PATH="VS\\CAR10\\K1\\"

#Address="Compacted\\CAR10\\Carry10PDRC2019_7_13_3_13_40.txt"
#PATH="VS\\CAR10\\PDRC\\"


#Address="Compacted\\CAR10\\Carry10QRC2019_7_13_3_13_13.txt"
#PATH="VS\\CAR10\\QRC\\"


#Address="Compacted\\CAR10\\Carry10RCR32019_7_13_3_15_47.txt"
#PATH="VS\\CAR10\\RCR3\\"



#Address="Compacted\\CAR10\\Carry10FU12019_7_12_12_4_51.txt"
#PATH="VS\\CAR10\\FU1\\"


#Address="Compacted\\Majority6RCR2019_7_10_17_31_59.txt"
#PATH="VS\\MAJ6\\"



#Address="Compacted\\Majority7RCR2019_7_11_6_21_52.txt"
#PATH="VS\\MAJ7\\"


#Address="Compacted\\Majority8RCR2019_7_12_4_40_45.txt"
#PATH="VS\\MAJ8\\"



#Address="Compacted\\Majority9RCR2019_7_15_2_16_54.txt"
#PATH="VS\\MAJ9\\"


#Address="Compacted\\Majority10RCR22019_7_18_3_11_59.txt"
#PATH="VS\\MAJ10\\"

#Address="Compacted\\Majority11RCR32019_8_1_21_28_10.txt"
#PATH="VS\\MAJ11\\"

#Address="Compacted\\MAJ11\\Majority11RCR2019_7_21_20_53_2.txt"
#PATH="VS\\MAJ11_\\RCR\\"

#Address="Compacted\\Majority11RCR32019_8_1_21_28_10.txt"
#PATH="VS\\MAJ11_\\RCR3\\"

#Address="Compacted\\MAJ11\\Majority11FU12019_7_16_16_44_10.txt"
#PATH="VS\\MAJ11_\\FU1\\"


#Address="Compacted\\MAJ11\\Majority11CRA2019_7_15_4_12_43.txt"
#PATH="VS\\MAJ11_\\CRA\\"


#Address="Compacted\\MAJ11\\Majority11k12019_7_21_20_47_15.txt"
#PATH="VS\\MAJ11_\\K1\\"

#Address="Compacted\\MAJ11\\Majority11QRC2019_7_21_20_50_4.txt"
#PATH="VS\\MAJ11_\\QRC\\"
action_list=[0,1]
VVP=Visualize_value_pattern(Address,action_list,PATH)