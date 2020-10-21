# Manitoba COVID-19 data repo
This app runs on Heroku and simply gathers up the Government of Manitoba dashboard data each night at 11 pm (Winnipeg time) and then pushes the new JSONs files to remote in the Github repository.

Note that a JSONs for October 4th and October 10th are missing due to an error a while back.

Couldn't figure out how to get Heroku's scheduler to work without payment and so.... this runs on a 24-hour while loop. I'll address this when/if it the script breaks.
¯\\_(ツ)_/¯

