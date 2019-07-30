file_name=$1
echo ${file_name}
zip -r ${file_name} * -x build.sh
echo "The build is completed"

