import praw
from praw.models import Comment
import time
import os
import json
import sys
import riddle_web_scraper


def main():
	saved_comments_file = "comments_replied_to.txt"

	comments_replied_to = get_saved_comments(saved_comments_file)

	reddit = authenticate()
	riddle = riddle_web_scraper.get_riddle()
	try:
		print("End program with ctrl-c")
		print("Initiating riddling...\n")
		while True:
			run_bot(reddit,riddle,comments_replied_to)
	except KeyboardInterrupt:
		print("\nExiting riddling...")
	finally:
		with open(saved_comments_file,"w") as file:
			json.dump(comments_replied_to, file)
		print("\nWrote to " + saved_comments_file + " successfully.\n")

def authenticate():
	print("Authenticating...")
	reddit = praw.Reddit('riddlebot', user_agent = "u/riddle_bot")
	print("Authenticated as {}\n".format(reddit.user.me()))
	return reddit


def get_saved_comments(filename):
	if not os.path.isfile(filename):
		print(filename + " not found.")
		sys.exit()
	with open(filename, 'r') as file:
		try:
			comments_replied_to = json.load(file)
			return comments_replied_to
		except ValueError:
			return {}


def run_bot(reddit, riddle, comments_replied_to):
	unread_messages = []
	for item in reddit.inbox.unread(limit=None):
		if isinstance(item, Comment):
			try:
				handle_comment(item,comments_replied_to,reddit, riddle)
				riddle = riddle_web_scraper.get_riddle()
				unread_messages.append(item)
				print("Replied to: " + str(item.author))
			except Exception as e:
				print("Error: " + str(e))
				print("Not marking item as read.")
	reddit.inbox.mark_read(unread_messages)
	sleep_time = 60
	print("Sleeping for " + str(sleep_time/60) + " minutes...")
	time.sleep(sleep_time)


def handle_comment(comment, comments_replied_to, reddit, riddle):
	if str(reddit.user.me()) in comment.body:
		reply_text = '''It appears I have been summoned! 
						Riddle me this...\n\n{}'''.format(riddle.question)
		reply_text += '''\n\nReply with \"answer plz\" and I shall PM you the answer :}'''
		comment.reply(reply_text)
		comments_replied_to[comment.id] = riddle.answer
	elif "answer plz" in comment.body:
		answer_key = get_answer_key(comment,reddit)
		if answer_key is None:
			raise LookupError("Comment.parent() isn't riddle_bot.")
		elif answer_key not in comments_replied_to:
			raise LookupError("Answer key isn't in comments_replied_to.")
		else:
			reply_text = '''The answer to my riddle is: \n\n'''
			reply_text += comments_replied_to[answer_key]
			reply_text += '''\n\nI hope you enjoyed the riddle! :}'''
			comment.author.message("Riddle",reply_text)


def get_answer_key(comment, reddit):
	# answer key is the id of the comment that mentioned riddle_bot
	# get parent of comment until parent == riddle post
	parent = reddit.comment(comment.id).parent()
	if parent.author.name != reddit.user.me():
		return None
	else:
		answer_key = parent.parent().id
		return answer_key

if __name__ == '__main__':
	main()