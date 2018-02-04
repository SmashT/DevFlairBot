import praw
import config
import time

# Gets the correct link flair, None if untagged
def get_flair_id(flair_name, flair_data):
    if flair_name is None:
        return next(x for x in flair_data
                           if x['flair_text_editable'])['flair_template_id']
    for flair in flair_data:
        if flair['flair_css_class'] == (flair_name + 'Dev'):
            return flair['flair_template_id']
        
reddit = praw.Reddit(user_agent=config.user_agent,
                     client_id=config.client_id,
                     client_secret=config.client_secret,
                     username=config.username,
                     password=config.password)
with open('tagged.txt', 'r') as f:
    posts_tagged = set(x for x in f.readlines() if x)
# Bot running forever
while True:   
    # Goes to subbreddit
    try:
        battalion1944 = reddit.subreddit(config.subreddit) 
        # Checks new submissions
        for submission in battalion1944.new():
            # Already tagged, ignore
            if submission.id in posts_tagged:
                continue
            old_flair = submission.link_flair_text
            choices = submission.flair.choices()
            # Searches in comments
            for comment in submission.comments:
                author = comment.author
                # Checks mod flair
                if comment.author_flair_css_class == config.mod_flair:
                    print('Developer responded')
                    template_id = get_flair_id(old_flair, choices)
                    flair_text = 'Developer Response' if old_flair is not None else 'UntaggedDev'
                    print(template_id)
                    print(flair_text)
                    # Changes the link flair
                    submission.flair.select(template_id, )
                    # Saves the submission
                    posts_tagged.add(submission.id)
                    print('Link flair changed')
                    # Write our updated list back to the file
        with open("tagged.txt", "w") as f:
            for post_id in posts_tagged:
                f.write(post_id + "\n")


    except Exception as e:
        print(e)
    time.sleep(5)
