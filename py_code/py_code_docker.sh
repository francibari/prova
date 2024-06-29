docker build -t py_image_project_sc .

docker run -it --rm  -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix  py_image_project_sc