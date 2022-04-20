---
author: "Kürşat Kutlu Aydemir"
title: "Quartz Scheduler as a Service"
date: 2022-04-18
tags:
- java
- development
- automation
github_issue_number: 1856
---

![Close-up view of mechanical watch with roman numerals and day of month and month pointers](/blog/2022/04/quartz-scheduler-as-a-service/pexels-mat-brown-552598.webp)

Photo by Mat Brown from Pexels

[//]: # (from https://www.pexels.com/photo/round-silver-colored-chronograph-watch-552598/)

### Quartz Job Scheduler

"Quartz is a richly featured, open source job scheduling library that can be integrated within virtually any Java application — from the smallest stand-alone application to the largest e-commerce system." ([Quartz Scheduler overview](http://www.quartz-scheduler.org/overview/))

Besides its advanced features, most basic and frequently used feature is job scheduling and job execution. Some frameworks like Spring Scheduler have their integration practice using Quartz Scheduler which allows using its default scheduling method.

In this post I am going to tell you a different approach to show how we can use Quartz Scheduler to schedule our jobs. We actually still will be using the existing scheduling mechanism of Quartz but we're going to show how we can manage the scheduled and unscheduled jobs online. This way you can manage all the available jobs or create new ones on the fly.

### Quartz Scheduler as a Service

Previously I led development of an enterprise "Business Service Management" software to replace IBM's TBSM product at a major telco company in Turkey. This was a challenging project and found a solid place in the customer environment after a successful release.

Scheduled key performance indicators (KPI) retrieval and background reporting jobs were a significant part of this project. KPIs were either internal business service availability and health metrics or measured metrics calculated and stored in external data sources. Reports are also another type of schedulable jobs as many organizations need the data to be reported at certain intervals.

In an enterprise web application with such needs you would need to allow your customer to create their own customized scheduled jobs (KPIs, reports, etc.) in an easily manageable way. For this I came up with a simple solution by blending the existing Quartz Scheduler scheduling mechanism with some spice.

So here is the model we used:

* A database table for creating/​updating scheduler job definitions
* Observer Schduler Job for observing the scheduler job table to watch for any updates in the scheduled jobs: new job, updated job, or disabled job, etc.
* Business Job: You might define several schedulable business job types. KPI is one of those and I am going to give an example of it.

Simplicity should be a design goal, however the details can have their complexities.

This design doesn't replace or provide an alternative to how Quartz Scheduler schedules its jobs. That is subject to job persistence and is out of this article's scope. I am assuming we are scheduling the jobs all in Quartz Scheduler's RAM-store or Job-store.

#### Read and Manage Job Data

Ideally you should store and manage the jobs as services in a database and you can then connect to this job storage either via DB connection or API. For security reasons even if you think that your application or services are internal and totally authenticated and authorised you should still perform DB operations via APIs. But for capability perspective yes you can use many ways to read and manage a data storage.

For this simple project I am not going to use a database but instead a JSON file as job service definitions repository. But you can simply convert this method to a database or API method.

I am going to use a JSON file named `kpi.json` in my project and define a simple set of attributes for each KPI item. Any service or scheduled job can have more or fewer attributes according to the requirements of the business use case.

#### Spring Application

You can use any framework or even without using any framework you can create your application from scratch and build a JAR. Here in this project I chose to go with Spring framework. You can also simply initialize a Spring application [here](https://start.spring.io/).

#### Design

As I suggested a model above as a scheduling service solution, here is a high-level design of the model.

![Quartz Scheduler service model diagram](/blog/2022/04/quartz-scheduler-as-a-service/qs-service-design.png)

The overall solution would have a data storage for holding scheduled job service definitions and a UI for managing their attributes like enabling/​disabling or changing scheduling dates etc.

In this solution we have two different Quartz Scheduler job types: observer job and business job. Observer job is a single job triggered frequently, say, every 5 seconds or every 1 minute, and checks the existing job definitions in the job storage. If it sees any update on the job definitions or new jobs it behaves accordingly. Business jobs are the job definitions found in job storage and designed to perform certain business actions. The business jobs can be notification jobs, KPI measuring jobs, and any other scheduled business jobs which should have their own scheduling interval.

In this example project I specifically used KPI term as the business case just to make it more relevant.

#### Scheduler

`KPIJobWatcher` class is responsible to schedule the observer job. In Spring application startup this is going to be our starting point to the scheduling service management.

#### Spring Application Startup

```java
@SpringBootApplication
public class QSchedulerApplication {

	public static void main(String[] args) {
		SpringApplication.run(QSchedulerApplication.class, args);
	}

	Scheduler kpiScheduler;

	@EventListener(ApplicationReadyEvent.class)
	public void onAppStartUp() {
		try {
			// initializing KPI Trigger
			SchedulerFactory sf = new StdSchedulerFactory();
			kpiScheduler = sf.getScheduler();

			// watcher runs an observer job which monitors and manages KPI jobs
			KPIJobWatcher watcher = new KPIJobWatcher(kpiScheduler);
			watcher.run();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
```

`KPIJobWatcher` schedules the Observer job:

```java
public class KPIJobWatcher {
    private static final Logger logger = LoggerFactory.getLogger(KPIJobWatcher.class);

    Scheduler kpiScheduler;
    public KPIJobWatcher(Scheduler s) {
        kpiScheduler = s;
    }

    /**
     * run KPIJobWatcher
     * @throws Exception
     */
    public void run() throws Exception {

        try {
            // Setting the KPI Job factory of observerScheduler
            KPIJobFactory jf = new KPIJobFactory((StdScheduler)kpiScheduler);
            kpiScheduler.setJobFactory(jf);

            // Scheduling KPI Observer Job
            JobDetail observerJob = newJob(KPIObserverJob.class)
                    .withIdentity("observerJob", "observergroup")
                    .build();

            SimpleTrigger trigger = newTrigger()
                    .withIdentity(observerJob.getKey() + "_trigger", "observergroup")
                    .withSchedule(org.quartz.SimpleScheduleBuilder.simpleSchedule()
                            .withIntervalInSeconds(10)
                            .repeatForever())
                    .build();

            Date ft = kpiScheduler.scheduleJob(observerJob, trigger);
            logger.info(observerJob.getKey() + " has been scheduled to run at: " + ft);

            // Starting KPI Observer Scheduler
            kpiScheduler.start();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

Before moving on to observer job here I want to notice that you can use a custom `JobFactory` and attach it to the current scheduler object so that you can use custom jobs with custom constructors created within this custom JobFactory as part of the factory design pattern.

#### JobFactory

```java
public class KPIJobFactory implements JobFactory {
    Scheduler kpiScheduler;
    public KPIJobFactory(Scheduler s) {
        kpiScheduler = s;
    }

    public KPIObserverJob newJob(TriggerFiredBundle bundle, Scheduler Scheduler) throws SchedulerException {

        JobDetail jobDetail = bundle.getJobDetail();
        Class<KPIObserverJob> jobClass = (Class<KPIObserverJob>) jobDetail.getJobClass();
        try {
            // this is how we construct our custom job with custom factory
            return jobClass.getConstructor(Scheduler.getClass()).newInstance(kpiScheduler);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }
}
```

#### Observer Job

As suggested in the model above the observer job is triggered frequently and manages the overall scheduling job service in the background. I created the `KPIObserverJob` class as the observer job in this project and as you can see in the previous section `KPIJobFactory` creates instances of this observer job.

##### KPIObserverJob

Observer Job has some specific methods like `ScheduleJob` and `UnscheduleJob` to manage scheduling jobs.

```Java
public class KPIObserverJob implements Job {

    private static final Logger logger = LoggerFactory.getLogger(KPIObserverJob.class);

    List<JobDetail> jobList;
    Scheduler kpiScheduler;

    public KPIObserverJob(StdScheduler s) {
        kpiScheduler = s;
    }

    List<String> scheduledJobList;
    HashMap<String, JobDetail> alreadyScheduledJobList;

    String cronFormat = "SECOND MINUTE HOUR DAY_OF_MON MONTH DAY_OF_WEEK";

    @Override
    public void execute(JobExecutionContext context) throws JobExecutionException {
        scheduledJobList = new ArrayList<String>();
        alreadyScheduledJobList = new HashMap<String, JobDetail>();
        //JobKey jobKey = context.getJobDetail().getKey();

        jobList = new ArrayList<JobDetail>();

        // Get all KPIs and create their jobs
        CreateJobs();

        // Get the list of currently scheduled KPI jobs
        try {
            for (String groupName : kpiScheduler.getJobGroupNames()) {
                for (JobKey jk : kpiScheduler.getJobKeys(GroupMatcher.jobGroupEquals(groupName))) {
                    String jobName = jk.getName();
                    String jobGroup = jk.getGroup();

                    scheduledJobList.add(jobName);

                    JobDetail jd = kpiScheduler.getJobDetail(jk);
                    alreadyScheduledJobList.put(jobName, jd);

                    logger.info("already scheduled jobName {}", jobName);
                }
            }
        } catch (SchedulerException e) {
            e.printStackTrace();
        }

        // Schedule or unschedule KPI jobs if not done yet
        for (JobDetail job : jobList) {
            try {
                if (!scheduledJobList.contains(job.getKey().getName()))
                {
                    if (job.getJobDataMap().getInt("isRunning") == 1) {
                        logger.info("scheduling job: kpiJobName_{}", job.getJobDataMap().getString("kpiName"));
                        ScheduleJob(job);
                    }
                } else {
                    // Check any changes in the KPI job definition
                    JobDetail sJD = alreadyScheduledJobList.get("kpiJobName_" + job.getJobDataMap().getString("kpiName"));
                    if (!job.getJobDataMap().getString("cron").equals(sJD.getJobDataMap().getString("cron"))) {
                        logger.info("rescheduling job: kpiJobName {} , new cron: {}",
                                job.getJobDataMap().getString("kpiName"), job.getJobDataMap().getString("cron"));
                        UnscheduleJob(job.getJobDataMap().getString("kpiName"));
                        ScheduleJob(job);
                    }

                    if (job.getJobDataMap().getInt("isRunning") == 0) {
                        logger.info("Unscheduling: kpiJobName {}" + job.getJobDataMap().getString("kpiName"));
                        UnscheduleJob(job.getJobDataMap().getString("kpiName"));
                    }
                }
            } catch (SchedulerException e) {
                e.printStackTrace();
            }
        }

        // Finally unschedule deleted jobs if they are not listed anymore
        for (String kpiName : scheduledJobList) {
            boolean unschedule = true;
            if (!kpiName.equals("observerJob")) {
                JobDetail toBeRemovedJob = null;
                for (JobDetail jdetail : jobList) {
                    if (jdetail.getKey().getName().equals(kpiName)) {
                        unschedule = false;
                    }
                }

                if (unschedule) {
                    logger.info("Unscheduling: " + "kpiJobId" + kpiName.split("_")[1]);
                    UnscheduleJob(kpiName.split("_")[1]);
                }
            }
        }
    }

    private static final Type KPI_JSON_TYPE = new TypeToken<List<KPI_JSON>>() {}.getType();

    /**
     * Create Quartz Scheduler jobs from the job records read from a data source
     */
    private void CreateJobs() {

        Gson gson = new Gson();
        try {
            // kpi.json as a service data storage where we get KPI job data to be scheduled
            JsonReader reader = new JsonReader(new FileReader("kpi.json"));
            List<KPI_JSON> kpiList = gson.fromJson(reader, KPI_JSON_TYPE);

            for (KPI_JSON kpiItem : kpiList) {
                logger.info("Found KPI in kpi.json: {} , enabled: {}", kpiItem.getName(), kpiItem.getIsRunning());

                JobDetail job = newJob(KPIJSONJob.class)
                        .withIdentity("kpiJobName_" + kpiItem.getName(), "kpigroup")
                        .usingJobData("kpiName", kpiItem.getName())
                        .usingJobData("cron", kpiItem.getCron())
                        .usingJobData("lastRan", kpiItem.getLastRan())
                        .usingJobData("kpiDescription", kpiItem.getKpiDescription())
                        .usingJobData("lastMeasuredValue", kpiItem.getLastMeasuredValue())
                        .usingJobData("filename", kpiItem.getFilename())
                        .usingJobData("type", kpiItem.getType())
                        .usingJobData("isRunning", kpiItem.getIsRunning())
                        .build();

                jobList.add(job);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * Schedule a job
     * @param job
     * @throws SchedulerException
     */
    private void ScheduleJob(JobDetail job) throws SchedulerException {
        String cron = job.getJobDataMap().getString("cron");
        CronTrigger trigger = newTrigger()
                .withIdentity(job.getKey().getName() + "_trigger", "kpigroup")
                .withSchedule(cronSchedule(cron))
                .startNow()
                .build();
        Date ft = kpiScheduler.scheduleJob(job, trigger);
    }

    /**
     * Unschedule a job
     * @param kpiName
     */
    private void UnscheduleJob(String kpiName) {
        TriggerKey tk = new TriggerKey("kpiJobName_" + kpiName + "_trigger", "kpigroup");
        try {
            kpiScheduler.unscheduleJob(tk);
            kpiScheduler.deleteJob(new JobKey("kpiJobName_" + kpiName, "kpigroup"));
        } catch (SchedulerException e) {
            e.printStackTrace();
        }
    }
}
```

#### Business Jobs

Business jobs, as suggested in the model, can be any schedulable jobs. Managing/​updating the business jobs frequently is a key point here. As the enterprise demands grow and change continuously, KPIs are generated at intervals (daily, weekly, monthly, etc.) and for frequent notification needs this kind of scheduling job management can be an important part of a solution.

Here I created `KPIJSONJob` as my business job:

```java
public class KPIJSONJob implements Job {
    private static final Logger logger = LoggerFactory.getLogger(KPIJSONJob.class);
    private KPI_JSON kpi;

    @Override
    public void execute(JobExecutionContext context) throws JobExecutionException {
        JobDataMap dataMap = context.getJobDetail().getJobDataMap();

        kpi.setName(dataMap.getString("kpiName"));
        kpi.setKpiDescription(dataMap.getString("kpiDescription"));
        kpi.setIsRunning(dataMap.getInt("isRunning"));
        kpi.setFilename(dataMap.getString("filename"));
        kpi.setCron(dataMap.getString("cron"));
        kpi.setLastRan(dataMap.getString("lastRan"));
        kpi.setType(dataMap.getString("type"));
        kpi.setLastMeasuredValue(dataMap.getString("lastMeasuredValue"));

        this.processKPI();
    }

    public class KPIMeasured {
        public String name;
        public String value;
    }

    private static final Type KPIMEASURED_TYPE = new TypeToken<List<KPIMeasured>>() {}.getType();
    protected void processKPI() {
        // processKPI is supposed to get the KPI measured value from an external datasource and updates kpi.json
        // ...
    }

}
```

#### Running this Solution

Let's give it a try and see it in action. Say we have the `kpi.json` as our job storage, with the following KPI jobs defined:

```json
[
  {
    "name": "critical_ticket_count",
    "type": "JSON_FILE",
    "cron": "0 0 1 ? * * *",
    "isRunning": 0,
    "lastRan": "2022-04-01 01:00:00",
    "kpiDescription": "Open critical ticket count",
    "lastMeasuredValue": "7",
    "filename": "kpi_measured.json"
  },
  {
    "name": "failed_customer_api_call",
    "type": "JSON_FILE",
    "cron": "0 0 2 ? * * *",
    "isRunning": 0,
    "lastRan": "2022-04-01 02:00:00",
    "kpiDescription": "Last 24-Hour failed API call count",
    "lastMeasuredValue": "23",
    "filename": "kpi_measured.json"
  }
]
```

When we run the Spring application it starts logging like below:

```plain
2022-04-11 13:48:12.354  INFO 13033 --- [eduler_Worker-1] com.example.qscheduler.KPIObserverJob    : Found KPI in kpi.json: critical_ticket_count , enabled: 0
2022-04-11 13:48:12.355  INFO 13033 --- [eduler_Worker-1] com.example.qscheduler.KPIObserverJob    : Found KPI in kpi.json: failed_customer_api_call , enabled: 0
2022-04-11 13:48:12.355  INFO 13033 --- [eduler_Worker-1] com.example.qscheduler.KPIObserverJob    : already scheduled jobName observerJob
```

Initially I set the `isRunning` attribute of those KPI jobs to 0 and my scheduler service is not scheduling them. My KPIObserverJob triggers every 10 seconds because I set it to trigger that way in `KPIJobWatcher`.

Now let's see if I update `critical_ticket_count` KPI's `isRunning` value to 1:

```plain
2022-04-11 13:52:32.347  INFO 13033 --- [eduler_Worker-7] com.example.qscheduler.KPIObserverJob    : Found KPI in kpi.json: critical_ticket_count , enabled: 1
2022-04-11 13:52:32.348  INFO 13033 --- [eduler_Worker-7] com.example.qscheduler.KPIObserverJob    : Found KPI in kpi.json: failed_customer_api_call , enabled: 0
2022-04-11 13:52:32.348  INFO 13033 --- [eduler_Worker-7] com.example.qscheduler.KPIObserverJob    : already scheduled jobName observerJob
2022-04-11 13:52:32.349  INFO 13033 --- [eduler_Worker-7] com.example.qscheduler.KPIObserverJob    : scheduling job: kpiJobName_critical_ticket_count
```

As you can see from the logs `ObserverJob` noticed the enabled job and scheduled it.

Let's change the `cron` scheduling rule of `critical_ticket_count` job to `0 0 3 ? * * *` and see the logs again:

```plain
2022-04-11 13:55:12.354  INFO 13033 --- [eduler_Worker-3] com.example.qscheduler.KPIObserverJob    : Found KPI in kpi.json: critical_ticket_count , enabled: 1
2022-04-11 13:55:12.355  INFO 13033 --- [eduler_Worker-3] com.example.qscheduler.KPIObserverJob    : Found KPI in kpi.json: failed_customer_api_call , enabled: 0
2022-04-11 13:55:12.356  INFO 13033 --- [eduler_Worker-3] com.example.qscheduler.KPIObserverJob    : already scheduled jobName observerJob
2022-04-11 13:55:12.356  INFO 13033 --- [eduler_Worker-3] com.example.qscheduler.KPIObserverJob    : already scheduled jobName kpiJobName_critical_ticket_count
2022-04-11 13:55:12.356  INFO 13033 --- [eduler_Worker-3] com.example.qscheduler.KPIObserverJob    : rescheduling job: kpiJobName critical_ticket_count , new cron: 0 0 3 ? * * *
```

The Observer job now rescheduled the job since we changed its cron rule. These are all how we make observer job manage the KPI business jobs. If you have more attributes and if you want your observer job to reschedule or perform different operations on business job definition updates you should enrich your `ObserverJob`.

### Extend by Creating a Management UI

Managing the scheduler jobs using a UI is not in the scope of this post. But that is not much different than managing any data on a web application. I encourage you to do your own implementations if this solution sounds useful to you.

### Conclusion

This solution helps you create your own scheduling job management solution on the fly and lets you create, update, or delete the Quartz Scheduler jobs dynamically.

The complete implementation can be found in the [GitHub project](https://github.com/ashemez/QScheduler).
