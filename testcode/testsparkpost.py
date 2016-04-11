from sparkpost import SparkPost
sp = SparkPost('816861acefe647bab3df3c272fd798d0647040dd')

response = sp.transmissions.send(
    recipients=['2404222267@mms.att.net'],
    #recipients=['shahvineet98@gmail.com'],
    text = 'hello',
    #html='<p>Hello world</p>',
    from_email='mail@mail.shahv98.me',
    subject='Hello from python-sparkpost',
    track_opens=True,
    track_clicks=True
)

print(response)
