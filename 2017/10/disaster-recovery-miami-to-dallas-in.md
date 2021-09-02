---
author: Ian Neilsen
title: Disaster Recovery — Miami to Dallas in one hit
github_issue_number: 1329
tags:
- devops
- disaster-recovery
- virtualization
- replication
date: 2017-10-03
---

Hurricane Irma came a knocking but didn’t blow Miami away.

Hurricanes are never fun, and neither is knowing that your business servers may be in the direct path of a major outage due to a natural disaster.

Recently we helped a client prepare a disaster recovery environment, 4 days out pending Hurricane Irma approaching Miami—​where it happens their entire server ecosystem sat. In recent months we had been discussing a long-term disaster recovery plan for this client’s infrastructure, but the final details hadn’t been worked out yet, and no work begun on it, when the news of the impending storm started to arrive.

Although the Miami datacenter they are using is highly regarded and well-rated, the client had the foresight to think about an emergency project to replicate their entire server ecosystem out of Miami to somewhere a little safer.

Fire suits on, battle helmets ready, GO! Two team members jumped in and did an initial review of the ecosystem: six Linux servers, one Microsoft SQL Server database with about 50 GB of data, and several little minions. All of this hosted on a KVM virtualization platform. OK, easy, right? Export the VM disks and stand up in a new datacentre on a similar KVM-based host.

But no downtime could be scheduled at that time, and cloning the database would take too much time to make a replica. If we can’t clone the VM disks without downtime we need another plan. Enter our save-the-day idea: use the database clone from the development machine.

So first things first: Build the servers in the new environment using the cloned copy, rsync the entire disk across, hoping that a restart would return the machine into a working state, take the development database and use the Microsoft tools at our disposal to replicate one current snapshot, then replicate row level details, in preparation of reducing the amount of lost data, should the datacenter lose connection.

Over the course of the next 16 hours, with 2 DevOps engineers, we replicated 6 servers, migrated 100+ GB of data twice and had a complete environment ready for a manual cutover.

Luckily the hurricane didn’t cause any damage to the datacenter, which never lost power or connectivity, so the sites never went down.

Even though it wasn’t used in this case, this emergency work did have a silver lining: Until this client’s longer-term disaster recovery environment is built, these system replicas can serve as cold standby, which is much better than having to rebuild from backups if their primary infrastructure goes out.

That basic phase is out of the way, so the client can breathe easier. Along the way, we produced some updated documentation, and gained deeper knowledge of the client’s software ecosystem. That’s a win!

The key takeaways here: Don’t panic, and do a little planning prior. Leaving things to the last minute rarely works well.
And preferable to all of the above: Plan and build your long-term disaster recovery environment now, well before any possible disaster is on the horizon!

To all the people affected by Hurricane Irma we wish a speedy rebuild.
