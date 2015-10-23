#!/usr/bin/env python                                                                                                                                                                                       
#-*- coding: utf-8 -*- 

from flask import Flask,request, render_template, flash, jsonify, make_response, Response, url_for, redirect
from pymongo import MongoClient
import json, datetime, local_settings, calendar, collections
from modules.sched_portal_objects import *

config = local_settings.env
app = Flask(__name__)


"""
Initialise Mongdo DB Connection
"""
client = MongoClient(config.get('MONGODB_HOST'))
mongodb = client[config.get('MONGODB_COLLECTION')]

"""
Flask config for changing Debug mode, SECRET_KEY
"""
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
))


#Used to display errors on webpage
@app.errorhandler( 500 )
def internal_500_error( exception ):
     #app.logger.exception( exception )
     return json.dumps( exception )

@app.errorhandler( 404 )
def internal_404_error( exception ):
     #app.logger.exception( exception )
     return 'scheduler <br/>\n%s<br/>\n%s' % ( exception, request.url )

@app.errorhandler( 401 )
def internal_401_error( exception ):
     #app.logger.exception( exception )
     return 'scheduler<br/>\n%s<br/>\n%s' % ( exception, request.url )


def default_encoder( obj, encoder=json.JSONEncoder() ):
    if isinstance( obj, ObjectId ): 
        return str( obj )  
    if isinstance(obj, datetime):
        return obj.strftime( '%Y-%m-%d %H:%M:%S' )
    return encoder.default( obj )


@app.route("/login", methods = [ 'GET' ] )
def log_in_get():
     token_id = "hi" #request.headers.get('x-token')
     resp = make_response()
     resp.headers.add('X-token',token_id)

     return render_template('log_in.html',resp=resp )

@app.route("/login", methods = [ 'POST' ] )
def log_in_post():
     token_id = "hi" #request.headers.get('x-token')
     try:
          payload = request.data
          payload_json = json.loads(payload)
          user_details = payload_json[0]
          user_details.update({ "headers":dict(request.headers), "cookies":dict(request.cookies) })
          user_init = user(mongodb)
          get_result = user_init.check_login(user_details)
          result = json.dumps (get_result, default=default_encoder, indent = 2, sort_keys = True)
          resp = make_response(result)
          resp.headers.add('X-token',token_id)
     except Exception as e:
          resp="Error! %s " % e
     return resp

@app.route("/login", methods = [ 'OPTIONS' ] )
def log_in_options():
     return ''

@app.route("/logout", methods = [ 'DELETE' ] )
def logout_del():
     try:
          payload = request.data
          payload_json = json.loads(payload)
          id_raw = payload_json[0]
          logout_init = user(mongodb)
          logout = logout_init.logout(id_raw.get('id'))
          result = json.dumps (logout, default=default_encoder, indent = 2, sort_keys = True)
          resp = make_response(result)
     except Exception as e:
          resp="Error! %s " % e
     return resp

@app.route("/logout", methods = [ 'OPTIONS' ] )
def logout_options():
     return ''

@app.route("/home/<token_id>", methods = [ 'GET' ] )
def home_get(token_id):
     token_init = token(mongodb)
     token_auth= token_init.token_validator(token_id)

     if token_auth.get('success')==True:
          sched_init = view_sched(mongodb)
          get_sched = sched_init.months()
          #resp = json.dumps(get_sched.get('data'))
          resp = render_template('monthly.html', months=get_sched.get('data'))
     else:
          message = json.dumps("Failed: %s" % token_auth.get('reason'))
          resp = redirect(url_for('log_in_get'))
          flash(message)
     return resp


@app.route("/home/<token_id>", methods = [ 'OPTIONS' ] )
def home_options(token_id):
     #token_id = "hi" #request.headers.get('x-token')
     return ''

@app.route("/home/<token_id>/staff_management", methods = [ 'GET' ] )
def staff_get(token_id):
     token_init = token(mongodb)
     token_auth= token_init.token_validator(token_id)

     if token_auth.get('success')==True:
          staff_init = staff_management(mongodb)
          get_staff = staff_init.get()
          if get_staff.get('success') == False:
               message = json.dumps(get_staff.get('reason'))
               flash(message)
          #flash(get_staff.get('data'))
          resp = render_template('staff_management.html', staff=get_staff.get('data'))
     else:
          message = json.dumps("Failed: %s" % token_auth.get('reason'))
          resp = redirect(url_for('log_in_get'))
          flash(message)
     return resp

@app.route("/home/<token_id>/staff_management", methods = [ 'OPTIONS' ] )
def staff_options(token_id):
     #token_id = "hi" #request.headers.get('x-token')
     return ''

@app.route("/home/<token_id>/staff_management", methods = [ 'POST' ] )
def staff_add(token_id):
     token_init = token(mongodb)
     token_auth= token_init.token_validator(token_id)

     if token_auth.get('success')==True:

          try:
               payload = request.data
               payload_json = json.loads(payload)
          except Exception as e:
               resp="Failed to load data!Reason: %s" % e
               return json.dumps(resp)

          staff_init = staff_management(mongodb)
          add_staff = staff_init.add(payload_json)

          if add_staff.get('success') == False:
               message = json.dumps(add_staff.get('reason'))
               flash(message)
          resp = json.dumps(add_staff, default=default_encoder, indent = 1)
     else:
          message = json.dumps("Failed: %s" % token_auth.get('reason'))
          resp = redirect(url_for('log_in_get'))
          flash(message)
     return resp

