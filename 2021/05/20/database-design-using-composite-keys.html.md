---
author: "Emre Hasegeli"
title: "Database Design: Using Composite Keys"
tags: database, development, performance, postgres, sql
gh_issue_number: 1745
---

![](/blog/2021/05/20/database-design-using-composite-keys/shipping-containers.jpg)
[Photo](https://unsplash.com/photos/kyCNGGKCvyw) by [Chuttersnap](https://unsplash.com/@chuttersnap)

Whether to use single-column or composite keys is another long-debated subject of database design. I previously wrote to support [using natural keys](/blog/2021/03/15/database-design-using-natural-keys) and here I want to make good arguments for using composite keys.

### Single-column vs. Composite

Single-column keys are widely used nowadays. I wouldn’t be surprised if many developers today don’t even think database design with composite keys is possible, even though they were essential in the beginning. Relational databases make no assumption that the keys must be composed of a single column.

Let’s see the composite keys with the corporate database example again. First, we’d need departments and employees:

```sql
CREATE TABLE departments (
  department_id text NOT NULL,
  department_location text NOT NULL,

  PRIMARY KEY (department_id)
);

CREATE TABLE employees (
  username text NOT NULL,
  department_id text NOT NULL,

  PRIMARY KEY (username),
  FOREIGN KEY (department_id) REFERENCES departments
);
```

Then our database grows, and we need to split the departments into multiple teams. Here’s what they’ll look like:

```nohighlight
| id | department  | team           | members |
| -- | ----------- | -------------- | ------- |
|  1 | sysadmin    | infrastructure |       5 |
|  2 | sysadmin    | internal_tools |       3 |
|  3 | development | internal_tools |       4 |
|  4 | development | web_site       |       8 |
```

As you noticed there are 2 teams named `internal_tools`, so we cannot use this as the primary key column. We can add a surrogate auto-increment column to use as the primary key, or make the department and team the primary key. Let’s go with the surrogate key option first to demonstrate the problem:

```sql
CREATE TABLE teams (
  team_id int NOT NULL GENERATED ALWAYS AS IDENTITY,
  department_id text NOT NULL,
  team_name text NOT NULL
  team_members int NOT NULL,

  PRIMARY KEY (team_id),
  UNIQUE (department_id, team_name),
  FOREIGN KEY (department_id) REFERENCES departments
);
```

As you noticed, we used the surrogate column as the primary key, and added an additional unique index to ensure the team name to be unique in with the department. Now, let’s relate the employees with the teams:

```sql
ALTER TABLE employees
  ADD COLUMN team_id int NOT NULL,
  ADD FOREIGN KEY (team_id) REFERENCES teams;
```

Now, we know both the department and the team of an employee, but the problem is that they can point to inconsistent rows. For example, I can INSERT myself as an employee:

```nohighlight
| username | department_id | team_id |
| -------- | ------------- | ------- |
| hasegeli | sysadmin      |       3 |
```

`team_id` 3 is in development department, so now you’d never know if I am in the sysadmin or development department. This is a very common source of data integrity problems in the databases. Applications have no good option to handle this. They would typically crash or sometimes show the employee in one department and sometimes in the other.

You cannot easily add a constraint to the database to prevent this. The best option would be to remove the `department_id` when the `team_id` is added as we know the department of the team anyway, but this option is expensive and not always possible, for example when the `team_id` can be NULL.

### Relations with Composite Keys

Now, let’s create the teams table with a composite key:

```sql
DROP TABLE teams CASCADE;

CREATE TABLE teams (
  department_id text NOT NULL,
  team_id text NOT NULL,
  team_members int NOT NULL,

  PRIMARY KEY (department_id, team_id),
  FOREIGN KEY (department_id) REFERENCES departments
);

ALTER TABLE employees
  ALTER COLUMN team_id TYPE text,
  ADD FOREIGN KEY (department_id, team_id) REFERENCES teams;
```

With this method, we ensure data integrity and don’t need to disturb the existing users of the employees table while adding the teams. They can still reliably use the `department_id` column. We can also set the `team_id` as NULL and still maintain the data integrity.

### Ease of Change

As we have already seen, one of the benefits of using composite keys is to respond to database model changes easier and without compromising data integrity. This becomes relevant in many real world scenarios. For example, let’s add the employees to rooms which must belong to the same department:

```sql
CREATE TABLE rooms (
  department_id text NOT NULL,
  room_id text NOT NULL,
  room_location text NOT NULL,

  PRIMARY KEY (department_id, room_id),
  FOREIGN KEY (department_id) REFERENCES departments
);

ALTER TABLE employees
  ADD COLUMN room_id text,
  ADD FOREIGN KEY (department_id, room_id) REFERENCES rooms;
```

Nothing special needed to be done in here, and it is often easy to respond to more complicated change requests. Composite keys play well with database constraints. For example, let’s add an employee `rank` which needs to be unique in every department:

```sql
ALTER TABLE employees
  ADD COLUMN employee_rank int,
  ADD CHECK (employee_rank > 0),
  ADD UNIQUE (department_id, employee_rank);
```

This was so easy because we have the `department_id` in here. Now, let’s imagine a more complicated change request. We need to divide the departments into sections:

```sql
CREATE TABLE sections (
  department_id text NOT NULL,
  section_id text NOT NULL,
  section_location text NOT NULL,

  PRIMARY KEY (department_id, section_id),
  FOREIGN KEY (department_id) REFERENCES departments
);

ALTER TABLE teams
  ADD COLUMN section_id text NOT NULL,
  DROP CONSTRAINT teams_pkey CASCADE,
  ADD PRIMARY KEY (department_id, section_id, team_id),
  ADD FOREIGN KEY (epartment_id, section_id) REFERENCES sections;

ALTER TABLE employees
  ADD COLUMN section_id text NOT NULL,
  ADD FOREIGN KEY (department_id, section_id, team_id) REFERENCES teams;
```

As you see, we can make this happen with minimal impact to the users of the database. As a final practice, let’s reserve employee ranks between 1 and 10 for the `main` section of every department:

```sql
ALTER TABLE employees
  ADD CHECK (section_id = 'main' OR employee_rank > 10);
```

### Querying

Another advantage of using composite keys is to have more possibility for joining of tables. For example using the tables we created we can join employees to sections without using the teams tables. This would not be possible if we had used single-column keys everywhere.

Join conditions get complicated with composite keys. The `USING` clause helps. To demonstrate, let’s join all of the tables we created so far:

```sql
SELECT *
  FROM employees
    JOIN deparments USING (department_id)
    JOIN sections USING (department_id, section_id)
    JOIN rooms USING (department_id, room_id)
    JOIN teams USING (department_id, section_id, team_id);
```

The `USING` clause only works if you name the columns the same on all tables. I recommend doing so.

Another advantage of `USING` clause is to eliminate duplicate columns on the result set. If you run this query, you would not see the `department_id` column repeated 5 times.

### Performance Considerations

One disadvantage of using composite keys is to store more data on tables as references. You would also need more space for the indexes as the reference columns often need to be indexed. However storage is the cheapest of resources, and the performance advantages easily outweigh the extra storage.

The main performance advantage of using composite keys is eliminating the need for many joins as mentioned before. However, when you do need to join many tables, the query planner would have many different paths. It’s the query planners’ strong suit to find the best join order. Composite keys allow them to come up with better plans in many scenarios. To demonstrate this, let’s get our join-all-tables query and add some WHERE conditions:

```sql
SELECT *
  FROM employees
    JOIN deparments USING (department_id)
    JOIN sections USING (department_id, section_id)
    JOIN rooms USING (department_id, room_id);
    JOIN teams USING (department_id, section_id, team_id)
  WHERE username LIKE 'a%' AND
    department_location LIKE 'b%' AND
    section_location LIKE 'c%' AND
    room_location LIKE 'd%';
    team_members > 3;
```

Now we added 5 conditions using 5 columns on 5 different tables. The query planner can estimate which conditions are more selective and plan to join the tables from the smaller one to bigger one.
