import praw
from praw.models import Comment
import time
import os
import json
import sys
import riddle_web_scraper
import _thread
import threading

class RiddleBot:

	saved_comments_file = "comments_replied_to.txt"

	def __init__(self):
		self.reddit = self.authenticate()
		self.riddle = riddle_web_scraper.get_riddle()
		self.comments_replied_to = self.get_saved_comments(self.saved_comments_file)

	def authenticate(self):
		print("Authenticating...")
		reddit = praw.Reddit('riddlebot', user_agent = "u/riddle_bot")
		print("Authenticated as {}\n".format(reddit.user.me()))
		return reddit

	def get_saved_comments(self, filename):
		if not os.path.isfile(filename):
			print(filename + " not found.")
			sys.exit()
		with open(filename, 'r') as file:
			try:
				comments_replied_to = json.load(file)
				return comments_replied_to
			except ValueError:
				return {}

	def run_bot(self):
		event = threading.Event()
		threading.Thread(None, self.wait_for_input, None, (event,)).start()

		sleep_time = 60
		while True:
			try:
				self.go_through_inbox()
			except Exception as e:
				print("Error: " + str(e))
			print("Sleeping for " + str(sleep_time/60) + " minute...")
			if event.wait(sleep_time):
				break

		with open(self.saved_comments_file,"w") as file:
			json.dump(self.comments_replied_to, file)
		print("Wrote to " + self.saved_comments_file + " successfully.")

	def wait_for_input(self, event):
		input("Press Enter to stop program...\n")
		event.set()
		print("Ending riddling...")

	def go_through_inbox(self):
		unread_messages = []
		for item in self.reddit.inbox.unread(limit=None):
			if isinstance(item, Comment):
				try:
					self.reply_to_comment(item)
					self.riddle = riddle_web_scraper.get_riddle()
					unread_messages.append(item)
					print("Replied to: " + str(item.author))
				except Exception as e:
					print("Error: " + str(e))
					print("Not marking item as read.")
		self.reddit.inbox.mark_read(unread_messages)

	def reply_to_comment(self,comment):
		if str(self.reddit.user.me()) in comment.body:
			reply_text = '''It appears I have been summoned!
							Riddle me this...\n\n{}'''.format(self.riddle.question)
			reply_text += '''\n\nReply with \"answer plz\" and I shall PM you the answer :}'''
			comment.reply(reply_text)
			self.comments_replied_to[comment.id] = self.riddle.answer
		elif "answer plz" in comment.body:
			riddle_answer = self.get_riddle_answer(comment)
			comment.author.message("Riddle",riddle_answer)

	def get_riddle_answer(self, comment):
		# answer key is the id of the comment that mentioned riddle_bot
		parent = self.reddit.comment(comment.id).parent()
		answer_key = parent.parent().id
		if parent.author.name != self.reddit.user.me():
			return '''Sorry, it seems as though I forgot the answer to my own riddle.
					  The fact that I haven't lost my very own head is a riddle in itself.'''
		elif answer_key not in self.comments_replied_to:
			return '''Sorry, it seems as though I forgot the answer to my own riddle.
					  The fact that I haven't lost my very own head is a riddle in itself.'''
		else:
			reply_text = '''The answer to my riddle is: \n\n'''
			reply_text += self.comments_replied_to[answer_key]
			reply_text += '''\n\nI hope you enjoyed the riddle! :}'''
			return reply_text
			

if __name__ == '__main__':
	riddle_bot = RiddleBot()
	riddle_bot.run_bot()
