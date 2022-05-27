# Testing - Online production catalogue
## By Tom Naylor

**View live site:** https://tn83-wno-test-bed.herokuapp.com/

**View GitHub repo:** https://github.com/tomnaylor/ci-ms4-opera-rep


Welcome to the testing readme for the online production catalogue


## Table of contents
* [Testing](#testing)
  * [Unit tests in Django](#unit-tests-in-django)
  * [Automatic testers / validators](#automatic-testers-and-validators)
  * [Testing against the user Stories](#testing-against-the-user-stories)
  * [Manual Testing](#manual-testing)
  * [Known Bugs](#known-bugs)


## Testing

As well as the manual testing below I have also used the Chrome Dev Tools and PEP8 validators. I found them very helpful to notify me of any potential problems and code that violates the standard. I also used the googles lighthouse to test the site load times and user experience.

### Unit tests in Django

[TestCase](https://docs.djangoproject.com/en/4.0/topics/testing/overview/) is an automated testing class that I've used to program tests against the models, forms and views of the app. You can run tests on a forked version using "python3 manage.py test" in the bash shell. All tests are listed below along with a description of what they test against.

#### Profiles

Tests for profiles span three files: **test_forms.py**, **test_models.py** and **test_views.py** as there are a number of tests for this app.

##### test_forms

* **ProductionCommentFormTest**
    * **test_profile_comment_fields_are_required** tests that without a comment the form will be invalid
    * **test_profile_comment_fields_are_inc_in_form_metaclass** tests that comment is the only form element in meta fields
    * **xx** xxx
    * **xx** xxx
    * **xx** xxx





### Automatic testers and validators

#### PEP8 validator
The app.py code was copied into the validator and passed without error

#### Lighthouse
I used lighthouse on both the desktop and mobile versions of the site. The desktop performance score was 100% (94% for mobile).


### Testing against the user Stories
#### As a first time user:

* easily register and recover my password
    * Django has an allauth intergration that makes user accounts easy and secure to manage. The site takes advantage of the 2-step verification process to make sure that the email address is valid. Logging in, out and changing passwords is easily done via the top menu and all sensitive data is help in the secure postgres DB

* donate to the company
    * I have used Stripe to bring card payments directly into the app. Every production and on various pages on the app has links to donate. Productions have three options, £5, £10 and £20. Once clicked, the user only needs to fill in a simple form (which is auto filled for logged in users), enter the car details and click "donate". If they are a logged in user, their donation will be linked to their account so they can keep track of donations. The donations will also feature on the production (if one has been selected) to show recent donations and a sum total. The Stripe intergration will also email the donator once the funds have been cleared.

* see this years productions
    * Productions on the home page and productions page are ordered by date. They will also show the current productions and mark any dead shows with a clear message. 

* see who is in the cast or creatives for a production
    * Every production has a number of fields to link to personal profiles. These are cast, creative, staff and composer. Each one will have their photos in the section and a link to their profile on the app. Inside their profile, you can also view all productions they have been part of, so you can track thru their history.

* watch videos of the production or backstage
    * Videos are currently taken from youTube and shown direct on the production page. In the future I hope to host the videos to put some behind a possible paywall.

* like the productions I want to keep track of
    * Every production can be liked by a logged in user. There is a box on the top of the production that turns this on and off. Also, on the profile page, there is a list of productions so you can quickly see which ones you've chosen.

* browse photos from the live performance and backstage
    * photos form a carasel on the productions page. This is responsive and shows more detail and the screen gets bigger.

* leave a review about a production
    * Every logged in user can post one review toward a production. From the production page, they can also delete their own review and click edit to be taken to another page to edit it directly.


#### As the site owner, I want to:
* build an online audience for my productions
    * comments and likes mean the user may choose to create an account. This will then give accurate email addresses for marketing. Not putting good content behind a uwer account / payment will help build an audience that may at the start be just casual.

* receive secure donations using STRIPE
    * Stripe payments have been added throughout the app, the payment page is quick and simple to drive more donations

* make the app easy to navigate and mobile friendly
    * The app was made in a "mobile first" way. That means it's well suited for the vast population that will visit the site.
* create a single app for alll the production news and media




### Manual Testing
I have preformed manual tests on a number of browsers and devices to cover most scenarios and feel assured the website works as intended for all visitors. This included using google dev tools to simulate different screen sizes and using a real android and apple phone and family to act as first time visitors. In total:

* The app was tested using Chrome, Edge and Safari browsers.
* The app was tested on a number of devices such as Desktop, Laptop, iPhone and android.
* The app was tested extensively to ensure all links, styles and events worked as expected


### Known Bugs

#### Resolved
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
* making user comment unique to production and user. See comment model and here: https://stackoverflow.com/questions/2201598/how-to-define-two-fields-unique-as-couple
* **xxxx** xxxxxx



#### Un-Resolved

* **xxxxx** xxxxx
