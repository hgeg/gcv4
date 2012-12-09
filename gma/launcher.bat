:launch
python manage.py runserver 127.0.0.1:%cname%
pause > nul

:purge
del gma_database
python manage.py syncdb