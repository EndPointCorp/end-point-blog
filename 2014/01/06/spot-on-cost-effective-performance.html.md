---
author: Josh Williams
gh_issue_number: 909
tags: automation, linux, python, testing, cassandra, mongodb
title: Spot On Cost Effective Performance Testing
---

AWS is, in my humble opinion, pricey. However, they provide a nice alternative to the on-demand EC2 instances most people are familiar with: Spot instances. In essence, spot instances allow you to bid on otherwise compute idle time. Recent changes to the web console seem to highlight spot instances a bit more than they used to, but I still don’t see them mentioned often.

The advantage is you get the same selection of instance sizes, and they perform the same as a normal on-demand instance for (usually) a fraction of the price. The downside is that they may disappear at a moment’s notice if there’s not enough spare capacity when someone else spins up a normal on-demand instance, or simply outbids you. It certainly happened to us on occasion, but not as frequently as I originally expected. They also take a couple minutes to evaluate the bid price when you put in a request, which can be a bit of a surprise if you’re used to the almost-instantaneous on-demand instance provision time.

We made extensive use of spot instances in some of the software cluster testing we recently did. For our purposes those caveats were no big deal. If we got outbid, the test could always be restarted in a different Availability Zone with a little more capacity, or we just waited until the demand went down.

At the height of our testing we were spinning up 300 m1.xlarge instances at once. Even when getting the best price for those spot instances, the cost of running a cluster that large adds up quickly! Automation was very important. Our test scripts took hold of the entire process, from spinning up the needed instances, kicking off the test procedure and keeping an eye on it, retrieving the results (and all the server metrics, too) once done, then destroying the instances at the end.

### Here’s how we did it:

In terms of high level key components, first, that test driver script was home-grown and fairly specific to the task. Something like Chef could have been taught to spin up spot instances, but those types of configuration management tools are better at keeping systems up and running. We needed the ability to run a task, and immediately shut down the instances when done. That script was written in Python, and leans on the boto library to control the instances.

Second, a persistent ‘head node’ was kept up and running as a normal instance. This ran a Postgres instance and provided a centralized place for the worker nodes to report back to. Why Postgres?  I needed a simple way to number and count the nodes in a way immune to race conditions, and sequences were what came to mind. It also gave us a place to collect the test results and system metrics, and compress down before transferring out from AWS.

Third, customized AMI’s were used. Why script the installation of ssh keys, Java, YCSB or Cassandra or whatever, system configuration like our hyper 10-second interval sysstat, application parameters, etc, onto each of those 300 stock instances?  Do it once on a tiny micro instance, get it how you want it, and snapshot the thing into an AMI. Everything’s ready to go from the start.

There, those are the puzzle pieces. Now how does it all fit together?

When kicking off a test we give the script a name, a test type, a data node count, and maybe a couple other basic parameters if needed. The script performs the calculations for dataset size, number of client nodes needed to drive those data nodes, etc. Once it has all that figured out the script creates two tables in Postgres, one for data nodes and one for client nodes, and then fires off two batch requests for spot instances. We give them a launch group name to make sure they’re all started in the same AZ, our customized AMI, a bit of userdata, and a bid price:

```
max_price = '0.10'
instance_type = 'm1.xlarge'
#(snip)
ec2.request_spot_instances(
    max_price, ami, instance_type=instance_type, count=count,
    launch_group=test_name, availability_zone_group=test_name,
    security_groups=['epstatic'],
    user_data=user_data,
    block_device_map=bdmap
)
```

Okay, at this point I’ll admit the AMI’s weren’t quite that simple, as there’s still some configuration that needs to happen on instance start-up. Luckily AWS gives us a handy way to do that directly from the API. When making its request for a bunch of spot instances, our script sets a block of userdata in the call. When userdata is formulated as text that appears to be a script—​starting with a shebang, like #!/bin/bash—​that script is executed on first boot. (If you have cloud-init in your AMI’s, to be specific, but that’s a separate conversation.)  We leaned on that to relay test name and identifier, test parameters, and anything else our driver script needed to communicate to the instances at start. That thus became the glue that tied the instances back to the script execution. It also let us run multiple tests in parallel.

You may have also noticed the call explicitly specifies the block device map. This overrides any default mapping that may (or may not) be built into the selected AMI. We typically spun up micro instances when making changes to the images, and as those don’t have any instance storage available we couldn’t preconfigure that in the AMI. Setting it manually looks something like:

```
from boto.ec2.blockdevicemapping import BlockDeviceMapping, BlockDeviceType
bdmap = BlockDeviceMapping()
sdb = BlockDeviceType()
sdb.ephemeral_name = 'ephemeral0'
bdmap['/dev/sdb'] = sdb
sdc = BlockDeviceType()
sdc.ephemeral_name = 'ephemeral1'
bdmap['/dev/sdc'] = sdc
sdd = BlockDeviceType()
sdd.ephemeral_name = 'ephemeral2'
bdmap['/dev/sdd'] = sdd
sde = BlockDeviceType()
sde.ephemeral_name = 'ephemeral3'
bdmap['/dev/sde'] = sde
```

