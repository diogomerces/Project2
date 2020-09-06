CREATE TABLE score (
score_id varchar(50)NOT NULL,
average_score float,
overall int,
curriculum int,
job_support int,
PRIMARY KEY(score_id)
);

CREATE TABLE course (
course_id varchar(50) NOT NULL,
course_name varchar(100),
PRIMARY KEY(course_id)
);

CREATE TABLE school(
school_id varchar(50) not null,
school_name varchar(50),
PRIMARY KEY(school_id)
);

CREATE TABLE location(
location_id varchar(50)not null,
city_name varchar(50),
city_id varchar(50),
country_name varchar(50),
country_id varchar(50),
PRIMARY KEY (location_id)
);

CREATE TABLE personal(
name_id varchar(50),
person_name varchar(200),
ser_alumi varchar(50),
grad_year varchar(50),
job_title varchar(500),
PRIMARY KEY(name_id)
);

CREATE TABLE badge(
badge_id varchar(50) not null,
badge_name varchar(200),
badge_description varchar(5000),
PRIMARY KEY(badge_id)
);

CREATE TABLE review (
review_id varchar(50),
created_at varchar(20),
tag_line varchar (500),
review_body text,
course varchar(500),
name_id varchar(50),
score_id varchar(50),
school_id varchar(50),
PRIMARY KEY (review_id)
);


CREATE TABLE school_location(
school_id varchar(50),
location_id varchar(50)
);

CREATE TABLE school_badge(
school_id varchar(50),
badge_id varchar(50)
); 

CREATE TABLE school_course(
school_id varchar(50),
course_id varchar(50)
);


