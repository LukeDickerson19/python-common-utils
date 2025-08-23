


echo '----------------------- LOCAL CICD SCRIPT STARTS HERE ---------------------------'

service_account=svc-firebug
repo_name=regression-tester
tmp_home=/home/$service_account/tmp-$repo_name/$repo_name

# install dependencies in a new virtual environment
cd $tmp_home
virt_env_name=virt_env
virtualenv -p python3 $virt_env_name
. $tmp_home/$virt_env_name/bin/activate
pip install --no-cache -r deploy/requirements.txt

# setup for tests
cd $tmp_home/
rm -rf logs
mkdir logs
touch logs/test_log.txt

# run tests
cd $tmp_home/tests
coverage run validator_unittests.py
cat results.txt
python get_test_results.py
# $? =  is the exit status of the most recently-executed command; by convention, 0 means success and anything else indicates failure.
if [ $? -eq 0 ]
then
    echo "All tests Passed. Pushing updated code to EC2 ..."
    deactivate # deactivate virtual environment
    rm $tmp_home/logs/test_log.txt # remove test log
    # # virtual enironments are by default not relocateable,
    # # so delete this one and make a new one in REPO_HOME
    # rm -rf $tmp_home/$virt_env_name/
    # repo_home=/home/$service_account/$repo_name
    # rm -rf $repo_home # delete old repo
    # mv $tmp_home $repo_home # move new repo to old repo's location
    # cd $repo_home
    # # create new virtual environment in new repo
    # virtualenv -p python3 $virt_env_name
    # . $repo_home/$virt_env_name/bin/activate
    # pip install --no-cache -r deploy/requirements.txt
    # deactivate

else
    echo "Not all tests Passed. Not pushing updated code to EC2."
    deactivate # deactivate virtual environment
fi
rm -rf /home/$service_account/tmp-$repo_name/

echo '----------------------- LOCAL CICD SCRIPT ENDS HERE -----------------------------'

