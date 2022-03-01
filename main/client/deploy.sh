#yarn build;
scp -r /Users/huanchen/Project/ch/keepgoing-electron-app/dist/html/ root@chome:/usr/share/nginx
ssh root@chome "cd /usr/share/nginx; rm -rf auto-script-admin;mv html auto-script-admin"
