import  pprint, dpath.util, requests, datetime, json, bson, copy, calendar, collections
from bson.objectid import ObjectId

class user( ):
    def __init__( self, mongodb ):
        self.__mongodb = mongodb
        self.__result = {'success':False, 'reason':None, 'data':None}

    def check_login(self,login):
        try:
            user_check = self.__mongodb.user.find_one( { "username": login.get('username'), "password":login.get('password') } )
        except Exception as e:
            user_check = None

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
        try:
            if len(details.get('initials')) == 0:
                self.__result['reason']="Failed to add!Initials cannot be empty"
            else:                
                self.__mongodb.staff.insert(details)
                self.__result['success']=True
                self.__result['reason']="Staff added(%s)" % details.get('initials')
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
                months_int = {
                    "January":1, 
                    "February":2, 
                    "March":3, 
                    "April":4, 
                    "May":5, 
                    "June":6, 
                    "July":7, 
                    "August":8, 
                    "September":9, 
                    "October":10, 
                    "November":11, 
                    "December":12
                }
                month = data.get('month')
                number_days =calendar.monthrange(self.__now.year, months_int.get(month) )[1]
                date ={}
                for days in range(1,int(number_days)+1):
                    date_raw = datetime.date(self.__now.year,months_int.get(month),days )
                    day=date_raw.strftime('%A')
                    date.update({str(date_raw):day})
                #collections.OrderedDict(date)

                self.__result['success']=True
                self.__result['reason']="Dates for selected month generated"
                self.__result['data']=date
        except Exception as e:
            self.__result['reason']="Failed! %s" % e

            
        return self.__result




class schedule( ):
    def __init__(self, mongodb):
        self.__mongodb = mongodb
        self.__result = {'success':False, 'reason':None, 'data':None}
        self.__now = datetime.datetime.now()        
    


    def create(self, data):

        date_raw = data.get('date')
        date_fragments = date_raw.split(":")

        sched={
            "date":date_fragments[0],
            "day":date_fragments[1],
            "pseudo_name":data.get('pseudo_name'),
            "from":data.get('from'),
            "to":data.get('to'),
        }
        self.__result['data']=sched
        return self.__result
