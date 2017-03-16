#!/usr/bin/env python

import sys; sys.path.insert(0, 'lib') # this line is necessary for the rest
import os                             # of the imports to work!

import web
import sqlitedb
from jinja2 import Environment, FileSystemLoader
import json

from pgmpy.models import BayesianModel
from pgmpy.inference import VariableElimination
from pgmpy.readwrite import XMLBIFReader
MODEL_FILE = 'bayes453.bif.xml'
model = XMLBIFReader(MODEL_FILE).get_model()
infer = VariableElimination(model)
baseline_result = {}
for node in model.nodes():
        baseline_result[node] = infer.query([node])[node].values[1]
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

urls = ('/bayes', 'bayes', '/search', 'search', '/test', 'test', '/view', 'view')

class test:
    def GET(self):
        return json.dumps({'status': 0})
    def POST(self):
        return json.dumps({'status': 1})

class bayes:
    def GET(self):
        #return json.dumps({'status': 2})
        return render_template('bayes.html')
    def POST(self):
        #return json.dumps({'status': 3})
        #return render_template('bayes.html')

        params = web.input()
        Sandwiches = params['Sandwiches']
        Italian = params['Italian']
        Burgers = params['Burgers']
        Pizza = params['Pizza']
        Seafood = params['Seafood']
        Mexican = params['Mexican']
        Chinese = params['Chinese']

        probMap = {}

        if Sandwiches == "true":
            probMap['Sandwiches'] =1
        elif Sandwiches == "false":
            probMap['Sanwiches'] = 0#False
        if Italian == "true":
            probMap['Italian'] = 1#True
        elif Sandwiches == "false":
            probMap['Italian'] = 0#False
        if Burgers== "true":
            probMap['Burgers'] = 1#True
        elif Burgers == "false":
            probMap['Burgers'] = 0#False
        if Pizza == "true":
            probMap['Pizza'] = 1#True
        elif Pizza == "false":
            probMap['Pizza'] = 0#False
        if Seafood == "true":
            probMap['Seafood'] = 1#True
        elif Seafood == "false":
            probMap['Seafood'] = 0#False
        if Mexican == "true":
            probMap['Mexican'] = 1#True
        elif Mexican == "false":
            probMap['Mexican'] = 0#False
        if Chinese == "true":
            probMap['Chinese'] = 1#True
        elif Chinese == "false":
            probMap['Chinese'] = 0#False

        # execute the bayes function with the probMap
        prob_result = {}
        if len(probMap) > 0:
            for node in model.nodes():
                if node not in probMap:
                    query_res = infer.query([node],evidence=probMap)[node].values[1]
                    if abs(query_res - baseline_result[node]) > 0.025:
                        prob_result[node] = query_res- baseline_result[node]
        else:
            prob_result = baseline_result
        return render_template('bayes.html', prob_result = prob_result)

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
            reviewsResult = sqlitedb.getReviewsByRestaurant(restaurantId)
            #print reviewsResult
        except Exception as e:
            t.rollback()
            error = str(e)
            #return json.dumps({'status': 1, 'error': error})
            return render_template('view.html', error = error)
        else:
            t.commit()
            if not result:
                #return json.dumps({'status': 0, 'message': 'no results'})
                return render_template('view.html')
            #return json.dumps({'status': 0, 'results': list(result)})
            if reviewsResult is None:
                return render_template('view.html', result = result,categories = categories_string)
            else:
                return render_template('view.html', result = result,categories = categories_string,reviews=reviewsResult)


class search:
    def GET(self):
        categories = sqlitedb.getAllCategories()
        #t = sqlitedb.transaction()
        #try:
            #result = sqlitedb.getRestaurantById('W9Bh_7mfuUrEAdQBJMVOvA')
        #    result = sqlitedb.search(None, None, None, None, None, None, None, None, None, None)
        #    updateMessage = 'search successful'
        #except Exception as e:
        #    t.rollback()
        #    updateMessage = str(e)
            #search_result = 'error'
        #    return json.dumps({'status': 1, 'message': updateMessage})
            #return render_template('search.html', message = updateMessage)
        #else:
        #    t.commit()
        #    return json.dumps({'status': 0, 'results': list(result)})
            #return render_template('search.html', message = updateMessage, search_result = search_result)
        return render_template('search.html', categories = categories)

    def POST(self):
        categories = sqlitedb.getAllCategories()
        post_params = web.input()
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
        numResults = post_params['numResults']
        sortBy = post_params['sortBy']
        #print post_params
        t = sqlitedb.transaction()
        try:
            search_result = sqlitedb.search(restaurantId, name, category, minPrice, maxPrice, city, lat, longi, distance, minStars, numResults,sortBy)
            #search_result = sqlitedb.search(None, None, None, None, None, None, None, None, None, '5')
            #search_result = sqlitedb.getRestaurantById('W9Bh_7mfuUrEAdQBJMVOvA')
            updateMessage = 'search successful'
        except Exception as e:
            t.rollback()
            updateMessage = str(e)
            #search_result = 'error'
            #return json.dumps({'status': 1, 'message': updateMessage})
            return render_template('search.html', message = updateMessage,categories = categories)
        else:
            t.commit()
            #return json.dumps({'status': 0, 'results': list(search_result)})
            return render_template('search.html', message = updateMessage, search_result = search_result,categories=categories)

if __name__ == '__main__':
    web.internalerror = web.debugerror
    app = web.application(urls, globals())
    app.add_processor(web.loadhook(sqlitedb.enforceForeignKey))
    app.run()
