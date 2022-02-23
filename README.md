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

    
