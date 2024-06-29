docker build -t root_image_project_sc .

docker run -it --rm  -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix  root_image_project_sc