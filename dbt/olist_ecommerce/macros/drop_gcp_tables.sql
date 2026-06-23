{% macro drop_all_tables_in_dataset() %}

    {% set base_prefix = target.dataset.split('_')[:-1] | join('_')%}
    
    {% set datasets = [base_prefix ~ '_silver', base_prefix ~ '_gold'] %}
    
    {% for dataset in datasets %}
        {{ log("------------------------------------------------", info=True) }}
        {{ log("Removing dataset: " ~ dataset, info=True) }}
        
        {# Pobieramy wszystkie tabele i widoki z wyliczonego datasetu #}
        {% set relations = dbt_utils.get_relations_by_prefix(schema=dataset, prefix='') %}
        
        {% if relations | length == 0 %}
            {{ log("Nothing to remove" ~ dataset, info=True) }}
        {% endif %}
        
        {% for relation in relations %}
            {{ log("Removing table/view: " ~ relation.identifier, info=True) }}
            {% do adapter.drop_relation(relation) %}
        {% endfor %}
        
    {% endfor %}

{% endmacro %}