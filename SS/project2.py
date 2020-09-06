
# you must populate this dict with the schools required -> try talking to the teaching team about this


schools = {   
'ironhack' : 10828,
'app-academy' : 10525,
'springboard' : 11035    
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
#Create student ID

def student_id(x):
    if str(x) != "Anonymous":
        #re_name=re.findall('([a-z])',str(x.lower()))#
        student_id=x[0:3].lower()+str(np.random.choice(99999, 1, replace=False))[1:-1]
    else:
        student_id="ano"+str(np.random.choice(99999, 1, replace=True))[1:-1]
    return student_id

####### Filter comments

comments_filter=comments.copy()
comments_filter.dropna(subset = ["overallScore","graduatingYear"], inplace=True)
#####Create studend df
    
person_identification=comments_filter[["id","name", "graduatingYear","isAlumni","jobTitle"]]
person_identification["student_id"]=person_identification["name"].apply(student_id)
cols=['id','student_id', 'name', 'graduatingYear', 'isAlumni', 'jobTitle']
person_identification=person_identification[cols]
person_identification=person_identification.reset_index(drop=True)

#####Create review df
reviews=comments_filter[["id","queryDate","tagline","review_body"]]
reviews=reviews.reset_index(drop=True)


#####Create review df
scores=comments_filter[["id","school_id","program","overallScore","overall","curriculum","jobSupport"]]
scores=scores.reset_index(drop=True)


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

# any data cleaning still missing here? take a look at the description
schools = pd.concat(schools_list)
schools.head()


#https://www.switchup.org/chimera/v1/bootcamp-data?mainTemplate=bootcamp-data%2Fdescription&path=%2Fbootcamps%2Fironhack&isDataTarget=false&bootcampId=10828&logoTag=logo&truncationLength=250&readMoreOmission=...&readMoreText=Read%20More&readLessText=Read%20Less