---
title: "Building real-time application with SignalR, .NET8 and three.js"
date: 2023-12-31
---

![clock](https://images.pexels.com/photos/219677/pexels-photo-219677.jpeg)

Users want to see real-time data in applications where latest data is reflected without refreshing the application. Adding real-time functionality to a .NET application is easy with [SignalR](https://dotnet.microsoft.com/en-us/apps/aspnet/signalr) library.

SignalR uses WebSockets, Server-Sent Events, or Long Polling, depending on the capabilities of the client and server, to establish a persistent connection between the client and the server. SignalR, from server-side, pushes code to connected clients. SignalR is good for applications that require high-frequency updates from the server, such as real-time gaming.

C# code can be used to write SignalR hubs, which easly integrates with other ASP.NET features like dependency injection, authentication, authorization, and scalability.

#### What we'll build

![signalr app](/blog/2023/12/building-real-time-application-with-signalr-and-.net8/signal-real-time-cube.gif)

We will learn how to use SignalR for real-time communication to send camera position of a cube, built using [three.js](https://threejs.org/), to all users in the page.
- User can load the webpage and request to control a cube for 2  minutes.
- Control can be released manually or it will be released after 2 minutes.
- User can control the camera position of cube, which will be seen my all the users vieweing the page.
- When one user is controlling the cube, other users requesting the control will be added to queue. Queued users will be granted control automatically when controlling user's time is over.

First we will create a web application and create a SignalR communication between client and server. After that, we will add more items to the codebase to achieve the above mentioned features.

### Creating web application, installing and configuring SignalR

Create web application
```bash
> dotnet new webapp -o EPSignalRControl
> code .\EPSignalRControl\
```

The SignalR server library is included in the ASP.NET Core shared framework. The JavaScript client library isn't automatically included in the project. For this tutorial, use Library Manager (LibMan) to get the client library from unpkg. unpkgis a fast, global content delivery network for everything on npm.

```bash
> dotnet tool install -g Microsoft.Web.LibraryManager.Cli
> libman install @microsoft/signalr@latest -p unpkg -d wwwroot/js/signalr --files dist/browser/signalr.js
```

#### Creating a SignalR hub
We'll create a **ControlHub** which inheritates Hub class. We'll also create `CameraData` model class for passing data between SignalR server and client.

```csharp
public class CameraData
{
    public double x { get; set; } = 0;
    public double y { get; set; } = 0;
    public double z { get; set; } = 5;
}
```
```csharp
using Microsoft.AspNetCore.SignalR;

namespace EPSignalRControl.Hubs;

public class ControlHub : Hub
{
    public async Task SendData(CameraData data)
    {
        // Broadcast the data to all clients
        await Clients.All.SendAsync("ReceiveData", data);
    }
}
```
The [Hub](https://learn.microsoft.com/en-us/dotnet/api/microsoft.aspnetcore.signalr.hub?view=aspnetcore-8.0) class has Clients, Context and Groups properties:
- **[Clients](https://learn.microsoft.com/en-us/dotnet/api/microsoft.aspnetcore.signalr.hub.clients?view=aspnetcore-8.0)**: can be used to invoke methods on the clients connected to this hub.

- **[Context](https://learn.microsoft.com/en-us/dotnet/api/microsoft.aspnetcore.signalr.hub.context?view=aspnetcore-8.0)**: the hub caller context for accessing information about the hub caller connection.

- **[Groups](https://learn.microsoft.com/en-us/dotnet/api/microsoft.aspnetcore.signalr.hub.groups?view=aspnetcore-8.0)**: the group manager to manage connections in groups.

`Clients.All` calls a method on all connected clients. So, control hub sends back the data received from one client, back to all connected clients. Similary, we can use `Clients.Caller` to send back data to client that invoked the hub method.

Then, we need to register the services using `AddSignalR()` and configure the endpoints using `MapHub()` required by SignalR in `Program.cs`
```csharp
using EPSignalRControl.Hubs;

var builder = WebApplication.CreateBuilder(args);
// Add services to the container.
builder.Services.AddRazorPages();

builder.Services.AddSignalR(); // Register SignalR service

var app = builder.Build();
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
    app.UseHsts();
}
app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();
app.UseAuthorization();
app.MapRazorPages();

app.MapHub<ControlHub>("/controlHub"); // Map ControlHub to endpoint

app.Run();
```
#### Connecting to SignalR Hub using Javascript library
We'll reference the SignalR Javascript library as well create `site.js` file and reference it in `Index.cshtml`

```html
<script src="~/js/signalr/dist/browser/signalr.js"></script>
<script type="module" src="~/js/site.js" asp-append-version="true"></script>
```
In `site.js` file, we will:
- connect to Control Hub using endpoint `/connecthub`
- start the connection with Control Hub
- send data to server by invoking `SendData` method of ControlHub
- add listener for `ReceiveData` to recieve the data sent from SignalR Hub

```javascript
const controlHubConnection = new signalR.HubConnectionBuilder()
    .withUrl("/controlhub")
    .build();

controlHubConnection.on("ReceiveData", function (cameraData) {
    console.log(`position.x = ${cameraData.x}`);
    console.log(`position.y = ${cameraData.y}`);
    console.log(`position.z = ${cameraData.z}`);
});

controlHubConnection.start().then(function () {
    console.log("Connected to ControlHub");
    console.log("Invoking SendData");
    controlHubConnection.invoke("SendData", {
        x: 100,
        y: 100,
        z: 100
    }).catch(function (err) {
    return console.error(err.toString());
});
}).catch(function (err) {
    console.error("Error connecting to ControlHub: " + err);
});
```

At this point if we run the web application and open the browser and see the dev tools console, we will see:
```console
Connected to ControlHub
Invoking SendData
position.x = 100
position.y = 100
position.z = 100
```
If we open another tab and browse the web application. In previous tab's dev tools console, we will see position values are appended. This is because new tab invoked `SendData` and server recieved and sent back data to all connected clients.
```console
Connected to ControlHub
Invoking SendData
position.x = 100
position.y = 100
position.z = 100
position.x = 100
position.y = 100
position.z = 100
```

This is the basic way of implmenting SignlaR in the project to achieve real-time functionality. Now, we'll dive deep into creating a but more practical usage that can be extended for other use.

### Adding more features
>One thing to note is Hubs are transient, so we cannot store state in the property of hub class. Each hub method call is executed on a new hub instance.


#### We will add following things on the backend:
- Add `ControlRequest.cs` model to hold SignalR connection id and requested date time.
```csharp
public class ControlRequest
{
    public string ConnectionId { get; set; } = string.Empty;
    public DateTime RequestTime { get; set; }
}
```
- Add two variables in ControlHub.cs, `currentControl` variable to hold the details of current active request and `controlQueue` to hold the requests in queue.
```csharp
private static Queue<ControlRequest> controlQueue = new Queue<ControlRequest>();
private static ControlRequest? currentControl;
```
- Add `ControlTimer.cs`class that has properties for Concurrent Dictionary mapping of connection id and ControlTimer object; Control Hub context and Control Hub clients.
```csharp
using System.Collections.Concurrent;
using Microsoft.AspNetCore.SignalR;

public class ControlTimer : System.Timers.Timer
{
    public static ConcurrentDictionary<string, ControlTimer> ControlTimers = new();
    public HubCallerContext hubContext { get; set; }
    public IHubCallerClients hubCallerClients { get; set; }
    public ControlTimer(double interval) : base(interval) { }
}
```
- Add two more variable in ControlHub.cs, 
    - `controlTimer` for storing accessing control timer dictionary, control hub context and control hub clients that can be access during the interval of timer that runs for the active request.
    - `CONTROL_TIME` holds the time in seconds for which the active request has control.
```csharp
private ControlTimer? controlTimer;
private const int CONTROL_TIME = 60; //seconds
```
- Add `RequestControl` method to `ControlHub` that is invoked by client to request the control. The method adds the connection id of the invoked request to queue, creates and adds control timer for currently invoked request. If the queue has only one request, it gives control to the current request, starts the timer and sends message to the requesting client notifying the access is granted. If the queue has more than one request, requesting client is notified that their request is queued.
```csharp
public async Task RequestControl()
{
    var controlRequest = new ControlRequest
    {
        ConnectionId = Context.ConnectionId,
        RequestTime = DateTime.Now
    };

    // Add the control request to the queue
    controlQueue.Enqueue(controlRequest);

    // Add timer to dictionary for request
    controlTimer = new ControlTimer(500)
    {
        hubContext = Context,
        hubCallerClients = Clients
    };
    controlTimer = ControlTimer.ControlTimers.GetOrAdd(controlRequest.ConnectionId, controlTimer);

    // Grant control if the queue is empty or it's the first request
    if (controlQueue.Count == 1 || controlQueue.Peek() == controlRequest)
    {
        currentControl = controlRequest;

        SetupTimerForRelease(controlRequest);

        await Clients.Client(controlRequest.ConnectionId).SendAsync("ControlGranted");
    }
    else
    {
        await Clients.Client(controlRequest.ConnectionId).SendAsync("ControlQueued");
    }
}
```
- Add `SetupTimerForRelease` method to add call to `ReleaseControlMiddleware` method on regular interval from the running timer.
```csharp
public void SetupTimerForRelease(ControlRequest controlRequest)
{
    if (controlRequest != null && controlTimer == null)
    {
        controlTimer = ControlTimer.ControlTimers.GetOrAdd(controlRequest.ConnectionId, controlTimer);
    }
    controlTimer.Elapsed += new ElapsedEventHandler(ReleaseControlMiddleware);
    controlTimer.Enabled = true;
}
```
- Add `ReleaseControlMiddleware` and `AutoReleaseControl` method, which is called by running timer, which checks if the time for the current control has elapsed. Sends the time remaining message to user with control. If the time has elapsed, calls `ClearTimerAndControl` to clear the timer and release control.
```csharp
public void ReleaseControlMiddleware(object source, ElapsedEventArgs e)
{
    _ = AutoReleaseControl(source, e);
}

public async Task AutoReleaseControl(object source, ElapsedEventArgs e)
{
    var controlTimer = (ControlTimer)source;
    HubCallerContext hcallerContext = controlTimer.hubContext;
    IHubCallerClients hubClients = controlTimer.hubCallerClients;

    if (currentControl != null)
    {
        var elapsedSeconds = Math.Ceiling(DateTime.Now.Subtract(currentControl.RequestTime).TotalSeconds);
        await hubClients.Client(currentControl.ConnectionId).SendAsync("ControlRemaining", CONTROL_TIME - elapsedSeconds);
        if (elapsedSeconds >= CONTROL_TIME)
        {
            await ClearTimerAndControl(hubClients, hcallerContext);
        }
    }
}
```
- Add `ClearTimerAndControl` method which:
    - clears the timer for given connection id
    - sends message to controlling client informing that their control time is released
    - sends default camera position data to all the clients to reset the cube camera position
    - dequeues the current control from queue, which is the first item
    - gives control to the next request in the queue
    - sends message to the client who is granted the control
```csharp
private async Task ClearTimerAndControl(IHubCallerClients hubClients, HubCallerContext context)
{
    try
    {
        // Clear the timer when control is explicitly released
        ClearControlTimer(context.ConnectionId);

        await hubClients.Client(context.ConnectionId).SendAsync("ControlReleased");
        await hubClients.All.SendAsync("ReceiveData", new CameraData());
        // Release control
        currentControl = null;

        // Remove the first request from the queue
        if (controlQueue.Count > 0)
            controlQueue.Dequeue();

        // Grant control to the next in the queue
        if (controlQueue.Count > 0)
        {
            currentControl = controlQueue.Peek();
            currentControl.RequestTime = DateTime.Now;
            SetupTimerForRelease(currentControl);
            await hubClients.Client(currentControl.ConnectionId).SendAsync("ControlGranted", currentControl.RequestTime.ToString());
        }
    }
    catch (Exception ex)
    {
        await Clients.All.SendAsync(ex.ToString());
    }
}
```
- Add `ClearControlTimer` method which gets the control timer of the given connection id. Removes the `ReleaseControlMiddleware` from the control timer and disables the control timer
```csharp
private void ClearControlTimer(string connectionId)
{
    controlTimer = ControlTimer.ControlTimers.GetOrAdd(connectionId, new ControlTimer(500));
    if (controlTimer != null)
    {
        controlTimer.Elapsed -= new ElapsedEventHandler(ReleaseControlMiddleware);
        controlTimer.Enabled = false;
        controlTimer = null;
    }
}
```
- Add `ReleaseControl` method to `ControlHub`, that is invoked manually by controlling client to release the control. It checks if the requesting client has the current control access and calls method to clear timer and 
```csharp
public async Task ReleaseControl()
{
    if (currentControl != null && currentControl.ConnectionId == Context.ConnectionId)
    {
        await ClearTimerAndControl(Clients, Context);
    }
}
```
- Add `SendData` method, which receives the data from controlling user and then sends the recieved data to all the clients.
```csharp
public async Task SendData(CameraData cameraData)
{
    controlTimer = ControlTimer.ControlTimers.GetOrAdd(Context.ConnectionId, new ControlTimer(500));
    if (controlTimer != null && controlTimer.hubContext != null && Context.ConnectionId == controlTimer.hubContext.ConnectionId)
    {
        // Broadcast the received sensor data to all clients
        await controlTimer.hubCallerClients.All.SendAsync("ReceiveData", cameraData);
    }
}
```

#### We will add following things on the frontend:
That's all the code required for the backend part. Now lets look at adding the frontend part in `Index.cshtml`.
- Add a receiver section to show the three js cube and update the camera position using the received data from SignalR connection
- Add a controller section with button to request the control using SignalR connection and show the three js cube. The cube can be rotated with mouse which sends the data to backend using SignalR connection, the backend then sends the data back to all the clients to update the cube camera position in receiver section
- Add a section to show the message from backend.
```html
@page
@model IndexModel
@{
    ViewData["Title"] = "Home page";
}

<div id="wrapper">
    <h3>Receiver</h3>
    <div id="receiver-wrapper"></div>

    <hr />
    <h3>Controller</h3>

    <button class="btn btn-primary" id="requestCtrlBtn" disabled></button>
    <div class="alert alert-info d-none" role="alert" id="message"></div>

    <div id="controller-wrapper"></div>
</div>

<script src="~/js/signalr/dist/browser/signalr.js"></script>
<script type="module" src="~/js/site.js" asp-append-version="true"></script>
```
The javascript code that adds all the functionality to above code: 
- First we'll add click handler to invoke `RequestControl` method using SignalR connection
- Add listeners for `ControlGranted`, `ControlQueued`, `ControlReleased` and `ControlRemaining` events to use the message received along with those event to update the UI accordingly
```js
let controlRequested = false;
let controlGranted = false;
let destroyController = false;

const requestCtrlBtn = document.getElementById('requestCtrlBtn')
requestCtrlBtn.disabled = true;
requestCtrlBtn.innerText = "Request Control";

const messageCtrl = document.getElementById('message')

requestCtrlBtn.addEventListener('click', () => {
    let action = 'RequestControl';
    if (controlGranted) {
        action = 'ReleaseControl';
    }
    controlHubConnection.invoke(action).catch(function (err) {
        return console.error(err.toString());
    });
})

controlHubConnection.on("ControlGranted", function () {
    controlGranted = true;
    controlRequested = false;
    requestCtrlBtn.disabled = false;
    requestCtrlBtn.classList.remove(...['btn-primary', 'btn-warning']);
    requestCtrlBtn.classList.add('btn-success');
    requestCtrlBtn.innerText = "Release Control";
    destroyController = createController();
});

controlHubConnection.on("ControlQueued", function () {
    controlRequested = true;
    controlGranted = false;
    requestCtrlBtn.disabled = true;
    requestCtrlBtn.classList.remove('btn-primary');
    requestCtrlBtn.classList.add('btn-warning');
    requestCtrlBtn.innerText = "Waiting in Queue";
});

controlHubConnection.on("ControlReleased", function () {
    controlRequested = false;
    controlGranted = false;
    requestCtrlBtn.disabled = false;
    requestCtrlBtn.innerText = "Request Control";
    requestCtrlBtn.classList.remove(...['btn-success', 'btn-warning']);
    requestCtrlBtn.classList.add('btn-primary');
    messageCtrl.innerText = '';
    messageCtrl.classList.add('d-none');

    if (destroyController != null) {
        destroyController();
        destroyController = null;
    }
});

controlHubConnection.on("ControlRemaining", function (seconds) {
    messageCtrl.classList.remove('d-none');
    messageCtrl.innerText = `Control Granted: ${seconds} seconds remaining`;
});
```

- Import `three.js` library along with `OrbitalControl` addons to control the cube camera position at the top of the file
```javascript
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
```

- Add `createRenderer`, `createScene`, `createCamera` and `createCube` helper methods that are required for creating cube and attaching it to the receiver as well as controller section to show a cube
```javascript
function createRenderer(canvsDOMId) {
    // Load a Renderer
    let renderer = new THREE.WebGLRenderer({ alpha: false, antialias: true });
    renderer.setClearColor(0xC5C5C3);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(250, 250);
    document.getElementById(canvsDOMId).appendChild(renderer.domElement);

    return renderer;
}

function createScene() {
    // Load 3D Scene
    let scene = new THREE.Scene();

    // Load Light
    var ambientLight = new THREE.AmbientLight(0xcccccc);
    scene.add(ambientLight);

    var directionalLight = new THREE.DirectionalLight(0xffffff);
    directionalLight.position.set(0, 0, 1).normalize();
    scene.add(directionalLight);

    return scene;
}

function createCamera(cameraZPosition = 10) {

    // Load Camera Perspektive
    let camera = new THREE.PerspectiveCamera(50, 250 / 250, 1, 200);
    camera.position.z = 5;

    // Load the Orbitcontroller
    return camera;
}

function createCube() {
    const geometry = new THREE.BoxGeometry(2, 2, 2).toNonIndexed();;

    const positionAttribute = geometry.getAttribute('position');
    const colors = [];
    const color = new THREE.Color();
    for (let i = 0; i < positionAttribute.count; i += 3) {

        if (i >= 0 && i <= 11) {
            color.set(0xffff00); // x facing yellow
        }
        else if (i >= 12 && i <= 23) {
            color.set(0xff0000); // y facing red
        }
        else {
            color.set(0x0000ff); // z facing blue
        }

        // define the same color for each vertex of a triangle
        colors.push(color.r, color.g, color.b);
        colors.push(color.r, color.g, color.b);
        colors.push(color.r, color.g, color.b);

    }
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
    const material = new THREE.MeshBasicMaterial({ vertexColors: true });
    let cube = new THREE.Mesh(geometry, material);

    // wireframe
    var geo = new THREE.EdgesGeometry(cube.geometry); // or WireframeGeometry
    var mat = new THREE.LineBasicMaterial({ color: 0xffffff });
    var wireframe = new THREE.LineSegments(geo, mat);
    cube.add(wireframe);

    return cube;
}
```
- User the helper methods to create cube on receiver section and render to display the cube
```javascript
// Define variables
const receiverRenderer = createRenderer('receiver-wrapper');
const receiverScene = createScene();
const receiverCamera = createCamera();
const receiverCube = createCube();
receiverScene.add(receiverCube);

let receiverControls = new OrbitControls(receiverCamera, receiverRenderer.domElement);
receiverControls.enabled = false;
function animate() {
    requestAnimationFrame(animate);
    receiverControls.update();
    receiverRenderer.render(receiverScene, receiverCamera);
}
animate();
```
- Listen to `ReceiveData` event to update the receiver section cube with updated camera position data
```javascript
controlHubConnection.on("ReceiveData", function (cameraData) {
    receiverCamera.position.x = cameraData.x;
    receiverCamera.position.y = cameraData.y;
    receiverCamera.position.z = cameraData.z;
});
```
- Add `createController` method which is called when the request is granted to user to control the cube. It creates a cube and renders on the controller section and listens to the camera position change. When the cube is rotated, it calls sever method `SendData` using SignalR connection. 
- It also returns a method that cancels the cube renderer and removes listener from controller cube. This returned method is called when `ControlReleased` event is called from server.
```javascript
function createController() {
    const controllerRenderer = createRenderer('controller-wrapper');
    const controllerScene = createScene();
    const controllerCamera = createCamera();
    const controllerCube = createCube();
    controllerScene.add(controllerCube);

    let controls = new OrbitControls(controllerCamera, controllerRenderer.domElement);
    function onPositionChange(o) {
        controlHubConnection.invoke("SendData", controllerCamera.position).catch(function (err) {
            return console.error(err.toString());
        });
    }
    controls.addEventListener('change', onPositionChange);

    let request;
    function controllerAnimate() {
        request = requestAnimationFrame(controllerAnimate);
        controls.update();
        controllerRenderer.render(controllerScene, controllerCamera);
    }

    controllerAnimate();

    return function () {
        document.getElementById('controller-wrapper').innerHTML = '';
        cancelAnimationFrame(request);
        controls.removeEventListener('change', onPositionChange);
    }
}
```

We learned basic of SignalR and how to build a simple application to communicate between backend and frontend using SignalR connection. We also looked into an practical implementation on how can we use SignalR to control the graphical object built in [three.js](https://threejs.org/). We can extend the application to build a multi-player game as well as use it to send the message to frontend from a long running backend background jobs.

You can get the code at: [Github](https://github.com/bimalghartimagar/EPSignalRControl)

Look at the [Demo](https://nifty.azurewebsites.net/)