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
import re
from collections import Counter
from core.settings import BASE_DIR, CORE_DIR
import plotly.graph_objects as go

@login_required(login_url="/login/")
def index(request):
    df = pd.read_csv(BASE_DIR + "/apps/static/assets/data.csv", encoding="utf-16")

    def get_total_candidates():
        return df.shape[0]
    
    def get_total_candidates_exp():
        exps = []
        for each_candidate_exp in df["experiences"]:
            exps = exps + [exps for exps in eval(each_candidate_exp)]
        return len(exps)
    
    def get_total_candidates_skill():
        skills = []
        for each_candidate_skill in df["skills"]:
            skills = skills + [skill for skill in eval(each_candidate_skill)]
        return len(skills)

    def get_location_pie_chart_html():
        def get_location_value_count():
            predefined_locs = ['sembilan', 'penang', 'kedah', 'kelantan', 'melacca', 'selangor', 'pahang', 'johore',
                    'johor bahru', 'sabah', 'sarawak', 'perak', 'malacca', "other countries (singapore)", 'kuala lumpur',
                   'others (malaysia)', 'terengganu', 'singapore']

            def get_location(loc):
                if loc is None:
                    return "unknown"
                if isinstance(loc, str) is False:
                    return "unknown"
                locs = loc.split(",")
                if len(locs) == 0:
                    return "unknown"
                
                res_loc = locs[0].lower().strip()
                if len(locs) == 3:
                    res_loc = locs[1].lower().strip()
                    if res_loc == "malaysia":
                        res_loc = locs[0].strip()
                        
                if 'kuala lumpur' in res_loc:
                    res_loc = 'kuala lumpur'
                if 'putrajaya' in res_loc:
                    res_loc = 'selangor'
                
                if res_loc == 'malaysia':
                    res_loc = 'others (malaysia)'
                    
                if res_loc == 'singapore':
                    res_loc = 'other countries (singapore)'
                    
                if 'negri' in res_loc:
                    res_loc = res_loc.replace('negri', '').strip()
                    
                if res_loc not in predefined_locs:
                    res_loc = "other countries"
                return res_loc
            
            df["current_location_clean"] = df["current_location"].apply(get_location)
            df_res = df.groupby('current_location_clean').agg(loc_count=('current_location_clean', 'count')).reset_index().value_counts()
            return df_res
        
        res = get_location_value_count()
        labels = [a for (a, b) in res.index]
        values = [b for (a, b) in res.index]
        fig = px.pie(labels, values=values, names=labels)
        fig.update_layout({
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'font_color': 'white'
        })
        graph_div = plotly.offline.plot(fig, auto_open=False, output_type="div")
        return graph_div 

    def get_top_skills_bar_html():
        def get_skill(skill):
            if skill is None:
                return "unknown"
            
            tmp = skill.lower()
            tmp = re.sub("\(.*?\)",'',tmp).strip()
            return tmp
        df['skills_clean'] = df["skills"].apply(get_skill)
        skills_by_total = []
        for each_person_skills in df["skills_clean"]:
            tmp = eval(each_person_skills)
            skills_by_total = skills_by_total + tmp

        cnt = Counter(skills_by_total)
        result = cnt.most_common(20)

        result = sorted(result, key=lambda x: x[1])

        labels = [a for (a, b) in result]
        values = [b for (a, b) in result]

        data = {"Total Count": values, "Skill": labels}
        fig = px.bar(data, x="Total Count", y="Skill", orientation='h')
        fig.update_layout({
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'font_color': 'white'
        })
        graph_div = plotly.offline.plot(fig, auto_open=False, output_type="div")
        return graph_div 

    def get_edus():
        courses = []
        for each_person_educations in df["educations"]:
            person_edus = eval(each_person_educations)
            for person_edu in person_edus:
                if len(person_edu) != 2:
                    continue
                person_edu_sp = person_edu[0].split(",")
                if len(person_edu_sp) != 2:
                    continue
                level = person_edu_sp[0].strip()
                course = person_edu_sp[1].strip()
                
                course = course.lower()
                course = re.sub("\(.*?\)",'',course).strip()
                courses.append(course)
                
        cnt = Counter(courses)
        topN = cnt.most_common(100)
        result = {"data": [[a,b] for (a, b) in topN]}
        return result;

    def get_total_skills_histogram_html():
        skills_by_total = []
        for each_person_skills in df["skills"]:
            tmp = eval(each_person_skills)
            skills_by_total.append(len(tmp))
        data = {"Total Skills":skills_by_total}
        fig = px.histogram(data, x="Total Skills")
        fig.update_layout({
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'font_color': 'white',
            'yaxis_title': 'Total Candidates'
        })
        graph_div = plotly.offline.plot(fig, auto_open=False, output_type="div")
        return graph_div 

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
     'location_pie_chart': get_location_pie_chart_html(),
     'skill_top_bar_chart': get_top_skills_bar_html(),
     'skill_histogram_chart': get_total_skills_histogram_html(),
     'educations': get_edus()
    }

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'index.html':
            return index(request)
            
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template
        context['dummy_table'] = get_dummy_tables_html()

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

def get_dummy_tables_html():
    df = pd.read_csv(BASE_DIR + "/apps/static/assets/data.csv", encoding="utf-16")

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns)[1:],
                    fill_color='#1a2035',
                    align='left'),
        cells=dict(values=[df.name, df.current_title, df.current_location,
                    df.experiences, df.educations, df.skills],
                   fill_color='#1f283e',
                   align='left'))
    ])
    fig.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'font_color': 'white',
        'height': 1500
    })
    table_div = plotly.offline.plot(fig, auto_open=False, output_type="div")
    return table_div 
