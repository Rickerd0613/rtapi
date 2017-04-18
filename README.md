# RT Python Module

## Installation

`pip install rtapi`

## Information
General Notes:
- All numbers should be given as strings
- Almost all data is returned in a dictionary
- All data return from the server is unicode
- Go to https://rt-wiki.bestpractical.com/wiki/REST to view available paramaters for dictionaries

## Requirements
- python2.7
- requests

## Methods
Available Methods:
- createTicket(ticketProperties)
- getTicketProperties(ticketID)
- getTicketLinks(ticketID)
- getTicketAttachments(ticketID)
- getTicketAttachment(ticketID, attachmentID)
- getTicketAttachmentContent(ticketID, attachmentID)
- getTicketHistory(ticketID)
- getTicketHistoryEntry(ticketID, historyID)
- searchTicket(query)
- editTicket(ticketID, ticketProperties)
- editTicketLinks(ticketID, linkProperties)
- getUserProperties(userID)
- createUser(userProperties)
- editUser(userProperties)
- getQueueProperties(queueID)
- respondTicket(ticketID, replyProperties)
- logout()

## Usage
```python
import rtapi

connector = rtapi.rt.Connector("localhost:8080", "user", "password")

properties = {"id": "ticket/new", "Queue": "General", "Requestor": "user@umich.edu", "Priority": "4", "Subject": "Test REST Module", "Text": "test"}

response = connector.createTicket(properties)
print response
```
