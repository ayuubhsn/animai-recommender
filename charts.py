import plotly.express as px
from data import df
def lag_topp10(df):
    topp10 = df.sort_values("score", ascending=False).head(10)
    fig = px.bar(topp10, x="tittel", y="score", title="Topp 10 anime ")
    fig.update_layout(yaxis_range=[50, 1000])
    return fig