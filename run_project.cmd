@echo off
echo Running Django Project...
call venv1\Scripts\activate
cd Splitt_bills
python manage.py runserver

pause