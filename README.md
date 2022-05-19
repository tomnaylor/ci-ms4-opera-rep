### Problems
* getting __str__ to also return related field text (and str() on date) #title = Work.objects.get(id=self.work)
* getting static files to work
* saving images from admin (adding a record) into media folder
* https://stackoverflow.com/questions/35288793/django-media-url-tag #9 - post to add default image if no image uploaded for production
* https://docs.djangoproject.com/en/4.0/ref/templates/builtins/#date date formats for template
* https://stackoverflow.com/questions/2218327/django-manytomany-filter - filter many to many : productions = Production.objects.filter(creatives__id=person.id)
    * https://docs.djangoproject.com/en/4.0/topics/db/queries/#complex-lookups-with-q-objects Q to add an "or" to filter
    * https://fedingo.com/django-get-unique-values-from-queryset/ to get distinct() returns
* https://stackoverflow.com/questions/1981524/django-filtering-on-foreign-key-properties Search using foreign key property
* https://able.bio/rhett/how-to-set-and-get-environment-variables-in-python--274rgt5 - env vars help
    * https://www.gitpod.io/docs/environment-variables
    * https://blog.doppler.com/environment-variables-in-python
* migration to postgres problems:
    * https://stackoverflow.com/questions/11337420/can-i-use-an-existing-user-as-django-admin-when-enabling-admin-for-the-first-tim
    * https://www.dev2qa.com/how-to-force-reset-django-models-migrations/
    * https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html
    * https://hevodata.com/learn/sqlite-to-postgresql/
    * had to create new user, then make into super user thru CLI, then make profile for user "tom"
    
* CORS AWS Setup - https://docs.aws.amazon.com/AmazonS3/latest/userguide/ManageCorsUsing.html
* https://github.com/bradleyg/django-s3direct - used to upload django admin images to s3 - REMOVE, CRED VARS WERE NO IN DEV ENVIRON

### Talk about
* Heroku turning off collect static + requirements file corrupt
* AWS setup - bucket, cors etc. bucket policy (public access list not done??!)

Product form: https://learn.codeinstitute.net/courses/course-v1:CodeInstitute+FSF_102+Q1_2020/courseware/4201818c00aa4ba3a0dae243725f6e32/c557000edc0549b5b372ab66702580b3/?child=first - products / forms + views


# Future
* twitter intergration to show tweets with hashtag


# info
* heroku run rails db:migrate
* insall heroku cli "curl https://cli-assets.heroku.com/install.sh | sh"
* To update the current terminal session with the latest set of persistent environment variables, use: eval $(gp env -e)
* "heroku run python3 manage.py migrate"
* RUN in bash on heroku after git push - or in gitpod "heroku run bash"
    * python3 manage.py migrate works zero then run migrate