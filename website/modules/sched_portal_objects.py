import  pprint, dpath.util, datetime, json, bson, copy, calendar, collections, csv
from bson.objectid import ObjectId

class custom_calendar( ):
    def __init__(self, mongodb):
        self.__mongodb = mongodb
        self.__result = {'success':False, 'reason':None, 'data':None}
        self.__now = datetime.datetime.now()        

    def list_months(self):
        months_raw = self.__mongodb.month.find({},{'_id':0}).sort("month_number", 1)
        months=[]
        try:
            for month in months_raw:
                months.append(month)

            self.__result['success']=True
            self.__result['reason']="List of Months returned"
            self.__result['data']= months



        except Exception as e:
            self.__result['reason']="Failed to Generate Months List!Reason %s " % e

        return self.__result



class user( ):
    def __init__( self, mongodb ):
        self.__mongodb = mongodb
        self.__result = {'success':False, 'reason':None, 'data':None}

    def check_login(self,login):
        user_check = None
        try:
            user_check = self.__mongodb.user.find_one( { "username": login.get('username'), "password":login.get('password') } )
        except Exception as e:
            self.__result['reason']="Error!:Reason %s" % e
            return self.__result

        if user_check == None:
            self.__result['reason']="Invalid username/password"
        else:
            self.__result['reason']= login.get('username')
            self.__result['success']=True
            try:
                token = self.__mongodb.token.insert( { 
                    "login_date" :datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "headers":login.get('headers'),
                    "cookies":login.get('cookies'),
                    "user_id":user_check.get('_id'),
                    "username":user_check.get('username'),
                    "last_activity":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                } )
                self.__result['data']=token
            except Exception as e:
                self.__result['reason']= "Error! %s" % e 
            
        return self.__result

    def logout(self, token_id):
        try:
            self.__mongodb.token.remove( { "_id": ObjectId(token_id) } )
            self.__result['success']=True
            self.__result['reason']="Token(%s) Deleted.Logout successful" % token_id
        except Exception as e:
            self.__result['reason']= "Error! %s" % e 
        return self.__result


class token( ):
    def __init__( self, mongodb ):
        self.__mongodb = mongodb
        self.__response = {'success':False, 'reason':None, 'data':None}

    def token_validator(self,token_id):
        try:
            token = self.__mongodb.token.find_one({"_id": ObjectId(token_id)})
        except Exception as e:
            token = None

        if token:
            last_act = datetime.datetime.strptime(token.get('last_activity'),'%Y-%m-%d %H:%M:%S')
            now_raw = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            now = datetime.datetime.strptime(now_raw,'%Y-%m-%d %H:%M:%S')
            time_left = (now - last_act).total_seconds()/60

            if time_left <= 60:
                self.__mongodb.token.update(
                    {
                        "_id": ObjectId(token_id)
                    },
                    { "$set":
                      {
                          "last_activity": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                      }
                  },
                    upsert= False,
                    multi=False
                )
                self.__response['reason'] = "Token accepted"
                self.__response['success'] = True

            else:
                self.__mongodb.token.remove( { "_id": ObjectId(token_id) } )
                self.__response['reason'] = "Login session expired"
                self.__response['success'] = False

            return  self.__response
                    
        else:
            self.__response['reason'] ="token invalid"
            self.__response['success'] = False
            return  self.__response

class view_sched( ):
    def __init__( self, mongodb ):
        self.__mongodb = mongodb
        self.__result = {'success':False, 'reason':None, 'data':None}

    def months(self):
        try:
            get_months_raw = self.__mongodb.calendar.find()
            get_months = {}
            for x in get_months_raw:
                get_months.update(x)
        except Exception as e:
            self.__result['reason']="Error! %s" % e
            get_months = None

        if get_months == None:
            self.__result['reason']="No Data Found!"
        else:
            self.__result['reason']="Data Found"
            self.__result['success']=True
            self.__result['data']=get_months.get('months')
        return self.__result