@app.route("/home/<token_id>/staff_management/<prof_init>", methods = [ 'GET' ] )
def profile_get_(token_id,prof_init):
     token_init = token(mongodb)
     token_auth= token_init.token_validator(token_id)

     if token_auth.get('success')==True:
          profile_init = profile(mongodb)
          get_profile = profile_init.get(prof_init)


          if get_profile.get('success') == False:
               message = json.dumps(get_profile.get('reason'))
               flash(message)

          sched_init = view_sched(mongodb)
          get_sched = sched_init.months()

          resp = render_template('profile.html', profile=get_profile.get('data'), months = get_sched.get('data'))
     else:
          message = json.dumps("Failed: %s" % token_auth.get('reason'))
          resp = redirect(url_for('log_in_get'))

     return resp


@app.route("/home/<token_id>/staff_management/<prof_init>", methods = [ 'PUT' ] )
def profile_put(token_id,prof_init):
     token_init = token(mongodb)
     token_auth= token_init.token_validator(token_id)

     if token_auth.get('success')==True:
          try:
               payload = request.data
               payload_json = json.loads(payload)
          except Exception as e:
               resp="Failed to load data!Reason: %s" % e
               return json.dumps(resp)

          profile_init = profile(mongodb)
          update_profile = profile_init.update(payload_json)

          if update_profile.get('success') == False:
               message = json.dumps(update_profile.get('reason'))
               flash(message)

          resp =json.dumps(update_profile, indent=2)
     else:
          message = json.dumps("Failed: %s" % token_auth.get('reason'))
          resp = redirect(url_for('log_in_get'))

     return resp


@app.route("/home/<token_id>/staff_management/<prof_init>", methods = [ 'DELETE' ] )
def profile_del(token_id,prof_init):
     token_init = token(mongodb)
     token_auth= token_init.token_validator(token_id)

     if token_auth.get('success')==True:
          try:
               payload = request.data
               payload_json = json.loads(payload)
          except Exception as e:
               resp="Failed to load data!Reason: %s" % e
               return json.dumps(resp)
          
          staff_init = staff_management(mongodb)
          delete_staff = staff_init.delete(payload_json)

          if delete_staff.get('success') == False:
               message = json.dumps(delete_staff.get('reason'))
               flash(message)

          resp = json.dumps(delete_staff, default=default_encoder)
     else:
          message = json.dumps("Failed: %s" % token_auth.get('reason'))
          resp = redirect(url_for('log_in_get'))

     return resp


@app.route("/home/<token_id>/staff_management/<prof_init>/create_sched", methods = [ 'GET' ] )
def profile_sched_get(token_id,prof_init):
     return ''

@app.route("/home/<token_id>/staff_management/<prof_init>/create_sched", methods = [ 'OPTIONS' ] )
def profile_sched_opts(token_id,prof_init):
     return ''


@app.route("/home/<token_id>/staff_management/<prof_init>/create_sched", methods = [ 'POST' ] )
def profile_sched_post(token_id,prof_init):
     token_init = token(mongodb)
     token_auth= token_init.token_validator(token_id)

     if token_auth.get('success')==True:
          try:
               payload = request.data
               payload_json = json.loads(payload)
          except Exception as e:
               resp="Failed to load data!Reason: %s" % e
               return json.dumps(resp)

          gen_month_init = profile(mongodb)
          gen_month = gen_month_init.gen_month(payload_json)

          if gen_month.get('success') == False:
               message = json.dumps(gen_month.get('reason'))
               flash(message)
          
          resp =json.dumps(gen_month,default=default_encoder, indent=2, sort_keys =True)
          #resp = render_template('profile.html', dates = data)
     else:
          message = json.dumps("Failed: %s" % token_auth.get('reason'))
          resp = redirect(url_for('log_in_get'))

     return resp


@app.route("/home/<token_id>/staff_management/<prof_init>/create_sched", methods = [ 'PUT' ] )
def profile_sched_pust(token_id,prof_init):
     token_init = token(mongodb)
     token_auth= token_init.token_validator(token_id)

     if token_auth.get('success')==True:
          try:
               payload = request.data
               payload_json = json.loads(payload)
          except Exception as e:
               resp="Failed to load data!Reason: %s" % e
               return json.dumps(resp)

          sched_init = schedule(mongodb)
          create_sched = sched_init.create(payload_json)

          if create_sched.get('success') == False:
               message = json.dumps(create_sched.get('reason'))
               flash(message)
          
          resp =json.dumps(create_sched,default=default_encoder, indent=2, sort_keys =True)
          #resp = render_template('profile.html', dates = data)
     else:
          message = json.dumps("Failed: %s" % token_auth.get('reason'))
          resp = redirect(url_for('log_in_get'))

     return resp




if __name__ == "__main__":
    app.run(debug=True)
    #app.run()
