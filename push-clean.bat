@echo off
setlocal
cd /d "C:\Users\huawei\hh-max-bot"
set GIT_AUTHOR_NAME=Ogulgerek Dilekova
set GIT_AUTHOR_EMAIL=ogulgerekdilekova0-lgtm@users.noreply.github.com
set GIT_COMMITTER_NAME=Ogulgerek Dilekova
set GIT_COMMITTER_EMAIL=ogulgerekdilekova0-lgtm@users.noreply.github.com
git add -A
for /f %%i in ('git write-tree') do set TREE=%%i
for /f %%i in ('git rev-parse HEAD') do set PARENT=%%i
for /f %%i in ('git commit-tree %TREE% -p %PARENT% -m "clean up project files"') do set COMMIT=%%i
git update-ref refs/heads/main %COMMIT%
git reset --hard main
git push origin main