class staff_management( ):
    def __init__(self, mongodb):
        self.__mongodb = mongodb
        self.__result = {'success':False, 'reason':None, 'data':None}
        
    def add(self, details):
        initials = details.get('initials').lower()
        profile_init = profile(self.__mongodb)
        get_profile = profile_init.get(initials)
        
        if get_profile.get('data')!=None:
            self.__result['reason']="Failed to add!Initials %s already exist" % initials
        else:
            try:
                if len(details.get('initials')) == 0:
                    self.__result['reason']="Failed to add!Initials cannot be empty"
                else:                
                    self.__mongodb.staff.insert(details)
                    self.__result['success']=True
                    self.__result['reason']="Staff added(%s)" % initials
            except Exception as e:
                self.__result['reason']="Failed! %s" % e
            
        return self.__result

    def get(self):
        try:
            staff_raw = self.__mongodb.staff.find({}, { '_id':0 })
            staff = []
            for s in staff_raw:
                staff.append(s)
        except Exception as e:
            self.__result['reason']="Failed! %s" % e

        if len(staff) == 0:
            self.__result['reason']="No Data Found!"
        else:
            self.__result['reason']="Data Found"
            self.__result['success']=True
            self.__result['data']=staff
        return self.__result


    def delete(self, data):
        try:
            if len(data.get('initials')) == 0:
                self.__result['reason']="Failed to update!Initials cannot be empty"
            else:
                self.__mongodb.staff.remove({"_id": ObjectId(data.get('_id'))})

                self.__result['success']=True
                self.__result['reason']="(%s) has been deleted" % data.get('initials')
        except Exception as e:
            self.__result['reason']="Failed to delete %s" % e
            
        return self.__result

class profile( ):
    def __init__(self, mongodb):
        self.__mongodb = mongodb
        self.__result = {'success':False, 'reason':None, 'data':None}
        self.__now = datetime.datetime.now()        

    def get(self, initials):
        profile = None
        try:
            profile_raw = self.__mongodb.staff.find( { 'initials':initials } )
            profile=[]
            for p in profile_raw:
                profile.append(p)
            self.__result['success']=True
        except Exception as e:
            self.__result['reason']="Failed! %s" % e

        if len(profile)==0:
            self.__result['reason']="No Data found for %s" % initials
        else:
            self.__result['reason']="Data found for %s" % initials
            self.__result['data']=profile

        return self.__result

    def update(self, data):
        profile = None
        try:
            profile = self.__mongodb.staff.find_one( { 'initials':data.get('initials') } )
            self.__result['success']=True

        except Exception as e:
            self.__result['reason']="Failed! %s" % e
        
        if profile == None:
            self.__result['reason']="No Data found for %s %s" % (data.get('first_name'), data.get('last_name'))
        else:
            
            try:
                self.__mongodb.staff.update(
                    {
                        "_id": ObjectId(data.get('_id'))
                    },
                    {
                        '$set': {
                            "initials": data.get('initials'),
                            "first_name": data.get('first_name'),
                            "last_name": data.get('last_name')
                      }

                    },
                    upsert= False,
                    multi=False
                )
                self.__result['reason']="%s %s has been updated" % (data.get('first_name'), data.get('last_name'))
                self.__result['success']=True
            except Exception as e:
                self.__result['reason']="Failed to Update!Reason: %s" % e
        
        return self.__result
        

    def gen_month(self, data):
        try:
            if len(data.get('month')) == 0:
                self.__result['reason']="Failed to add!Initials cannot be empty"
            else:
                months_init = custom_calendar(self.__mongodb)
                get_months = months_init.list_months()
                months_raw = get_months.get('data')
                months={}
                for m in months_raw:
                    months.update( { m.get('month'):m.get('month_number') } )

                month = data.get('month')
                number_days =calendar.monthrange(self.__now.year, months.get(month) )[1]
                date ={}
                for days in range(1,int(number_days)+1):
                    date_raw = datetime.date(self.__now.year,months.get(month),days )
                    day=date_raw.strftime('%A')
                    date.update({str(date_raw):day})
                    #date.update({"test":day})
                self.__result['success']=True
                self.__result['reason']="Dates for selected month generated"
                self.__result['data']=date
        except Exception as e:
            self.__result['reason']="Failed to Generate Dates for %s! %s" % ("data.get('month')", e)

            
        return self.__result


 
