---
author: "Indra Pranesh Palanisamy"
title: "Identifying Vulnerabilities in Code Using Horusec"
featured:
  image_url: /blog/2023/03/identifying-vulnerabilities-using-horusec/pexels-indra-pranesh-palanisamy-15837790.webp
description: "Horusec is an open-source tool for identifying security vulnerabilities in code that can help developers improve the security of their applications by detecting potential threats and suggesting corrections. Learn how to integrate Horusec into your development process and enhance your code's security."
github_issue_number: 1949
date: 2023-03-28
tags:
- security
- epitrax
---

![The sun has just started to rise over the horizon. A group of fishermen can be seen pushing their small wooden boats into the water, preparing to start their day's work. The air is still cool and quiet, with only the sound of waves gently lapping against the shore as the fishermen row out into the open sea, ready to begin their early morning fishing expedition.](/blog/2023/03/identifying-vulnerabilities-using-horusec/pexels-indra-pranesh-palanisamy-15837790.webp)

<!-- Photo by Indra Pranesh Palanisamy, 2022 -->

[Horusec](https://horusec.io/site/) is an open source tool which, by orchestrating other security tools, identifies security flaws and vulnerabilities in source code. It puts all the possible vulnerabilities it finds into a database for analysis.

Currently, Horusec supports C#, Java, Kotlin, Python, Ruby, Go, JavaScript, TypeScript, PHP, Swift, C, Dart, Elixir, shell, Terraform, Kubernetes, nginx, HTML, and JSON. You can see an up-to-date list of [supported languages](https://docs.horusec.io/docs/cli/analysis-tools/overview/#available-programming-languages-and-tools) in Horusec's docs.

It can also be integrated with CI/CD to execute the scan every time a developer creates a pull request or merge request.

### Horusec CLI Installation

**Requirements**: Docker, Git.

The easiest installation method listed in the docs is `curl`ing Horusec's install script and piping it into `bash`:

```plain
curl -fsSL https://raw.githubusercontent.com/ZupIT/horusec/main/deployments/scripts/install.sh | bash -s latest
```

Be aware that there is risk to piping unseen commands into the shell like this: It can lead to unintended consequences and it is a bad security practice.

If a user blindly pipes the output of a website response to be run by a shell without fully understanding what each command does, they may inadvertently execute malicious code or perform actions that could compromise the security of the system.

To mitigate these risks, one solution is to use a virtual machine specifically set up for code scanning. This virtual machine should have no production data, no secret keys, and no other sensitive information. It should be used only for the purpose of scanning source code and nothing else.

To instead download an executable directly, as well as for instructions for different platforms, see the [installation docs](https://docs.horusec.io/docs/cli/installation/).

### VS Code Extension

Horusec has a [VS Code extension](https://docs.horusec.io/docs/extensions/visual-studio-code/) which is helpful for making complete code analysis with a single click.

![Screenshot of Horusec VS Code extension](/blog/2023/03/identifying-vulnerabilities-using-horusec/horusec-vscode.webp)

### Usage

Navigate to the application directory and run the `generate` command to make a configuration file called `horusec-config.json` which has a set of [customisations](https://docs.horusec.io/docs/cli/commands-and-flags/#global-flags):

```plain
cd /path/to/project
horusec generate
```

The `start` command executes the code scan throughout the repository, searching for possible vulnerabilities:

```plain
horusec start -p . --output-format=json --json-output-file=<filename>.json
```

All the detected vulnerabilities are stored in the named JSON output file.

### Classification of Vulnerabilities

Horusec may identify (or, as the docs say, accuse) possible vulnerabilities that aren't vulnerabilities at all. Possible vulnerabilites need to be classified to sort out those that are wrong.

Here are the classification types from [Horusec's docs](https://docs.horusec.io/docs/tutorials/how-to-classify-a-vulnerability/#classification-types):

- **False positive:** Vulnerability found is wrong, because it is accused in a test file or it is not a vulnerability in fact, and is safe code.
- **Accepted Risk:** Vulnerability that was accused, but at the moment, you don't have the option to correct it, so it is classified as an accepted risk to not raise alarms in future runs.
- **Corrected:** Vulnerability that doesn't exist and can be considered as corrected.
- **Vulnerability:** A possible security problem found and accused by the analysis.

The hashes to be ignored can be added to the configuration file, `horusec-config.json`:

```json
{
  ...
  "horusecCliFalsePositiveHashes": [
      "f9e5abe187ad4246daa4e9113e0a11a175347e793fbc40acd7663df67b2f89d2",
      "878c35116d043311403a0a2e8a64f2c8d00479a1c23373dcd50372ff35e123c8"
  ],
  "horusecCliRiskAcceptHashes": [
      "5c9af42834ca77233a0e7afc98df317fb0e6041ea69a109754f278331039f844",
      "b494003277bcd7792390f032ba39e9a860da66ddb1ccfcd8a581978eab744561"
  ],
  ...
}
```

#### Ignore Files

To entirely ignore a file or certain paths under the directory, add the paths to the configuration file:

```json
{
  ...
  "horusecCliFilesOrPathsToIgnore": [
      "**/tmp/**",
      "**/.vscode/**"
  ],
  ...
}
```

### Code Scanning in EpiTrax

The use of a code scan tool has become an integral part of our work with the EpiTrax disease surveillance system for public health.

By integrating Horusec into our software development process, we have been able to identify potential security vulnerabilities, code quality issues, and other problems before they can cause any significant harm.

Moreover, it has helped us reduce the overall cost and time associated with bug-fixing and maintenance tasks, making our projects more efficient and effective. By automating the scanning process, we can identify problems quickly and accurately, allowing us to prioritize and address the most critical ones first.

By leveraging the power of code scans, we can ensure that our code is of the highest quality, and our projects are as secure and reliable as possible.

<br>

_Special thanks to my colleagues Kürşat Kutlu Aydemir and Edgar Mlowe for their insights and feedback on this blog post._
