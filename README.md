# Cybourse
An educational platform, with a built-in blog, quiz system, ranking system, and public profiles
**Currently I am doing a complete change of the project, so put it into your watchlist so that you don't miss out on all the awesome features coming soon**

## Technology Used
This site is built using:
- Django 5
- Django Rest Framework 3
- VueJS

## Features
- Home page with a featured section!
- Quiz system with options to show quizzes to some students, hide the final result, and allow only one or more attempts
- User Profiles with rank, solved quizzes, and social links
- Ranking System
- The ability for users to propose new articles which if approved by administrators will be credited to the user
- Save articles for later
- A lot more to come!

## Running the site

Clone the repo locally:

`git clone https://github.com/mohabgabber/cybourse.git && cd cybourse`

Create a virtual environment:

`pip install virtualenv && virtualenv env`

Install requirements

`pip install -r requirements.txt`

Create a .env file in the root directory of the repository and add the values for the following variables:
```
secret_key=INSERTVALUE // The secret key for the site deployment
static_root=INSERTVALUE // The root directory for static files
media_root=INSERTVALUE // The root directory for media files
emuser=INSERTVALUE // Email user (the email itself) example@example.tld
empass=INSERTVALUE // The email password
emfrommail=INSERTVALUE // The "from" field when sending emails
tinymce=INSERTVALUE // Tinymce API token is required, acquire one from here: https://www.tiny.cloud/
recaptchapub=INSERTVALUE // Google Recaptcha Publich Key
recaptchapri=INSERTVALUE // Google Recaptcha Private Key
```



## Contributing
To contribute, fork the repository and submit a pull request <3
Just so you know, all contributions and enhancements are welcome.

## License
    Cybourse, is an open-source educational platform, with tons of features!
    Copyright (C) 2024  Mohab Gabber

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>
