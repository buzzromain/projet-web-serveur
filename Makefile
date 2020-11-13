git:
	git checkout master; git add -A .; git commit -a -m "$m"; git push --set-upstream origin master;
git-pull:
	git pull origin master; git pull origin PRODUCTION;
deploy:
	git checkout PRODUCTION; git merge master; git push --set-upstream origin PRODUCTION; git checkout master;
init-dev:
	virtualenv venv; source venv/bin/activate; pip3 install -r requirements.txt;
run-dev:
	export FLASK_ENV=development; export FLASK_APP=buzzromainblog; pip3 install -e .; flask run;
