---
title: "Client Profile: J.G. Title Company"
date: 2023-12-27
author: Juan Pablo Ventoso
description: Summary of our work with J.G. Title, a prominent service company specializing in automotive dealership titling and registration processes across the country.
featured:
  image_url: /blog/2023/12/client-profile-j-g-title-company/j-g-title-company.webp
github_issue_number: 2022
tags:
- dotnet
- development
- clients
---

![The J.G. Title Company logo sits in the center of an image on a blue background with futuristic designs reminiscent of circuit boards. Text on either side of the logo reads "Nationwide titling", with text under reading "info@jgtitleco.com" and "https://jgtitleco.com"](/blog/2023/12/client-profile-j-g-title-company/j-g-title-company.webp)

[J.G. Title](https://jgtitleco.com/) is a prominent service company specializing in automotive dealership titling and registration processes across the country. They simplify operations for their dealers, businesses, and individuals by giving tax/fee quotes, document validation, and checklists for all jurisdictions.

Jordan Kivett, the owner of J.G. Title, envisioned an innovative web application to simplify dealership operations. He contacted us to request a quote for developing this solution and making his vision a reality. This project became a great opportunity for our [.NET team](/team/) to build a robust system with state-of-the-art technologies functioning seamlessly together.

### The solution

J.G. Title submitted a detailed document containing a description of the requirements for the J.G. Title Suite app along with workflow diagrams explaining their current business processes. After analyzing all the documents and having some initial meetings, we decided to divide the project into different stages, and estimate each phase of work separately. We ended up with three phases:

- Phase I: Create a product that allows users to enter deals into the system and retrieve the quote estimation, including taxes, fees, and charges for services across 50 states.
- Phase II: Implement several UI improvements such as a detailed dealership dashboard, financial management, and integration with [QuickBooks](https://quickbooks.intuit.com/).
- Phase III: Add an ambitious PDF document management section featuring document recognition, analysis, and manipulation, to perform automatic validations on the document's contents and automatically generate PDF outputs from the deal's details.

### Tech stack

- [.NET](https://dotnet.microsoft.com/en-us/learn/dotnet/what-is-dotnet) 6 with [C#](https://learn.microsoft.com/en-us/dotnet/csharp/tour-of-csharp/)
- [PostgreSQL](https://www.postgresql.org/) 14
- [Rocky Linux](https://rockylinux.org/) 9 with [Nginx](https://www.nginx.com/)

We had already worked with this combination of technologies for several clients, and we are confident in the combined power in a robust database such as Postgres along with .NET 6 running in a Linux environment. It has proven to be a stable, fast, and reliable setup for our web solutions.

We also used [Trello](https://trello.com/) for tracking the project's progress and tasks, [GitHub](https://github.com/) for version control, and [Visual Studio 2022](https://visualstudio.microsoft.com/vs/) or [VS Code](https://code.visualstudio.com/) with [.NET CLI](https://learn.microsoft.com/en-us/dotnet/core/tools/) as a coding environment. Some of us also used [VS Code dev containers](https://code.visualstudio.com/docs/devcontainers/tutorial). [pgAdmin](https://www.pgadmin.org/) is our usual tool to manage the local Postgres database, as well as [Postman](https://www.postman.com/) to test our API endpoints.

### The team

Most of our .NET team is involved on this project. We also receive valuable help from our hosting team and our Postgres developers.

- [Bimal Gharti Magar](/team/bimal-gharti-magar/)
- [Dan Briones](/team/dan-briones/)
- [Dylan Wooters](/team/dylan-wooters/)
- [Juan Pablo Ventoso](/team/juan-pablo-ventoso/)
- [Kevin Campusano](/team/kevin-campusano/)
- [Mike DeLange](/team/mike-delange/)

The client is also highly involved in all aspects of the development process, from requirements gathering to documenting, testing, and providing feedback. We have bi-weekly standup calls, and the entire team (End Point + J.G. Title) interacts actively through Trello, working together and updating each task as the work progresses.

### Results

We began working on the project on October 25, 2022, and completed Phase I within the expected timeline, on June 7, 2023. The next phases were launched iteratively, with new deployments usually scheduled twice a week.

The application is now widely used by dealerships and the J.G. Title team. They have over 200 users registered in the system, with more than 8,000 deals quoted, and new deals being added at an increasing rate.

![. On the right side is an image of a laptop and phone, each running the J.G. Title Suite application. Text on the left reads "From chaos to clarity. Simplify, streamline, succeed: Embrace clarity in your dealership's tax and title operations. Our dedicated team of specialists conducted extensive research and established partnerships with local DMVs and state Treasurers to become the trusted partner for automotive dealerships and businesses nationwide, offering efficient and reliable title and registration services. We continue transforming automotive title management on a national scale and welcome you to experience the future of automotive titling."](/blog/2023/12/client-profile-j-g-title-company/j-g-title-suite-featured.png)<br>
The J.G. Title Suite application, featured on the company's website.

We are continuing work on several tasks related to Phase III of the project. As the application keeps growing and users send feedback, new phases of work will surely be added to the project in the future.

This partnership is a testament to our shared vision for efficiency and innovation, and we're excited to continue reshaping the industry with J.G. Title Company!
