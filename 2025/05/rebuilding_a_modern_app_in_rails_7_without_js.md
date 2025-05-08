---
author: "Couragyn Chretien"
title: "Rebuilding a Modern App in Rails 7 Without JavaScript Frameworks"
date: 2025-05-07
description: This blog post explores how a modern project management app was successfully rebuilt using Rails 7 can be achieved without relying on JavaScript frameworks
tags:
- Rails 7
- Hotwire
- Turbo Streams
- JavaScript
---

In the realm of web development, the allure of JavaScript frameworks like React and Vue is undeniable. However, I recently embarked on a journey to rebuild a modern web application using Rails 7, Hotwire, and Turbo, deliberately avoiding any JavaScript frameworks. The outcome was a streamlined stack, improved performance, and a more maintainable codebase.

### Why Consider a Framework-Free Approach in 2025?

The complexity introduced by modern JavaScript frameworks can sometimes overshadow their benefits. Managing dependencies, build tools, and the intricacies of client-side rendering often lead to increased development overhead. With the advancements in Rails 7, particularly the introduction of Hotwire and Turbo, it's now feasible to build dynamic, responsive applications without the need for additional JavaScript frameworks.

### The Application: A Simplified Project Management Tool

I had previously built an app that was esentially a dumbed down version of Trello. The app is a lightweight project management tool featuring:

- Boards and cards

- Drag-and-drop functionality

- Real-time updates

- Commenting system

- User authentication and role management

Originally built with a React frontend and a Rails API backend, I decided to reconstruct it as a Rails 7 application, using Hotwire and Turbo for interactivity.

### Advantages of Using Rails 7 with Hotwire and Turbo

1. **Simplified Stack**: Eliminating the need for separate frontend frameworks reduced complexity and streamlined the development process.

1. **Enhanced Performance**: Server-rendered HTML and Turbo's partial page updates led to faster load times and a more responsive user experience.

1. **Improved Maintainability**: A unified codebase made it easier to manage and scale the application over time.

### Challenges Encountered
While the experience was largely positive, there were some hurdles:

- **Implementing Drag-and-Drop**: Achieving this functionality required integrating a lightweight JavaScript library and connecting it with Stimulus controllers.

- **Real-Time Collaboration**: Utilizing Turbo Streams and ActionCable facilitated real-time updates, but required careful handling to ensure consistency across clients.

- **File Uploads**: Managing file uploads and displaying progress indicators necessitated additional configuration and integration with Active Storage.

### Successes Achieved
Despite the challenges, several aspects of the rebuild were notably successful:

- **Modal Dialogs with Turbo Frames**: Loading forms and content into modals became straightforward, enhancing user interaction without additional JavaScript.

- **Live Updates with Turbo Streams**: Real-time broadcasting of updates improved collaboration features and kept users informed without manual refreshes.

- **Interactive Elements with Stimulus**: Implementing dynamic behaviors like toggles and dropdowns was efficient and required minimal JavaScript.

### Comparison to the Previous React-Based Build

| Feature                | React Version                       | Hotwire Version                        |
| ---------------------- | ----------------------------------- | -------------------------------------- |
| Build Complexity       | High (Webpack, Babel, etc.)         | Low (No bundler required)              |
| Developer Onboarding   | Steep learning curve                | 	More accessible for full-stack devs   |
| Performance            | Fast post-hydration                 | Fast initial load with partial updates |
| Real-Time Capabilities | Requires state management libraries | Built-in with Turbo Streams            |
| Maintenance Overhead   | Higher due to separate codebases    | Lower with a unified codebase          |

### Final Thoughts
Rebuilding the application using Rails 7 with Hotwire and Turbo proved to be a rewarding experience. The simplified stack, improved performance, and enhanced maintainability made it a compelling approach for developing modern web applications. While certain complex functionalities required additional effort, the overall benefits outweighed the challenges.

For developers seeking to build responsive and dynamic applications without the overhead of JavaScript frameworks, exploring the capabilities of Rails 7 with Hotwire and Turbo is highly recommended.