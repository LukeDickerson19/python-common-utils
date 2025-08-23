
echo '---------------------------- BUILD SCRIPT STARTS HERE ---------------------------'

ec2_ip_address=10.176.28.21 # PROD ec2: priv-dev-ccpa-vendordelete
service_account=svc-firebug
ssh_key=$1
repo_name=regression-tester

# create tmp dir on ec2 instance
ssh -tt -i $ssh_key $service_account@$ec2_ip_address "rm -rf tmp-$repo_name; mkdir -p tmp-$repo_name/$repo_name"
ssh -tt -i $ssh_key $service_account@$ec2_ip_address "pwd; ls"

pwd
ls

# copy the updated code into the tmp dir
rsync -vrzh --exclude=.git/ $PWD/ccpa-analytics/ccpa-batch-process/regression-tester/ $service_account@$ec2_ip_address:/home/$service_account/tmp-$repo_name/$repo_name/
ssh -tt -i $ssh_key $service_account@$ec2_ip_address "cd tmp-$repo_name/$repo_name; pwd; ls"

# run ./local_cicd_setup.sh on the ec2 instance
ssh -tt -i $ssh_key $service_account@$ec2_ip_address ". /home/$service_account/tmp-$repo_name/$repo_name/deploy/build_deploy.sh"

echo '---------------------------- BUILD SCRIPT ENDS HERE -----------------------------'


