#!/bin/bash

aws ec2 describe-subnets --profile=TEST --region eu-central-1 | jq -r '.Subnets[] | {CidrBlock}' > test_tmp
aws ec2 describe-subnets --profile=STAGE --region eu-central-1 | jq -r '.Subnets[] | {CidrBlock}' > stage_tmp
sed -i -e 's/\.30\./\.00\./g' test_tmp
sed -i -e 's/\.25\./\.00\./g' stage_tmp
sort test_tmp  > test-net
sort stage_tmp > stage-net
rm test_tmp; rm stage_tmp
sed -i -e 's/}//g' test-net
sed -i -e 's/{//g' test-net
sed -i -e 's/}//g' stage-net
sed -i -e 's/{//g' stage-net
sed -i '/^$/d' test-net
sed -i '/^$/d' stage-net
colordiff test-net stage-net
