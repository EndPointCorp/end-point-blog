---
author: "Indra Pranesh Palanisamy, Kürşat Kutlu Aydemir and Edgar Mlowe"
title: "Identifying Vulnerabilities in Code using Horusec"
featured:
  image_url: /blog/2023/03/identifying-vulnerabilities-using-horusec/pexels-indra-pranesh-palanisamy-15837790.webp
description: "In this blog post, we explore how Horusec, an open-source tool for identifying security vulnerabilities in code, can help developers improve the security of their applications by detecting potential threats and providing actionable insights. Learn how to integrate Horusec into your development process and enhance your code's security."
date: 2023-03-07
tags:
- code-scan
- security
- vulnerability
---

![The sun has just started to rise over the horizon, casting a warm orange glow over the calm sea. A group of fishermen can be seen pushing their small wooden boats into the water, preparing to start their day's work. The air is still cool and quiet, with only the sound of waves gently lapping against the shore as the fishermen row out into the open sea, ready to begin their early morning fishing expedition.](/blog/2023/03/identifying-vulnerabilities-using-horusec/pexels-indra-pranesh-palanisamy-15837790.webp)

<!-- Photo by Pranesh, 2022 -->

## Horusec

[Horusec](https://horusec.io/site/) is an open source tool that orchestrates other security tools and identifies security flaws or vulnerabilities in projects during the development process and puts all results in a database for analysis and generation of metrics.

Currently, Horusec supports - C#, Java, Kotlin, Python, Ruby, Golang, Terraform, Javascript, Typescript, Kubernetes, PHP, C, HTML, JSON, Dart, Elixir, Shell, Nginx, Swift.

It can also be integrated with CI/CD to execute the scan every time a developer raises a merge request.

### Horusec CLI Installation

#### Requirements

- Docker
- Git

```
curl -fsSL https://raw.githubusercontent.com/ZupIT/horusec/main/deployments/scripts/install.sh | bash -s latest
```

### VS Code Extension

Horusec has a [VS code extension](https://docs.horusec.io/docs/extensions/visual-studio-code/) which is super helpful making complete code analysis with a single click.

### Usage

Navigate to application directory:

```
cd /path/to/project
```

#### Generate

This command generates a configuration file called `horusec-config.json` which has a set of [customisations](https://docs.horusec.io/docs/cli/commands-and-flags/#global-flags).

```
horusec generate
```

#### Start

The start command executes the code scan throughout the repository searching possible vulnerabilities. All the detected vulnerabilities are stored in the outfile JSON file.

```
horusec start -p . --output-format=json --json-output-file=<filename>.json
```

### Classification of Vulnerabilities

Horusec may identify vulnerabilities that are not even one. Vulnerabilities have to be classified to avoid some unwanted ones.

##### False positive

Vulnerability found is wrong, because it is accused in a test file or it is not a vulnerability in fact, and is a safe code.

##### Accepted Risk

Vulnerability that was accused, but at the moment, you don't have the option to correct it, so it is classified as an accepted risk to move forward in the daily process.

##### Corrected

Vulnerability that doesn't exist and can be considered as corrected.

##### Vulnerability

A possible security failure found and accused by the analysis.

The hashes to be ignored classified can be added to the configuration file horusec-config.json

```
"horusecCliFalsePositiveHashes": [
    HASH1, HASH2
],
"horusecCliRiskAcceptHashes": [
    HASH1, HASH2
],
```

#### Ignore files

To ignore a file or certain paths under the directory, add the paths to the configuration file,

```
"horusecCliFilesOrPathsToIgnore": [
    PATH1, PATH2
]
```

### Code Scan in EpiTrax

The use of a code scan tool has become an integral part of EpiTrax. By integrating Horusec into our software development process, we have been able to identify potential security vulnerabilities, code quality issues, and other problems before they can cause any significant harm.

Moreover, it has helped us reduce the overall cost and time associated with bug-fixing and maintenance tasks, making our projects more efficient and effective. By automating the scanning process, we can identify issues quickly and accurately, allowing us to prioritize and address the most critical issues first.

By leveraging the power of code scans, we can ensure that our code is of the highest quality, and our projects are as secure and reliable as possible.