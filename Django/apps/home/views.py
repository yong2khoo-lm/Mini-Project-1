# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
import plotly.express as px
import plotly
from plotly.graph_objects import Layout;
import pandas as pd
from core.settings import BASE_DIR, CORE_DIR

@login_required(login_url="/login/")
def index(request):
    df = pd.read_csv(BASE_DIR + "/apps/static/assets/data.csv", encoding="utf-16")

    def get_total_candidates():
        return df.shape[0]
    
    def get_total_candidates_exp():
        exps = []
        for each_candidate_exp in df["experiences"]:
            exps = exps + [exp for exps in eval(each_candidate_exp) for exp in exps["exp"]]
        return len(exps)
    
    def get_total_candidates_skill():
        skills = []
        for each_candidate_skill in df["skills"]:
            skills = skills + [skill for skill in eval(each_candidate_skill)]
        return len(skills)

    def get_location_pie_chart_html():
        df['state'] = df["current_location"].str.splict(",")[1]
        df['state'].groupby(['city']).agg(count_state=('city', 'count')).reset_index().value_counts()


        #fig = px.pie(values=random_x, names=names)

    def get_dummy_histogram_html():
        data = {"type": [1,2,3,2,3,4,5,6,5,3,2,2]}
        fig = px.histogram(data, x="type")
        fig.update_layout({
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'font_color': 'white'
        })
        graph_div = plotly.offline.plot(fig, auto_open=False, output_type="div")
        return graph_div 

    def get_dummy_bar_html():
        data = {"type": ["a", "b", "c"], "value": [1,2,3]}
        fig = px.bar(data, x="type", y="value", orientation='v')
        fig.update_layout({
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'font_color': 'white'
        })
        graph_div = plotly.offline.plot(fig, auto_open=False, output_type="div")
        return graph_div 

    def get_dummy_col_html():
        data = {"type": ["a", "b", "c"], "value": [1,2,3]}
        fig = px.bar(data, x="value", y="type", orientation='h')
        fig.update_layout({
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'font_color': 'white'
        })
        graph_div = plotly.offline.plot(fig, auto_open=False, output_type="div")
        return graph_div 
    def get_dummy_pie_html():
        labels = ['a', 'b', 'c']
        values = [1,2,3]
        fig = px.pie(labels, values=values, names=labels)
        fig.update_layout({
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'font_color': 'white'
        })
        graph_div = plotly.offline.plot(fig, auto_open=False, output_type="div")
        return graph_div 

    context = {
     'total_candidates': get_total_candidates(),
     'total_candidates_exp': get_total_candidates_exp(),
     'total_candidates_skill': get_total_candidates_skill(),
     #'location_pie_chart': get_location_pie_chart_html(),
     'dummy_pie': get_dummy_pie_html(),
     'dummy_pie2': get_dummy_pie_html(),
     'dummy_bar': get_dummy_bar_html(),
     'dummy_col': get_dummy_col_html(),
     'dummy_histogram': get_dummy_histogram_html()

    }

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

def load_index():
    a = 1

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
