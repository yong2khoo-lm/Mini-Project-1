# Description
1. LinkedIn as one of the most popular platforms for candidate searching.
2. Market demand on Data Scientist expertise is increasing, demand is greater than supply
3. Thus, potential candidate overview and speed in identify the correct candidate is crucial in this talent war
4. With this, we have the idea to scrap the LinkedIn profile, focus on Data Scientist.

# Approach
1. Web scraping on LinkedIn with Selenium. (As one requires login in order to view the candidates' profile)
2. Focus on Data Scientist. 
3. Identify the [Url](https://www.linkedin.com/search/results/people/?keywords=Data%20Scientist&origin=SWITCH_SEARCH_VERTICAL&page=1) to get the Candidate list.
4. Scrape the candidate urls from candidate list.
5. Scrape the candidate profile to get the information, such as name, location, experiences, education and skills.

# Analysis and Visualization
1. Candidates by Location - To understand the candidate origin location and thus define hiring strategy. Pie chart gives good overview on the most dense Data Scientist location
2. Candidates Skill sets - To get insight of the candidate skills, which is crucial in the job roles.
3. Total Skills Histogram - Have an understanding of how many skills the candidate input to their profiles.
4. Candidates Education Word Cloud - To get a high level understanding of the distribution of the candidate education background.
5. Table - Show the raw scraped data

# Hosting
1. With [Digital Ocean](https://www.digitalocean.com/), at [here](https://king-prawn-app-7mrjr.ondigitalocean.app/).

# Challenges
## Web scraping
1. LinkedIn [filed lawsuit](https://news.linkedin.com/2022/may/an-update-on-scraping) on company scraping its site.
2. Throughout the scraping period, two of my linkedon accounts are suspected to have unusual activities. Then, I have to scrape at a low frequency, around 10+ candidates or around 20 web pages per hour.
3. XPath is dynamic in LinkedIn site, so CSS Selectors are chosen as the approach.
4. Pypi package [Linked Scraper](https://pypi.org/project/linkedin-scraper/) doesn't work. Have to write the script from scratch.

## Django
1. Use [plotly](https://plotly.com/) to plot graph. As it is relatively easier to render at html
2. Use a js [wordcloud lib](https://github.com/timdream/wordcloud2.js/) instead of from python.
3. Great to have found the [Atlantis template](https://appseed.us/admin-dashboards/django-dashboard-atlantis-dark), which features User Registration and Login.

# Project Requirements

- [x] Scrape data
- [x] Clean it, document it, visualize it
- [x] Project runnable at local
- [x] Push to Github with proper commit messages
- [x] Host it on Digital Ocean

# Enhancement
1. To meet the original objective, aka, hunting for data scientist from LinkedIn, it is better to display the results in a tabular format, with searching feature.


