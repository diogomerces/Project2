
# you must populate this dict with the schools required -> try talking to the teaching team about this


schools = {   
'ironhack' : 10828,
'app-academy' : 10525,
'springboard' : 11035,
'le-wagon' : 10868,
'academia-de-codigo' : 10494,
'edit-disruptive-digital-education' : 10731,
'nyc-data-science-academy' : 10925   
}

import re
import pandas as pd
from pandas.io.json import json_normalize
import requests
import numpy as np

#aux function to apply regex and remove tags
  
def remove_tags(x):###################################
    TAG_RE = re.compile(r'<[^>]+>')############################
    return TAG_RE.sub('',x)##############################################

def get_comments_school(school):

  # defines url to make api call to data -> dynamic with school if you want to scrape competition
  url = "https://www.switchup.org/chimera/v1/school-review-list?mainTemplate=school-review-list&path=%2Fbootcamps%2F" + school + "&isDataTarget=false&page=3&perPage=10000&simpleHtml=true&truncationLength=250"
  #makes get request and converts answer to json
  data = requests.get(url).json()
  #converts json to dataframe
  reviews =  pd.DataFrame(data['content']['reviews'])
  
  reviews['review_body'] = reviews['body'].apply(remove_tags)
  reviews['school'] = school
  reviews['school_id'] = schools[str(school)] #############################
  return reviews


###############################################################
"""# could you write this as a list comprehension? ;)
comments = []

for school in schools.keys():
    print(school)
    comments.append(get_comments_school(school))"""
    
comments=[get_comments_school(school) for school in schools.keys()]    

comments = pd.concat(comments)

######################################################################################
#Create random ID

import random

global key_list
key_list=[i for i in range(0,100000)]
random.shuffle(key_list)

def generate_id(y):
    global key_list
    x=(key_list).pop()
    generate_id=str(x)
    return generate_id


"""def generate_id(y):
    global key_list
    x=(key_list).pop()
    if str(y) != "Anonymous":
        generate_id=str(y)[0:1].lower()+str(x)
    else:
        generate_id="an"+str(x)
    return generate_id"""
      
###############################################################

from pandas.io.json import json_normalize

def get_school_info(school, school_id):
    url = 'https://www.switchup.org/chimera/v1/bootcamp-data?mainTemplate=bootcamp-data%2Fdescription&path=%2Fbootcamps%2F'+ str(school) + '&isDataTarget=false&bootcampId='+ str(school_id) + '&logoTag=logo&truncationLength=250&readMoreOmission=...&readMoreText=Read%20More&readLessText=Read%20Less'

    data = requests.get(url).json()

    data.keys()

    courses = data['content']['courses']
    courses_df = pd.DataFrame(courses, columns= ['courses'])

    locations = data['content']['locations']
    locations_df = json_normalize(locations)

    badges_df = pd.DataFrame(data['content']['meritBadges'])
    
    website = data['content']['webaddr']
    description = data['content']['description']
    logoUrl = data['content']['logoUrl']
    school_df = pd.DataFrame([website,description,logoUrl]).T
    school_df.columns =  ['website','description','LogoUrl']

    locations_df['school'] = school
    courses_df['school'] = school
    badges_df['school'] = school
    school_df['school'] = school

    locations_df['school_id'] = school_id
    courses_df['school_id'] = school_id
    badges_df['school_id'] = school_id
    school_df['school_id'] = school_id    
    
    # how could you write a similar block of code to the above in order to record the school ID?

    return locations_df, courses_df, badges_df, school_df

locations_list = []
courses_list = []
badges_list = []
schools_list = []

for school, id in schools.items():
    print(school)
    a,b,c,d = get_school_info(school,id)
    locations_list.append(a)
    courses_list.append(b)
    badges_list.append(c)
    schools_list.append(d)
    
    
locations = pd.concat(locations_list)
locations.head()

courses = pd.concat(courses_list)
courses.head(10)

badges = pd.concat(badges_list)
badges.head()


schools = pd.concat(schools_list)
schools.head()


#####Create course df + school_course

course=courses[["school_id","courses"]]
cols=["school_id","course_name"]
course.columns=cols
course_t=pd.DataFrame(course.groupby(['school_id',"course_name"]).first())
course_t= course_t.reset_index()
course_t["course_id"]=course_t["course_name"].apply(generate_id)

school_course=course_t[["school_id","course_id"]]

course=course_t[["course_id","course_name"]]

####### Filter comments

comments_filter=comments.copy()

comments_filter=comments_filter.reset_index(drop=True)

condit=[comments_filter["program"].tolist()[index] in (course["course_name"][course.index]).tolist() for index,i in enumerate(comments_filter["program"].tolist())]
comments_filter["teste"]=pd.DataFrame(condit)
comments_filter=comments_filter[comments_filter["teste"]]

#comments_filter.dropna(subset = ["overallScore","graduatingYear","program"], inplace=True)





#####Create review df
review=comments_filter[["id","queryDate","tagline","review_body","program"]]
review["name_id"]=comments_filter["name"].apply(generate_id)
review["score_id"]=comments_filter["overallScore"].apply(generate_id)

#review2 = review.merge(course_t, how = 'inner', left_on ="program", right_on = 'course_name')


#review["program_id"]=comments_filter["program"].apply(generate_id)########mal
#cols=['review_id', 'created_at', 'tag_line', 'review_body', 'name_id', 'score_id','course_id']

#review = review2.drop(columns = ['program','school_id','course_name'],  axis =1)

