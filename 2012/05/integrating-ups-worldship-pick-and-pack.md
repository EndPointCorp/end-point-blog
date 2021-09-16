---
author: Terry Grant
title: Integrating UPS Worldship - Pick and Pack
github_issue_number: 621
tags:
- ecommerce
- shipping
date: 2012-05-29
---



### Using UPS WorldShip to automate a pick and pack scenario

There are many options when selecting an application to handle your shipping needs. Typically you will be bound to one of the popular shipping services; UPS, FedEx, or USPS or a combination thereof. In my experience UPS Worldship offers a very robust shipping application that is dynamic enough to accommodate integration with just about any custom or out of the box ecommerce system.

UPS Worldship offers many automating features by allowing you to integrate in many different ways. The two main automated features consist of batch label printing and individual label printing. I would like to cover my favorite way of using UPS Worldship that allows you to import and export data seamlessly.

You should choose the solution that works best for you and your shipping procedure. In this blog post I would like to discuss a common warehouse scenario refereed to as [Pick And Pack](https://en.wikipedia.org/wiki/Pick_and_pack). The basic idea of this scenario is an order is selected for a warehouse personnel to fulfill, it is then picked, packed, and shipped. UPS Worldship allows you to do this in a very automated way with a bit of customization. This is a great solution for a small to medium sized business that wants to automate their shipping process and communicate tracking information with their customers.

### Overall Breakdown of Process

There are a few steps involved in integrating your system with UPS Worldship. To get started I have listed the high-level breakdown of the process. I mention a few tables in this example, that I will explain in detail in the next section.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2012/05/integrating-ups-worldship-pick-and-pack/image-0-big.png" imageanchor="1" style="clear:left; float:left;margin-right:1em; margin-bottom:1em"><img border="0" height="400" src="/blog/2012/05/integrating-ups-worldship-pick-and-pack/image-0.png" width="318"/></a></div>

1. An order is placed on your website and saved into your database. For the sake of this example this will be the ‘orders’ table
1. A warehouse worker can then print out a packing slip that contains a barcode
1. Worldship then grabs the order information from the ‘orders’ table and inserts the shipping information in the the mapped fields
1. The Worldship operator then presses ‘F7’ which will process the shipment with UPS, thus retrieving a tracking number
1. Worldship marks the order as shipped and inserts the tracking number into a place holder tracking table
1. Worldship prints an active shipping label for your customer’s order

### Setting Up Your Data Structure

In order to integrate Worldship seamlessly you will need to make a few database modifications. I have decided to use two tables ‘orders’ and ‘ups_order_tracking’. The ‘orders’ table represents a standard table that contains the shipping information for an order. The ‘ups_order_tracking’ table is used to hold an order number and a tracking number. The order number, of course, refers to the unique order number in the ‘orders’ table. Every system is different, but this is a simple way that worked for me in the past. You will most likely need to make a few modifications to suit the needs of your data model and environment. I have included an example that will show what you will need at the very least.

**‘orders’**

This is the bare information needed by Worldship in order to fill in the shipping information for a package. I have added two other columns ‘tracking’, and ‘tracking_sent’. The ‘tracking’ column will hold the tracking number for this order. The ‘tracking_sent’ is a boolean that will keep track of our tracking number emails discussed later in this post.

```nohighlight
Column                   |         Type          |
-------------------------+-----------------------+
 id                      | integer               |
 order_status_id         | integer               |
 ship_to_name            | character varying     |
 ship_to_address         | character varying     |
 ship_to_address2        | character varying     |
 ship_to_city            | character varying     |
 ship_to_state_code      | character varying     |
 ship_to_province        | character varying     |
 ship_to_zip             | character varying     |
 tracking                | character varying     |
 tracking_sent           | boolean               |
```
**‘ups_order_tracking’**

This table acts as a temporary holding table for the tracking number for an individual order. I have found that it is much easier to have Worldship insert rows to a table and have a trigger copy the information to the ‘orders’ table (or something similar depending on your database), as opposed to updating a table. Since this is the case we smiply need to create a trigger that will updated the ‘orders’ table when a row is inserted into ‘ups_order_tracking’.

```nohighlight
Column        |         Type          |
--------------+-----------------------+
 order_id     | integer               |
 tracking     | character varying     |
```

### Setting Up Triggers

This article is written with Postgres used as the database. You will need to make the appropriate adjustments for your environment. The ‘ups_order_tracking’ table will need a simple trigger that is responsible for the following:

- Updating the ‘order.order_status_id’ column with a shipped flag (in this example 2 means it has been shipped)
- Updating ‘order.tracking’ with the tracking number supplied by Worldship

```nohighlight
BEGIN
:
:  UPDATE order
:    SET order_status_id = 2 WHERE id = NEW.order_id;
:  UPDATE order
:    SET tracking = NEW.tracking WHERE id = NEW.order_id;
:     RETURN NEW;
END;
```
After you have configured your database you are now ready to setup and integrate Worldship.

### Integrating UPS Worldship

UPS Worldship offers many ways to import shipment data. Since this article is about automating a pick and pack scenario, I am only going to cover how to use the Connection Assistant to import and export data from your database.

You will need to install the appropriate ODBC driver and setup access to your database before starting this step. RazorSQL.com has a decent explanation to get you started: [ODBC Setup](https://www.razorsql.com/docs/odbc_setup.html). Once you have this setup and connecting to your database you can continue to the ‘Importing Data’ section below.

**Importing Data**

Follow these steps below and reference the starting on Page 10: [UPS Importing Shipment Instructions](https://www.ups.com/media/en/Importing_Shipment_Data.pdf).

Please note the following steps:

- Step 4: make sure you select ‘By Known ODBC Source’ and select your installed ODBC driver you setup previously

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2012/05/integrating-ups-worldship-pick-and-pack/image-1-big.png" imageanchor="1" style="clear:right; float:right; margin-left:1em; margin-bottom:1em"><img border="0" height="230" src="/blog/2012/05/integrating-ups-worldship-pick-and-pack/image-1.png" width="320"/></a></div>

- Step 8 (part 1): you want to select the ‘orders’ table (or whatever your table is called) and map the appropriate shipment information to the Worldship fields on the right
- Step 8 (part 2): When mapping your data from your orders table make sure you set the Reference ID field to the order number. This allows you to 1) Use the order number later when exporting your order data and 2) You can then search UPS by your tracking number OR your Reference ID which is also your order number (very convenient if a tracking number is lost!)
- Step 12: If you have custom shipping options that is predetermined make sure you map these as seen in Step 12
- Name your map something meaningful like ‘Shipment Import’

- Step 20: Make sure you select your newly named import map under Keyed Import as this is how Worldship knows to use your ODBC driver and map to import your shipping data

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2012/05/integrating-ups-worldship-pick-and-pack/image-2-big.png" imageanchor="1" style=""><img border="0" height="261" src="/blog/2012/05/integrating-ups-worldship-pick-and-pack/image-2.png" width="320"/></a></div>

**Exporting Data**

Follow these steps below and reference the starting on Page 1 [UPS Exporting Shipment Data Instructions](https://www.ups.com/media/en/Exporting_Shipment_Data.pdf).
Please note the following steps:

- Skip to Page 8: ‘Export Shipment Data using Connection Assistant’ since we want to automatically update our ‘ups_order_tracking’ table after a label is processed

- Step 8: Make sure you map the tracking number and order number to the ‘ups_order_tracking’ table.

- Name your map something meaningful like ‘Shipment Export’

- Step 12: You can either configure Worldship to update your ‘ups_order_tracking’ table at the ‘End of the Day’ or ‘After processing Shipment’. I prefer to have Worldship update my ‘ups_order_tracking’ after each label is printed so the data is immediately available in the database.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2012/05/integrating-ups-worldship-pick-and-pack/image-3-big.png" imageanchor="1" style=""><img border="0" height="261" src="/blog/2012/05/integrating-ups-worldship-pick-and-pack/image-3.png" width="320"/></a></div>

### Processing an Order

Now that you have setup Worldship to interface with your database by creating maps you can use the ‘Keyed Import’ functionality to start processing packages. After you have selected your map under ‘Keyed Import’ you will see a small dialog box that is waiting for input.

**Scanner**

In my experience the fastest way to pull shipment data is by using a scanner that can scan the barcode on your packing slip. This barcode is the encoded order number that is referenced by your ‘orders’ table and used by the maps you created to retrieve the appropriate data. Most scanners can be configured to supply the key after a successful scan has occurred. NOTE: You must make sure the ‘Keyed Import’ box has focus and is waiting import. The basic process is as follows:

- An order is printed with a barcode (I was able to make use of [PHP Barcode Generator](https://www.barcodebakery.com/en) to generate my barcodes on the packing slip). You will need to find something that suites your needs if you want to make use of barcodes.
- User either scans an order or enters the order number in manually into the Keyed Import input.
- Worldship then pulls the order data is pulled from the database and inserted into the proper Worldship fields.
- The Worldship operator then presses the ‘F7’ key to process the shipment.
- Worldship then inserts the order_id and tracking number into ups_order_tracking tabl.e
- The ups_order_tracking table’s trigger is executed and updates the ‘orders’ table (or whatever is needed for your data model).
- Worldship prints out the shipping label and runs the action you selected to run after a shipment is processed, or at the end of day.
- Your order is now marked as shipped, updated with a tracking number, and you have a package ready to be picked up by UPS.

This might be enough for your needs, but I like to send an email to the customer letting them know their order has shipped and giving them a UPS tracking number to track their package.

### Email the Customer a Tracking Number

UPS Worldship does offer a feature that will send an email with a tracking number after the label is printed. This might be enough for some people, but it does not offer anything in the way of customizing the communication. Most businesses prefer branded emails with custom information in all communication sent to their customers. As such, I integrated a small feature that sends a custom and branded email to customers. This email includes their tracking number with a link to the UPS tracking page along with a friendly message letting them know their order is on the way.

Remember the order.tracking_sent boolean mentioned earlier ? This is where that field will come in handy. I wrote a small Perl script that runs every few hours. The script queries the ‘orders’ table and looks for:

- order.order_status_id = 2 (The order has been set to shipped)

- order.tracking_set IS NULL (A tracking email has not been sent)

After it pulls a list of all of the orders that have been marked as shipped AND have not had a tracking email sent, it pulls the tracking number and fires off an email to the customer with the tracking number. The script then sets ‘order.tracking_sent’ to TRUE so the next time the script runs it does not resend the tracking number to the customer. This is of course a very custom feature specific to this database. I am sure you would want to customize this to your needs. I thought it was worth mentioning as customers really like confirmation that 1) Their order was placed and 2) Their order has shipped (with a means of tracking its progress).

### Final Thoughts

As mentioned initially UPS Worldship offers many ways of integrating into your environment and offers many customizations. UPS offers great support if you simply contact your UPS representative they can put you in touch with a developer that can answer any question you have. I believe that for a Pick and Pack scenario using a packing slip with a barcode, a scanner, and a properly configured Worldship application you can streamline a small to medium sized warehouse environment. Unfortunately there are not many affordable solutions for small to medium sized e-commerce businesses, but UPS Worldship does a great job trying to fill that need and automate your shipping and communication needs.


