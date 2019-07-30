#!/bin/ksh

env_url=${1}

script_dir="$( cd "$(dirname "$0")" ; pwd -P )"

mail_list=${MAIL_LIST:-mpopescu@admocs.com}

echo Email Report will be sent to : $MAIL_LIST

if [[ ${env_url} = "" ]];then
    echo "FAILURE: ENV_URL is not defined"
    exit 1
fi

sed -i "s|##ENV_URL##|${env_url}|" ${script_dir}/Profiles/gitpipeline.glbl

curl ${env_url} >/dev/null 2>/dev/null

curl_returncode=$?

if [[ ${curl_returncode} -ne 0 ]];then
    echo "Site is not available, curl reuturned ${curl_returncode}"
    exit 1
fi

rm -rf .project 2>/dev/null

katalon_opts='-browserType="Chrome (headless)" -retry=0 -statusDelay=15 -testSuitePath="Test Suites/BasicSanity" -executionProfile="gitpipeline"'
report_dir=${script_dir}/Reports/run_$(date '+%Y%m%d_%H%M%S')
docker run --rm -v ${script_dir}:/katalon/katalon/source:ro -v ${report_dir}:/katalon/katalon/report -e KATALON_OPTS="$katalon_opts" katalonstudio/katalon:1.2.0
grep FAILED $report_dir/report.csv 1>/dev/null 2>/dev/null
if [[ $? -eq 0 ]];then
  echo "Katalon test faliure report" | mailx -r DeploymentManager-DoNotReply@amdocs.com -s "Katalon test faliure report" -a $report_dir/report.html ${mail_list}
fi
