from django.urls import path
from django.urls import include
from django.views.generic import TemplateView

urlpatterns = [
    #index
    path('',include('index.urls')),
    # top keywords
    path('topword/', include('app_top_keyword.urls')),
    #app top persons
    path('topgpe/', include('app_top_person.urls')),
    #app top persons
    path('topperson/', include('app_top_person_v2.urls')),
    # top name entity keyword
    path('topner/', include('app_top_ner.urls')),
    # sentiment analysis
    path('sentiment/', include('app_sentiment.urls')),
    # user keyword analysis
    path('userkeyword/', include('app_user_keyword.urls')),
    # full text search and associated paragraphs for user keywords
    path('userkeyword_assoc/', include('app_user_keyword_association.urls')),
    # sentimental score for user keywords
    path('userkeyword_sentiment/', include('app_user_keyword_sentiment.urls')),
    # news recommendation
    path('news_rcmd/', include('app_news_rcmd.urls')),
    # leaderboard
    path('leaderboard/', include('app_leaderboard.urls')),
    # course introduction
    path('introduction', TemplateView.as_view(template_name='introduction.html'), name='course_introduction'),
    # course delicious
    path('delicious', TemplateView.as_view(template_name='delicious.html'), name='delicious'),



]
