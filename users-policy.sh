#!/bin/bash

USERS=$(aws iam list-users --query Users[].[UserName] | jq -r .[] | jq -r .[])

for USER in $USERS
do
    echo "Collect Policies for user: $USER"
    echo "USER - $USER" >> res.txt
    POLICY_NAMES=$(aws iam list-attached-user-policies --user-name $USER --query AttachedPolicies[].[PolicyName] | jq -r .[] | jq -r .[])
    POLICY_ARNS=$(aws iam list-attached-user-policies --user-name $USER --query AttachedPolicies[].[PolicyArn] | jq -r .[] | jq -r .[])


    POLICY_NAME_A=($POLICY_NAMES)
    POLICY_ARN_A=($POLICY_ARNS)

    x=${#POLICY_NAME_A[@]}

    echo "Count of policies is $x"
    #for POLICY_NAME in $POLICY_NAMES
    for ((i = 0; i < $x; i++))
    do
        echo "$i-policy"
        echo "PolicyName and ARN for $USER:"
        echo ${POLICY_NAME_A[i]}
        echo "Policy name - ${POLICY_NAME_A[i]}" >> res.txt
        echo ${POLICY_ARN_A[i]}
        VERSION=$(aws iam list-policies | jq '.Policies[] | select(.PolicyName=="'${POLICY_NAME_A[i]}'")' | jq -r '{DefaultVersionId}' | jq -r .[])
        aws iam get-policy-version --version-id $VERSION --policy-arn ${POLICY_ARN_A[i]} >> res.txt
        echo "Done policy $i"
        echo "___________"
    done

    echo "Done fot User: $USER"
    echo "##################################################"
    echo "##################################################" >> res.txt

done
