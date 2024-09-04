---
title: "Automating DNS Management with GitLab CI/CD"
author: Kannan Ponnusamy
date: 2024-09-06
github_issue_number: 2076
description: Managing DNS records across multiple domains using GitLab CI/CD features and its Terraform HTTP backends
featured:
  image_url: /blog/2024/09/automating-dns-management-with-gitlab-ci-cd/robot-manufacturing-floor.webp
tags:
- terraform
- git
- cloud
- devops
---

![Several robotic arms sit perched over mechanical tracks in a factory, ready to do some type of assembly.](/blog/2024/09/automating-dns-management-with-gitlab-ci-cd/robot-manufacturing-floor.webp)<br>
[Photo](https://unsplash.com/photos/a-factory-filled-with-lots-of-orange-machines-8gr6bObQLOI) by [Simon Kadula](https://unsplash.com/@simonkadula)

At End Point, managing DNS records across multiple domains has historically been a manual task. This blog post details our journey from manual processes to an automated workflow using GitLab CI/CD.

### Our Initial Approach

With multiple domains and frequent updates necessary to manage the servers, manual handling of DNS changes became a bottleneck. Initially, our process looked like this:

- Make changes to the OpenTofu configuration files
- Create a merge request (MR) in GitLab
- They would run `tofu plan` manually and paste the plan output into the MR for review
- A coworker would review the MR and approve the changes
- Once merged, the engineer would manually run `tofu apply` to implement the changes

While this process worked, automating it could enhance our productivity and minimize errors, integrating our DNS management directly into our CI/CD pipeline.

### The Solution: Automating with GitLab CI/CD

- Change Submission: Engineers make changes to the OpenTofu files and submit a merge request
- Plan Creation: A GitLab CI/CD job automatically generates an OpenTofu plan when changes are proposed
- Review Process: A coworker reviews the automatically generated plan in the MR
- Applying Changes: Once approved and merged, another CI/CD job automatically runs `tofu apply` to implement the changes

### Implementation Details:

#### 1. `.gitlab-ci.yaml`

If you are doing this on a self-hosted GitLab instance you would need to import the repo to your hosted GitLab workspace and use it there.

We divided our GitLab CI/CD pipelines into three main stages:

1. Validation: Where we check if everything looks right
2. Planning: Where we create a plan to show the changes
3. Deployment: Where the changes get applied once everything is approved

It's important to note that our CI/CD pipeline runs on a dedicated worker. This means only this worker has access to the secret keys needed for DNS management. By isolating these credentials to a single, controlled environment, we significantly reduce the risk of unauthorized access or accidental exposure of sensitive data.

```yaml
include:
  - component: gitlab.com/components/opentofu/job-templates@main
    inputs:
      version: 0.24.0
      opentofu_version: 1.6.2
      auto_apply: false

before_script:
  - source /home/gitlab-runner/.tofu.env

stages: [ validate, build, deploy]

fmt-example.com:
  extends: [ .opentofu:fmt ]
  variables:
    TF_ROOT: "example.com"
    TF_STATE_NAME: "example_com"
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
      changes:
        - example.com/*
    - if: '$CI_COMMIT_BRANCH == "main"'
      changes:
        - example.com/*

validate-example.com:
  extends: [ .opentofu:validate ]
  variables:
    TF_ROOT: "example.com"
    TF_STATE_NAME: "example_com"
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
      changes:
        - example.com/*
    - if: '$CI_COMMIT_BRANCH == "main"'
      changes:
        - example.com/*

plan-example.com:
  extends: [ .opentofu:plan ]
  variables:
    TF_ROOT: "example.com"
    TF_STATE_NAME: "example_com"
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
      changes:
        - example.com/*
    - if: '$CI_COMMIT_BRANCH == "main"'
      changes:
        - example.com/*
  after_script:
    - source /home/gitlab-runner/.tofu.env
    - ./gitlab-comment-tofu-log.sh $TF_ROOT/plan_output.txt

apply-example.com:
  extends: [ .opentofu:apply ]
  variables:
    TF_ROOT: "example.com"
    TF_STATE_NAME: "example_com"
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
      changes:
        - example.com/*
  after_script:
    - source /home/gitlab-runner/.tofu.env
    - ./gitlab-comment-tofu-log.sh $TF_ROOT/apply_output.txt
```

#### 2. Posting OpenTofu plan/apply logs as merge request comments

To facilitate code reviews, we created a script (`gitlab-comment-tofu-log.sh`) that automatically formats and posts the OpenTofu plan and apply logs as comments on merge requests. This ensures that reviewers can easily understand the changes before approving them.

Here is the script:

```bash
#!/bin/bash

set -e

echo "GitLab MR Comment Script Starts"

if [ $# -eq 0 ]; then
    echo "Error: No output file path provided"
    echo "Usage: $0 <path_to_output_file>"
    exit 1
fi

output_file="$1"
echo "Using output file: $output_file"

echo "Checking environment variables"
if [ -z "$GITLAB_API_TOKEN" ]; then
    echo "Error: GITLAB_API_TOKEN is not set"
    exit 1
fi

if [ -z "$CI_PROJECT_ID" ]; then
    echo "Error: CI_PROJECT_ID is not set"
    exit 1
fi

if [ -n "$CI_MERGE_REQUEST_IID" ]; then
    echo "Using CI_MERGE_REQUEST_IID: $CI_MERGE_REQUEST_IID"
else
    echo "CI_MERGE_REQUEST_IID not set, fetching from API"
    CURRENT_COMMIT_SHA=$(git rev-parse HEAD)
    echo "Current commit SHA: $CURRENT_COMMIT_SHA"

    MR_INFO=$(curl --silent --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" \
        "https://<link_to_self_hosted_gitlab>/api/v4/projects/$CI_PROJECT_ID/repository/commits/$CURRENT_COMMIT_SHA/merge_requests")

    if [ "$(echo $MR_INFO | jq '. | length')" -eq 0 ]; then
        echo "Error: No merge request found for this commit" >&2
        exit 1
    fi

    CI_MERGE_REQUEST_IID=$(echo $MR_INFO | jq '.[0].iid')
    echo "Found Merge Request IID: $CI_MERGE_REQUEST_IID"
fi

echo "Reading output file: $output_file"
if [ ! -f "$output_file" ]; then
    echo "Error: File $output_file not found"
    exit 1
fi

file_name=$(basename "$output_file")
if [[ "$file_name" == plan_* ]]; then
    heading="<br>Plan log for $TF_ROOT"
    output=$(awk '/OpenTofu used the selected providers/,0' "$output_file")
elif [[ "$file_name" == apply_* ]]; then
    heading="<br>Apply log for $TF_ROOT"
    output=$(awk '/OpenTofu has been successfully initialized/,0' "$output_file")
else
    heading="<br>Tofu Output for $TF_ROOT"
fi

echo "Filtered output read. Length: ${#output} characters"

echo "Cleaning and formatting output"
cleaned_output=$(echo -e "$output" | sed -e 's/\x1b\[[0-9;]*m//g' \
    -e 's/\\u001b\[[0-9;]*m//g' \
    -e 's/\\n/\n/g' \
    -e 's/\\"//g' \
    -e 's/^"//g' \
    -e 's/"$//g')
echo "Cleaned output. Length: ${#cleaned_output} characters"

# Format the output with heading and code block
formatted_output="$(printf '## %s\n\n```\n%s\n```' "$heading" "$cleaned_output")"
echo "Formatted output. Length: ${#formatted_output} characters"

echo "Posting comment to GitLab MR"
response=$(curl --silent --show-error --fail \
     --request POST \
     --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" \
     --header "Content-Type: application/json" \
     --data "$(jq -n --arg body "$formatted_output" '{"body": $body}')" \
     "https://code.self_hosted_gitlab.com/api/v4/projects/$CI_PROJECT_ID/merge_requests/$CI_MERGE_REQUEST_IID/notes")


if [ $? -eq 0 ]; then
    echo "Comment successfully posted to GitLab MR"
else
    echo "Error: Failed to post comment to GitLab MR. Response: $response"
    exit 1
fi

echo "Script completed successfully"
```

Here is the `tofu plan` output comment:

![The screenshot shows a plan log entry in merge request. The log entry reports actions by OpenTofu, indicating it used selected providers to generate an execution plan.](/blog/2024/09/automating-dns-management-with-gitlab-ci-cd/plan.webp)

Here is the `tofu apply` output comment:

![The screenshot shows a tofu apply log entry in merge request. The log entry reports apply action by OpenTofu, indicating it used selected providers to apply the above generated plan.](/blog/2024/09/automating-dns-management-with-gitlab-ci-cd/apply.webp)


#### 3. Migrating to GitLab’s Remote HTTP Backend

Transitioning your local Tofu state to a remote backend hosted by GitLab can streamline state management and enhance security. Follow these straightforward steps to achieve this.

1. First, set up the necessary environment variables with your specific details:

    ```bash
    export TF_STATE_NAME="example_net"
    export TF_HTTP_ADDRESS="https://<link_to_GitLab_instance>>/api/v4/projects/460/terraform/state/$TF_STATE_NAME"
    export TF_HTTP_USERNAME="<create_a_user>"
    export TF_HTTP_PASSWORD="<create_a_password>"
    ```

2. Initialize the remote backend with Tofu, specifying your new backend configuration:

    ```bash
    tofu init -migrate-state \
      -backend-config="address=$TF_HTTP_ADDRESS" \
      -backend-config="username=$TF_HTTP_USERNAME" \
      -backend-config="password=$TF_HTTP_PASSWORD"
    ```

3. Verify the migration by running:

    ```plain
    tofu plan
    ```

After these steps, your Tofu environment will be fully integrated with GitLab’s remote HTTP backend, with state management and enhanced collaboration and security.

Automation of our DNS management with GitLab CI/CD and OpenTofu has transformed our operations, making them more efficient, error-resistant, and secure. We encourage other teams to explore similar automation strategies to enhance their infrastructure management processes.
