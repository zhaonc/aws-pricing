from re import L


def spot_instance():
    import streamlit as st
    import plotly.express as px
    from pricing import get_spot_prices

    @st.cache(show_spinner=False)
    def get_data():
        with st.spinner('Loading data...'):
            df = get_spot_prices()
            df = df[['region', 'instance_type', 'generation', 'instance_name', 'instance_family', 'instance_size', 'system', 'price']]
            return df

    df = get_data()
    df_ = df.dropna(subset=['price'])

    regions = sorted(df_['region'].unique())
    selected_regions = st.sidebar.multiselect('Regions', regions, [])
    df_ = df_[df_['region'].isin(selected_regions if selected_regions else regions)]

    instance_types = sorted(df_['instance_type'].unique())
    selected_instance_types = st.sidebar.multiselect('Instance Types', instance_types, [])
    df_ = df_[df_['instance_type'].isin(selected_instance_types if selected_instance_types else instance_types)]

    generations = sorted(df_['generation'].unique())
    selected_generations = st.sidebar.multiselect('Generations', generations, [])
    df_ = df_[df_['generation'].isin(selected_generations if selected_generations else generations)]

    instance_families = sorted(df_['instance_family'].unique())
    selected_instance_families = st.sidebar.multiselect('Instance Families', instance_families, [])
    df_ = df_[df_['instance_family'].isin(selected_instance_families if selected_instance_families else instance_families)]


    instance_sizes = sorted(df_['instance_size'].unique())
    selected_instance_sizes = st.sidebar.multiselect('Instance Sizes', instance_sizes, [])
    df_ = df_[df_['instance_size'].isin(selected_instance_sizes if selected_instance_sizes else instance_sizes)]

    systems = sorted(df_['system'].unique())
    selected_systems = st.sidebar.multiselect('System', systems, [])
    df_ = df_[df_['system'].isin(selected_systems if selected_systems else systems)]

    max_price = float(df_['price'].max())
    selected_max_price = st.sidebar.slider('Max price', min_value=0., max_value=max_price, step=0.01, value=max_price)
    df_ = df_[df_['price'] <= selected_max_price]
    
    df_display = df_[['region', 'instance_type', 'generation', 'instance_name', 'system', 'price']]

    st.write('## Pricing', df_display)

    # Plot
    for dim in ['region', 'instance_type', 'generation', 'instance_family', 'instance_size', 'system']:
        fig = px.box(df_, y='price', x=dim)
        st.plotly_chart(fig, use_container_width=True)