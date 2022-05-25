# Future
* twitter intergration to show tweets with hashtag


# info
* heroku run rails db:migrate
* insall heroku cli "curl https://cli-assets.heroku.com/install.sh | sh"
* To update the current terminal session with the latest set of persistent environment variables, use: eval $(gp env -e)
* "heroku run python3 manage.py migrate"
* RUN in bash on heroku after git push - or in gitpod "heroku run bash"
    * python3 manage.py migrate works zero then run migrate



Make sure your manage.py file is connected to your mysql database
Use this command to backup your current database and load it into a db.json file:
python3 manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json
Connect your manage.py file to your postgres database
Then use this command to load your data from the db.json file into postgres:
python3 manage.py loaddata db.json