import requests

# url = 'http://10.0.0.95:5555/GPTResponse'
# myobj = {'prompt': 'What did I last say?'}

myobj = {'transcript': "Julie Bratton: Hi, I'm Julie Bratton, co-founder of first juice. And we're developing products that are lower in sugar and sweetness for toddlers. So parents don't have to worry about the statistic. Julie Bratton: That was 15 s. So hopefully, you got who I am, what my company does and what problem we're solving. Julie Bratton: And for him. So that's what you want to do. And then you can quickly roll into your problem. Side your situational analysis. Here's another example of a problem slide. Julie Bratton: The problem slides. Key is to say who what the problem is and who has the problem. That is your customer who's going to pay you for it? Make this as relatable as you possibly can. One way to do that might be. How did you discover the problem? Julie Bratton: Remember, if this is a technical problem level. Set it right, make sure it's easy to understand and then use consistent language when you start setting up the situation, especially for technical areas. If you call it something. You have a term for the problem. Use that same term throughout. Don't mix Max terms, because that can lose people. Julie Bratton: I put a picture here for a problem picture speaks a thousand words. You get it right away. The homeowner's house is on its roof. He can't take a shower right? Julie Bratton: If you're gonna use a picture, make sure it's very crisp. It's grainy. Don't have any little watermarks on it, so I know that you stole the picture. but be very selective and find the right images Julie Bratton: from the problem. You'll roll right into the solution. Julie Bratton: I think this is probably one of the most important slides in your deck. this is your value proposition. Slide to."}

url = 'https://10.0.0.95:5555/MakeQuiz'
# url = "https://aptiversity.com:5555/MakeQuiz"

x = requests.post(url, json = myobj, verify=False)


print(x.text)