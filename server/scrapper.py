from newspaper import Article
url = 'http://www.myprotein.com/thezone/training/bad-weather-workouts-get-fit-at-home-with-these-exercise-tips/'
a = Article(url, language = 'en')
a.download()
a.parse()
print(a.title[:5000])
print(a.text[:5000])