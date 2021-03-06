#!/usr/bin/env python

import sys; sys.path.insert(0, 'lib') # this line is necessary for the rest
import os                             # of the imports to work!

import web
import sqlitedb
from jinja2 import Environment, FileSystemLoader
import json

###########################################################################################
##########################DO NOT CHANGE ANYTHING ABOVE THIS LINE!##########################
###########################################################################################

######################BEGIN HELPER METHODS######################

# helper method to render a template in the templates/ directory
#
# `template_name': name of template file to render
#
# `**context': a dictionary of variable names mapped to values
# that is passed to Jinja2's templating engine
#
# See curr_time's `GET' method for sample usage
#
# WARNING: DO NOT CHANGE THIS METHOD
def render_template(template_name, **context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    jinja_env = Environment(autoescape=True,
            loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
            extensions=extensions,
            )
    jinja_env.globals.update(globals)

    web.header('Content-Type','text/html; charset=utf-8', unique=True)

    return jinja_env.get_template(template_name).render(context)

#####################END HELPER METHODS#####################

urls = ('/search', 'search',
        '/view', 'view'
        '/test', 'test')

class test:
    def GET(self):
        return json.dumps({'status': 0})
    def POST(self):
        return json.dumps({'status': 1})

class view:
    def GET(self):
        #print itemID
        params = web.input()
        restaurantId = params['restaurantId']
        #print itemID
        t = sqlitedb.transaction()
        try:
            #print "try statement"
            result = sqlitedb.getRestaurantById(restaurantId) #edit function to handle exception
            categories = sqlitedb.getCategories(restaurantId)
            categories_string = 'None'
            if categories:
                categories_string = ''
                for c in categories:
                    categories_string += c.Category
                    categories_string += '; '
        except Exception as e:
            t.rollback()
            error = str(e)
            return render_template('view.html', error = error)
        else:
            t.commit()
            if not result:
                return render_template('view.html')
            return render_template('view.html', result = result,categories = categories_string)
    
class search:
    def GET(self):
        #categories = sqlitedb.getCategories()
        return render_template('search.html')


    def POST(self):
        post_params = web.input()
        #if(defined(post_params)):
        restaurantId = post_params['restaurantId']
        name = post_params['name']
        category = post_params['category']
        minPrice = post_params['minPrice']
        maxPrice = post_params['maxPrice']
        city = post_params['city']
        lat = post_params['lat']
        longi = post_params['long']
        distance = post_params['distance']
        minStars = post_params['minStars']
        t = sqlitedb.transaction()
        try:
            search_result = sqlitedb.search(restaurantId, name, category, minPrice, maxPrice, city, lat, longi, distance, minStars)
            updateMessage = 'search successful'
        except Exception as e:
            t.rollback()
            updateMessage = str(e)
            #search_result = 'error'
            return render_template('search.html', message = updateMessage)
        else:
            t.commit()
            return render_template('search.html', message = updateMessage, search_result = search_result)
    
###########################################################################################
##########################DO NOT CHANGE ANYTHING BELOW THIS LINE!##########################
###########################################################################################

if __name__ == '__main__':
    web.internalerror = web.debugerror
    app = web.application(urls, globals())
    app.add_processor(web.loadhook(sqlitedb.enforceForeignKey))
    app.run()
