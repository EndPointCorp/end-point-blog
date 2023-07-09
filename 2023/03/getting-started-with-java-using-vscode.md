---
author: "Trevor Slocum"
title: "Getting started with Java development using Visual Studio Code"
description: "A guide on how to install the Extension Pack for Java in Visual Studio Code."
date: 2023-03-17
tags:
- programming
- java
- vscode
github_issue_number: 1946
---

![A fall sunset above an open plain: The yellow sun sets behind snowy mountains, casting orange glow on the left side of the sky, while the right side of the sky is dominated by dark storm clouds rising up and to the right in a dramatic diagonal. From the edge of the mountain towards the viewer spans a large brown plain. On it is a small shack and in the center of the image is a small, run-down tractor.](/blog/2023/03/getting-started-with-java-using-vscode/farm-sunset.webp)<br>
Photo by Garrett Skinner, 2022

Visual Studio Code is a free source-code editor available for Windows, macOS, and Linux. While it includes a lot of features out of the box, you will likely need to extend its functionality to suit your purpose for using it. There are many extensions available, each providing their own set of features and functions.

In this guide we will install the [Extension Pack for Java](https://marketplace.visualstudio.com/items?itemName=vscjava.vscode-java-pack), which is a bundle of several extensions. Installing this extension pack will add the following features to Visual Studio Code:

- **Java language support** for parsing and highlighting our code
- **Java test runner** for testing our code
- **Java debugger** for debugging our code
- **Java project manager** for managing resources related to our code
- **Maven support** for building and packaging our code

Note: This guide assumes you have already installed a Java Development Kit. If you haven't done that yet, [OpenJDK](https://openjdk.org) is a great option.

### Step 1: Install Visual Studio Code

If you haven't yet, [download Visual Studio Code](https://code.visualstudio.com/download) and install it. If you need more help with this step, review the installation instructions linked on [this page](https://code.visualstudio.com/docs/setup/setup-overview#_cross-platform). Click the link that applies to your operating system to access the installation instructions.

### Step 2: Install the extension pack

Open Visual Studio Code and click on the extensions icon in the left sidebar, which looks like this:

![Three boxes stacked in an L shape, with a fourth box above and to the right of the empty space.](/blog/2023/03/getting-started-with-java-using-vscode/vscode-extensions-icon.png)

This will take you to the extensions marketplace. Type "Extension Pack for Java" into the search bar and press enter. The extension we are looking for is authored by Microsoft. Once you find the extension pack in this list, click the **Install** button.

### Step 3: Use the extension pack

Once the installation is complete, a "Get Started with Java Development" screen is displayed. The first item on this screen is "Get your runtime ready" with an "Install JDK" button. We already have a JDK installed, so we can skip this. The remaining items on the screen are helpful to review, as they give a brief overview of the features we have just added to our editor.

To ensure our JDK and extension pack are working together correctly, click **File > New file...**. You will be prompted to choose a file type. Enter "Java" and select "Java Class". You will be prompted for a file name. Enter `HelloWorld.java`. You will then be prompted to choose where to save the file. Create a new directory somewhere, and save the file inside of the newly created directory.

The file `HelloWorld.java` is now open in our editor. Add the following text to the file:

```java
class HelloWorld {
    public static void main (String args[])
    {
        System.out.println("Hello, world!");
    }
}
```

Save the file, then click the play icon at the top right of the window. This is the **Run** button. By default, it will run your Java application normally.  You can also click the dropdown next to the icon and select **Debug** to run your Java application with the debugger attached, which is very helpful when problem-solving.

When you click the **Run** button, assuming everything is set up properly, your code will be compiled and executed. A terminal window will be opened, where your program may take in user input and/or write output. In this terminal window, the text "Hello, world!" will be written by the program.

If you are seeing the expected behavior, then congratulations are in order! You have just finished setting up Visual Studio Code for Java development.

If you are not seeing the expected behavior, restart from the beginning and confirm that you have followed each step correctly.

Happy coding!

> For more guides and a deeper dive on the content in this one, see VS Code's [Java docs](https://code.visualstudio.com/docs/java/java-tutorial).
