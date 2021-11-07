def spot_instance():
    import streamlit as st
    from pricing import get_spot_prices

    @st.cache(show_spinner=False)
    def get_data():
        with st.spinner('Loading data...'):
            df = get_spot_prices()
            df = df[['region', 'instance_type', 'generation', 'instance_size', 'system', 'price']]
            return df

    df = get_data()
    regions = sorted(df['region'].unique())
    instance_types = sorted(df['instance_type'].unique())
    generations = sorted(df['generation'].unique())
    instance_sizes = sorted(df['instance_size'].unique())
    systems = sorted(df['system'].unique())

    selected_regions = st.sidebar.multiselect('Regions', regions, [])
    selected_instance_types = st.sidebar.multiselect('Instance Types', instance_types, [])
    selected_generations = st.sidebar.multiselect('Generations', generations, [])
    selected_instance_sizes = st.sidebar.multiselect('Instance Sizes', instance_sizes, [])
    selected_systems = st.sidebar.multiselect('System', systems, [])

    df_ = df
    df_ = df_[df_['region'].isin(selected_regions if selected_regions else regions)]
    df_ = df_[df_['instance_type'].isin(selected_instance_types if selected_instance_types else instance_types)]
    df_ = df_[df_['generation'].isin(selected_generations if selected_generations else generations)]
    df_ = df_[df_['instance_size'].isin(selected_instance_sizes if selected_instance_sizes else instance_sizes)]
    df_ = df_[df_['system'].isin(selected_systems if selected_systems else systems)]

    df_ = df_.dropna(subset=['price'])

    st.write('## Pricing', df_)

def reserved_instance():
    import streamlit as st
    from pricing import get_spot_prices