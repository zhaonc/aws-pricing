import streamlit as st
import apps
from streamlit.logger import get_logger
from collections import OrderedDict

LOGGER = get_logger(__name__)

APPS = OrderedDict([
    ('Spot Instance', apps.spot_instance)
])

def run():
    app_name = st.sidebar.selectbox('Pricing', list(APPS.keys()), 0)
    app = APPS[app_name]

    st.markdown('# {}'.format(app_name))
    app()


if __name__ == '__main__':
    run()