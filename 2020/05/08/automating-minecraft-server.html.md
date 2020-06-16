---
author: "Zed Jensen"
title: "Automating Server Deployment"
tags:  
gh_issue_number:
---

Last year I bought an old Dell Optiplex off eBay to use as a dedicated Minecraft server for my friends and me. It worked well for a while, but when my university cancelled classes and I moved home, I left it at my college apartment and was unable to fix it when it failed for some reason. I still wanted to play Minecraft with friends, though, so I had to figure out a solution in the meantime.

I'd previously used a basic DigitalOcean droplet for a Minecraft server, but that had suffered with lag issues, especially with more than two or three people logged in. Their $5 tier of servers provides 1GB of RAM and 1 CPU core, so it's not too much of a surprise that it struggled with a Minecraft server. However, more performant virtual machines cost a lot more, and I wanted to keep my solution as cheap as possible. My dad pointed out that most companies don't actually charge for virtual machines on a monthly basis - in reality, it's an hourly rate based on when your instance exists. So, he suggested I create a virtual machine and start my Minecraft server every time I wanted to play, then shut it down and delete it when I was finished, thus saving the cost of running it when it wasn't being used.


I decided in any case to try [UpCloud](https://upcloud.com/), a similar service based in Helsinki, Finland. They offer several cheap tiers of virtual machines, including:

<div class="table-scroll">
  <table>
    <thead>
      <td>Memory</td>
      <td>CPU</td>
      <td>Storage</td>
      <td>Transfer</td>
      <td>Price</td>
    </thead>
    <tr>
      <td>1 GB</td>
      <td>1</td>
      <td>25 GB</td>
      <td>1 TB</td>
      <td>$5/mo</td>
    </tr>
    <tr>
      <td>2 GB</td>
      <td>1</td>
      <td>50 GB</td>
      <td>2 TB</td>
      <td>$10/mo</td>
    </tr>
    <tr>
      <td>4 GB</td>
      <td>2</td>
      <td>80 GB</td>
      <td>4 TB</td>
      <td>$20/mo</td>
    </tr>
    <tr>
      <td>8 GB</td>
      <td>4</td>
      <td>160 GB</td>
      <td>5 TB</td>
      <td>$40/mo</td>
    </tr>
  </table>
</div>

There are more tiers, but for a Minecraft server I didn't need anything that powerful. I decided on the $40/month tier—or, in my case, $0.06/hr.