Then, we wait. The process AWS goes through to evalutate, provision, and boot takes a number of minutes. The script actually goes through a couple of stages at this point. Initially we only watched the tables in the Postgres database, and once the right number of instances reported in, the test was allowed to continue. But we soon learned that not all EC2 instances start as they should. Now the script gets the expected instance IDs, and tells us which ones haven’t reported in. If a few minutes pass, and one or two still aren’t reporting in (more on that in a bit) we know exactly which instances are having problems, and can fire up replacements.

An example output from the test script log, if i-a2c4bfd1 doesn’t show up soon and we can’t connect to it ourselves, we can be confident it’s never going to check in:

```
2014-01-02 05:01:46 Requesting node allocation from AWS...
2014-01-02 05:02:50 Still waiting on start-up of 300 nodes...
2014-01-02 05:03:51 Still waiting on start-up of 5 nodes...
2014-01-02 05:04:52 Checking that all nodes have reported in...
2014-01-02 05:05:02 I see 294/300 data servers reporting...
2014-01-02 05:05:02 Missing Instances: i-e833499b,i-d63349a5,i-d43349a7,i-c63349b5,i-a2c4bfd1,i-d03349a3
2014-01-02 05:05:12 I see 294/300 data servers reporting...
2014-01-02 05:05:12 Missing Instances: i-e833499b,i-d63349a5,i-d43349a7,i-c63349b5,i-a2c4bfd1,i-d03349a3
2014-01-02 05:05:22 I see 296/300 data servers reporting...
2014-01-02 05:05:22 Missing Instances: i-e833499b,i-c63349b5,i-a2c4bfd1,i-d63349a5
2014-01-02 05:05:32 I see 298/300 data servers reporting...
2014-01-02 05:05:32 Missing Instances: i-a2c4bfd1,i-e833499b
2014-01-02 05:05:42 I see 298/300 data servers reporting...
2014-01-02 05:05:42 Missing Instances: i-a2c4bfd1,i-e833499b
2014-01-02 05:05:52 I see 299/300 data servers reporting...
2014-01-02 05:05:52 Missing Instances: i-a2c4bfd1
2014-01-02 05:06:02 I see 299/300 data servers reporting...
2014-01-02 05:06:02 Missing Instances: i-a2c4bfd1
2014-01-02 05:06:12 I see 299/300 data servers reporting...
2014-01-02 05:06:12 Missing Instances: i-a2c4bfd1
2014-01-02 05:06:22 I see 299/300 data servers reporting...
2014-01-02 05:06:22 Missing Instances: i-a2c4bfd1
2014-01-02 05:06:32 I see 299/300 data servers reporting...
2014-01-02 05:06:32 Missing Instances: i-a2c4bfd1
```

Meanwhile on the AWS side, as each instance starts up that userdata mini-script writes out its configuration to various files. The instance then kicks off a phone home script, which connects back to the Postgres instance on the head node, adds its own ID, IP address, and hostname, and receives back its node number. (Hurray INSERT ... RETURNING!)  It also discovers any local instance storage it has, and configures that automatically. The node is then configured for its application role, which may depend on what it’s discovered so far. For example, nodes 2-n the Cassandra cluster will look up the IP address for node 1, and use that for its gossip host, as well as use their node numbers for the ring position calculation. Voila, hands-free cluster creation for Cassandra, MongoDB, or whatever we need.

Back on the script side, once everything’s reported in and running as expected, a sanity check is run on the nodes. For example with Cassandra it checks that the ring reports the correct number of data nodes, or similarly for MongoDB that the correct number of shard servers are present. If something’s wrong, the human that kicked off the test (who hopefully hasn’t run off to dinner expecting that all is well at this point) is given the opportunity to correct the problem. Otherwise, we continue with the tests, and the client nodes are all instructed to begin their work at the same time, beginning with the initial data load phase.

Coordinated parallel execution isn’t easy. Spin off threads within the Python script and wait until each returns?  Set up asynchronous connections to each, and poll to see when each is done?  Nah, pipe the node IP address list using the subprocess module to:

```
xargs -P <em>(node count)</em> -n 1 -I {} ssh root@{} <em>(command)</em>
```

It almost feels like cheating. Each step is distributed to all the client nodes at once, and doesn’t return until all of the nodes complete.

Between each step, we perform a little sanity check, and push out a sysstat comment. Not strictly necessary, but if we’re looking through a server’s metrics it makes it easy to see which phase/test we’re looking at, rather than try to refer back to timestamps.

```nohighlight
run_across_nodes(data_nodes+client_nodes, "/usr/lib/sysstat/sadc -C \\'Workload {0} finished.\\' -".format(workload))
```

When the tests are all done, it’s just a matter of collecting the test results (the output from the load generators) and the metrics. The files are simply scp’d down from all the nodes. The script then issues terminate() commands to AWS for each of the instances it’s used, and considers itself done.

### Fun AWS facts we learned along the way:

Roughly 1% of the instances we spun up were duds. I didn’t record any hard numbers, but we routinely had instances that never made it through the boot process to report in, or weren’t at all accessible over the network. Occasionally it seemed like shortly after those were terminated, a subsequent run would be more likely to get a dud instance. Presumably I was just landing back on the same faulty hardware. I eventually learned to leave the dead ones running long enough to kick off the tests I wanted, then terminate them once everything else was running smoothly.

On rare occasion, instances were left running after the script completed. I never got around to figuring out if it was a script bug or if AWS didn’t act on a .terminate() command, but I soon learned to keep an eye on the running instance list to make sure everything was shut down when all the test runs were done for the day.