class schedule( ):
    def __init__(self, mongodb):
        self.__mongodb = mongodb
        self.__result = {'success':False, 'reason':None, 'data':None}
        self.__now = datetime.datetime.now()        
    
    def create(self, data):
        try:
            date_fragments = data.get('date').split(":")
            from_fragments = data.get('from').split(":")
            to_fragments = data.get('to').split(":")
            
            if int(to_fragments[0])<=int(from_fragments[0]):
                self.__result['reason']="Failed to add schedule for %s. Start and Finish time invalid" % data.get('initials')
            else:
                total_hours = int(to_fragments[0]) - int(from_fragments[0])
                start_date = "%s" % (date_fragments[0])
                date_created = "%s-%s-%s %s:%s"%(self.__now.year, self.__now.month, self.__now.day, self.__now.hour, self.__now.minute)
                sched={
                    "start_date":datetime.datetime.strptime(start_date,'%Y-%m-%d' ),
                    "day":date_fragments[1],
                    "initials":data.get('initials'),
                    "from":data.get('from'),
                    "to":data.get('to'),
                    "month":data.get('month'),
                    "name":data.get('name'),
                    "assignment":data.get('assignment'),
                    "total_hours":total_hours,
                    "date_created":datetime.datetime.strptime(date_created,'%Y-%m-%d %H:%M' )
                }

                months_init = custom_calendar(self.__mongodb)
                get_months = months_init.list_months()
                months_raw = get_months.get('data')
                months={}
                for m in months_raw:
                    months.update( { m.get('month'):m.get('total_hours') } )

                monthly_total_hours = months.get(data.get('month')) + total_hours 
            

                self.__mongodb.schedule.insert(sched)
                self.__mongodb.month.update( { "month":data.get('month') }, { '$set':{ "last_updated" : date_created, "total_hours":monthly_total_hours} } )

                self.__result['reason']="Schedule created for %s" % data.get('initials')
                self.__result['success']=True
            
        except Exception as e:
            self.__result['reason']="Failed to create schedule for %s!Reason:%s" % (data.get('initials'), e)

        return self.__result

    def get(self, initials):
        try:
            get_sched_raw = self.__mongodb.schedule.find({'initials':initials})
            get_sched = []
            for sched in get_sched_raw:
                get_sched.append(sched)


            if len(get_sched)==0:
                self.__result['reason']="No Schedule Found for %s" % initials
            else:
                self.__result['reason']="Schedule Found for %s" % initials
                self.__result['success']=True
                self.__result['data']=get_sched
        except Exception as e:
            self.__result['reason']="Unable to find schedule for %s!Reason:%s" % (initials, e)
            
        return self.__result

    def delete(self, data):
        try:
            initials = data.get('initials')
            sched_id = data.get('id')
            self.__mongodb.schedule.remove( {"_id": ObjectId(sched_id) } )

            self.__result['reason']="Schedule for %s(%s) has been deleted" % (initials, sched_id)
            self.__result['success']=True

        except Exception as e:
            self.__result['reason']="Unable to delete schedule for %s(%s)!Reason:%s" % (initials, sched_id, e)
            
        return self.__result


    def monthly(self, month):
        try:
            monthly_sched_raw = self.__mongodb.schedule.find({'month':month}).sort("start_date", 1)
            monthly_sched = []
            for sched in monthly_sched_raw:
                monthly_sched.append(sched)


            if len(monthly_sched)==0:
                self.__result['reason']="No Schedule Found for %s" % month
            else:
                self.__result['reason']="Schedule Found for %s" % month
                self.__result['success']=True
                self.__result['data']=monthly_sched
        except Exception as e:
            self.__result['reason']="Unable to find schedule for %s month!Reason:%s" % (month, e)
            
        return self.__result


    
 
class export( ):
    def __init__(self, mongodb):
        self.__mongodb = mongodb
        self.__result = {'success':False, 'reason':None, 'data':None}

    def get(self):
        try:
            export_raw = self.__mongodb.month.find( { "last_updated":{"$ne":None } } )
            export=[]
            for e in export_raw:
                export.append(e)
            self.__result['reason']="List of Months available for exportare returned"
            self.__result['success']=True
            self.__result['data']=export
        except Exception as e:
            self.__result['reason']="Unable to find schedule to be exported!Reason:%s" % e
        return self.__result

    def export_to_pc(self, data):
        try:
            if data.get('month')==None:
                self.__result['reason']="month is empty"
            else:
                sched_raw = self.__mongodb.month.find( { "month": data.get('month') } )
                sched={}
                day =[]
                for s in sched_raw:
                    day.append(s.get('day'))
                file_name = "novermber.csv" 
                my_dict = {"test": 1, "testing": 2}

                with open(file_name, 'wb') as f:  # Just use 'w' mode in 3.x
                    w = csv.DictWriter(f, my_dict.keys())
                    w.writeheader()
                    w.writerow(my_dict)
                self.__result['reason']="Scheduling for the month of % are exported" % data.get('month')
                self.__result['success']=True
                self.__result['data']=file_name
        except Exception as e:
            self.__result['reason']="Unable to export schedule!Reason:%s" % e
        return self.__result
