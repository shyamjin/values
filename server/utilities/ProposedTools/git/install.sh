export SOURCE_DIR=`pwd`
export tool_name=TOOLNAME
if [ ! -d ~/vpbin ]
        then
        mkdir ~/vpbin
fi
if [ ! -d ~/vpbin/$tool_name ]
        then
        mkdir ~/vpbin/$tool_name
fi
export target_dir=~/vpbin/$tool_name
cp -rf * $target_dir
chmod -R 777 $target_dir

## Please add your installation steps here


rm -rf $target_dir

echo "Deployment was Success !"

