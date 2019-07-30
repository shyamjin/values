title Set Enviroment Variables for DPM

setx DEV_MODE "False"
setx DOCKER_IND "False"
setx DPM_BUILD_NUMBER "1"
setx DPM_DB_HOST "localhost"
setx DPM_DB_PORT "27017"
setx DPM_PIPELINE_NUMBER "1"
setx DPM_PORT "8000"
setx DPM_TYPE "dpm_master"
setx DPM_VERSION "3.2.3_hf4"
setx MONGO_SECURED "False"
setx TEST_HOST "1.1.1.1"
setx BUILD_DATE "01012017"
setx USE_SSL "false"

echo off

echo All enviroment variables are updated .  you might need to restart the cmd session
pause