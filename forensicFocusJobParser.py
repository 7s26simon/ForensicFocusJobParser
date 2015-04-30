import urllib2, email, smtplib, os.path
import cPickle as pickle
from bs4 import BeautifulSoup

a = '''
################
####H4D00K3N####
################'''

print a

class Job:
	"""docstring for Job"""
	def __init__(self, title, date, url):
		self.title = title
		self.date = date
		self.url = "http://www.forensicfocus.com/"+url
	def describJob(self):
		return (self.title +" "+ self.date +" "+ self.url)

def createJobsArray():
	# Open target URL and read it
	soup = BeautifulSoup(urllib2.urlopen('http://www.forensicfocus.com/jobs').read())
	# Find all strings beginning with 'a'
	bigFatString = soup.find_all('a')
	# print(type(bigFatString))
	# find all strings which include 'tr' and 'topic'
	findAll = soup.find_all("tr", class_="topic")

	# Empty jobs array
	jobsArray = []

	for section in findAll:

		title = section.find("a", class_="topictitle").get_text()
		titleEncoded = title.encode('ascii','ignore')

		row = section.find_all("td")
		date = row[3].find("div").get_text()
		# Look for everything beginning with href
		url = section.find_all("a")[3].get("href")
		# Get job title, date and URL from rows specified above
		job = Job(titleEncoded, date, url)
		# Append found job into jobs the empty array
		jobsArray.append(job)
	return jobsArray


# Sends email to itself, automatically fwds to address via gmail forwarding
def sendEmail(job):
	senderEmail = "sender_email_address"
	recipients = ["recipient_email_address"]
	s = smtplib.SMTP("smtp.gmail.com",587)
	s.ehlo()
	s.starttls() 
	s.ehlo()
	s.login(senderEmail, 'your_password_goes_here')

	for job in jobsFilteredByLocation:
		msg = email.message_from_string(job.describJob())
		msg['Subject'] = "New Job Lad: " + job.title
		s.sendmail(senderEmail, recipients, msg.as_string())
		print "Email sent"
	s.quit()
	#exit() # Added this but not sure if it's needed, probs not

# I dont understand what this (jobs) thing is. Might need u to explain what that's doing
def saveJobsToDisk(jobs):
	with open('jobs.hadooken', 'wb') as output:
		print "start write..."
		for job in jobs:
			print job.title
			pickle.dump(job, output)
		output.close()

# Reads in what's already in jobs.hadooken and adds to 'OldJobsArray'
def getJobsFromDisk():
	oldJobsArray = []
	with open('jobs.hadooken', 'rb') as input:
		while True:
			try:
				job = pickle.load(input)
				print job.title, "was successfully read from file"
				oldJobsArray.append(job)
			except EOFError:
				print "end of file"
				break
				
		return oldJobsArray
		input.close()

		
with open('jobs.hadooken', 'ab') as input:
	input.close()

# Locations we're looking for in our search using beautifulsoup
locationsArray = ["Liverpool", "Wirral", "Merseyside", "Northwest", "merseyside", "Wales", "Chester", "North West", "Cheshire", "Manchester"]
jobsArray = createJobsArray()
oldJobsArray = getJobsFromDisk()

# Empty array we're going to use 
jobsFilteredByLocation = []

# Looks for jobs we've found and added to original array
for job in jobsArray:
	for location in locationsArray:
		# dont understand this line
		found = job.title.find(location)

		if found > 0:
			if len(oldJobsArray) > 0:
				if any(oldJob.title == job.title for oldJob in oldJobsArray):
					print "Job already sent previously"
				else:
					print "adding ", job.title, "to array because it isnt in the old array"
					jobsFilteredByLocation.append(job)
			else:
				print "adding ", job.title, "to array"
				jobsFilteredByLocation.append(job)
			
# Send email with jobs we've filtered
sendEmail(jobsFilteredByLocation)

# Create an array of jobs sent and new jobs we've filtered
mergedArray = oldJobsArray + jobsFilteredByLocation

# Save each job in the new array to disk
for job in mergedArray:
	print "Job title: ", job.title
saveJobsToDisk(mergedArray)