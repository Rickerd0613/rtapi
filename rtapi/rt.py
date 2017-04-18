from requests import get, post
import urllib


class Connector(object):
    def __init__(self, host, username, password):
        """Accepts host, username, and password and creates the connector"""
        self.username = username
        self.password = password
        self.host = host
        self.credentials = {'user': self.username, 'pass': self.password}
        self.testConnection()

    def testConnection(self):
        """Tests the connection to the host and returns True if login is successful"""
        r = get("http://" + self.host + "/REST/1.0/",
                params=self.credentials)
        if "200" in r.text:
            return True
        elif "401" in r.text:
            print "Invalid credentials"
            return False

    def createTicket(self, ticketProperties):
        """Accepts a dictionary as input and creates a ticket with those properties"""
        content = ""
        for key, value in ticketProperties.iteritems():
            content += key + ": " + value + "\n"
        encoded = "content=" + urllib.quote_plus(content)
        r = post("http://" + self.host + "/REST/1.0/ticket/new", params=self.credentials, data=encoded)
        return r.text

    def getTicketProperties(self, ticketID):
        """Accepts ticket ID as input and returns a dictionary of ticket properties"""
        r = get("http://" + self.host + "/REST/1.0/ticket/" + ticketID + "/show", params=self.credentials)
        ticketProperties = {}
        data = r.text.split("\n")
        for line in data:
            if "200 Ok" in line or line == '':
                continue
            split = line.split(":", 1)
            ticketProperties[split[0]] = split[1][1:]
        return ticketProperties

    def getTicketLinks(self, ticketID):
        """Accepts ticket ID as input and returns a dictionary of ticket links"""
        r = get("http://" + self.host + "/REST/1.0/ticket/" + ticketID + "/links/show", params=self.credentials)
        ticketLinks = {}
        data = r.text.split("\n")
        for line in data:
            if "200 Ok" in line or line == '' or "id: ticket/" in line:
                continue
            split = line.split(":", 1)
            ticketLinks[split[0]] = split[1][1:]
        return ticketLinks

    def getTicketAttachments(self, ticketID):
        """Accepts ticket ID as input and returns a dictionary of ticket attachments"""
        r = get("http://" + self.host + "/REST/1.0/ticket/" + ticketID + "/attachments", params=self.credentials)
        ticketAttachments = {}
        data = r.text.split("\n")
        for line in data:
            if "200 Ok" in line or line == '' or "id: ticket/" in line:
                continue
            if "Attachments: " in line:
                line = line.split("Attachments: ")[1]
            if "," in line[-1]:
                line = line[:-1]
            if " " in line[0]:
                line = line[13:]
            split = line.split(":", 1)
            ticketAttachments[split[0]] = split[1][1:]
        return ticketAttachments

    def getTicketAttachment(self, ticketID, attachmentID):
        """Accepts ticket ID and attachment ID as input and returns a dictionary of attachments"""
        headers = False
        content = False
        r = get("http://" + self.host + "/REST/1.0/ticket/" + ticketID + "/attachments/" + attachmentID,
                params=self.credentials)
        attachmentProperties = {}
        data = r.text.split("\n")
        for line in data:
            if "200 Ok" in line or line == '':
                continue
            if headers == True and " " in line[0]:
                newSplit = line[9:].split(":", 1)
                attachmentProperties["Headers"][newSplit[0]] = newSplit[1][1:]
                continue
            elif content == True and " " in line[0]:
                attachmentProperties["Content"].append(line[9:])
                continue
            split = line.split(":", 1)
            if "Headers" in split[0]:
                headers = True
                newSplit = split[1][1:].split(":", 1)
                attachmentProperties[split[0]] = {newSplit[0]: newSplit[1][1:]}
                continue
            if "Content" in split[0]:
                headers = False
                content = True
                attachmentProperties[split[0]] = [split[1][1:]]
                continue
            attachmentProperties[split[0]] = split[1][1:]

        attachmentProperties["Content"] = "\n".join(attachmentProperties["Content"])
        return attachmentProperties

    def getTicketAttachmentContent(self, ticketID, attachmentID):
        """Accepts ticket ID and attachment ID as input and returns a string of attachment content"""
        r = get("http://" + self.host + "/REST/1.0/ticket/" + ticketID + "/attachments/" + attachmentID + "/content",
                params=self.credentials)
        data = r.text.split("\n")
        data = data[2:]
        return "\n".join(data)

    def getTicketHistory(self, ticketID):
        """Accepts ticket ID as input and returns a dictionary of the ticket history"""
        r = get("http://" + self.host + "/REST/1.0/ticket/" + ticketID + "/history", params=self.credentials)
        ticketHistory = {}
        data = r.text.split("\n")
        data = data[4:]
        for line in data:
            if "200 Ok" in line or line == '' in line:
                continue
            split = line.split(":", 1)
            ticketHistory[split[0]] = split[1][1:]
        return ticketHistory

    def getTicketHistoryEntry(self, ticketID, historyID):
        """Accepts ticket ID and history ID as input and returns a dictionary of ticket history entry properties"""
        r = get("http://" + self.host + "/REST/1.0/ticket/" + ticketID + "/history/id/" + historyID,
                params=self.credentials)
        ticketHistoryEntry = {}
        data = r.text.split("\n")
        data = data[4:]
        content = False
        attachments = False
        for line in data:
            if "200 Ok" in line or line == '' in line:
                continue
            if content == True and " " in line[0]:
                ticketHistoryEntry["Content"] += line + "\n"
                continue
            else:
                content = False
            if attachments == True and " " in line[0]:
                newSplit = line[13:].split(":", 1)
                ticketHistoryEntry["Attachments"] = {newSplit[0]: newSplit[1][1:]}
                continue
            split = line.split(":", 1)
            if "Content" in split[0]:
                ticketHistoryEntry[split[0]] = split[1][1:] + "\n"
                content = True
                continue
            if "Attachments" in split[0]:
                attachments = True
                continue
            # print split
            ticketHistoryEntry[split[0]] = split[1][1:]
        return ticketHistoryEntry

    def searchTicket(self, query):
        """Accepts a query string as input and returns a dictionary of tickets that match"""
        search = self.credentials
        search["query"] = query
        r = get("http://" + self.host + "/REST/1.0/search/ticket", params=search)
        tickets = {}
        data = r.text.split("\n")[2:]
        for line in data:
            if line == '':
                continue
            split = line.split(":", 1)
            tickets[split[0]] = split[1][1:]
        return tickets

    def editTicket(self, ticketID, ticketProperties):
        """Accepts ticket ID and ticket properties dictionary as input and returns a response from the server"""
        content = ""
        for key, value in ticketProperties.iteritems():
            content += key + ": " + value + "\n"
        encoded = "content=" + urllib.quote_plus(content)
        r = post("http://" + self.host + "/REST/1.0/ticket/" + ticketID + "/edit", params=self.credentials,
                 data=encoded)
        print r.text

    def editTicketLinks(self, ticketID, linkProperties):
        """Accepts ticket ID and link properties dictionary as input and returns a response from the server"""
        content = ""
        for key, value in linkProperties.iteritems():
            content += key + ": " + value + "\n"
        encoded = "content=" + urllib.quote_plus(content)
        r = post("http://" + self.host + "/REST/1.0/ticket/" + ticketID + "/links", params=self.credentials,
                 data=encoded)
        print r.text

    def getUserProperties(self, userID):
        """Accepts user ID as input and returns a dictionary of user properties"""
        r = get("http://" + self.host + "/REST/1.0/user/" + userID, params=self.credentials)
        userProperties = {}
        data = r.text.split("\n")[2:]
        for line in data:
            if line == '':
                continue
            split = line.split(":", 1)
            userProperties[split[0]] = split[1][1:]
        return userProperties

    def createUser(self, userProperties):
        """Accepts user properties dictionary as input and returns a response from the server"""
        content = ""
        for key, value in userProperties.iteritems():
            content += key + ": " + value + "\n"
        encoded = "content=" + urllib.quote_plus(content)
        r = post("http://" + self.host + "/REST/1.0/user/new", params=self.credentials, data=encoded)
        return r.text

    def editUser(self, userProperties):
        """Accepts user properties dictionary as input and returns a response from the server"""
        content = ""
        for key, value in userProperties.iteritems():
            content += key + ": " + value + "\n"
        encoded = "content=" + urllib.quote_plus(content)
        r = post("http://" + self.host + "/REST/1.0/user/edit", params=self.credentials, data=encoded)
        return r.text

    def getQueueProperties(self, queueID):
        """Accepts queue as input and returns a dictionary of queue properties"""
        r = get("http://" + self.host + "/REST/1.0/queue/" + queueID, params=self.credentials)
        queueProperties = {}
        data = r.text.split("\n")[2:]
        for line in data:
            # print line
            if line == '':
                continue
            split = line.split(":", 1)
            queueProperties[split[0]] = split[1][1:]
        return queueProperties

    def respondTicket(self, ticketID, replyProperties):
        """Accepts ticket ID and response properties dictionary as input and returns a response from the server"""
        content = ""
        for key, value in replyProperties.iteritems():
            content += key + ": " + value + "\n"
        encoded = "content=" + urllib.quote_plus(content)
        r = post("http://" + self.host + "/REST/1.0/ticket/" + ticketID + "/comment", params=self.credentials,
                 data=encoded)
        return r.text

    def logout(self):
        """Logs out the user and returns response from server"""
        r = post("http://" + self.host + "/REST/1.0/logout", params=self.credentials, data="")
        return r.text