cols=['review_id', 'created_at', 'tag_line', 'review_body', 'name_id', 'score_id',"course_id"]
review.columns=cols



#####Create personal identification df
    
personal=comments_filter[["name","isAlumni","graduatingYear","jobTitle","id"]]
##personal["name_id"]=personal["name"].apply(generate_id)



personal2 = personal.merge(review, how = 'inner', left_on ="id", right_on = 'review_id')
personal = personal2.drop(columns = ['id','review_id','created_at',"tag_line","review_body","score_id","course_id"],  axis =1)
cols=['name_id', 'name', 'isAlumni',"graduatingYear",'jobTitle']
cols2=['name_id', 'person_name', 'ser_alumi', "grad_year",'job_title']
personal=personal[cols]
personal.columns=cols2

#####Create score df
score=comments_filter[["overallScore","overall","curriculum","jobSupport","id"]]

score2 = score.merge(review2, how = 'inner', left_on ="id", right_on = 'id')
cols=['score_id','overallScore', 'overall', 'curriculum', 'jobSupport'] 
score=score2[cols]


score=score[cols]
cols2=['score_id','average_score', 'overall', 'curriculum', 'job_support'] 
score.columns=cols2

course=course.reset_index(drop=True)
personal=personal.reset_index(drop=True)
review=review.reset_index(drop=True)
score=score.reset_index(drop=True)



#####Create location df
location = pd.concat(locations_list)
location_bridge = location.copy()
location = location.drop(columns = ['id','description','country.abbrev','city.keyword','state.id','state.name','state.abbrev','state.keyword','school','school_id'],  axis =1)

location['country.name'].fillna('Online', inplace = True)
location['city.name'].fillna('Online', inplace = True)
location['country.id'].fillna(-1, inplace = True)
location['city.id'].fillna(-1, inplace = True)

location = pd.DataFrame(location.groupby(['country.id','country.name','city.id','city.name']).first())

location = location.reset_index()

location["location_id"]=location["city.name"].apply(generate_id)

#ALterando a posição da coluna location_id
cols =["location_id",'country.id','country.name','city.id','city.name']
location = location[cols]
location.rename({'country.id': 'country_id','country.name': 'country_name',
                'city.id': 'city_id','city.name':'city_name'}, inplace = True, axis=1)




####################Create  Tabela Badge df
badge = pd.concat(badges_list)
badge_bridge = badge.copy()

#exclui as colunas 'keyword', 'school'
badge = badge.drop(columns = ['keyword', 'school','school_id' ],  axis =1)

#Altera nomes da colunas 
badge.rename({'name': 'badge_name','description': 'badge_description'}, inplace = True, axis=1)

#Removido <p> e </p>
badge['badge_description'] = badge['badge_description'].str.lstrip('</p>').str.rstrip('</p>')

#Agrupando badge_name e badge_description
badge = pd.DataFrame(badge.groupby(['badge_name'])['badge_description'].first())
badge = badge.reset_index()

#Criação do badge_id
badge["badge_id"]=badge["badge_name"].apply(generate_id)

cols =["badge_id",'badge_name','badge_description']
badge = badge[cols]

####################Create  Tabela School df
school = pd.concat(schools_list)

#Alterando o nome school por school_name
school.rename({'school': 'school_name'}, inplace = True, axis=1)

#Excluindo colunas website, description e LogoUrl
school = school.drop(columns = ['website','description','LogoUrl'],  axis =1)

#Alterando a ordem das colunas
cols =["school_id",'school_name']
school = school[cols]

############ Tabela School_badge brigde

school_badge = badge_bridge.merge(badge, how = 'inner', left_on ="name", right_on = 'badge_name')

school_badge = school_badge.drop(columns = ['name', 'keyword', 'description', 'school',
       'badge_name', 'badge_description'],  axis =1)


### Tabela School_location_bridge

school_location = location.merge(location_bridge, how = 'inner', left_on ="country_name", right_on = 'country.name')

school_location = school_location.drop(columns = ['country_id', 'country_name', 'city_id', 'city_name',
       'id', 'description', 'country.id', 'country.name', 'country.abbrev',
       'city.id', 'city.name', 'city.keyword', 'state.id', 'state.name',
       'state.abbrev', 'state.keyword', 'school'],  axis =1)

#########################

#IMPORT TO SQL


# import the module
from sqlalchemy import create_engine

# create sqlalchemy engine
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="tasmania",
                               db="djm"))

"""course.to_sql('course', con = engine, if_exists = "append",index=False)

personal.to_sql('personal', con = engine, if_exists = "append",index=False)

review.to_sql('review', con = engine, if_exists = "append",index=False)

score.to_sql('score', con = engine, if_exists = "append",index=False)

school_course.to_sql('school_course', con = engine, if_exists = "append",index=False)

badge.to_sql('badge', con = engine, if_exists = "append",index=False)

location.to_sql('location', con = engine, if_exists = "append",index=False)

school.to_sql('school', con = engine, if_exists = "append",index=False)

school_location.to_sql('school_location', con = engine, if_exists = "append",index=False)

school_badge.to_sql('school_badge', con = engine, if_exists = "append",index=False)"""

print("Done")


#QUERIES - BUSINESS QUESTIONS








#https://www.switchup.org/chimera/v1/bootcamp-data?mainTemplate=bootcamp-data%2Fdescription&path=%2Fbootcamps%2Fironhack&isDataTarget=false&bootcampId=10828&logoTag=logo&truncationLength=250&readMoreOmission=...&readMoreText=Read%20More&readLessText=Read%20Less