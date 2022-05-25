from pywebio import *
from pywebio.output import *
from pywebio.pin import *
import pandas as pd
from os import path
import plotly.express as px
import json

curr_dir = path.dirname(path.abspath(__file__))
hist_file_path = path.join(curr_dir, 'data', 'time_spending_hist.csv')
top5_file_path = path.join(curr_dir, 'data', 'top5_busy_days.json')

spending_hist = pd.read_csv(hist_file_path)
hist_plot = px.line(spending_hist, 
                    x='Date (PST)', 
                    y='Time Spent on Tweeting (mins)',
                    template='ggplot2',
                    height=600,
                    title='Elon\'s time spent on tweeting in the past 5 years'
                   )
hist_plot.add_hrect(y0=-0.8, y1=5,
                    annotation_text="<b>Usage below 5 mins: 75% of the days</b>", 
                    annotation_position="bottom",
                    annotation=dict(font_size=15, font_color='navy'),
                    fillcolor="navy", opacity=0.2, line_width=0
                    )
hist_plot.add_hrect(y0=15, y1=30,
                    annotation_text="<b>Usage above 15 mins: 25 days</b>", 
                    annotation_position="top",
                    annotation=dict(font_size=15, font_color='purple'),
                    fillcolor="purple", opacity=0.1, line_width=0
                    )
hist_plot.update_yaxes(range=[-0.8, 30])
hist_plot_html = hist_plot.to_html(include_plotlyjs="require", full_html=True)

md = r'''
Elon is known for his work ethics and being transparent about how to manage bandwidth cross many challenging projects. 

We're interested in knowing how much time he spent on communicating ideas on Twitter. So we pulled his data of the past 5 years and made an estimate.

Data used for this analysis:
- Tweets and replies queried from Twitter. 
- We **do not** have his app usage data. 

The algorithm is simple: `Total time spending` = `Typing` + `Drafting` + `Reading`
- `Typing`: tweet_letter_count / average_typing_speed (300 letters per minute)
- `Drafting`: +5 seconds to each tweet
- `Reading`: +5 seconds to each reply

__
<sub>Source code and data set: https://github.com/pywebio/twitter-time-spending</sub>
'''

css = """
#pywebio-scope-images {
    height: calc(100vh - 150px);
    overflow-y: hidden;
}
#pywebio-scope-images:hover {
    overflow-y: scroll;
}
#pywebio-scope-input {
    height: calc(100vh - 150px);
    overflow-y: hidden;
}
#pywebio-scope-input:hover {
    overflow-y: scroll;
}
/* Works on Firefox */
* {
  scrollbar-width: thin;
}
/* Works on Chrome, Edge, and Safari */
*::-webkit-scrollbar {
  width: 7px;
}
*::-webkit-scrollbar-track {
  background: transparent;
}
*::-webkit-scrollbar-thumb {
  background-color: gray;
  border-radius: 20px;
  border: 2px
}
"""

def put_top5():
    with open(top5_file_path, 'r') as f:
        top5_data = json.load(f)

    tab_data = []

    for key in top5_data.keys():
        tab_item = {}
        tab_item['title'] = key
        tab_item['content'] = [put_markdown(f'> {t}') for t in top5_data[key]]
        tab_data.append(tab_item)
    put_tabs(tab_data)

def main():
    global hist_plot_html
    session.set_env(title='Elon Musk\'s Time Spent on Tweeting')

    put_markdown('# How Much Time Elon Musk Spent on Tweeting Things')
    put_row(
        [put_scope('motive'), None, put_scope('pic')],
        size="minmax(60%, 6fr) 20px 3fr",
    )

    with use_scope('pic'):
        #put_html('<blockquote class="twitter-tweet"><p lang="en" dir="ltr">To be clear, I’m spending &lt;5% (but actually) of my time on the Twitter acquisition. It ain’t rocket science!<br><br>Yesterday was Giga Texas, today is Starbase. Tesla is on my mind 24/7.<br><br>So may seem like below, but not true. <a href="https://t.co/CXfWiLD2f8">pic.twitter.com/CXfWiLD2f8</a></p>&mdash; Elon Musk (@elonmusk) <a href="https://twitter.com/elonmusk/status/1527418023069503511?ref_src=twsrc%5Etfw">May 19, 2022</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>')
        #put_markdown(md).style('font-size: 12px; color: gray; background: #f6f6f6;')
        put_image('https://i.ibb.co/zmbmdw5/62733.jpg')
    
    with use_scope('motive'):
        put_markdown(md).style('font-size: 14px; background: #f6f6f6;')
    
    put_html(hist_plot_html)
    put_markdown('### His busiest 5 days on Twitter')
    put_top5()

if __name__ == '__main__':
    start_server(main, debug=True, port=9999)