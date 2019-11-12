import time


class Time_Calculate:
    def __init__(self):
        self.begin='begin'


    def startTimer(self):
        local_time= time.localtime(time.time())
        format_time=time.strftime('DAY: %Y-%m-%d  Time: %H : %M : %S',local_time)
        #print format_time
        #print local_time
        day=local_time[2]
        Hour= local_time[3]
        Min= local_time[4]
        second= local_time[5]
        return format_time,Hour,Min,second,day

    #time1 ceased time, time2 begin time (only correct in same month)
    def elapsed(self,Hour1,Hour2,Min1,Min2,second1,second2,day1,day2):
        #print (day1,day2)
        result=0
        if day1==day2:        
            result=result+second1-second2
            result=result+60*(Min1-Min2)
            result=result+3600*(Hour1-Hour2)
        elif day1==day2+1:
            Hour1+=24
            result=result+second1-second2
            result=result+60*(Min1-Min2)
            result=result+3600*(Hour1-Hour2)
        elif day1>day2+1:
            Hour1+=24
            result=result+second1-second2
            result=result+60*(Min1-Min2)
            result=result+3600*(Hour1-Hour2)
            result=result+(day1-day2-1)*24*3600

        return result
