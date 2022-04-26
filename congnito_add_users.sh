#!/bin/bash

for i in 02 03 04 05 06 07 08 09 10
do aws cognito-idp admin-create-user --user-pool-id eu-central-1_1111111 \
	        --username T"$i"RC001 --temporary-password Qwerty123! \
		--user-attributes Name=custom:target_sub_id,Value="T"$i"RC001" \
		Name=custom:target_comp_id,Value="T$i" Name=custom:username,Value="T"$i"RC001" \
		Name=custom:password,Value="Qwerty12" --region eu-central-1 --profile TEST

aws cognito-idp admin-set-user-password --user-pool-id eu-central-1_1111111 \
	        --username T"$i"RC001 --password Password123 --permanent --region eu-central-1 --profile TEST

done
